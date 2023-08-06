from abc import ABCMeta, abstractmethod


class AppConfig(metaclass=ABCMeta):

    APPLICATION_ENV = "RELIABILITY_PLATFORM_APPLICATION_ENV"
    APPLICATION_ID = "RELIABILITY_PLATFORM_APPLICATION_ID"
    APPLICATION_NAME = "RELIABILITY_PLATFORM_APPLICATION_NAME"
    ATTACK_LOADER = "RELIABILITY_PLATFORM_ATTACK_LOADER"

    # Proofdock specific settings
    PROOFDOCK_API_URL = "RELIABILITY_PLATFORM_PROOFDOCK_API_URL"
    PROOFDOCK_API_TOKEN = "RELIABILITY_PLATFORM_PROOFDOCK_API_TOKEN"

    @abstractmethod
    def get(self, item: str, default=None) -> str:
        raise NotImplementedError("Function get is not implemented")
