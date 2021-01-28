# CLASS IMPLEMENTATION OF PERIODIC SCHEDULE ALGORITHM
# FOR THE ALGORITHM SIMULATOR PROJECT
# DEVELOPED BY: ELIZABELLE SERDIÑA
# SUPERVISED BY: GEORGE CHARALAMBOUS
# (C)2020
import schedule


class Periodic(schedule):
    def __init__(self, job):
        self.typeofjob = job
        self.gymitems = [["Plank Workout", "5 mins", [
            ["Basic Plank", None, 60],
            ["Elbow Plank", None, 30],
            ["Leg raised Plank", "30 Seconds - Each Leg", 60],
            ["One Side Plank", "30 Seconds - Each Side", 60],
            ["Basic Plank", None, 30],
            ["Elbow Plank", None, 60]
        ]], ["5-Minute Workout #1", "5 mins", [
            ["Burpees", None, 60],
            ["Jumping Jacks", None, 60],
            ["Mountain Climbers", None, 60],
            ["Push-ups", None, 60],
            ["Running in Place", None, 60]
        ]]]
