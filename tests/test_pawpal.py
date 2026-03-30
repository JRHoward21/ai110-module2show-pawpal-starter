import pytest
from pawpal_system import Owner, Task, Pet
from datetime import datetime, timedelta, date
from pawpal_system import DailyPlanner, Schedule


class TestOwnerCreation:
    """Test suite for Owner creation functionality."""
    
    def test_owner_creation_with_name_and_email(self):
        """Verify that an Owner can be created with name and email."""
        owner = Owner(name='Jordan', email='jordan@example.com')
        assert owner.name == 'Jordan'
        assert owner.email == 'jordan@example.com'
    
    def test_owner_attributes_are_accessible(self):
        """Verify that owner attributes can be retrieved and modified."""
        owner = Owner(name='Sam', email='sam@example.com')
        assert owner.name == 'Sam'
        owner.name = 'Samuel'
        assert owner.name == 'Samuel'


class TestTaskCompletion:
    """Test suite for Task completion functionality."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's completed status to True."""
        task = Task(
            name='Feed dog',
            description='Morning feeding',
            duration=10,
            frequency='daily',
            priority=3,
            category='feeding'
        )
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True
    
    def test_mark_incomplete_changes_status(self):
        """Verify that calling mark_incomplete() changes the task's completed status to False."""
        task = Task(
            name='Feed dog',
            description='Morning feeding',
            duration=10,
            frequency='daily',
            priority=3,
            category='feeding',
            completed=True
        )
        assert task.completed is True
        task.mark_incomplete()
        assert task.completed is False


class TestTaskAddition:
    """Test suite for adding tasks to pets."""
    
    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name='Fluffy', species='cat', age=3)
        assert len(pet.tasks) == 0
        
        task1 = Task(
            name='Litter box',
            description='Clean litter box',
            duration=15,
            frequency='daily',
            priority=4,
            category='hygiene'
        )
        pet.add_task(task1)
        assert len(pet.tasks) == 1
        
        task2 = Task(
            name='Play time',
            description='Interactive play',
            duration=20,
            frequency='daily',
            priority=3,
            category='exercise'
        )
        pet.add_task(task2)
        assert len(pet.tasks) == 2
    
    def test_added_task_is_in_pet_tasks(self):
        """Verify that an added task actually appears in the pet's task list."""
        pet = Pet(name='Rex', species='dog', age=5)
        task = Task(
            name='Walk',
            description='Morning walk',
            duration=30,
            frequency='daily',
            priority=5,
            category='exercise'
        )
        pet.add_task(task)
        assert task in pet.tasks
        assert pet.get_task('Walk') == task


# ==================== FIXTURES ====================

@pytest.fixture
def planner():
    """Fixture providing a clean DailyPlanner instance."""
    return DailyPlanner()


@pytest.fixture
def schedule(planner):
    """Fixture providing a Schedule instance with a planner."""
    return Schedule(planner)


@pytest.fixture
def sample_pets_with_tasks(planner):
    """Fixture providing a planner with multiple pets and various tasks."""
    # Create pets
    dog = Pet(name='Rex', species='dog', age=5)
    cat = Pet(name='Fluffy', species='cat', age=3)
    
    # Create tasks with varying priorities for Rex
    task_high_priority = Task(
        name='Urgent feeding',
        description='High-priority feeding',
        duration=15,
        frequency='daily',
        priority=5,
        category='feeding'
    )
    task_med_priority = Task(
        name='Regular grooming',
        description='Standard grooming',
        duration=30,
        frequency='weekly',
        priority=3,
        category='grooming'
    )
    task_low_priority = Task(
        name='Optional playtime',
        description='Casual play',
        duration=20,
        frequency='daily',
        priority=1,
        category='exercise'
    )
    
    # Create tasks with different durations
    task_short = Task(
        name='Quick brush',
        description='Quick brushing',
        duration=5,
        frequency='daily',
        priority=2,
        category='grooming'
    )
    task_long = Task(
        name='Extended exercise',
        description='Long play session',
        duration=60,
        frequency='daily',
        priority=3,
        category='exercise'
    )
    
    # Add tasks to dog
    dog.add_task(task_high_priority)
    dog.add_task(task_med_priority)
    dog.add_task(task_low_priority)
    dog.add_task(task_short)
    dog.add_task(task_long)
    
    # Create tasks for cat
    cat_task = Task(
        name='Litter box cleaning',
        description='Clean and refill litter',
        duration=10,
        frequency='daily',
        priority=4,
        category='hygiene'
    )
    cat.add_task(cat_task)
    
    planner.add_pet(dog)
    planner.add_pet(cat)
    
    return planner


