import asyncio
import json
import logging
import time
import uuid
from typing import Dict, Optional, Any, Union # 增加 Any 和 Union

import websockets # 导入 websockets 库
# 从 websockets.exceptions 导入特定的连接关闭异常类型
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol # 类型提示，表示服务器端的 WebSocket 连接对象

# 导入框架核心组件
from core.adapters import BaseAdapter
from core.message import InternalMessage

# 使用特定于此适配器的 logger
logger = logging.getLogger("适配器.ReverseWSAdapter")

class ReverseWebSocketAdapter(BaseAdapter):
    """
    反向 WebSocket 适配器。
    作为 WebSocket 服务器运行，等待外部客户端连接进来，并接收和发送消息。
    """
    def __init__(self, kernel, adapter_id, config):
        """
        初始化反向 WebSocket 适配器。

        Args:
            kernel: RobotKernel 实例。
            adapter_id: 适配器 ID。
            config: 配置字典，应包含 'host', 'port' 等键。
        """
        super().__init__(kernel, adapter_id, config)
        # 从配置读取监听地址和端口，提供默认值
        self.host: str = config.get('host', '0.0.0.0')
        self.port: int = int(config.get('port', 8765)) # 确保端口是整数
        # WebSocket 服务器实例 (在 start 时创建)
        self._server: Optional[websockets.server.Serve] = None
        # 存储已连接的客户端 WebSocket 对象，使用 connection_id 作为键
        self._clients: Dict[str, WebSocketServerProtocol] = {}
        # 存储服务器主循环任务
        self._server_task: Optional[asyncio.Task] = None

    async def setup(self) -> None:
        """适配器设置。"""
        await super().setup() # 调用基类 setup
        logger.info(f"反向 WebSocket 服务器将在 ws://{self.host}:{self.port} 上监听连接。")

    async def _connection_handler(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """
        异步处理每一个新的 WebSocket 连接。
        当有客户端连接时，websockets.serve 会为每个连接调用此方法。

        Args:
            websocket: 代表当前客户端连接的 WebSocketServerProtocol 对象。
            path: 客户端请求连接的路径 (例如 "/ws")。
        """
        # --- 1. 注册客户端 ---
        # 使用客户端的 远程地址:端口 作为默认的 connection_id
        # 注意：如果客户端位于 NAT 之后，这可能不是唯一的。
        # 更可靠的方式是连接建立后生成一个 UUID 作为 connection_id。
        connection_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        # 或者使用 UUID: connection_id = str(uuid.uuid4())
        # 将客户端连接对象存入字典
        self._clients[connection_id] = websocket
        client_count = len(self._clients)
        logger.info(f"客户端已连接: ID='{connection_id}' (来自路径 '{path}')。当前连接数: {client_count}")

        # --- 2. 持续接收消息 ---
        try:
            # 使用 async for 循环持续接收来自此客户端的消息
            async for message_data in websocket:
                # 记录接收到的原始消息 (部分内容，避免日志过长)
                log_preview = str(message_data[:150]) + ('...' if len(str(message_data)) > 150 else '')
                logger.debug(f"从客户端 '{connection_id}' 收到消息: {log_preview}")

                # --- 2.1 解析消息 ---
                parsed_data: Any = None                 # 解析后的数据
                raw_data: Any = message_data            # 原始数据
                text_content_extracted: Optional[str] = None # 提取的文本内容
                msg_type = "text"                       # 默认消息类型

                if isinstance(message_data, bytes):
                     msg_type = "binary"
                     # 尝试将 bytes 解码为 utf-8 文本
                     try:
                          text_content = message_data.decode('utf-8')
                          raw_data = text_content # 如果解码成功，raw_data 也用解码后的文本
                          # 尝试将解码后的文本解析为 JSON
                          try:
                               parsed_data = json.loads(text_content)
                               # 如果解析成功，提取可能的文本内容 (假设在 message 字段)
                               if isinstance(parsed_data, dict):
                                    text_content_extracted = str(parsed_data.get('message', ''))
                               logger.debug(f"来自 '{connection_id}' 的二进制消息成功解析为 JSON。")
                          except json.JSONDecodeError:
                               # 不是 JSON，将解码后的文本作为 parsed_data
                               parsed_data = text_content
                               text_content_extracted = text_content # 文本内容就是本身
                               logger.debug(f"来自 '{connection_id}' 的二进制消息解码为文本 (非 JSON)。")
                     except UnicodeDecodeError:
                          # 无法解码为 UTF-8，保留原始 bytes
                          parsed_data = message_data
                          logger.warning(f"来自 '{connection_id}' 的二进制消息无法解码为 UTF-8。")
                elif isinstance(message_data, str):
                     msg_type = "text"
                     raw_data = message_data
                     # 尝试将文本解析为 JSON
                     try:
                          parsed_data = json.loads(message_data)
                          # 如果解析成功，提取可能的文本内容
                          if isinstance(parsed_data, dict):
                               text_content_extracted = str(parsed_data.get('message', ''))
                          logger.debug(f"来自 '{connection_id}' 的文本消息成功解析为 JSON。")
                     except json.JSONDecodeError:
                          # 不是 JSON，将原始文本作为 parsed_data
                          parsed_data = message_data
                          text_content_extracted = message_data # 文本内容就是本身

                # --- 2.2 提取其他上下文信息 (需要根据实际协议格式调整) ---
                # 示例：尝试从解析后的数据中获取 user_id, group_id, msg_id
                user_id_in_data: Optional[str] = None
                group_id_in_data: Optional[str] = None
                msg_id_in_data: Optional[str] = None
                user_name_in_data: Optional[str] = None

                if isinstance(parsed_data, dict):
                     # 兼容 userId 和 user_id
                     user_id_in_data = str(parsed_data.get('user_id') or parsed_data.get('userId') or '')
                     group_id_in_data = str(parsed_data.get('group_id') or parsed_data.get('groupId') or '')
                     msg_id_in_data = str(parsed_data.get('message_id') or parsed_data.get('msg_id') or '')
                     user_name_in_data = str(parsed_data.get('user_name') or parsed_data.get('nickname') or '')
                     # 如果 group_id 为 '0' 或空字符串，视作私聊或无群组上下文
                     if not group_id_in_data or group_id_in_data == '0': group_id_in_data = None
                     if not user_id_in_data: user_id_in_data = None # 确保空字符串转为 None
                     if not msg_id_in_data: msg_id_in_data = None
                     if not user_name_in_data: user_name_in_data = None

                # --- 2.3 创建 InternalMessage ---
                msg = InternalMessage(
                    adapter_id=self.adapter_id,         # 适配器 ID
                    protocol=self.protocol_name,        # 协议名称
                    connection_id=connection_id,        # 标识这个 WebSocket 连接
                    # user_id: 优先使用从数据中解析出的 ID，否则使用 connection_id 作为备用标识
                    user_id=user_id_in_data or connection_id,
                    user_name=user_name_in_data or f"WSUser_{connection_id[-4:]}", # 优先使用数据中的，否则生成默认名
                    group_id=group_id_in_data,          # 群组 ID (如果协议提供)
                    msg_id=msg_id_in_data,              # 消息 ID (如果协议提供)
                    msg_type=msg_type,                  # 消息类型 (text/binary/或其他)
                    text_content=text_content_extracted,# 提取的文本内容
                    parsed_data=parsed_data,            # 解析后的数据
                    raw_data=raw_data,                  # 原始数据
                    metadata={                          # 存储元数据
                        'remote_address': websocket.remote_address,
                        'path': path,
                        'websocket_id': connection_id # 重复存储 connection_id 便于访问
                    },
                    timestamp=time.time()               # 框架处理时间戳
                )

                # --- 2.4 推送消息到内核 ---
                await self._push_to_kernel(msg)

        # --- 3. 处理连接关闭 ---
        except ConnectionClosedOK:
            # 客户端正常关闭连接 (例如发送了关闭帧)
            logger.info(f"客户端 '{connection_id}' 正常断开连接。")
        except ConnectionClosedError as e:
            # 连接因错误而关闭 (例如网络问题、协议错误)
            logger.warning(f"客户端 '{connection_id}' 连接错误关闭: Code={e.code}, Reason='{e.reason}'")
        except ConnectionClosed as e:
             # 其他连接关闭情况
             logger.warning(f"客户端 '{connection_id}' 连接已关闭 (异常类型: {type(e).__name__}): {e}")
        except Exception as e:
            # 捕获处理消息循环中的其他未知错误
            logger.error(f"处理客户端 '{connection_id}' 消息时发生未知错误: {e}", exc_info=True)
        finally:
            # --- 4. 清理客户端 ---
            # 无论连接如何关闭，最终都需要从活动客户端字典中移除
            if connection_id in self._clients:
                del self._clients[connection_id]
                client_count_after = len(self._clients)
                logger.info(f"已移除客户端连接记录: '{connection_id}'。当前连接数: {client_count_after}")
            else:
                 # 如果在 finally 时 connection_id 已不在字典中 (理论上不应发生，除非并发问题)
                 logger.warning(f"尝试移除客户端 '{connection_id}' 时发现记录已不存在。")


    async def start(self) -> None:
        """启动 WebSocket 服务器。"""
        await super().start() # 调用基类 start，设置 is_running 标志等

        # 防止重复启动
        if self._server_task and not self._server_task.done():
             logger.warning("反向 WebSocket 服务器任务已在运行中。")
             self.is_running = True # 确保状态正确
             return

        try:
             # 使用 websockets.serve 启动服务器
             # 它会返回一个 Serve 对象，并开始在后台接受连接
             # _connection_handler 会被自动调用处理每个新连接
             self._server = await websockets.serve(
                 self._connection_handler, # 连接处理函数
                 self.host,              # 监听地址
                 self.port,              # 监听端口
                 # 可以添加其他 websockets 服务器配置参数
                 ping_interval=20,       # 每 20 秒发送一次 ping
                 ping_timeout=20,        # 20 秒内未收到 pong 则认为超时
                 # logger=logger,        # 可以传递 logger 给 websockets 库
             )
             # 启动成功
             self.is_running = True
             self.logger.info(f"反向 WebSocket 服务器已成功启动在 ws://{self.host}:{self.port}")

             # 创建一个后台任务来等待服务器关闭事件 (self._server.wait_closed())
             # 这样 start() 方法可以立即返回，而服务器在后台持续运行
             task_name = f"RWS_Server_{self.adapter_id}"
             self._server_task = asyncio.create_task(self._server.wait_closed(), name=task_name)
             # 将服务器任务也加入 Kernel 的运行任务列表，便于管理
             if self.kernel: # 确保 kernel 存在
                 self.kernel._running_tasks[task_name] = self._server_task

        except OSError as e:
             # 处理端口占用等 OS 级别错误
             self.logger.error(f"启动反向 WebSocket 服务器失败 (地址: {self.host}:{self.port}): {e}", exc_info=True)
             self.is_running = False # 标记为未运行
             self._server = None    # 清理服务器对象
        except Exception as e:
            # 处理其他未知启动错误
            self.logger.error(f"启动反向 WebSocket 服务器时发生未知错误: {e}", exc_info=True)
            self.is_running = False
            self._server = None


    async def stop(self) -> None:
        """停止 WebSocket 服务器并关闭所有客户端连接。"""
        await super().stop() # 调用基类 stop，设置 is_running 标志等

        # 1. 关闭服务器，停止接受新连接
        if self._server and self._server.is_serving():
            self.logger.info("正在关闭反向 WebSocket 服务器...")
            try:
                 self._server.close() # 请求关闭服务器
                 # 等待服务器完全关闭 (这会等待 wait_closed() 完成)
                 if self._server_task and not self._server_task.done():
                      # 等待任务完成，设置超时
                      await asyncio.wait_for(self._server_task, timeout=10.0)
                      self.logger.info("反向 WebSocket 服务器已关闭。")
                 else:
                      logger.info("反向 WebSocket 服务器似乎已关闭。")
            except asyncio.TimeoutError:
                 logger.warning("等待服务器关闭超时。可能仍有资源未释放。")
                 # 如果超时，可能需要手动取消任务
                 if self._server_task and not self._server_task.done():
                      self._server_task.cancel()
            except asyncio.CancelledError:
                 logger.info("服务器关闭任务被取消。")
            except Exception as e:
                 logger.error(f"关闭反向 WebSocket 服务器时出错: {e}", exc_info=True)
            finally:
                 self._server = None
                 self._server_task = None


        # 2. 主动关闭所有当前连接的客户端
        if self._clients:
             client_count_before_close = len(self._clients)
             self.logger.info(f"正在关闭 {client_count_before_close} 个剩余的客户端连接...")
             # 创建客户端列表副本进行迭代，因为在关闭过程中 _clients 字典会被修改
             clients_to_close = list(self._clients.values())
             # 清空字典，防止在关闭期间又有新消息尝试发送给这些客户端
             self._clients.clear()
             # 为每个客户端创建一个关闭任务
             close_tasks = [
                 client.close(code=1001, reason="服务器正在关闭")
                 for client in clients_to_close if client.open # 只关闭仍然打开的连接
             ]
             if close_tasks:
                  # 并发执行所有关闭任务，忽略单个关闭的异常
                  await asyncio.gather(*close_tasks, return_exceptions=True)
             self.logger.info(f"{len(close_tasks)} 个剩余客户端连接已尝试关闭。")
        else:
             self.logger.info("没有活动的客户端连接需要关闭。")

        # 确保最终状态为停止
        self.is_running = False


    async def send(self, message: 'InternalMessage') -> bool:
        """
        向指定的 WebSocket 客户端发送消息。

        Args:
            message: 要发送的 InternalMessage。需要包含 `connection_id` 来指定目标客户端。

        Returns:
            bool: 表示消息是否已成功尝试发送给客户端。
        """
        connection_id = message.connection_id # 获取目标客户端 ID
        if not connection_id:
            # 如果没有指定 connection_id，可以选择广播或报错
            self.logger.warning(f"无法发送消息 {message.internal_id}: 缺少目标 connection_id。"
                                f" 如需广播，请在插件逻辑中迭代所有连接或实现广播接口。")
            # 示例：如果需要广播给所有客户端
            # results = await asyncio.gather(*(self._send_to_client(cid, message) for cid in list(self._clients.keys())))
            # return all(results) # 或者 any(results)
            return False

        # 检查客户端连接是否存在且有效
        if connection_id not in self._clients:
            self.logger.warning(f"无法发送消息 {message.internal_id}: 找不到 ID 为 '{connection_id}' 的客户端连接 (可能已断开)。")
            return False

        # 调用内部发送方法
        return await self._send_to_client(connection_id, message)


    async def _send_to_client(self, connection_id: str, message: 'InternalMessage') -> bool:
        """将 InternalMessage 转换为协议格式并发送给单个客户端的内部实现。"""
        websocket = self._clients.get(connection_id)

        # 再次检查连接状态，因为在获取和发送之间可能断开
        if not websocket or not websocket.open:
             if connection_id in self._clients: # 如果还在字典中，清理掉
                 del self._clients[connection_id]
                 logger.info(f"发送前检测到客户端 '{connection_id}' 连接已关闭，已清理记录。")
             self.logger.warning(f"发送消息 {message.internal_id} 失败：客户端 '{connection_id}' 连接无效或已关闭。")
             return False

        # --- 1. 准备要发送的数据 ---
        data_to_send: Union[str, bytes]
        # 优先使用 parsed_data，其次是 text_content
        payload = message.parsed_data if message.parsed_data is not None else message.text_content

        # 根据 payload 类型序列化
        if isinstance(payload, (dict, list)):
            try:
                # 将字典或列表序列化为 JSON 字符串
                data_to_send = json.dumps(payload, ensure_ascii=False)
            except TypeError as json_err:
                 # 如果序列化失败 (例如包含无法序列化的对象)
                 self.logger.error(f"无法将消息 {message.internal_id} 的 parsed_data 序列化为 JSON: {json_err}", exc_info=True)
                 # 尝试发送其字符串表示形式作为后备
                 data_to_send = str(payload)
        elif isinstance(payload, (str, bytes)):
             # 如果是字符串或字节串，直接使用
             data_to_send = payload
        elif payload is not None:
             # 其他类型，转换为字符串
             data_to_send = str(payload)
        else:
             # 如果 payload 为 None (既没有 parsed_data 也没有 text_content)
             self.logger.warning(f"消息 {message.internal_id} 没有可发送的内容 (parsed_data 和 text_content 都为空)。")
             # 是否发送空字符串或空字节？取决于协议要求，这里选择不发送并返回失败
             return False


        # --- 2. 发送数据 ---
        try:
            # log_preview = str(data_to_send[:150]) + ('...' if len(str(data_to_send)) > 150 else '')
            # self.logger.debug(f"向客户端 '{connection_id}' 发送数据: {log_preview}")
            await websocket.send(data_to_send)
            # 发送成功
            return True
        except ConnectionClosed:
            # 在发送时发现连接已关闭
            self.logger.warning(f"发送消息到客户端 '{connection_id}' 失败：连接已关闭。")
            if connection_id in self._clients: # 清理无效连接
                 del self._clients[connection_id]
                 logger.info(f"发送时检测到客户端 '{connection_id}' 连接已关闭，已清理记录。")
            return False
        except Exception as e:
            # 捕获发送过程中的其他错误 (例如网络错误、序列化错误等)
            self.logger.error(f"向客户端 '{connection_id}' 发送消息时发生未知错误: {e}", exc_info=True)
            return False

    def get_status(self) -> Dict[str, Any]:
         """返回反向 WebSocket 适配器的状态。"""
         base_status = super().get_status()
         base_status.update({
              "listening": self.is_running and self._server is not None and self._server.is_serving(),
              "listen_address": f"ws://{self.host}:{self.port}",
              "connected_clients": len(self._clients),
              "client_ids": list(self._clients.keys()) # 列出当前连接的客户端ID
         })
         return base_status