from marshmallow import Schema, fields


class AttackTargetSchema(Schema):
    class Meta:
        fields = ["application", "environment"]

    # (required) Name of the application
    application = fields.String(required=True)

    # (optional) Environment in which the application is running, as the application can have the same
    # name across different environment you may want to set it to uniquely identify the application
    environment = fields.String(required=False)


class AttackActionSchema(Schema):
    class Meta:
        fields = ["type", "name", "value", "probability", "params"]

    # (required) Type of the attack e.g python.flask.request
    type = fields.String(required=True)

    # (required) Name of the action (delay, fault)
    name = fields.String(required=True)

    # (required) Value of the attack action, specific to the action
    # e.g.: 5 for attack "delay" means delay 5s
    value = fields.String(required=True)

    # (optional) Probabilit of the attack, if not set it will be 100%
    probability = fields.Number(required=False)

    # (optional) Additional parameters of the attack actions that are specific
    # to the type and name of the attack.
    # E.g for attack type "python.flask.request" and name "delay" additional
    # parameters may include "route": "/users/*"
    params = fields.Dict(required=False)


class AttackSchema(Schema):
    class Meta:
        fields = ["actions", "target"]

    # (required) List of the attack actions
    actions = fields.Nested(AttackActionSchema, required=True, many=True)

    # (optional) Target specify what application should be attacked, if not set all targets will be attacked
    target = fields.Nested(AttackTargetSchema, required=False)


attack_schema = AttackSchema(many=False)
attack_action_schema = AttackActionSchema(many=False)
attack_actions_schema = AttackActionSchema(many=True)
