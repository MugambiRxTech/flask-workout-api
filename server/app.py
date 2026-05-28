from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# -------------------- WORKOUT ROUTES --------------------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """List all workouts."""
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """Get a single workout with its exercises and workout_exercise details."""
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout."""
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    try:
        new_workout = Workout(
            date=workout_schema.fields['date'].deserialize(data['date']),
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(new_workout)), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout and its associated workout exercises."""
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted successfully."}), 200)


# -------------------- EXERCISE ROUTES --------------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises."""
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """Get a single exercise with its associated workouts."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise."""
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    try:
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise and its associated workout exercises."""
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted successfully."}), 200)


# -------------------- WORKOUT EXERCISE ROUTES --------------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout with reps/sets/duration."""
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)

    data = request.get_json()
    errors = workout_exercise_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(we)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(we)), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)