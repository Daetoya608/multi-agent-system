from pathlib import Path
from typing import Optional
from pydantic import Field, SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# Определяем базовую директорию проекта, чтобы путь к .env всегда был точным
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Класс конфигурации приложения.
    Автоматически считывает переменные из окружения или .env файла.
    """

    # --- ОБЩИЕ НАСТРОЙКИ ---
    APP_NAME: str = "My Awesome App"
    # ENVIRONMENT: str = Field(default="development", validation_alias="ENV")
    # DEBUG: bool = False
    #
    # # --- НАСТРОЙКИ ТЕЛЕГРАМА ---
    # # SecretStr скрывает токен при выводе в лог (будет отображаться как *******)
    # BOT_TOKEN: SecretStr
    # API_ID: int
    # API_HASH: SecretStr
    #
    # # --- БРОКЕР СООБЩЕНИЙ ---
    # RABBITMQ_HOST: str = "localhost"
    # RABBITMQ_PORT: int = 5672

    # --- НАСТРОЙКА ИСТОЧНИКА НАСТРОЕК (МЕТАДАННЫЕ) ---
    model_config = SettingsConfigDict(
        # Указываем файл .env и его кодировку
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",

        # Если в .env будут "лишние" переменные, которых нет в классе — игнорируем их
        extra="ignore",

        # Разрешаем регистронезависимое чтение (например, bot_token в .env тоже применится)
        case_sensitive=False
    )


# Создаем синглтон настроек для импорта в другие модули
settings = Settings()