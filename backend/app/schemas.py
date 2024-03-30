from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    name = fields.Str(required=True)
    task_type = fields.Str(required=True, validate=validate.OneOf(["single", "repeat"]))
    execute_type = fields.Str(required=True, validate=validate.OneOf(["immediate", "scheduled"]))
    schedule = fields.Str(validate=validate.OneOf(['daily', 'hourly', 'minutely', 'monthly']), missing=None)
    start_time = fields.DateTime(missing=None)
    next_run = fields.DateTime(missing=None) 