import pytest
from pawpal_system import Owner, Task, Pet


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
