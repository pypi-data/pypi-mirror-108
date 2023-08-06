import fnmatch

from proofdock.rp import core
from proofdock.rp.core import inject, dice, config, chaos


def execute(target=None, attack_actions=None, attack_ctx={}):
    for action in attack_actions:

        if not _is_app_targeted(target):
            continue

        if not _is_type_valid(action.get('type'), attack_ctx.get('type')) \
                or not _are_params_valid(action.get('params', {}), attack_ctx.get('params')):
            continue

        if not _is_lucky_to_be_attacked(action.get(core.ATTACK_KEY_PROBABILITY)):
            continue

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_DELAY:
            inject.delay(action[core.ATTACK_KEY_VALUE])

        if action[core.ATTACK_KEY_ACTION_NAME] == core.ATTACK_ACTION_FAULT:
            inject.failure(action[core.ATTACK_KEY_VALUE])


def _is_lucky_to_be_attacked(probability):
    is_lucky = dice.roll(probability)

    return is_lucky


def _is_type_valid(attack_type, ctx_type):
    if attack_type is None or ctx_type is None:
        return False

    return attack_type == ctx_type


def _are_params_valid(attack_params, ctx_params):
    for param_key, param_value in attack_params.items():
        # if params defined in attack does not exists on context do not attack
        if param_key not in ctx_params or not ctx_params[param_key]:
            return False

        # if params defined in attack and one passed in context matches (with wildcars)
        # accepts this params and continue checking
        if fnmatch.fnmatch(ctx_params[param_key], param_value or '*'):
            continue
        else:
            return False

    return True


def _is_app_targeted(target):
    if not target:
        return True

    application = target.get(core.ATTACK_KEY_TARGET_APPLICATION)
    environment = target.get(core.ATTACK_KEY_TARGET_ENVIRONMENT)

    is_app_targeted = \
        (application and application == chaos.loaded_app_config.get(config.AppConfig.APPLICATION_NAME)) \
        or not application

    is_env_targeted = \
        (environment and environment == chaos.loaded_app_config.get(config.AppConfig.APPLICATION_ENV)) \
        or not environment

    return is_app_targeted and is_env_targeted