# ==================== SORTING CORRECTNESS TESTS ====================

class TestSortingCorrectness:
    """Test suite for organize_tasks sorting functionality."""
    
    def test_organize_tasks_by_priority_descending(self, sample_pets_with_tasks, schedule):
        """Verify tasks are sorted by priority (highest first) when sorted by priority."""
        tasks = sample_pets_with_tasks.all_tasks()
        organized = schedule.organize_tasks(tasks, by="priority")
        
        # Extract priorities in order
        priorities = [t.priority for t in organized]
        
        # Verify they are in descending order (highest priority first)
        assert priorities == sorted(priorities, reverse=True), \
            f"Tasks not sorted by priority descending. Got: {priorities}"
    
    def test_organize_tasks_default_is_priority(self, sample_pets_with_tasks, schedule):
        """Verify default sorting is by priority (descending), then duration."""
        tasks = sample_pets_with_tasks.all_tasks()
        organized_default = schedule.organize_tasks(tasks)
        organized_priority = schedule.organize_tasks(tasks, by="priority")
        
        assert [t.name for t in organized_default] == [t.name for t in organized_priority], \
            "Default sort should match priority sort"
    
    def test_organize_tasks_by_duration(self, sample_pets_with_tasks, schedule):
        """Verify tasks are sorted by duration (shortest first) when sorted by duration."""
        tasks = sample_pets_with_tasks.all_tasks()
        organized = schedule.organize_tasks(tasks, by="duration")
        
        # Extract durations
        durations = [t.duration for t in organized]
        
        # Verify they are in ascending order (shortest first)
        assert durations == sorted(durations), \
            f"Tasks not sorted by duration ascending. Got: {durations}"
    
    def test_organize_tasks_by_category(self, sample_pets_with_tasks, schedule):
        """Verify tasks are grouped by category and sorted alphabetically within groups."""
        tasks = sample_pets_with_tasks.all_tasks()
        organized = schedule.organize_tasks(tasks, by="category")
        
        # Extract categories to verify grouping
        categories = [t.category for t in organized]
        
        # Verify they are in sorted order
        assert categories == sorted(categories), \
            f"Tasks not sorted by category. Got: {categories}"
    
    def test_organize_tasks_by_name(self, sample_pets_with_tasks, schedule):
        """Verify tasks are sorted alphabetically by name."""
        tasks = sample_pets_with_tasks.all_tasks()
        organized = schedule.organize_tasks(tasks, by="name")
        
        # Extract names
        names = [t.name for t in organized]
        
        # Verify they are in alphabetical order
        assert names == sorted(names), \
            f"Tasks not sorted by name. Got: {names}"
    
    def test_organize_tasks_by_start_time(self, schedule):
        """Verify tasks with start_time are sorted chronologically."""
        now = datetime.now()
        
        task1 = Task(
            name='Morning task',
            description='First task',
            duration=30,
            priority=2,
            category='general',
            start_time=now + timedelta(hours=1)
        )
        task2 = Task(
            name='Afternoon task',
            description='Second task',
            duration=30,
            priority=2,
            category='general',
            start_time=now + timedelta(hours=3)
        )
        task3 = Task(
            name='Evening task',
            description='Third task',
            duration=30,
            priority=2,
            category='general',
            start_time=now + timedelta(hours=5)
        )
        
        tasks = [task3, task1, task2]  # Intentionally unsorted
        organized = schedule.organize_tasks(tasks, by="start_time")
        
        # Verify chronological order
        start_times = [t.start_time for t in organized]
        assert start_times == sorted(start_times), \
            "Tasks not sorted by start_time chronologically"
        assert organized[0].name == 'Morning task'
        assert organized[1].name == 'Afternoon task'
        assert organized[2].name == 'Evening task'
    
    def test_organize_tasks_by_time_preference(self, schedule):
        """Verify tasks are sorted by preferred time (morning -> afternoon -> evening)."""
        task_morning = Task(
            name='Morning',
            description='Morning task',
            duration=20,
            priority=2,
            category='general',
            preferred_time='morning'
        )
        task_evening = Task(
            name='Evening',
            description='Evening task',
            duration=20,
            priority=2,
            category='general',
            preferred_time='evening'
        )
        task_afternoon = Task(
            name='Afternoon',
            description='Afternoon task',
            duration=20,
            priority=2,
            category='general',
            preferred_time='afternoon'
        )
        task_any = Task(
            name='Anytime',
            description='Anytime task',
            duration=20,
            priority=2,
            category='general',
            preferred_time='any'
        )
        
        tasks = [task_any, task_evening, task_morning, task_afternoon]
        organized = schedule.organize_tasks(tasks, by="time")
        
        # Verify time preference order
        assert organized[0].name == 'Morning'
        assert organized[1].name == 'Afternoon'
        assert organized[2].name == 'Evening'
        assert organized[3].name == 'Anytime'
    
    def test_organize_empty_task_list(self, schedule):
        """Verify organizing an empty task list returns an empty list."""
        organized = schedule.organize_tasks([], by="priority")
        assert organized == []
    
    def test_organize_single_task(self, schedule):
        """Verify organizing a single task returns that task unchanged."""
        task = Task(
            name='Only task',
            description='Single task',
            duration=15,
            priority=3,
            category='general'
        )
        organized = schedule.organize_tasks([task], by="priority")
        assert len(organized) == 1
        assert organized[0] == task


