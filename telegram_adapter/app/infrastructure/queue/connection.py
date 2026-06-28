import aio_pika
from loguru import logger
from app.config import settings

class RabbitMQConnectionManager:
    def __init__(self):
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None

    async def connect(self):
        """Устанавливает отказоустойчивое соединение с брокером."""
        if self._connection and not self._connection.is_closed:
            return

        logger.info(f"Подключение к RabbitMQ ({settings.RABBITMQ_HOST})...")
        try:
            # connect_robust автоматически переподключается при обрывах сети
            self._connection = await aio_pika.connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                login=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASS,
            )
            self._channel = await self._connection.channel()
            logger.success("Успешное подключение к RabbitMQ!")
        except Exception as e:
            logger.error(f"Ошибка подключения к RabbitMQ: {e}")
            raise

    def get_channel(self) -> aio_pika.RobustChannel:
        """Возвращает активный канал. Бросает ошибку, если коннекта нет."""
        if not self._channel or self._channel.is_closed:
            raise ConnectionError("Канал RabbitMQ не инициализирован.")
        return self._channel

    async def close(self):
        """Плавное закрытие (Graceful Shutdown)"""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            logger.info("Соединение с RabbitMQ закрыто.")

# Экземпляр на всё приложение
rabbitmq_manager = RabbitMQConnectionManager()
