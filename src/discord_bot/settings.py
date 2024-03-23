from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
  AI_SERVER_URL: str = "http://localhost:8000"  # or https://api.openai.com/v1
  API_KEY: str = "FAKE"
  MODEL_CHOICES: list[str] = ["gpt-3.5-turbo", "gpt-4", "phi"]
  DEFAULT_MODEL: str = MODEL_CHOICES[2]
  DISCORD_BOT_TOKEN: str
