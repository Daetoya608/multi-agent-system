# # app/infrastructure/queue/consumers.py
# import json
# import asyncio
# from aio_pika import IncomingMessage
# from loguru import logger

# from app.infrastructure.queue.connection import rabbitmq_manager
# from app.services.dispatcher import dispatcher # Тот самый диспетчер!
# from app.schemas.commands import parse_raw_message_to_dto # Ваша функция-парсер

# async def _process_incoming_message(message: IncomingMessage):
#     """Единый обработчик для всех входящих сообщений."""
    
#     # Контекстный менеджер .process() автоматически делает ACK при успешном выходе 
#     # и NACK (возврат в очередь), если внутри выпадет Exception.
#     async with message.process(ignore_processed=True):
#         try:
#             # 1. Читаем байты
#             raw_data = message.body.decode("utf-8")
#             payload = json.loads(raw_data)
            
#             # 2. Превращаем "грязный" JSON в строгий Pydantic DTO
#             command_dto = parse_raw_message_to_dto(payload)
            
#             # 3. Отдаем в чистый слой бизнес-логики (Диспетчер)
#             await dispatcher.handle(command_dto)
            
#         except Exception as e:
#             logger.error(f"Критическая ошибка при обработке сообщения: {e}")
#             # Отклоняем сообщение (requeue=False), чтобы оно не зациклило систему.
#             # В проде его обычно перехватывает DLX (Dead Letter Exchange).
#             await message.reject(requeue=False) 

# async def start_consumers(stop_event: asyncio.Event):
#     """Функция запуска воркеров (вызывается из main.py)"""
#     channel = rabbitmq_manager.get_channel()
    
#     # QoS: Не брать больше 10 задач одновременно на одного воркера
#     await channel.set_qos(prefetch_count=10)

#     # Объявляем очередь (durable=True - очередь переживет рестарт брокера)
#     queue = await channel.declare_queue("telegram_adapter_commands", durable=True)

#     logger.info("Запуск прослушивания очереди 'telegram_adapter_commands'...")
    
#     # Начинаем слушать. Вызов consume не блокирует поток выполнения.
#     await queue.consume(_process_incoming_message)
    
#     # Ждем сигнала остановки из main.py
#     await stop_event.wait()
