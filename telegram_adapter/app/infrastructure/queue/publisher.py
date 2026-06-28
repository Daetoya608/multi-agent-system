import json
import aio_pika
from pydantic import BaseModel
from loguru import logger
from app.infrastructure.queue.connection import rabbitmq_manager

class RabbitMQPublisher:
    def __init__(self, exchange_name: str = ""):
        # По умолчанию шлем в дефолтный обменник (напрямую в очередь)
        self.exchange_name = exchange_name

    async def publish(self, routing_key: str, message_dto: BaseModel):
        """
        Отправляет Pydantic DTO в RabbitMQ.
        :param routing_key: Имя очереди (например, 'orchestrator_events')
        :param message_dto: Pydantic объект (например, EventBotConnected)
        """
        channel = rabbitmq_manager.get_channel()
        
        # 1. Сериализуем Pydantic модель в JSON-строку, затем в байты
        payload = message_dto.model_dump_json().encode("utf-8")

        # 2. Формируем сообщение для брокера
        message = aio_pika.Message(
            body=payload,
            content_type="application/json",
            # PERSISTENT означает, что сообщение сохранится на жесткий диск RabbitMQ
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT, 
        )

        # 3. Отправляем
        exchange = channel.default_exchange
        await exchange.publish(
            message=message,
            routing_key=routing_key,
        )
        logger.debug(f"Сообщение отправлено в очередь '{routing_key}': {message_dto.__class__.__name__}")

# Экземпляр для отправки событий
event_publisher = RabbitMQPublisher()