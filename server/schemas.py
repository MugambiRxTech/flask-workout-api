from marshmallow import Schema, fields, validate, validates, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None)
    sets = fields.Int(load_default=None)
    duration_seconds = fields.Int(load_default=None)

    # Schema Validations
    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0.")

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0.")

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be greater than 0.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be empty."))
    category = fields.Str(required=True, validate=validate.OneOf(
        ['strength', 'cardio', 'flexibility', 'balance', 'endurance'],
        error="Category must be one of: strength, cardio, flexibility, balance, endurance."
    ))
    equipment_needed = fields.Bool(required=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, error_messages={"required": "Date is required."})
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(load_default=None)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

    # Schema Validations
    @validates('duration_minutes')
    def validate_duration_minutes(self, value):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0.")