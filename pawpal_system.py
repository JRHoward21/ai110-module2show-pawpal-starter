from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    name: str
    duration: int
    priority: int
    category: str

@dataclass
class Pet:
    name: str
    type: str
    age: int
    tasks: List[Task]

class Schedule:
    def __init__(self, tasks: List[Task], total_time: int):
        self.tasks = tasks
        self.total_time = total_time

    def generate_explanation(self) -> str:
        # TODO: Implement explanation generation
        return f"Schedule with {len(self.tasks)} tasks totaling {self.total_time} minutes."

class DailyPlanner:
    def generate_plan(self, pet: Pet, available_time: int) -> Schedule:
        # TODO: Implement plan generation logic
        considered_tasks = self.consider_constraints(pet.tasks, available_time)
        total_time = sum(task.duration for task in considered_tasks)
        return Schedule(considered_tasks, total_time)

    def consider_constraints(self, tasks: List[Task], time: int) -> List[Task]:
        # TODO: Implement constraint consideration (e.g., priority, time limits)
        # For now, return tasks that fit within time, sorted by priority
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        selected = []
        current_time = 0
        for task in sorted_tasks:
            if current_time + task.duration <= time:
                selected.append(task)
                current_time += task.duration
        return selected
