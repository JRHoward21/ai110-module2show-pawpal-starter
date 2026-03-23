from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Task:
    name: str
    duration: int
    priority: int  # Higher integer values indicate higher priority
    category: str
    prerequisites: List[str] = None  # List of task names that must be completed first

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []

@dataclass
class Pet:
    name: str
    type: str
    age: int
    tasks: List[Task]

class Schedule:
    def __init__(self, pet: Pet, tasks: List[Task], total_time: int):
        self.pet = pet
        self.tasks = tasks
        self.total_time = total_time

    def generate_explanation(self) -> str:
        if not self.tasks:
            return f"No tasks scheduled for {self.pet.name} today."
        
        task_summary = ", ".join(f"{task.name} ({task.category}, {task.duration} min)" for task in self.tasks)
        categories = set(task.category for task in self.tasks)
        category_balance = f" covering categories: {', '.join(categories)}" if len(categories) > 1 else f" focused on {list(categories)[0]}"
        return f"Schedule for {self.pet.name} ({self.pet.type}, age {self.pet.age}): {task_summary}. Total time: {self.total_time} minutes{category_balance}."

class DailyPlanner:
    def generate_plan(self, pet: Pet, available_time: int) -> Schedule:
        if available_time <= 0:
            raise ValueError("Available time must be positive.")
        if not pet.tasks:
            return Schedule(pet, [], 0)
        
        considered_tasks = self.consider_constraints(pet.tasks, available_time)
        total_time = sum(task.duration for task in considered_tasks)
        schedule = Schedule(pet, considered_tasks, total_time)
        # Optional: Update pet state if needed (e.g., mark tasks as done, but not implemented here)
        return schedule

    def consider_constraints(self, tasks: List[Task], time: int) -> List[Task]:
        # Validate inputs
        if time <= 0:
            return []
        
        # Build task map for prerequisites
        task_map = {task.name: task for task in tasks}
        
        # Filter tasks with unmet prerequisites (simple check: assume all tasks are available)
        valid_tasks = [task for task in tasks if all(prereq in task_map for prereq in task.prerequisites)]
        
        # Use a simple knapsack-like approach for optimal selection by priority
        # Treat priority as value, duration as weight, time as capacity
        n = len(valid_tasks)
        dp = [[0] * (time + 1) for _ in range(n + 1)]
        selected = [[[] for _ in range(time + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            task = valid_tasks[i - 1]
            for w in range(time + 1):
                if task.duration <= w:
                    if dp[i - 1][w - task.duration] + task.priority > dp[i - 1][w]:
                        dp[i][w] = dp[i - 1][w - task.duration] + task.priority
                        selected[i][w] = selected[i - 1][w - task.duration] + [task]
                    else:
                        dp[i][w] = dp[i - 1][w]
                        selected[i][w] = selected[i - 1][w]
                else:
                    dp[i][w] = dp[i - 1][w]
                    selected[i][w] = selected[i - 1][w]
        
        # Balance categories: Ensure at least one task per category if possible
        optimal = selected[n][time]
        categories_in_schedule = set(task.category for task in optimal)
        all_categories = set(task.category for task in valid_tasks)
        if categories_in_schedule != all_categories:
            # Add one task from missing categories if space allows
            for cat in all_categories - categories_in_schedule:
                cat_tasks = [t for t in valid_tasks if t.category == cat and t not in optimal]
                cat_tasks.sort(key=lambda t: t.priority, reverse=True)
                for t in cat_tasks:
                    if sum(task.duration for task in optimal) + t.duration <= time:
                        optimal.append(t)
                        break
        
        return optimal
