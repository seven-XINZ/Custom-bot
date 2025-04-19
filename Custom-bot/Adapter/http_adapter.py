import asyncio
import logging
import time
import json # 导入 json 模块用于解析
from typing import Any, Dict, Optional, Union

import aiohttp # 导入 aiohttp 用于 HTTP 客户端功能
from aiohttp import web # 导入 aiohttp web 用于创建服务器

# 导入框架核心组件
from core.adapters import BaseAdapter
from core.message import InternalMessage

# 使用特定于此适配器的 logger，名称与模块或类名相关联
logger = logging.getLogger("适配器.HttpAdapter")

class HttpAdapter(BaseAdapter):
    """
    处理 HTTP Webhook 请求的适配器 (作为 HTTP 服务器)。
    同时也能作为 HTTP 客户端向外发送请求 (通过 send 方法)。
    """

    def __init__(self, kernel, adapter_id, config):
        """
        初始化 HTTP 适配器。

        Args:
            kernel: RobotKernel 实例。
            adapter_id: 适配器 ID。
            config: 配置字典，应包含 'host', 'port', 'path' 等键。
        """
        super().__init__(kernel, adapter_id, config)
        # 从配置中读取监听地址、端口和路径，提供默认值
        self.host: str = config.get('host', '0.0.0.0')
        self.port: int = int(config.get('port', 8088)) # 确保端口是整数
        self.webhook_path: str = config.get('path', '/webhook')
        # aiohttp 服务器相关的内部状态
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self.app: Optional[web.Application] = None # aiohttp 应用实例

    async def setup(self) -> None:
        """初始化 aiohttp 应用并设置路由。"""
        await super().setup() # 调用基类的 setup (虽然基类是空的)
        # 创建 aiohttp 应用实例
        # 将 logger 传递给 aiohttp 应用，以便它记录请求等信息
        self.app = web.Application(logger=logger)
        # 添加处理 Webhook POST 请求的路由
        # TODO: 考虑是否需要支持其他 HTTP 方法 (GET, PUT等)
        self.app.router.add_post(self.webhook_path, self._handle_webhook)
        self.logger.info(f"HTTP Webhook 路由 '{self.webhook_path}' (POST) 已设置。")

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        """
        异步处理接收到的 Webhook HTTP 请求。

        Args:
            request: aiohttp 的 Request 对象。

        Returns:
            aiohttp 的 Response 对象 (通常是 200 OK)。
        """
        # 尝试从请求头获取唯一请求 ID，否则生成一个
        request_id = request.headers.get("X-Request-ID", f"http_{uuid.uuid4().hex[:8]}")
        remote_ip = request.remote or "未知来源" # 获取来源 IP
        log_prefix = f"Webhook 请求 {request_id} (来自 {remote_ip})"

        logger.info(f"{log_prefix}: 收到 POST 到路径 {request.path}")

        # 初始化变量用于存储处理结果
        raw_data: Optional[Union[bytes, str]] = None
        parsed_data: Any = None
        error_msg: Optional[str] = None
        text_content_extracted: Optional[str] = None
        message_type_extracted: str = 'unknown' # 默认消息类型

        # --- 1. 读取和解析请求体 ---
        try:
            request_body_bytes = await request.read() # 读取原始请求体 (bytes)
            content_type = request.content_type.lower() # 获取内容类型并转小写
            logger.debug(f"{log_prefix}: Content-Type='{content_type}', Body 大小={len(request_body_bytes)} bytes")

            if not request_body_bytes:
                 logger.warning(f"{log_prefix}: 请求体为空。")
                 raw_data = b'' # 标记为空字节
                 parsed_data = None
            elif content_type == 'application/json':
                raw_data = request_body_bytes # 保留原始字节
                try:
                    # 尝试将 bytes 解码为 utf-8 再解析 JSON
                    decoded_body = request_body_bytes.decode('utf-8')
                    parsed_data = json.loads(decoded_body)
                    # 尝试从 JSON 中提取文本内容和类型 (根据常见协议约定)
                    if isinstance(parsed_data, dict):
                         text_content_extracted = str(parsed_data.get('message') or parsed_data.get('raw_message') or '')
                         message_type_extracted = str(parsed_data.get('message_type', message_type_extracted))
                    logger.debug(f"{log_prefix}: 成功解析 JSON 数据。")
                except (UnicodeDecodeError, json.JSONDecodeError) as json_err:
                    error_msg = f"无法解析 JSON 数据: {json_err}"
                    logger.warning(f"{log_prefix}: {error_msg}")
                    # 解析失败，parsed_data 保持 None，raw_data 仍是原始 bytes
            elif content_type.startswith('text/'):
                 # 如果是文本类型，尝试解码
                 try:
                      text_content_extracted = request_body_bytes.decode('utf-8') # 假设 UTF-8
                      parsed_data = text_content_extracted # 解析后的数据就是文本本身
                      raw_data = text_content_extracted # raw_data 也存储文本
                      message_type_extracted = 'text'
                      logger.debug(f"{log_prefix}: 数据已作为文本处理。")
                 except UnicodeDecodeError as decode_err:
                      error_msg = f"无法将请求体解码为 UTF-8 文本: {decode_err}"
                      logger.warning(f"{log_prefix}: {error_msg}")
                      raw_data = request_body_bytes # 保留原始字节
                      parsed_data = raw_data # 解析数据也存原始字节
                      message_type_extracted = 'binary' # 视为二进制
            else:
                 # 其他未知类型，作为原始二进制数据处理
                 logger.debug(f"{log_prefix}: 未知 Content-Type，将作为原始二进制数据处理。")
                 raw_data = request_body_bytes
                 parsed_data = raw_data # 解析数据也存原始字节
                 message_type_extracted = 'binary'

        except Exception as e:
            # 捕获读取请求体过程中的其他错误
            error_msg = f"读取请求体时出错: {e}"
            logger.error(f"{log_prefix}: {error_msg}", exc_info=True)
            # 返回服务器错误响应
            return web.Response(text=f"处理请求时发生内部错误。", status=500)

        # --- 2. 提取其他信息 ---
        headers = dict(request.headers) # 获取请求头
        query_params = dict(request.query) # 获取查询参数

        # --- 3. 创建 InternalMessage ---
        # 尝试从已解析的数据中提取用户/群组/消息 ID (需要根据具体协议适配)
        # 这里提供一些基于常见 Webhook 协议 (如 OneBot) 的示例性提取逻辑
        user_id_extracted: Optional[str] = None
        group_id_extracted: Optional[str] = None
        msg_id_extracted: Optional[str] = None

        if isinstance(parsed_data, dict):
            user_id_extracted = str(parsed_data.get('user_id') or parsed_data.get('sender', {}).get('user_id'))
            group_id_extracted = str(parsed_data.get('group_id'))
            # 如果 group_id 不存在或为 0，则可能是私聊或特殊事件
            if group_id_extracted == '0': group_id_extracted = None
            msg_id_extracted = str(parsed_data.get('message_id'))
            # 可以根据 post_type 进一步细化 msg_type
            post_type = parsed_data.get('post_type')
            if post_type == 'notice': message_type_extracted = 'notice'
            elif post_type == 'meta_event': message_type_extracted = 'meta'
            # ... 可以添加更多根据协议内容的类型判断 ...

        # 构建 InternalMessage 对象
        msg = InternalMessage(
            adapter_id=self.adapter_id,      # 适配器 ID
            protocol=self.protocol_name,     # 协议名称
            session_id=request_id,           # 使用请求 ID 作为会话/交互 ID
            connection_id=remote_ip,         # 可以用来源 IP 作为连接标识符
            user_id=user_id_extracted,       # 提取到的用户 ID
            group_id=group_id_extracted,     # 提取到的群组 ID
            msg_id=msg_id_extracted,         # 提取到的消息 ID
            msg_type=message_type_extracted, # 解析或推断的消息类型
            text_content=text_content_extracted, # 提取到的文本内容
            parsed_data=parsed_data,         # 解析后的结构化数据
            raw_data=raw_data,               # 原始请求体数据
            metadata={                       # 存储额外信息
                'headers': headers,
                'remote_ip': remote_ip,
                'http_path': request.path,
                'query_params': query_params,
                'error': error_msg # 如果解析出错，记录错误信息
            },
            timestamp=time.time()            # 框架处理时间戳
        )

        # --- 4. 将消息推送到内核处理 ---
        await self._push_to_kernel(msg)

        # --- 5. 回复 HTTP 响应 ---
        # Webhook 通常期望快速响应 (例如 2xx) 表示已收到请求。
        # 实际的处理在 Kernel 和 Plugins 中异步进行。
        # 这里回复一个简单的 200 OK。
        # 如果需要将处理结果同步返回给调用方，需要实现更复杂的请求-响应模式，
        # 例如使用 Future 等待 Kernel 处理结果，但这会增加延迟和复杂性。
        return web.Response(text="OK", status=200, content_type="text/plain")


    async def start(self) -> None:
        """启动 aiohttp HTTP 服务器。"""
        await super().start() # 调用基类的 start，设置 is_running 标志等

        # 防止重复启动
        if self._site and self._site.is_serving():
             self.logger.warning("HTTP 服务器已在运行中。")
             self.is_running = True # 确保状态正确
             return

        # 确保 app 已初始化
        if not self.app:
             await self.setup() # 如果 app 不存在，尝试重新 setup
             if not self.app: # 如果 setup 后仍然失败
                  self.logger.error("无法创建 aiohttp 应用，启动失败。")
                  self.is_running = False
                  return

        # 创建 AppRunner 和 TCPSite
        if not self._runner:
            self._runner = web.AppRunner(self.app)
            try:
                await self._runner.setup()
            except Exception as setup_err:
                 self.logger.error(f"设置 AppRunner 失败: {setup_err}", exc_info=True)
                 self.is_running = False
                 self._runner = None
                 return

        if not self._site:
            self._site = web.TCPSite(self._runner, self.host, self.port)

        # 尝试启动服务器
        try:
            await self._site.start()
            # 启动成功后，更新运行状态
            self.is_running = True
            self.logger.info(f"HTTP 服务器已成功启动，监听地址: http://{self.host}:{self.port}{self.webhook_path}")
        except OSError as e:
             # 处理端口占用等 OS 级别错误
             self.logger.error(f"启动 HTTP 服务器失败 (地址: {self.host}:{self.port}): {e}", exc_info=True)
             self.is_running = False # 标记为未运行
             # 尝试清理资源
             await self.stop() # 调用 stop 方法进行清理
        except Exception as e:
            # 处理其他未知启动错误
            self.logger.error(f"启动 HTTP 服务器时发生未知错误: {e}", exc_info=True)
            self.is_running = False
            await self.stop()


    async def stop(self) -> None:
        """停止 aiohttp HTTP 服务器并清理资源。"""
        await super().stop() # 调用基类的 stop，设置 is_running 标志等

        # 按顺序停止和清理 aiohttp 组件
        if self._site:
            self.logger.info("正在停止 HTTP TCPSite...")
            try:
                 await self._site.stop()
                 self.logger.info("HTTP TCPSite 已停止。")
            except Exception as e:
                 self.logger.error(f"停止 HTTP TCPSite 时出错: {e}", exc_info=True)
            finally:
                 self._site = None # 清理引用

        if self._runner:
            self.logger.info("正在清理 HTTP AppRunner...")
            try:
                 await self._runner.cleanup()
                 self.logger.info("HTTP AppRunner 已清理。")
            except Exception as e:
                 self.logger.error(f"清理 HTTP AppRunner 时出错: {e}", exc_info=True)
            finally:
                 self._runner = None # 清理引用

        # 清理 app 对象
        self.app = None
        self.logger.info("HTTP 适配器已完全停止。")
        # 确保最终状态为停止
        self.is_running = False


    async def send(self, message: 'InternalMessage') -> bool:
        """
        使用 HTTP 协议发送消息。
        对于此适配器，这通常意味着扮演 HTTP 客户端的角色，向另一个服务发送请求。

        Args:
            message: 包含发送目标和内容的 InternalMessage。
                     需要从 message.metadata 中获取目标 URL、HTTP 方法、头等信息。
                     发送的数据通常来自 message.parsed_data 或 message.text_content。

        Returns:
            bool: 表示 HTTP 请求是否成功发送并收到 2xx 响应。
        """
        # --- 1. 从消息中提取发送所需信息 ---
        # 目标 URL 是必需的
        target_url = message.metadata.get("target_url")
        if not target_url:
             self.logger.warning(f"无法通过 HTTP 发送消息 {message.internal_id}: "
                                 f"消息元数据中缺少目标 URL ('target_url')。")
             return False

        # 获取 HTTP 方法，默认为 POST
        http_method = message.metadata.get("http_method", "POST").upper()
        # 获取请求头，可以从元数据获取，或设置默认值
        headers = message.metadata.get("headers", {"Content-Type": "application/json"})
        # 获取请求体数据
        data_to_send: Optional[Union[str, bytes, aiohttp.Payload]] = None
        payload_source = message.parsed_data if message.parsed_data is not None else message.text_content

        # --- 2. 准备请求体 ---
        try:
            if isinstance(payload_source, (dict, list)):
                # 如果是字典或列表，默认序列化为 JSON
                # 确保 Content-Type 是 application/json (或兼容类型)
                if "content-type" not in (k.lower() for k in headers):
                     headers["Content-Type"] = "application/json"
                data_to_send = json.dumps(payload_source, ensure_ascii=False)
                # aiohttp 会自动处理编码为 bytes
            elif isinstance(payload_source, str):
                # 如果是字符串，直接发送
                # 确保 Content-Type 是 text/* (或让 aiohttp 推断)
                if "content-type" not in (k.lower() for k in headers):
                     headers["Content-Type"] = "text/plain; charset=utf-8"
                data_to_send = payload_source
            elif isinstance(payload_source, bytes):
                # 如果是字节串，直接发送
                # Content-Type 应由元数据提供，否则默认为 application/octet-stream?
                if "content-type" not in (k.lower() for k in headers):
                     headers["Content-Type"] = "application/octet-stream"
                data_to_send = payload_source
            elif payload_source is not None:
                 # 其他类型，尝试转换为字符串
                 data_to_send = str(payload_source)
                 if "content-type" not in (k.lower() for k in headers):
                      headers["Content-Type"] = "text/plain; charset=utf-8"
            # else: data_to_send 保持 None，表示没有请求体 (例如 GET 请求)

            logger.debug(f"准备发送 HTTP {http_method} 请求到 {target_url}，"
                         f"数据类型: {type(data_to_send).__name__}, "
                         f"内容预览: {str(data_to_send)[:100] if data_to_send else '无'}...")

        except Exception as e:
             # 捕获序列化等准备阶段的错误
             self.logger.error(f"准备发送 HTTP 请求数据时出错 (消息 ID: {message.internal_id}): {e}", exc_info=True)
             return False


        # --- 3. 使用 aiohttp 发送请求 ---
        try:
            # 创建临时的 ClientSession (也可以考虑在适配器级别维护一个共享 Session)
            async with aiohttp.ClientSession() as session:
                 # 使用 session.request 发送请求
                 # data 参数可以接受 str, bytes, 或 Payload 对象
                 async with session.request(http_method, target_url, headers=headers, data=data_to_send) as response:
                      # 获取响应状态码和响应体 (可选)
                      status_code = response.status
                      response_text = await response.text(errors='replace') # 读取响应体文本

                      # 判断请求是否成功 (通常 2xx 状态码表示成功)
                      if 200 <= status_code < 300:
                           self.logger.info(f"HTTP 请求成功 ({status_code}) 到 {target_url}。"
                                             f" 响应预览: {response_text[:100]}...")
                           # 可以在这里处理响应内容，例如更新 message 状态或记录结果
                           # message.metadata['send_response_status'] = status_code
                           # message.metadata['send_response_body'] = response_text
                           return True # 返回成功
                      else:
                           # 请求失败 (非 2xx 状态码)
                           self.logger.error(f"HTTP 请求失败 ({status_code}) 到 {target_url}。"
                                             f" 错误响应: {response_text}")
                           # message.metadata['send_error'] = f"HTTP Error {status_code}"
                           # message.metadata['send_response_body'] = response_text
                           return False # 返回失败

        except aiohttp.ClientError as client_err:
            # 捕获 aiohttp 客户端错误 (连接错误、超时等)
            self.logger.error(f"发送 HTTP 请求到 {target_url} 时发生客户端错误: {client_err}", exc_info=True)
            # message.metadata['send_error'] = str(client_err)
            return False
        except Exception as e:
             # 捕获其他发送过程中的未知错误
             self.logger.error(f"发送 HTTP 请求 ({http_method} {target_url}) 时发生未知错误: {e}", exc_info=True)
             # message.metadata['send_error'] = str(e)
             return False