from dataclasses import dataclass
from pawpal_system import Task, Pet, DailyPlanner, Schedule

@dataclass
class Owner:
    name: str
    email: str


def main():
    owner = Owner(name='Jordan', email='jordan@example.com')

    dog = Pet(name='Mochi', species='dog', age=4)
    cat = Pet(name='Pixel', species='cat', age=2)

    dog.add_task(Task(name='Morning walk', description='30 minute walk', duration=30, frequency='daily', priority=5, category='exercise'))
    dog.add_task(Task(name='Feed', description='Breakfast feeding', duration=10, frequency='daily', priority=4, category='feeding'))
    cat.add_task(Task(name='Litter clean', description='Clean litter box', duration=15, frequency='daily', priority=4, category='hygiene'))
    cat.add_task(Task(name='Play time', description='15 minutes interactive play', duration=15, frequency='daily', priority=3, category='exercise'))
    dog.add_task(Task(name='Groom', description='Brushing fur', duration=20, frequency='weekly', priority=2, category='grooming'))

    planner = DailyPlanner()
    planner.add_pet(dog)
    planner.add_pet(cat)

    schedule = Schedule(planner)
    tasks = schedule.build(available_time=90)

    print(f"Today's Schedule for owner {owner.name} ({owner.email})")
    print('---------------------------------------------')
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t.summary()}")

    print('\nSummary:')
    print(schedule.explain())


if __name__ == '__main__':
    main()