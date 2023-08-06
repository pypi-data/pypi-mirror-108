from typing import Dict, List

from logzero import logger

from proofdock.rp.core import config, loader, parse, executor
# Application configuration
from proofdock.rp.core.inject import ChaosMiddlewareError

loaded_app_config = None

# List of attack actions that are intended for this target (running application)
loaded_attack_actions = []

# List of type of attacks that were detected
attack_capabilities = []


def register(app_config: config.AppConfig, capabilities: List[str] = None):
    """Register an application"""
    if app_config is None:
        raise Exception('Application config is not set')

    global attack_capabilities
    if capabilities and len(capabilities) > 0:
        attack_capabilities = capabilities

    global loaded_app_config
    if loaded_app_config is None:
        loaded_app_config = app_config
        loader.init(loaded_app_config, _set_attack_action, _get_attack_capabilities)


def attack(attack_ctx: Dict = {}):
    """Execute chaos"""

    try:
        # Update capabilities
        _update_attack_capabilities(attack_ctx)

        # Fault injection from Reliability Platform
        if loaded_attack_actions and len(loaded_attack_actions) > 0:
            executor.execute(attack_actions=loaded_attack_actions, attack_ctx=attack_ctx)

    except ChaosMiddlewareError as error:
        if error.__cause__:
            raise error.__cause__ from None
        else:
            raise error from None

    except Exception as ex:
        logger.error("Unable to perform chaos attack. Error: %s", ex, stack_info=True)


def _update_attack_capabilities(attack_ctx: Dict):
    if "type" in attack_ctx and attack_ctx["type"] not in attack_capabilities:
        attack_capabilities.append(attack_ctx["type"])


def _set_attack_action(attack_action: List[Dict]):
    # Validate
    parsed_attack_actions = parse.attack_actions(attack_action)

    # Configure
    global loaded_attack_actions
    loaded_attack_actions = parsed_attack_actions
    logger.debug("Current attack actions: {}".format(loaded_attack_actions))


def _get_attack_capabilities():
    return attack_capabilities