# ==================== RECURRENCE LOGIC TESTS ====================

class TestRecurrenceLogic:
    """Test suite for recurring task logic (complete_task and create_next_occurrence)."""
    
    def test_create_next_occurrence_daily_task(self):
        """Verify that marking a daily task complete creates a new task for the next day."""
        task = Task(
            name='Daily feeding',
            description='Feed the pet',
            duration=15,
            frequency='daily',
            priority=3,
            category='feeding',
            due_date=date.today()
        )
        
        next_task = task.create_next_occurrence()
        
        assert next_task is not None, "next_task should not be None for daily task"
        assert next_task.name == task.name
        assert next_task.frequency == 'daily'
        assert next_task.completed is False
        # Next task should be due tomorrow
        expected_due_date = date.today() + timedelta(days=1)
        assert next_task.due_date == expected_due_date
    
    def test_create_next_occurrence_weekly_task(self):
        """Verify that a weekly task creates next occurrence a week later."""
        task = Task(
            name='Weekly grooming',
            description='Groom the pet',
            duration=45,
            frequency='weekly',
            priority=2,
            category='grooming',
            due_date=date.today()
        )
        
        next_task = task.create_next_occurrence()
        
        assert next_task is not None
        assert next_task.frequency == 'weekly'
        expected_due_date = date.today() + timedelta(weeks=1)
        assert next_task.due_date == expected_due_date
    
    def test_create_next_occurrence_monthly_task(self):
        """Verify that a monthly task creates next occurrence a month later."""
        task = Task(
            name='Monthly checkup',
            description='Vet checkup',
            duration=60,
            frequency='monthly',
            priority=4,
            category='health',
            due_date=date.today()
        )
        
        next_task = task.create_next_occurrence()
        
        assert next_task is not None
        assert next_task.frequency == 'monthly'
        expected_due_date = date.today() + timedelta(days=30)
        assert next_task.due_date == expected_due_date
    
    def test_create_next_occurrence_one_time_task(self):
        """Verify that one-time tasks don't create next occurrences."""
        task = Task(
            name='One-time task',
            description='Special event',
            duration=30,
            frequency='once',
            priority=2,
            category='general'
        )
        
        next_task = task.create_next_occurrence()
        
        assert next_task is None, "One-time tasks should not create next occurrences"
    
    def test_complete_task_recurring_creates_next(self, planner, schedule):
        """Verify that completing a recurring task creates a new task for the next occurrence."""
        # Add a pet with a daily task
        pet = Pet(name='Buddy', species='dog', age=4)
        daily_task = Task(
            name='Morning walk',
            description='Daily walk',
            duration=30,
            frequency='daily',
            priority=4,
            category='exercise',
            due_date=date.today()
        )
        pet.add_task(daily_task)
        planner.add_pet(pet)
        
        # Get initial task count
        initial_task_count = len(pet.tasks)
        
        # Complete the task
        result = schedule.complete_task('Morning walk', pet_name='Buddy')
        
        assert result is True, "complete_task should return True"
        assert daily_task.completed is True, "Original task should be marked complete"
        
        # Check that a new task was created
        assert len(pet.tasks) == initial_task_count + 1, \
            "A new task should be created after completing a recurring task"
        
        # Find the new task (should be the second one)
        new_task = [t for t in pet.tasks if not t.completed and t.name == 'Morning walk']
        assert len(new_task) == 1, "Should have exactly one incomplete task with same name"
        assert new_task[0].due_date == date.today() + timedelta(days=1), \
            "New task should be due tomorrow"
    
    def test_complete_task_one_time_no_recurrence(self, planner, schedule):
        """Verify that completing a one-time task doesn't create a new task."""
        pet = Pet(name='Fluffy', species='cat', age=2)
        one_time_task = Task(
            name='Bath time',
            description='Give bath',
            duration=20,
            frequency='once',
            priority=2,
            category='hygiene'
        )
        pet.add_task(one_time_task)
        planner.add_pet(pet)
        
        initial_task_count = len(pet.tasks)
        
        schedule.complete_task('Bath time', pet_name='Fluffy')
        
        # No new task should be created for one-time tasks
        assert len(pet.tasks) == initial_task_count, \
            "One-time task completion should not create a new task"
    
    def test_complete_task_sets_last_completed(self, planner, schedule):
        """Verify that completing a task sets the last_completed timestamp."""
        pet = Pet(name='Max', species='dog', age=3)
        task = Task(
            name='Medication',
            description='Give medication',
            duration=5,
            frequency='daily',
            priority=5,
            category='health'
        )
        pet.add_task(task)
        planner.add_pet(pet)
        
        assert task.last_completed is None, "Initial last_completed should be None"
        
        schedule.complete_task('Medication', pet_name='Max')
        
        assert task.last_completed is not None, "last_completed should be set after completion"
        assert isinstance(task.last_completed, datetime), "last_completed should be a datetime"
    
    def test_complete_nonexistent_task_returns_false(self, planner, schedule):
        """Verify that completing a nonexistent task returns False."""
        pet = Pet(name='Buddy', species='dog', age=2)
        planner.add_pet(pet)
        
        result = schedule.complete_task('Nonexistent task', pet_name='Buddy')
        
        assert result is False, "Completing nonexistent task should return False"
    
    def test_task_properties_preserved_in_next_occurrence(self):
        """Verify that task properties are preserved when creating next occurrence."""
        task = Task(
            name='Custom task',
            description='Task description',
            duration=45,
            frequency='daily',
            priority=4,
            category='custom_category',
            preferred_time='afternoon',
            dependencies=['Task1', 'Task2']
        )
        
        next_task = task.create_next_occurrence()
        
        assert next_task.name == task.name
        assert next_task.description == task.description
        assert next_task.duration == task.duration
        assert next_task.frequency == task.frequency
        assert next_task.priority == task.priority
        assert next_task.category == task.category
        assert next_task.preferred_time == task.preferred_time
        assert next_task.dependencies == task.dependencies


