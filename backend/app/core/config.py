from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str
    REDIS_URL: str
    REDIS_PORT: str
    REDIS_USER: str
    REDIS_PASSWORD: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_S3_BUCKET: str
    # GROQ_API_KEY: str
    # LLM_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()