# Flask Workout API

## Description
A RESTful backend API for a workout tracking application used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow, it allows trainers to manage workouts and exercises, track sets, reps, and duration, and associate exercises with specific workouts.

## Installation

1. Clone the repository:
git clone https://github.com/MugambiRxTech/flask-workout-api.git
cd flask-workout-api
2. Install dependencies:
pipenv install
pipenv shell
3. Navigate to the server directory:
cd server
4. Initialize and migrate the database:
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
5. Seed the database:
python seed.py
## Running the App
python app.py
The API will run on `http://127.0.0.1:5555`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout with its exercises and details |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated entries |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise with its associated workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated entries |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets/duration |

## Models

- **Exercise** - stores exercise name, category, and equipment requirement
- **Workout** - stores workout date, duration, and notes
- **WorkoutExercise** - join table linking workouts and exercises with reps, sets, and duration

## Validations

### Table Constraints
- Exercise name must be unique
- Reps must be greater than 0
- Sets must be greater than 0
- A workout-exercise combination must be unique

### Model Validations
- Exercise name cannot be empty
- Exercise category must be one of: strength, cardio, flexibility, balance, endurance
- Workout duration must be greater than 0

### Schema Validations
- Reps must be greater than 0
- Sets must be greater than 0
- Duration in seconds must be greater than 0
- Workout duration in minutes must be greater than 0