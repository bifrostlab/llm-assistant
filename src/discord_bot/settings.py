from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

  DISCORD_BOT_TOKEN: str
  DISCORD_GUILD_ID: int
  AI_SERVER_URL: str = "http://localhost:8000"
