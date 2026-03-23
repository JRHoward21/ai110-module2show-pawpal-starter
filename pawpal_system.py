from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable

@dataclass
class Task:
    name: str
    description: str
    duration: int  # in minutes
    frequency: str = "once"  # e.g. "daily", "weekly", "monthly"
    completed: bool = False
    priority: int = 1  # high values mean higher urgency
    category: str = "general"

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.completed = False

    def is_due(self, frequency: Optional[str] = None) -> bool:
        """Check if this task is due based on frequency and completion status."""
        if frequency is None:
            frequency = self.frequency
        return not self.completed and frequency in {"daily", "weekly", "monthly", "once"}

    def summary(self) -> str:
        """Return a formatted summary of this task's details and status."""
        status = "Done" if self.completed else "Pending"
        return f"{self.name}: {self.description} ({self.duration}m, {self.frequency}, {status})"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str):
        """Remove a task from this pet's task list by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_task(self, task_name: str) -> Optional[Task]:
        """Retrieve a task by name, or None if not found."""
        for t in self.tasks:
            if t.name == task_name:
                return t
        return None

    def pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]

    def completed_tasks(self) -> List[Task]:
        """Return all completed tasks for this pet."""
        return [t for t in self.tasks if t.completed]


class DailyPlanner:
    def __init__(self):
        self.pets: Dict[str, Pet] = {}

    def add_pet(self, pet: Pet):
        """Register a pet in the daily planner."""
        self.pets[pet.name] = pet

    def remove_pet(self, pet_name: str):
        """Remove a pet from the daily planner by name."""
        self.pets.pop(pet_name, None)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Retrieve a pet by name, or None if not found."""
        return self.pets.get(pet_name)

    def all_pets(self) -> List[Pet]:
        """Return a list of all registered pets."""
        return list(self.pets.values())

    def all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Retrieve all tasks across all pets, optionally filtering by completion status."""
        tasks: List[Task] = []
        for pet in self.pets.values():
            tasks.extend(pet.tasks)
        if not include_completed:
            tasks = [t for t in tasks if not t.completed]
        return tasks

    def all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        return self.all_tasks(include_completed=False)

    def tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Retrieve all tasks for a specific pet."""
        pet = self.get_pet(pet_name)
        return pet.tasks if pet else []

    def tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Retrieve all tasks matching a specified frequency."""
        return [t for t in self.all_tasks() if t.frequency == frequency]


class Schedule:
    def __init__(self, planner: DailyPlanner):
        self.planner = planner
        self.scheduled_tasks: List[Task] = []
        self.total_time: int = 0

    def retrieve_tasks(self, pet_name: Optional[str] = None, only_pending: bool = True) -> List[Task]:
        """Retrieve tasks for scheduling, optionally filtered by pet and completion status."""
        if pet_name:
            tasks = self.planner.tasks_by_pet(pet_name)
        else:
            tasks = self.planner.all_tasks()
        if only_pending:
            tasks = [t for t in tasks if not t.completed]
        return tasks

    def organize_tasks(self, tasks: Iterable[Task], by: str = "priority") -> List[Task]:
        """Sort tasks by duration, category, or priority (default)."""
        if by == "duration":
            return sorted(tasks, key=lambda t: t.duration)
        if by == "category":
            return sorted(tasks, key=lambda t: (t.category, -t.priority, t.duration))
        # default: priority first, then shortest duration
        return sorted(tasks, key=lambda t: (-t.priority, t.duration, t.name))

    def build(self,
              available_time: int,
              pet_name: Optional[str] = None,
              categories: Optional[List[str]] = None,
              keep_completed: bool = False
              ) -> List[Task]:
        """Build an optimized schedule within the given time constraint."""
        if available_time <= 0:
            raise ValueError("available_time must be positive")

        candidates = self.retrieve_tasks(pet_name=pet_name, only_pending=not keep_completed)

        if categories:
            candidates = [t for t in candidates if t.category in categories]

        ordered = self.organize_tasks(candidates, by="priority")

        selected: List[Task] = []
        used_time = 0
        for task in ordered:
            if used_time + task.duration <= available_time:
                selected.append(task)
                used_time += task.duration

        self.scheduled_tasks = selected
        self.total_time = used_time
        return selected

    def explain(self) -> str:
        """Return a human-readable explanation of the scheduled tasks."""
        if not self.scheduled_tasks:
            return "No tasks could be scheduled with the current constraints."

        lines = [f"Planned {self.total_time} minutes for {len(self.scheduled_tasks)} tasks:"]
        for t in self.scheduled_tasks:
            lines.append(f"- {t.name} ({t.duration}m, {t.category}, priority {t.priority})")
        return "\n".join(lines)

    def complete_task(self, task_name: str, pet_name: Optional[str] = None) -> bool:
        """Mark a task as complete by name, optionally scoped to a specific pet."""
        tasks = self.retrieve_tasks(pet_name=pet_name, only_pending=False)
        for t in tasks:
            if t.name == task_name:
                t.mark_complete()
                return True
        return False

