import streamlit as st
from pawpal_system import Task, Pet, DailyPlanner, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Create Pet")
st.caption("First create a pet, then add tasks for that pet.")

col1, col2 = st.columns(2)
with col1:
    pet_name_input = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species_input = st.selectbox("Species", ["dog", "cat", "other"], key="species_input")

if st.button("Create Pet"):
    if pet_name_input:
        new_pet = Pet(name=pet_name_input, species=species_input, age=1)  # Default age
        st.session_state.planner.add_pet(new_pet)
        st.session_state.current_pet = new_pet
        st.success(f"Created pet: {new_pet.name} ({new_pet.species})")
    else:
        st.error("Please enter a pet name")

# Display current pets
if st.session_state.planner.all_pets():
    st.write("Current pets:")
    for pet in st.session_state.planner.all_pets():
        if st.button(f"Select {pet.name}", key=f"select_{pet.name}"):
            st.session_state.current_pet = pet
        st.write(f"- {pet.name} ({pet.species}) - {len(pet.tasks)} tasks")

st.divider()

st.subheader("Add Tasks")
st.caption("Add tasks for the selected pet.")

if st.session_state.current_pet is None:
    st.warning("Please create and select a pet first.")
else:
    st.info(f"Adding tasks for: {st.session_state.current_pet.name}")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_options = {"low": 1, "medium": 3, "high": 5}
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        priority_value = priority_options[priority_label]

    if st.button("Add task"):
        new_task = Task(
            name=task_title,
            description=f"{task_title} for {st.session_state.current_pet.name}",
            duration=duration,
            priority=priority_value,
            category="general"
        )
        st.session_state.current_pet.add_task(new_task)
        st.success(f"Added task: {task_title}")

    # Display current tasks for selected pet
    if st.session_state.current_pet.tasks:
        st.write(f"Current tasks for {st.session_state.current_pet.name}:")
        task_data = []
        for task in st.session_state.current_pet.tasks:
            task_data.append({
                "Task": task.name,
                "Duration": f"{task.duration}m",
                "Priority": task.priority,
                "Status": "Done" if task.completed else "Pending"
            })
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an optimized schedule based on available time and task priorities.")

available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=90)

if st.button("Generate schedule"):
    if not st.session_state.planner.all_pets():
        st.error("Please create at least one pet first.")
    elif not any(len(pet.tasks) > 0 for pet in st.session_state.planner.all_pets()):
        st.error("Please add at least one task to a pet first.")
    else:
        # Create schedule and build it
        schedule = Schedule(st.session_state.planner)
        scheduled_tasks = schedule.build(available_time=available_time)
        
        if scheduled_tasks:
            st.success(f"Scheduled {len(scheduled_tasks)} tasks in {schedule.total_time} minutes!")
            
            # Display scheduled tasks
            st.subheader("Today's Schedule")
            schedule_data = []
            for i, task in enumerate(scheduled_tasks, 1):
                schedule_data.append({
                    "Order": i,
                    "Task": task.name,
                    "Duration": f"{task.duration}m",
                    "Priority": task.priority,
                    "Category": task.category
                })
            st.table(schedule_data)
            
            # Show explanation
            st.subheader("Schedule Explanation")
            st.text(schedule.explain())
        else:
            st.warning("No tasks could be scheduled with the current constraints. Try increasing available time or adding more tasks.")
