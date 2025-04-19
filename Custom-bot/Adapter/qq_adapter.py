import asyncio
import json
import logging
import time
import uuid
from typing import Dict, Optional, Any, Union
import inspect # 保留 inspect 用于可能的调试

import websockets
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol

# 导入框架核心组件
from core.adapters import BaseAdapter
from core.message import InternalMessage

# 使用特定于此适配器的 logger
logger = logging.getLogger("适配器.QQAdapter")

class QQAdapter(BaseAdapter):
    """
    QQ 适配器，基于 OneBot v11 标准的反向 WebSocket 实现。
    作为 WebSocket 服务器运行，等待 QQ 机器人客户端连接。
    """
    def __init__(self, kernel, adapter_id, config):
        super().__init__(kernel, adapter_id, config)
        self.host: str = config.get('host', '0.0.0.0')
        self.port: int = int(config.get('port', 8765))
        self.access_token = config.get('access_token', None)
        self.event_path = config.get('path', '/onebot/v11/event')
        self._server: Optional[websockets.server.Serve] = None
        self._clients: Dict[str, WebSocketServerProtocol] = {}
        self._server_task: Optional[asyncio.Task] = None
        self._kernel_running_tasks_ref: Optional[Dict] = getattr(kernel, '_running_tasks', None)
        self._echo_futures: Dict[str, asyncio.Future] = {}
        # --- 修改日志级别 ---
        logger.debug(f"正在初始化适配器 '{self.adapter_id}' (协议: {self.protocol_name})") # INFO -> DEBUG

    async def setup(self) -> None:
        await super().setup()
        # --- 修改日志级别 ---
        logger.debug(f"QQ 适配器 (反向WS) 将在 ws://{self.host}:{self.port}{self.event_path} 上监听连接。") # INFO -> DEBUG
        if self.access_token: logger.debug("已配置 Access Token。") # INFO -> DEBUG

    async def _connection_handler(self, websocket: WebSocketServerProtocol, path: str) -> None:
        try: logger.debug(f"进入 _connection_handler: websocket 类型={type(websocket)}, path='{path}' (类型={type(path)})") # INFO -> DEBUG
        except Exception as log_err: logger.error(f"打印 _connection_handler 参数时出错: {log_err}")

        connection_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        # logger.info(f"收到来自 {connection_id} 的新 WebSocket 连接，请求路径: '{path}'") # 保留或改为 DEBUG

        if path != self.event_path:
            logger.warning(f"连接被拒绝: 路径 '{path}' 不匹配期望的路径 '{self.event_path}'。")
            await websocket.close(code=1008, reason="Invalid path"); return
        if self.access_token:
            auth_header = websocket.request_headers.get("Authorization")
            expected_auth = f"Bearer {self.access_token}"
            if not auth_header or auth_header != expected_auth:
                 logger.warning(f"连接被拒绝: Authorization 头无效或不匹配。收到: '{auth_header}'"); await websocket.close(code=1008, reason="Authorization failed"); return
            logger.debug("Access Token 验证通过。") # INFO -> DEBUG

        self._clients[connection_id] = websocket
        client_count = len(self._clients)
        # --- 保留 INFO 级别 ---
        logger.info(f"QQ 机器人客户端已连接: ID='{connection_id}' (来自路径 '{path}')。当前连接数: {client_count}")

        try:
            async for message_data in websocket:
                log_preview = str(message_data[:200]) + ('...' if len(str(message_data)) > 200 else '')
                logger.debug(f"从 QQ 客户端 '{connection_id}' 收到原始数据: {log_preview}") # INFO -> DEBUG

                try:
                    event = json.loads(message_data)
                    if not isinstance(event, dict): logger.warning(f"收到非 JSON 对象格式的数据: {type(event)}，已忽略。"); continue
                    if 'echo' in event:
                        echo_id = str(event['echo']); future = self._echo_futures.pop(echo_id, None)
                        if future and not future.done(): logger.debug(f"收到 Echo 响应 (ID: {echo_id})"); future.set_result(event)
                        else: logger.debug(f"收到未预期或已超时的 Echo 响应 (ID: {echo_id})，已忽略。")
                        continue
                    post_type = event.get("post_type");
                    if not post_type: logger.warning(f"收到的事件缺少 'post_type' 字段，已忽略: {event}"); continue
                    if post_type == "meta_event" and event.get("meta_event_type") == "heartbeat": continue

                    # --- 保留或调整事件/消息日志级别 ---
                    if post_type == "message":
                         message_type = event.get("message_type"); sub_type = event.get("sub_type")
                         msg_id = str(event.get("message_id", "")); user_id = str(event.get("user_id", ""))
                         sender_info = event.get("sender", {}); user_name = str(sender_info.get("nickname", ""))
                         raw_message = event.get("raw_message", ""); text_content = event.get("message", raw_message)
                         group_id = None; group_name = None
                         if message_type == "group": group_id = str(event.get("group_id", "")); group_name = f"Group_{group_id}" if group_id else None
                         elif message_type == "private": group_id = None; group_name = None
                         if not user_id: logger.warning(f"收到消息事件但缺少 user_id: {event}"); continue

                         # <<< 保留 INFO 级别，这是你希望看到的 >>>
                         logger.info(f"QQ适配器收到消息: User={user_id}, Group={group_id or '私聊'}, MsgID={msg_id}, Text='{text_content[:100]}...'")

                         msg = InternalMessage(
                              adapter_id=self.adapter_id, protocol=self.protocol_name, connection_id=connection_id, user_id=user_id, user_name=user_name,
                              group_id=group_id, group_name=group_name, msg_id=msg_id, msg_type="text", text_content=text_content, parsed_data=event, raw_data=message_data,
                              metadata={'onebot_post_type': post_type, 'onebot_message_type': message_type, 'onebot_sub_type': sub_type}, timestamp=event.get("time", time.time())
                         )
                         await self._push_to_kernel(msg)
                    elif post_type:
                         # 其他事件摘要可以设为 DEBUG 或 INFO，取决于你的需要
                         logger.debug(f"QQ适配器收到事件: Type={post_type}, SubType={event.get('sub_type') or event.get('notice_type') or event.get('request_type') or 'N/A'}, User={event.get('user_id')}, Group={event.get('group_id')}") # INFO -> DEBUG
                         # TODO: 将其他事件也转换为 InternalMessage 推送给内核处理

                except json.JSONDecodeError: logger.warning(f"从 QQ 客户端 '{connection_id}' 收到无法解析为 JSON 的数据: {message_data[:100]}...")
                except Exception as parse_err: logger.error(f"处理来自 QQ 客户端 '{connection_id}' 的数据时出错: {parse_err}", exc_info=True)
        except ConnectionClosedOK: logger.info(f"QQ 客户端 '{connection_id}' 正常断开连接。")
        except ConnectionClosedError as e: logger.warning(f"QQ 客户端 '{connection_id}' 连接错误关闭: Code={e.code}, Reason='{e.reason}'")
        except ConnectionClosed as e: logger.warning(f"QQ 客户端 '{connection_id}' 连接已关闭: {e}")
        except Exception as e: logger.error(f"处理 QQ 客户端 '{connection_id}' 时发生未知错误: {e}", exc_info=True)
        finally:
            if connection_id in self._clients: del self._clients[connection_id]; logger.info(f"已移除 QQ 客户端连接记录: '{connection_id}'。当前连接数: {len(self._clients)}")

    async def start(self) -> None:
        await super().start()
        if self._server_task and not self._server_task.done(): logger.warning("QQ 反向 WS 服务器任务已在运行中。"); self.is_running = True; return
        try:
            # --- 打印签名日志改为 DEBUG ---
            try:
                sig = inspect.signature(self._connection_handler); logger.debug(f"即将传递给 serve 的 handler 签名: {sig}"); param_names = list(sig.parameters.keys()); logger.debug(f"运行时参数列表: {param_names}"); assert 'path' in param_names, "'path' 参数缺失!"
            except Exception as inspect_err: logger.error(f"检查签名出错: {inspect_err}")

            self._server = await websockets.serve(self._connection_handler, self.host, self.port, ping_interval=30, ping_timeout=20)
            self.is_running = True
            # --- 保留 INFO 级别 ---
            self.logger.info(f"QQ 反向 WS 服务器已启动在 ws://{self.host}:{self.port}{self.event_path}")
            task_name = f"QQ_RWS_Server_{self.adapter_id}"; self._server_task = asyncio.create_task(self._server.wait_closed(), name=task_name)
            if self._kernel_running_tasks_ref is not None: self._kernel_running_tasks_ref[task_name] = self._server_task
        except OSError as e: self.logger.error(f"启动 QQ 反向 WS 服务器失败 (地址: {self.host}:{self.port}): {e}", exc_info=True); self.is_running = False; self._server = None
        except Exception as e: self.logger.error(f"启动 QQ 反向 WS 服务器时发生未知错误: {e}", exc_info=True); self.is_running = False; self._server = None

    async def stop(self) -> None:
        await super().stop()
        server_closed = False
        # --- 修改日志级别 ---
        if self._server and self._server.is_serving(): logger.debug("正在关闭 QQ 反向 WebSocket 服务器...") # INFO -> DEBUG
        try:
             if self._server: self._server.close();
             if self._server_task and not self._server_task.done(): await asyncio.wait_for(self._server_task, timeout=10.0); server_closed = True
             logger.debug("QQ 反向 WebSocket 服务器已关闭。") # INFO -> DEBUG
        except asyncio.TimeoutError: logger.warning("等待服务器关闭超时。"); self._server_task.cancel()
        except asyncio.CancelledError: logger.debug("服务器关闭任务被取消。") # INFO -> DEBUG
        except Exception as e: logger.error(f"关闭 QQ 反向 WebSocket 服务器时出错: {e}", exc_info=True)
        finally: self._server = None; self._server_task = None
        if self._clients:
             client_count = len(self._clients); logger.debug(f"正在关闭 {client_count} 个 QQ 客户端连接...") # INFO -> DEBUG
             clients_to_close = list(self._clients.values()); self._clients.clear()
             close_tasks = [client.close(code=1001, reason="服务器关闭") for client in clients_to_close if client.open]
             if close_tasks: await asyncio.gather(*close_tasks, return_exceptions=True)
             logger.debug(f"{len(close_tasks)} 个 QQ 客户端连接已尝试关闭。") # INFO -> DEBUG
        self.is_running = False
        logger.debug(f"适配器 '{self.adapter_id}' 已停止。") # INFO -> DEBUG

    async def send(self, message: 'InternalMessage') -> bool:
        # ... (发送逻辑基本不变，错误日志级别可以按需调整) ...
        target_connection_id: Optional[str] = message.connection_id
        if not target_connection_id and len(self._clients) == 1: target_connection_id = next(iter(self._clients.keys()))
        elif not target_connection_id and len(self._clients) > 1: logger.warning(f"无法发送消息 {message.internal_id}: 有多个 QQ 客户端连接，但未指定 connection_id。"); return False
        elif target_connection_id not in self._clients: logger.warning(f"无法发送消息 {message.internal_id}: 找不到目标 QQ 客户端连接 '{target_connection_id}'。"); return False
        if not target_connection_id: logger.error(f"发送消息 {message.internal_id} 时未能确定目标连接 ID。"); return False

        action: Optional[str] = None; params: Dict[str, Any] = {}
        if message.msg_type == "text" or message.attachments:
            action = "send_msg"
            if message.group_id and message.group_id != '0': params["message_type"] = "group"; params["group_id"] = int(message.group_id)
            elif message.user_id: params["message_type"] = "private"; params["user_id"] = int(message.user_id)
            else: logger.error(f"发送消息 {message.internal_id} 失败: 缺少 group_id 或 user_id。"); return False
            onebot_message_content = []
            if message.text_content: onebot_message_content.append({"type": "text", "data": {"text": message.text_content}})
            if message.attachments:
                 for att in message.attachments:
                      cq_code_str = self._attachment_to_cqcode_string(att)
                      if cq_code_str:
                           if onebot_message_content: onebot_message_content.append({"type": "text", "data": {"text": " "}})
                           onebot_message_content.append({"type": "text", "data": {"text": cq_code_str}})
                      else: logger.warning(f"无法将附件 {att} 转换为 CQ 码。")
            if not onebot_message_content: logger.warning(f"消息 {message.internal_id} 构建 OneBot 消息失败，无有效内容。"); return False
            params["message"] = onebot_message_content
        elif message.msg_type == "action_delete":
             action = "delete_msg"
             target_msg_ids = message.metadata.get("target_msg_ids")
             if isinstance(target_msg_ids, list) and target_msg_ids:
                  try: params["message_id"] = int(target_msg_ids[0])
                  except (ValueError, TypeError): logger.error(f"删除消息动作 {message.internal_id} 失败: 无效的消息 ID '{target_msg_ids[0]}'。"); return False
             else: logger.error(f"删除消息动作 {message.internal_id} 失败: 元数据中缺少有效的 target_msg_ids。"); return False
        if not action: logger.warning(f"无法处理消息 {message.internal_id}: 未知的消息类型或动作。"); return False

        try:
             echo_id = str(uuid.uuid4().hex); api_request = {"action": action, "params": params, "echo": echo_id}
             future = asyncio.Future(); self._echo_futures[echo_id] = future
             success = await self._send_to_client(target_connection_id, api_request)
             if success:
                  try:
                       timeout = self.config.get("api_timeout", 30); echo_response = await asyncio.wait_for(future, timeout=timeout)
                       if isinstance(echo_response, dict) and echo_response.get("status") == "ok": logger.info(f"API 调用 (echo: {echo_id}, action: {action}) 成功。"); return True # 保留 INFO
                       else: error_info = echo_response.get("msg") or echo_response.get("wording") or "未知错误"; retcode = echo_response.get("retcode", "N/A"); logger.error(f"API 调用 (echo: {echo_id}, action: {action}) 失败: {error_info} (retcode: {retcode})"); return False
                  except asyncio.TimeoutError: logger.error(f"等待 API 调用 (echo: {echo_id}, action: {action}) 的响应超时。"); self._echo_futures.pop(echo_id, None); return False
                  except Exception as wait_err: logger.error(f"等待 API 响应 (echo: {echo_id}) 时发生错误: {wait_err}", exc_info=True); return False
             else: self._echo_futures.pop(echo_id, None); return False
        except Exception as send_err:
             logger.error(f"发送 API 请求 (action: {action}) 时发生错误: {send_err}", exc_info=True)
             if 'echo_id' in locals() and echo_id in self._echo_futures: self._echo_futures[echo_id].cancel("发送 API 请求时出错"); del self._echo_futures[echo_id]
             return False

    async def _send_to_client(self, connection_id: str, data: Union[Dict, str]) -> bool:
        websocket = self._clients.get(connection_id)
        if not websocket or not websocket.open:
             if connection_id in self._clients: del self._clients[connection_id]; logger.info(f"发送时检测到 QQ 客户端 '{connection_id}' 连接已关闭，已清理。")
             return False
        try:
            if isinstance(data, dict): message_to_send = json.dumps(data, ensure_ascii=False)
            else: message_to_send = str(data)
            log_preview = message_to_send[:150] + ('...' if len(message_to_send) > 150 else '')
            # --- 保留 INFO 级别 ---
            logger.info(f"QQ适配器发送消息给 {connection_id}: {log_preview}")
            await websocket.send(message_to_send)
            return True
        except ConnectionClosed:
            logger.warning(f"发送数据到 QQ 客户端 '{connection_id}' 失败：连接已关闭。")
            if connection_id in self._clients: del self._clients[connection_id]; logger.info(f"清理已关闭 QQ 连接 '{connection_id}'。")
            return False
        except Exception as e:
            self.logger.error(f"向 QQ 客户端 '{connection_id}' 发送数据时发生未知错误: {e}", exc_info=True)
            return False

    def _attachment_to_cqcode_string(self, attachment: Dict[str, Any]) -> Optional[str]:
        att_type = attachment.get('type'); file_location = attachment.get('path') or attachment.get('url') or attachment.get('file_id'); base64_data = attachment.get('base64')
        def cq_escape(text: str) -> str: return str(text).replace('&', '&').replace('[', '[').replace(']', ']').replace(',', ',')
        if att_type == 'image':
             if file_location: return f"[CQ:image,file={cq_escape(file_location)}]"
             elif base64_data:
                  if isinstance(base64_data, str) and base64_data.startswith("base64://"): return f"[CQ:image,file={base64_data}]"
                  elif isinstance(base64_data, str) and base64_data.startswith("data:image"): logger.warning("推荐使用 base64:// 格式"); return f"[CQ:image,file={base64_data}]"
        elif att_type == 'video':
             if file_location: return f"[CQ:video,file={cq_escape(file_location)}]"
        elif att_type in ['audio', 'voice']:
             if file_location: return f"[CQ:record,file={cq_escape(file_location)}]"
        logger.warning(f"暂不支持将类型为 '{att_type}' 的附件转换为 CQ 码字符串。")
        return None

    def get_status(self) -> Dict[str, Any]:
         base_status = super().get_status()
         base_status.update({
              "listening": self.is_running and self._server is not None and self._server.is_serving(),
              "listen_address": f"ws://{self.host}:{self.port}{self.event_path}",
              "connected_clients": len(self._clients),
              "expected_path": self.event_path,
              "access_token_enabled": bool(self.access_token),
         })
         return base_status