#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create Exercises
    e1 = Exercise(name="Barbell Squat", category="strength", equipment_needed=True)
    e2 = Exercise(name="Running", category="cardio", equipment_needed=False)
    e3 = Exercise(name="Yoga Stretch", category="flexibility", equipment_needed=False)
    e4 = Exercise(name="Deadlift", category="strength", equipment_needed=True)
    e5 = Exercise(name="Jump Rope", category="endurance", equipment_needed=True)

    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()

    # Create Workouts
    w1 = Workout(date=date(2024, 1, 10), duration_minutes=60, notes="Morning strength session")
    w2 = Workout(date=date(2024, 1, 12), duration_minutes=45, notes="Cardio and flexibility day")
    w3 = Workout(date=date(2024, 1, 15), duration_minutes=30, notes="Quick endurance workout")

    db.session.add_all([w1, w2, w3])
    db.session.commit()

    # Create WorkoutExercises (join table entries)
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, sets=4, reps=8)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e4.id, sets=3, reps=6)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, duration_seconds=600)
    we5 = WorkoutExercise(workout_id=w3.id, exercise_id=e5.id, sets=3, reps=50)

    db.session.add_all([we1, we2, we3, we4, we5])
    db.session.commit()

    print("Seeding complete!")