import os
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings:
    def __init__(self):
        self.environment = Environment(
            os.getenv("ENVIRONMENT", Environment.DEVELOPMENT)
        )

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION


# Global settings instance
settings = Settings()
