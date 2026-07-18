from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str

    # Baïkal
    caldav_url: str
    caldav_username: str
    caldav_password: str

    # MQTT
    mqtt_host: str
    mqtt_port: int = 1883

    # Node-RED
    node_red_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

