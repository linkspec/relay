from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CA
    internal_ca: str = "certs/root_ca.crt"

    # LLM
    ollama_url: str
    ollama_model: str
    
    # Baïkal
    caldav_url: str
    caldav_username: str
    caldav_password: str

    # MQTT
    mqtt_host: str
    mqtt_port: int = 1883

    # Node-RED
    node_red_url: str

    # Vikunja 
    vikunja_api_key: str
    vikunja_url: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

