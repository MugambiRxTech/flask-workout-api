from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')

    # Model Validations
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Exercise name cannot be empty.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        allowed = ['strength', 'cardio', 'flexibility', 'balance', 'endurance']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()

    def __repr__(self):
        return f'<Exercise {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

    # Model Validations
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0.")
        return value

    @validates('date')
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Date cannot be empty.")
        return value

    def __repr__(self):
        return f'<Workout {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Table Constraints
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
        db.CheckConstraint('reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets > 0', name='check_sets_positive'),
    )

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'