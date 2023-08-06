import json
from typing import Callable, Dict, List

import requests
from circuitbreaker import circuit
from logzero import logger

from proofdock.rp.core.config import AppConfig
from proofdock.rp.core.loader import AttackLoader
from proofdock.rp.core.proofdock.session import client_session, get_error_message

DEFAULT_ROUTE = '/v1/attacks/synchronize'
DEFAULT_DOMAIN = "https://chaosapi.proofdock.io"


class ProofdockAttackLoader(AttackLoader):

    def __init__(self, app_config: AppConfig):
        self._app_config = app_config

    def is_allowed_to_call_endpoint(self):
        token = self._app_config.get(AppConfig.PROOFDOCK_API_TOKEN)
        name = self._app_config.get(AppConfig.APPLICATION_NAME)
        id = self._app_config.get(AppConfig.APPLICATION_ID)
        return bool(token and name and id)

    def run(self, set_attacks_action_func: Callable[[Dict], None], get_attack_capabilities_func: Callable[[], List]):
        with client_session(self._app_config.get(AppConfig.PROOFDOCK_API_TOKEN), verify_tls=False) as session:
            try:
                self._synchronize(session, set_attacks_action_func, get_attack_capabilities_func)
            except Exception as e:
                self.unload_actions()
                logger.warn(str(e))

    @circuit(expected_exception=(requests.RequestException, requests.ConnectionError, requests.ConnectTimeout),
             failure_threshold=5, recovery_timeout=120)
    def _synchronize(self, session, set_attacks_action_func, get_attack_capabilities_func):
        # Arrange
        timeout_in_seconds = 13
        target_domain = self._app_config.get(AppConfig.PROOFDOCK_API_URL, DEFAULT_DOMAIN)
        payload = self.create_request_body(self._app_config, get_attack_capabilities_func())

        # Act
        response = session.post(target_domain + DEFAULT_ROUTE, data=payload, timeout=timeout_in_seconds)
        if response.ok:
            attacks = response.json()
            set_attacks_action_func(attacks)
        else:
            raise Exception(get_error_message(response))

    def create_request_body(self, app_config, capabilities):
        payload = json.dumps({
            "id": app_config.get(AppConfig.APPLICATION_ID),
            "env": app_config.get(AppConfig.APPLICATION_ENV),
            "name": app_config.get(AppConfig.APPLICATION_NAME),
            "capabilities": capabilities
        })
        return payload
