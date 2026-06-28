# app/main.py
import asyncio
import signal
import sys

from loguru import logger

from app.config import settings
from app.services.registry_client import bot

# Настраиваем формат логирования для вывода в консоль
logger.remove()  # Удаляем дефолтный обработчик, чтобы настроить свой
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<calendar>{line}</calendar> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO",
)


async def main():
    logger.info(f"Старт приложения {settings.APP_NAME}...")
    logger.info(f"Текущее окружение: {settings.ENVIRONMENT} (Debug: {settings.DEBUG})")

    # 1. Создаем асинхронный замок ожидания
    stop_event = asyncio.Event()

    # 2. Функция-обработчик сигналов выключения системы
    def shutdown_signal_handler():
        logger.warning("Получен системный сигнал на отключение (SIGINT/SIGTERM)...")
        stop_event.set()  # Открываем замок, чтобы завершить ожидания в main()

    # 3. Регистрируем перехватчики Ctrl+C и команд Docker (SIGTERM)
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown_signal_handler)
        except NotImplementedError:
            # Защита для Windows, где метод add_signal_handler частично ограничен
            pass

    # 4. Запускаем сетевые подключения Telegram-бота в фоне
    await bot.start()
    logger.success("Бот успешно авторизован и слушает сервера Telegram.")

    try:
        # 5. Программа «засыпает» здесь, пока не сработает stop_event.set()
        await stop_event.wait()
    except KeyboardInterrupt:
        # Дополнительный отлов Ctrl+C для Windows сред разработки
        logger.warning("Приложение остановлено пользователем через KeyboardInterrupt.")
    finally:
        # 6. Блок Graceful Shutdown: выполнится всегда перед выходом
        logger.info("Начало плавного отключения. Закрытие сессий...")
        await bot.stop()
        logger.success("Все соединения закрыты. Безопасный выход.")
        sys.exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass