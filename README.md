# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The PawPal+ scheduler includes advanced features for generating reliable pet care plans:

- **Conflict Detection**: Automatically identifies overlapping tasks (same-pet and cross-pet) and warns users when a schedule is infeasible.
- **Time-Slot Assignment**: Assigns start times to tasks within available windows, respecting preferred times (morning, afternoon, evening).
- **Recurring Task Management**: Handles daily, weekly, and monthly tasks seamlessly; completing a recurring task generates the next occurrence.
- **Flexible Filtering & Sorting**: Filter tasks by pet, category, priority, or frequency; sort by duration, time preference, or urgency to find the best fit.
- **Conflict Resolution**: When overlaps are detected, the scheduler can reorder tasks by priority and reassign slots to resolve conflicts.

-**Testinging PawPal+**:
When the command python -m pytest is runned, the tests covers Owner and Pet Management (4 tests): Basic creation and attribute handling for owners and pets, plus task addition to pets.
Task Lifecycle (2 tests): Task completion status changes.
Sorting Correctness (9 tests): Validates the organize_tasks() method for sorting by priority, duration, category, name, start time, and time preferences.
Recurrence Logic (10 tests): Tests create_next_occurrence() and complete_task() for daily, weekly, monthly, and one-time tasks, ensuring proper next occurrence generation.
Conflict Detection (8 tests): Verifies detect_conflicts() identifies overlapping schedules for same-pet and cross-pet scenarios, including edge cases like unscheduled tasks.
Running python -m pytest executes all 32 tests, confirming the scheduler's reliability for pet care task management, sorting, recurrence, and conflict prevention.

Confidence Level: 4 stars

-**Features**:
Core Data Management
Pet and Owner Tracking: Manages pet profiles linked to owners, with basic attributes like name and email.
Task Management: Stores tasks with attributes including name, description, duration, frequency, priority, category, preferred time, due dates, and dependencies.
Task Filtering and Organization
Multi-Criteria Filtering: Filters tasks by pet, completion status, category, frequency, and due date (e.g., tasks due today).
Flexible Sorting: Organizes tasks by priority (default), duration, category, time preference (morning/afternoon/evening), name, or start time.
Scheduling and Optimization
Greedy Schedule Building: Optimizes task selection within available time constraints, prioritizing high-priority tasks using a knapsack-like algorithm.
Time Slot Assignment: Assigns sequential time blocks to selected tasks, starting from a specified hour.
Conflict Detection: Identifies overlapping tasks for the same pet or across pets using interval overlap checks.
Conflict Resolution: Reorders conflicting tasks by priority and reassigns time slots to eliminate overlaps.
Recurring Task Handling
Recurrence Management: Automatically creates next occurrences for daily, weekly, or monthly tasks upon completion.
Task Completion Tracking: Marks tasks complete with timestamps and handles recurrence logic.
Additional Utilities
Schedule Explanation: Generates human-readable summaries of built schedules.
Cross-Pet Coordination: Manages tasks across multiple pets in a daily planner.

-**Demo**:
https://1drv.ms/i/c/b3131aebb623beef/IQAciC6hVeiWSai1ESE0wMsCAct3LoPcFyL5iM57qv_sZAE?e=hEpgrb

