# PawPal+ Project Reflection

## 1. System Design

- track a pet
- create a schedule
- make a daily planner

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

--- My UML Design includes a Task, Pet, Schedule, and Daily Planner class. The DailyPlanner generates the plan and consider constraints. It then uses "Pet" (which contains name, type, age, and tasks) and creates "Schedule" (which contains tasks, total time, and explanation). Pet has "Task" within it and schedule contains "Task". "Task" contains name, duration, priority, and category.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

--- Yes, the designed lacked depth in relationships and robustness. There wasn't a clear connection between "Pets" and "Schedule" so the AI suggested I added validation, dependency graphs, and more sohpisticated selection algorithms.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

--- Your scheduler chooses a simple greedy selection strategy (build_with_time_slots picks task by prioritized order and fills available minutes in sequence), which is fast and easy to reason about (O(n log n) sort + linear scan), but it may miss better overall arrangements that maximize task count or reduce cross-pet overlap in a non-greedy way. It's reasonable for this scenario because it offers simplicity, clarity, predictable behavior.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

--- I used AI throughout the project for design brainstorming, debugging, and refactoring. It helped me think through how to separate responsibilities between the Task, Pet, DailyPlanner, and Schedule classes, and it was especially useful when I wanted to improve the scheduler logic without making it too complicated.

The most helpful prompts were specific, code-focused questions, such as:

“How should I divide responsibilities across these classes?”
“Why is this scheduling logic not behaving correctly?”
“What edge cases should I test for recurring tasks and conflicts?”
“How can I keep the scheduler simple but still reliable?”

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

--- One moment where I did not accept an AI suggestion as-is was when it pushed toward a more complex scheduling system with extra dependency logic and optimization ideas. Instead of copying everything directly, I compared those suggestions to the assignment goals and decided to keep a simpler greedy scheduling approach because it was easier to understand, explain, and test.

I verified AI suggestions by checking whether they fit my UML design, reviewing the logic in my code, and using my test cases in test_pawpal.py to make sure core behaviors like sorting, recurrence, and conflict detection were still working as expected.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

--- I tested the most important behaviors of the system:

creating owners and pets
adding tasks to pets
marking tasks complete or incomplete
sorting tasks by priority, duration, category, name, start time, and time preference
creating the next occurrence for recurring tasks
detecting scheduling conflicts between overlapping tasks
These tests were important because they cover the core reliability of the project. If task tracking, sorting, or recurrence is wrong, then the daily schedule becomes less useful or misleading.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

--- I am fairly confident that my scheduler works correctly for the main scenarios it was designed for. The logic is consistent, and the project includes tests for the most important scheduling behaviors.

If I had more time, I would test more edge cases such as:

tasks with the same priority and duration
very small or zero available time
duplicate task names
dependency chains or circular dependencies
monthly recurrence near the end of a month
larger multi-pet schedules with many overlapping tasks


## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

--- The part I am most satisfied with is that I turned the UML design into a working system that does more than just store data—it can actually organize tasks, build a plan, handle recurring tasks, and detect conflicts. I also like that the project connects the backend logic to a usable Streamlit interface.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?


--- If I had another iteration, I would improve the scheduler by making it more advanced than a simple greedy strategy. I would also redesign parts of the UI to make task editing, deleting, and calendar-style viewing easier, and I would consider adding persistent storage so data is saved between sessions.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

--- One important thing I learned is that good system design comes from iteration. Starting with UML gave me structure, but implementation and testing showed where the design needed to improve. I also learned that AI is most useful when I treat it as a tool for brainstorming and feedback—not as something to trust blindly without verification.

