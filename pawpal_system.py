from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable
from datetime import datetime, timedelta, date

@dataclass
class Owner:
    name: str
    email: str


@dataclass
class Task:
    name: str
    description: str
    duration: int  # in minutes
    frequency: str = "once"  # e.g. "daily", "weekly", "monthly"
    completed: bool = False
    priority: int = 1  # high values mean higher urgency
    category: str = "general"
    preferred_time: str = "any"  # "morning", "afternoon", "evening", "any"
    start_time: Optional[datetime] = None  # scheduled start time
    last_completed: Optional[datetime] = None  # when task was last completed
    due_date: Optional[date] = None  # when this task instance is due
    dependencies: List[str] = field(default_factory=list)  # task names that must come first

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True
        self.last_completed = datetime.now()

    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next occurrence of a recurring task."""
        if self.frequency == "once":
            return None
            
        # Create a new task instance with the same properties but reset completion status
        next_task = Task(
            name=self.name,
            description=self.description,
            duration=self.duration,
            frequency=self.frequency,
            priority=self.priority,
            category=self.category,
            preferred_time=self.preferred_time,
            dependencies=self.dependencies.copy() if self.dependencies else []
        )
        
        # Set the due date based on frequency
        if self.frequency == "daily":
            # Next occurrence is tomorrow (today + 1 day)
            next_task.due_date = datetime.now().date() + timedelta(days=1)
        elif self.frequency == "weekly":
            # Next occurrence is next week (today + 1 week)
            next_task.due_date = datetime.now().date() + timedelta(weeks=1)
        elif self.frequency == "monthly":
            # Next occurrence is next month (today + 30 days)
            next_task.due_date = datetime.now().date() + timedelta(days=30)
            
        return next_task

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.completed = False

    def is_due(self, frequency: Optional[str] = None) -> bool:
        """Check if this task is due based on frequency and completion status."""
        if self.completed:
            return False
            
        # If due_date is set, check against it
        if self.due_date:
            return datetime.now().date() >= self.due_date
            
        if frequency is None:
            frequency = self.frequency
            
        if frequency == "once":
            return not self.completed
            
        if not self.last_completed:
            return True  # Never done, so it's due
            
        now = datetime.now()
        days_since_completion = (now - self.last_completed).days
        
        if frequency == "daily":
            return days_since_completion >= 1
        elif frequency == "weekly":
            return days_since_completion >= 7
        elif frequency == "monthly":
            return days_since_completion >= 30
            
        return True  # Unknown frequency, assume due

    def conflicts_with(self, other: 'Task') -> bool:
        """Check if this task conflicts with another task."""
        if not self.start_time or not other.start_time:
            return False
            
        # Check for time overlap
        self_end = self.start_time + timedelta(minutes=self.duration)
        other_end = other.start_time + timedelta(minutes=other.duration)
        
        return (self.start_time < other_end and other.start_time < self_end)

    def summary(self) -> str:
        """Return a formatted summary of this task's details and status."""
        status = "Done" if self.completed else "Pending"
        time_info = f" at {self.start_time.strftime('%H:%M')}" if self.start_time else ""
        return f"{self.name}: {self.description} ({self.duration}m, {self.frequency}, {status}){time_info}"


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

    def filter_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status. Status can be 'pending', 'completed', or None for all."""
        if status == "pending":
            return self.pending_tasks()
        elif status == "completed":
            return self.completed_tasks()
        else:
            return self.tasks.copy()


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

    def tasks_by_status(self, completed: bool) -> List[Task]:
        """Retrieve all tasks with a specific completion status."""
        return [t for t in self.all_tasks() if t.completed == completed]

    def tasks_by_category(self, category: str) -> List[Task]:
        """Retrieve all tasks in a specific category."""
        return [t for t in self.all_tasks() if t.category == category]

    def tasks_due_today(self) -> List[Task]:
        """Retrieve all tasks that are due today based on frequency."""
        return [t for t in self.all_tasks() if t.is_due()]

    def filter_tasks(self, 
                    pet_name: Optional[str] = None,
                    status: Optional[str] = None,  # "pending", "completed", "all"
                    category: Optional[str] = None,
                    frequency: Optional[str] = None,
                    due_today: bool = False) -> List[Task]:
        """Filter tasks by multiple criteria."""
        tasks = self.all_tasks()
        
        if pet_name:
            tasks = [t for t in tasks if any(pet.name == pet_name for pet in self.all_pets() 
                                           if t in pet.tasks)]
        
        if status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]
            
        if category:
            tasks = [t for t in tasks if t.category == category]
            
        if frequency:
            tasks = [t for t in tasks if t.frequency == frequency]
            
        if due_today:
            tasks = [t for t in tasks if t.is_due()]
            
        return tasks


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

    def retrieve_tasks_filtered(self, 
                               pet_name: Optional[str] = None,
                               status: Optional[str] = None,  # "pending", "completed", "all"
                               category: Optional[str] = None,
                               frequency: Optional[str] = None,
                               due_today: bool = False) -> List[Task]:
        """Retrieve tasks with advanced filtering options."""
        return self.planner.filter_tasks(
            pet_name=pet_name,
            status=status,
            category=category,
            frequency=frequency,
            due_today=due_today
        )

    def organize_tasks(self, tasks: Iterable[Task], by: str = "priority") -> List[Task]:
        """Sort tasks by various criteria: priority, duration, category, time, start_time."""
        if by == "duration":
            return sorted(tasks, key=lambda t: t.duration)
        elif by == "category":
            return sorted(tasks, key=lambda t: (t.category, -t.priority, t.duration))
        elif by == "time":
            # Sort by preferred time, then priority
            time_order = {"morning": 0, "afternoon": 1, "evening": 2, "any": 3}
            return sorted(tasks, key=lambda t: (time_order.get(t.preferred_time, 3), -t.priority, t.duration))
        elif by == "start_time":
            # Sort by scheduled start time, with None values at the end
            return sorted(tasks, key=lambda t: t.start_time if t.start_time else datetime.max)
        elif by == "name":
            return sorted(tasks, key=lambda t: t.name)
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
                
                # Handle recurring tasks
                if t.frequency != "once":
                    next_task = t.create_next_occurrence()
                    if next_task:
                        # Find the pet and add the next occurrence
                        if pet_name:
                            pet = self.planner.get_pet(pet_name)
                            if pet:
                                pet.add_task(next_task)
                        else:
                            # If no specific pet, try to find which pet this task belongs to
                            for pet in self.planner.all_pets():
                                if t in pet.tasks:
                                    pet.add_task(next_task)
                                    break
                
                return True
        return False

    def get_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Find which pet a task belongs to."""
        try:
            for pet in self.planner.all_pets():
                if task in pet.tasks:
                    return pet
            return None
        except Exception as e:
            # Return None if there's any error (e.g., planner not initialized)
            return None

    def detect_conflicts(self, scheduled_tasks: List[Task]) -> List[str]:
        """Detect scheduling conflicts across tasks.

        This inspects provided tasks that have assigned start times and reports
        either same-pet or cross-pet overlaps. It defends against missing attributes
        and keeps failure mode as warnings to avoid crashing the app.

        Args:
            scheduled_tasks: List of Task objects that may include start_time.

        Returns:
            List[str]: conflit warning messages (empty if no conflicts).
        """
        conflicts = []
        
        try:
            # Input validation
            if not scheduled_tasks:
                return conflicts
                
            if not hasattr(self, 'planner') or self.planner is None:
                conflicts.append("Warning: No planner available for conflict detection")
                return conflicts
            
            # Filter tasks that have start times for efficiency
            tasks_with_times = [task for task in scheduled_tasks if task and hasattr(task, 'start_time') and task.start_time]
            
            if len(tasks_with_times) < 2:
                return conflicts  # Need at least 2 tasks to have conflicts
            
            # Check for conflicts
            for i, task1 in enumerate(tasks_with_times):
                try:
                    pet1 = self.get_pet_for_task(task1)
                    pet1_name = pet1.name if pet1 and hasattr(pet1, 'name') else "Unknown"
                    
                    for task2 in tasks_with_times[i+1:]:
                        try:
                            if not hasattr(task2, 'start_time') or not task2.start_time:
                                continue
                                
                            # Check for time overlap
                            if hasattr(task1, 'conflicts_with') and callable(getattr(task1, 'conflicts_with', None)):
                                if task1.conflicts_with(task2):
                                    pet2 = self.get_pet_for_task(task2)
                                    pet2_name = pet2.name if pet2 and hasattr(pet2, 'name') else "Unknown"
                                    
                                    task1_name = getattr(task1, 'name', 'Unknown Task')
                                    task2_name = getattr(task2, 'name', 'Unknown Task')
                                    
                                    if pet1 and pet2 and pet1 == pet2:
                                        # Same pet conflict
                                        conflicts.append(f"Same-pet conflict: '{task1_name}' and '{task2_name}' for pet '{pet1_name}' overlap in time")
                                    else:
                                        # Different pets conflict
                                        conflicts.append(f"Cross-pet conflict: '{task1_name}' (pet: {pet1_name}) and '{task2_name}' (pet: {pet2_name}) overlap in time")
                            else:
                                conflicts.append(f"Warning: Task '{getattr(task1, 'name', 'Unknown')}' missing conflict detection method")
                                
                        except Exception as e:
                            task1_name = getattr(task1, 'name', 'Unknown Task')
                            task2_name = getattr(task2, 'name', 'Unknown Task')
                            conflicts.append(f"Warning: Error checking conflict between '{task1_name}' and '{task2_name}': {str(e)}")
                            
                except Exception as e:
                    task1_name = getattr(task1, 'name', 'Unknown Task')
                    conflicts.append(f"Warning: Error processing task '{task1_name}': {str(e)}")
                    
        except Exception as e:
            conflicts.append(f"Warning: Unexpected error in conflict detection: {str(e)}")
            
        return conflicts

    def assign_time_slots(self, tasks: List[Task], start_hour: int = 9) -> List[Task]:
        """Assign time slots to tasks starting from a given hour."""
        current_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
        
        for task in tasks:
            task.start_time = current_time
            current_time += timedelta(minutes=task.duration)
            
        return tasks

    def build_with_time_slots(self,
                             available_time: int,
                             start_hour: int = 9,
                             pet_name: Optional[str] = None,
                             categories: Optional[List[str]] = None) -> List[Task]:
        """Build schedule with assigned time slots and conflict detection."""
        # Get tasks due today
        candidates = self.retrieve_tasks_filtered(
            pet_name=pet_name,
            status="pending",
            due_today=True
        )
        
        if categories:
            candidates = [t for t in candidates if t.category in categories]

        # Sort by time preference, then priority
        ordered = self.organize_tasks(candidates, by="time")

        # Select tasks that fit in available time
        selected = []
        used_time = 0
        for task in ordered:
            if used_time + task.duration <= available_time:
                selected.append(task)
                used_time += task.duration

        # Assign time slots
        self.assign_time_slots(selected, start_hour)
        
        # Check for conflicts (though with sequential assignment, there shouldn't be any)
        conflicts = self.detect_conflicts(selected)
        if conflicts:
            # If conflicts exist, try to resolve by reordering
            selected = self.resolve_conflicts(selected)
        
        self.scheduled_tasks = selected
        self.total_time = used_time
        return selected

    def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Try to resolve schedule conflicts with a simple priority reordering.

        This method is a best-effort resolver for overlapping tasks.
        It reorders by descending priority and reassigns slots sequentially from
        the earliest existing start time.

        Args:
            tasks: List of scheduled Task objects (may contain overlaps).

        Returns:
            List[Task]: reordered tasks with updated start_time assignments.
        """
        # Simple resolution: sort by priority and reassign times
        resolved = sorted(tasks, key=lambda t: (-t.priority, t.duration))
        start_time = min((t.start_time for t in resolved if t.start_time), default=datetime.now())
        if start_time:
            start_hour = start_time.hour
            return self.assign_time_slots(resolved, start_hour)
        return resolved

    def get_schedule_summary(self) -> str:
        """Get a detailed summary including conflicts and time slots."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        lines = [f"Schedule Summary: {self.total_time} minutes for {len(self.scheduled_tasks)} tasks"]
        lines.append("")
        
        for i, task in enumerate(self.scheduled_tasks, 1):
            time_str = f" at {task.start_time.strftime('%H:%M')}" if task.start_time else ""
            lines.append(f"{i}. {task.name} ({task.duration}m, priority {task.priority}){time_str}")
            if task.dependencies:
                lines.append(f"   Dependencies: {', '.join(task.dependencies)}")
        
        conflicts = self.detect_conflicts(self.scheduled_tasks)
        if conflicts:
            lines.append("")
            lines.append("⚠️ Conflicts detected:")
            for conflict in conflicts:
                lines.append(f"   {conflict}")
        
        return "\n".join(lines)

