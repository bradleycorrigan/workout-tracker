import streamlit as st
from supabase import create_client

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Setup connection
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # Define a function to fetch workouts from the database
    def get_workouts():
        data = supabase.table("workouts").select("*").execute()
        return data.data
    workouts = get_workouts()

    # A function to fetch exercise types
    def get_exercise_types():
        data = supabase.table("exercise_types").select("name").execute()
        return [item['name'] for item in data.data]
    exercise_options = get_exercise_types()

    # delete a workout
    @st.dialog("Do you really want to delete this?")
    def delete_workout(workout_id):
        st.write("This action cannot be undone.")
        if st.button("Yeah, delete it", type="primary"):
            supabase.table("workouts").delete().eq("id", workout_id).execute()
            st.success("Workout deleted successfully!")
            st.rerun() # refresh the page to show the updated list
    
    # edit a workout
    @st.dialog("Edit Workout")
    def edit_workout(log, exercise_options):
        # index finds the current exercise name in the options list, so it can be pre-selected in the dropdown
        current_idx = exercise_options.index(log['workout_type'])

        new_name = st.selectbox("Workout Name", options=exercise_options, index=current_idx)
        new_weight = st.number_input("Weight", value=float(log['weight']))
        new_reps = st.number_input("Reps", value=int(log['reps']), step=1)
        new_sets = st.number_input("Sets", value=int(log['sets']), step=1)

        if st.button("Save Changes"):
            update_data = {
                "workout_type": new_name,
                "weight": new_weight,
                "reps": new_reps,
                "sets": new_sets
            }
            # update the workout in the database
            supabase.table("workouts").update(update_data).eq("id", log['id']).execute()
            st.success("Workout updated successfully!")
            st.rerun() # refresh the page to show the updated workout

    # create the ui container 
    with st.form ("entry_form"):
        # define the form fields and assign them to variables
        workout_name = st.selectbox("Workout Name", options=exercise_options)
        workout_date = st.date_input("Workout Date")
        weight = st.number_input("Weight", min_value=0.0)
        reps = st.number_input("Reps", min_value=0)
        sets = st.number_input("Sets", min_value=0)

        # create a submit button for the form
        submit_button = st.form_submit_button("Submit")
    # handle the event 
    if submit_button:
        # dictionary keys must match supabase column names exactly
        payload = {
            "workout_type": workout_name,
            "workout_date": workout_date.isoformat(), # convert date to string
            "weight": weight,
            "reps": reps,
            "sets": sets
        }

        # send the dictionary to supabase
        supabase.table("workouts").insert(payload).execute()
        st.success("Workout entry submitted successfully!")


    # display all workouts in the database

    # creating a dictionary to group workouts by date
    grouped_workouts = {}

    for workout in workouts:
        date_key = workout['workout_date']
        if date_key not in grouped_workouts:
            grouped_workouts[date_key] = [] # creates a new list for a new date 
        grouped_workouts[date_key].append(workout) # adds each workout to each date's group 

    st.subheader("Workout History (Grouped by Date)")

    for date_key, logs in sorted(grouped_workouts.items(), reverse=True):
        #  the master card is the session 
        with st.expander(f"**📆 {date_key}**", expanded=True):

            for log in logs:
                # an exercise card for each workout
                with st.container():
                    # two columns, one for the name, and one for the stats 
                    col_name, col_stats, col_menu = st.columns([2, 1, 0.5])

                    with col_name:
                        st.markdown(f"**{log['workout_type']}**")
                        # use a caption for a sub label
                        st.caption("Main Movement")
                    
                    with col_stats: 
                        # right align the stats
                        st.markdown(f"**{log['weight']}kg**")
                        st.write(f"{log['sets']} sets x {log['reps']} reps")

                    with col_menu: 
                        # hamburger menu
                        with st.popover("✏️"):
                            # edit option
                            if st.button("✏️ Edit", key = f"edit_{log['id']}"):
                                edit_workout(log, exercise_options)
                            # delete option
                            if st.button("🗑️ Delete", key = f"del_{log['id']}"):
                                delete_workout(log['id'])

                #  divider between exercises
                st.divider()