# ==================== CONFLICT DETECTION TESTS ====================

class TestConflictDetection:
    """Test suite for schedule conflict detection functionality."""
    
    def test_detect_conflicts_no_conflicts(self, schedule):
        """Verify that no conflicts are detected when tasks don't overlap."""
        now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        task1 = Task(
            name='Task 1',
            description='First task',
            duration=30,
            priority=2,
            category='general',
            start_time=now
        )
        task2 = Task(
            name='Task 2',
            description='Second task',
            duration=30,
            priority=2,
            category='general',
            start_time=now + timedelta(minutes=30)  # Starts after task1 ends
        )
        
        conflicts = schedule.detect_conflicts([task1, task2])
        
        assert len(conflicts) == 0, "No conflicts should be detected for non-overlapping tasks"
    
    def test_detect_conflicts_same_pet_overlap(self, planner, schedule):
        """Verify that overlapping times are flagged for the same pet."""
        pet = Pet(name='Rex', species='dog', age=5)
        
        now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        task1 = Task(
            name='Walk',
            description='Morning walk',
            duration=30,
            priority=3,
            category='exercise',
            start_time=now
        )
        task2 = Task(
            name='Feeding',
            description='Lunch feeding',
            duration=30,
            priority=4,
            category='feeding',
            start_time=now + timedelta(minutes=15)  # Overlaps with task1
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        planner.add_pet(pet)
        
        conflicts = schedule.detect_conflicts([task1, task2])
        
        assert len(conflicts) > 0, "Conflicts should be detected for overlapping same-pet tasks"
        assert any('Same-pet conflict' in conflict for conflict in conflicts), \
            "Conflict message should indicate same-pet overlap"
    
    def test_detect_conflicts_cross_pet_overlap(self, planner, schedule):
        """Verify that overlapping times are flagged for different pets."""
        dog = Pet(name='Rex', species='dog', age=5)
        cat = Pet(name='Fluffy', species='cat', age=3)
        
        now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        dog_task = Task(
            name='Dog walk',
            description='Dog exercise',
            duration=30,
            priority=3,
            category='exercise',
            start_time=now
        )
        cat_task = Task(
            name='Cat play',
            description='Cat playtime',
            duration=30,
            priority=3,
            category='exercise',
            start_time=now + timedelta(minutes=15)  # Overlaps with dog_task
        )
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        planner.add_pet(dog)
        planner.add_pet(cat)
        
        conflicts = schedule.detect_conflicts([dog_task, cat_task])
        
        assert len(conflicts) > 0, "Conflicts should be detected for overlapping cross-pet tasks"
        assert any('Cross-pet conflict' in conflict for conflict in conflicts), \
            "Conflict message should indicate cross-pet overlap"
    
    def test_detect_conflicts_empty_list(self, schedule):
        """Verify that no conflicts are detected for empty task list."""
        conflicts = schedule.detect_conflicts([])
        
        assert len(conflicts) == 0, "Empty task list should have no conflicts"
    
    def test_detect_conflicts_single_task(self, schedule):
        """Verify that no conflicts are detected for single task."""
        task = Task(
            name='Single task',
            description='Only task',
            duration=30,
            priority=2,
            category='general',
            start_time=datetime.now()
        )
        
        conflicts = schedule.detect_conflicts([task])
        
        assert len(conflicts) == 0, "Single task cannot have conflicts"
    
    def test_detect_conflicts_tasks_without_times(self, schedule):
        """Verify that tasks without start_time don't generate conflicts."""
        task1 = Task(
            name='Task 1',
            description='No time assigned',
            duration=30,
            priority=2,
            category='general'
            # No start_time
        )
        task2 = Task(
            name='Task 2',
            description='Also no time',
            duration=30,
            priority=2,
            category='general'
            # No start_time
        )
        
        conflicts = schedule.detect_conflicts([task1, task2])
        
        # Tasks without times shouldn't create conflicts (they're unscheduled)
        assert len(conflicts) == 0, "Unscheduled tasks should not create conflicts"
    
    def test_detect_conflicts_touching_boundaries_no_overlap(self, schedule):
        """Verify that back-to-back tasks (touching at boundary) are not flagged as conflicts."""
        now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        task1 = Task(
            name='Task 1',
            description='First task',
            duration=30,
            priority=2,
            category='general',
            start_time=now
        )
        task2 = Task(
            name='Task 2',
            description='Immediately after',
            duration=30,
            priority=2,
            category='general',
            start_time=now + timedelta(minutes=30)  # Exactly when task1 ends
        )
        
        conflicts = schedule.detect_conflicts([task1, task2])
        
        # Back-to-back tasks (touching at boundary) should not conflict
        assert len(conflicts) == 0, "Back-to-back tasks at exact boundary should not conflict"
    
    def test_detect_conflicts_multiple_overlaps(self, planner, schedule):
        """Verify that multiple overlapping conflicts are all detected."""
        pet = Pet(name='Buddy', species='dog', age=3)
        now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        task1 = Task(
            name='Task 1',
            description='First',
            duration=60,
            priority=2,
            category='general',
            start_time=now
        )
        task2 = Task(
            name='Task 2',
            description='Overlaps with 1',
            duration=60,
            priority=2,
            category='general',
            start_time=now + timedelta(minutes=30)
        )
        task3 = Task(
            name='Task 3',
            description='Overlaps with 1 and 2',
            duration=60,
            priority=2,
            category='general',
            start_time=now + timedelta(minutes=45)
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        planner.add_pet(pet)
        
        conflicts = schedule.detect_conflicts([task1, task2, task3])
        
        # Should detect multiple conflicts
        assert len(conflicts) >= 2, "Should detect multiple overlapping conflicts"
