from pawpal_system import Owner, Task, Pet, DailyPlanner, Schedule
from datetime import datetime, timedelta
from datetime import datetime, timedelta


def main():
    owner = Owner(name='Jordan', email='jordan@example.com')

    dog = Pet(name='Mochi', species='dog', age=4)
    cat = Pet(name='Pixel', species='cat', age=2)

    # Create tasks with time preferences and dependencies - added out of order
    # Adding evening walk first (out of logical order)
    dog.add_task(Task(name='Evening walk', description='Evening walk', duration=25, frequency='daily', 
                     priority=4, category='exercise', preferred_time='evening'))
    
    # Then cat's play time
    cat.add_task(Task(name='Play time', description='15 minutes interactive play', duration=15, frequency='daily', 
                     priority=3, category='exercise', preferred_time='afternoon'))
    
    # Then dog's morning walk
    dog.add_task(Task(name='Morning walk', description='30 minute walk', duration=30, frequency='daily', 
                     priority=5, category='exercise', preferred_time='morning'))
    
    # Then cat's litter clean
    cat.add_task(Task(name='Litter clean', description='Clean litter box', duration=15, frequency='daily', 
                     priority=4, category='hygiene', preferred_time='morning'))
    
    # Then dog's feed breakfast
    dog.add_task(Task(name='Feed breakfast', description='Morning feeding', duration=10, frequency='daily', 
                     priority=4, category='feeding', preferred_time='morning'))
    
    # Then dog's groom (weekly task)
    dog.add_task(Task(name='Groom', description='Brushing fur', duration=20, frequency='weekly', 
                     priority=2, category='grooming', preferred_time='evening'))

    # Add some dependencies
    evening_walk = dog.get_task('Evening walk')
    if evening_walk:
        evening_walk.dependencies = ['Feed breakfast']  # Evening walk depends on breakfast being fed

    planner = DailyPlanner()
    planner.add_pet(dog)
    planner.add_pet(cat)

    print("=== PawPal Enhanced Scheduling Demo ===\n")

    # Show tasks as added (out of order)
    print("0. Tasks as Added (Out of Order):")
    all_tasks = planner.all_tasks()
    for i, task in enumerate(all_tasks, 1):
        print(f"  {i}. {task.name} ({task.duration}m, priority {task.priority}, {task.preferred_time})")
    print()

    # Demonstrate filtering
    print("1. Filtering Tasks:")
    print(f"All tasks: {len(planner.all_tasks())}")
    print(f"Pending tasks: {len(planner.filter_tasks(status='pending'))}")
    print(f"Tasks due today: {len(planner.tasks_due_today())}")
    print(f"Dog's tasks: {len(planner.filter_tasks(pet_name='Mochi'))}")
    print(f"Exercise tasks: {len(planner.filter_tasks(category='exercise'))}")
    print()

    # Demonstrate detailed filtering results
    print("1b. Filtered Task Lists:")
    print("Pending tasks:")
    for task in planner.filter_tasks(status='pending'):
        print(f"  - {task.name} ({task.category}, {task.preferred_time})")
    
    print("Dog's tasks:")
    for task in planner.filter_tasks(pet_name='Mochi'):
        print(f"  - {task.name} ({task.category}, priority {task.priority})")
    
    print("Exercise category tasks:")
    for task in planner.filter_tasks(category='exercise'):
        print(f"  - {task.name} ({task.preferred_time}, {task.duration}m)")
    print()

    # Demonstrate sorting
    print("2. Task Sorting Options:")
    schedule = Schedule(planner)
    tasks = schedule.retrieve_tasks_filtered(status='pending', due_today=True)
    
    print("By priority (default):")
    for task in schedule.organize_tasks(tasks, by="priority"):
        print(f"  - {task.name} (priority {task.priority}, {task.duration}m)")
    
    print("By time preference:")
    for task in schedule.organize_tasks(tasks, by="time"):
        print(f"  - {task.name} ({task.preferred_time}, priority {task.priority})")
    
    print("By duration:")
    for task in schedule.organize_tasks(tasks, by="duration"):
        print(f"  - {task.name} ({task.duration}m, priority {task.priority})")
    
    print("By category:")
    for task in schedule.organize_tasks(tasks, by="category"):
        print(f"  - {task.name} ({task.category}, priority {task.priority})")
    print()

    # Demonstrate time-based scheduling
    print("3. Time-Based Scheduling:")
    scheduled_tasks = schedule.build_with_time_slots(available_time=90, start_hour=8)
    
    print(f"Scheduled {len(scheduled_tasks)} tasks in {schedule.total_time} minutes:")
    for task in scheduled_tasks:
        time_str = task.start_time.strftime('%H:%M') if task.start_time else 'TBD'
        print(f"  {time_str}: {task.name} ({task.duration}m, {task.preferred_time})")
    print()

    # Demonstrate conflict detection
    print("4. Conflict Detection:")
    conflicts = schedule.detect_conflicts(scheduled_tasks)
    if conflicts:
        print("Conflicts found:")
        for conflict in conflicts:
            print(f"  - {conflict}")
    else:
        print("No conflicts detected in current schedule.")
    print()

    # Demonstrate recurring task handling
    print("5. Recurring Task Handling:")
    print("Marking 'Morning walk' as completed...")
    schedule.complete_task('Morning walk', 'Mochi')
    
    # Simulate time passing (in real app, this would be automatic)
    morning_walk = dog.get_task('Morning walk')
    if morning_walk:
        # Simulate it was completed yesterday
        morning_walk.last_completed = datetime.now() - timedelta(days=1)
        print(f"Morning walk last completed: {morning_walk.last_completed.strftime('%Y-%m-%d %H:%M')}")
        print(f"Is due today: {morning_walk.is_due()}")
    
    print(f"Total tasks after completing 'Morning walk': {len(planner.all_tasks())}")
    
    # Check if a new morning walk task was created
    morning_walk_tasks = [t for t in planner.all_tasks() if t.name == 'Morning walk']
    print(f"Number of 'Morning walk' tasks: {len(morning_walk_tasks)}")
    for i, task in enumerate(morning_walk_tasks, 1):
        status = "Completed" if task.completed else "Pending"
        due_info = f" (due: {task.due_date})" if task.due_date else ""
        print(f"  Task {i}: {status}{due_info}")
    
    print("\n6. Weekly Task Recurrence:")
    print("Marking 'Groom' as completed...")
    schedule.complete_task('Groom', 'Mochi')
    
    # Check groom tasks
    groom_tasks = [t for t in planner.all_tasks() if t.name == 'Groom']
    print(f"Number of 'Groom' tasks: {len(groom_tasks)}")
    for i, task in enumerate(groom_tasks, 1):
        status = "Completed" if task.completed else "Pending"
        due_info = f" (due: {task.due_date})" if task.due_date else ""
        print(f"  Task {i}: {status}{due_info}")
    print()
    
    print("\n7. Enhanced Conflict Detection Demo:")
    
    # Create fresh tasks for conflict demonstration
    print("Creating overlapping tasks for demonstration...")
    
    # Create cross-pet conflict: dog's task and cat's task at same time
    dog_brush = Task(name='Brush fur', description='Brush dog fur', duration=15, frequency='daily', 
                    priority=3, category='grooming', preferred_time='morning')
    dog.add_task(dog_brush)
    dog_brush.start_time = datetime.now().replace(hour=10, minute=0)
    
    cat_brush = Task(name='Brush fur', description='Brush cat fur', duration=20, frequency='daily', 
                    priority=3, category='grooming', preferred_time='morning')
    cat.add_task(cat_brush)
    cat_brush.start_time = datetime.now().replace(hour=10, minute=5)  # Overlaps with dog brush
    
    cross_pet_tasks = [dog_brush, cat_brush]
    conflict_messages = schedule.detect_conflicts(cross_pet_tasks)
    
    if conflict_messages:
        print("Cross-pet conflicts detected:")
        for msg in conflict_messages:
            print(f"  - {msg}")
    else:
        print("No cross-pet conflicts detected.")
    
    print("\n7b. Two Tasks at Exactly Same Time Demo:")
    # Add two tasks scheduled at the same exact start time to verify warning behavior
    dog_slots_conflict = Task(name='Shared grooming', description='Groom dog', duration=20, frequency='daily',
                             priority=5, category='grooming', preferred_time='afternoon')
    cat_slots_conflict = Task(name='Shared grooming', description='Groom cat', duration=15, frequency='daily',
                             priority=4, category='grooming', preferred_time='afternoon')
    dog.add_task(dog_slots_conflict)
    cat.add_task(cat_slots_conflict)
    shared_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    dog_slots_conflict.start_time = shared_time
    cat_slots_conflict.start_time = shared_time

    exact_conflict_tasks = [dog_slots_conflict, cat_slots_conflict]
    exact_conflicts = schedule.detect_conflicts(exact_conflict_tasks)

    if exact_conflicts:
        print("Same-time conflicts detected:")
        for msg in exact_conflicts:
            print(f"  - {msg}")
    else:
        print("No same-time conflicts detected.")

    print("\n8. Same-Pet Conflict Demo:")
    
    # Create same-pet conflicts for the dog
    dog_walk1 = Task(name='Short walk', description='Short walk', duration=15, frequency='daily', 
                    priority=4, category='exercise', preferred_time='morning')
    dog.add_task(dog_walk1)
    dog_walk1.start_time = datetime.now().replace(hour=11, minute=0)
    
    dog_walk2 = Task(name='Another walk', description='Another walk', duration=20, frequency='daily', 
                    priority=3, category='exercise', preferred_time='morning')
    dog.add_task(dog_walk2)
    dog_walk2.start_time = datetime.now().replace(hour=11, minute=10)  # Overlaps with first walk
    
    same_pet_tasks = [dog_walk1, dog_walk2]
    same_pet_conflicts = schedule.detect_conflicts(same_pet_tasks)
    
    if same_pet_conflicts:
        print("Same-pet conflicts detected:")
        for msg in same_pet_conflicts:
            print(f"  - {msg}")
    else:
        print("No same-pet conflicts detected.")


if __name__ == '__main__':
    main()