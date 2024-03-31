from marshmallow import fields, Schema, validate, ValidationError

class NullableDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if value == '':
            return None
        return super()._deserialize(value, attr, data, **kwargs)

class TaskSchema(Schema):
    name = fields.Str(required=True)
    task_type = fields.Str(required=True, validate=validate.OneOf(["single", "repeat", '', None]))
    execute_type = fields.Str(required=True, validate=validate.OneOf(["immediate", "scheduled", '', None]))
    schedule = fields.Str(validate=validate.OneOf(['daily', 'hourly', 'minutely', 'monthly', 'weekly', '', None]), missing=None)
    start_time = NullableDateTimeField(missing=None)
    next_run = NullableDateTimeField(missing=None)
    day_of_week = fields.List(fields.Str(), validate=validate.ContainsOnly(["0", "1", "2", "3", "4", "5", "6", '', None]), missing=None)
