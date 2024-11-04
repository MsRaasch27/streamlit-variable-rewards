import streamlit as st
import sqlite3
import random
import time

# Connect to the SQLite database
conn = sqlite3.connect('prizes.db')
c = conn.cursor()

# Create the prizes table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS prizes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )''')
conn.commit()

# Functions for database operations
def add_prize(name):
    c.execute('INSERT INTO prizes (name) VALUES (?)', (name,))
    conn.commit()

def get_prizes():
    c.execute('SELECT * FROM prizes')
    return c.fetchall()

def delete_prize(prize_id):
    c.execute('DELETE FROM prizes WHERE id = ?', (prize_id,))
    conn.commit()

def update_prize(prize_id, new_name):
    c.execute('UPDATE prizes SET name = ? WHERE id = ?', (new_name, prize_id))
    conn.commit()

def get_random_prize():
    prizes = get_prizes()
    if prizes:
        return random.choice(prizes)[1]  # Return prize name
    return None

# Streamlit UI
st.title("Prize Manager")

# Input new prize name
new_prize = st.text_input("Enter a new prize:")
if st.button("Add Prize") and new_prize:
    add_prize(new_prize)
    st.success(f"Added prize: {new_prize}")

# Display existing prizes with options to edit and delete
st.subheader("Current Prizes")
for prize_id, prize_name in get_prizes():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        new_name = st.text_input(f"Prize ID {prize_id}", prize_name, key=prize_id)
    with col2:
        if st.button("Update", key=f"update_{prize_id}"):
            update_prize(prize_id, new_name)
            st.success("Prize updated")
    with col3:
        if st.button("Delete", key=f"delete_{prize_id}"):
            delete_prize(prize_id)
            st.warning("Prize deleted")

# Timer functionality
if "timer_started" not in st.session_state:
    st.session_state.timer_started = False
if "next_display_time" not in st.session_state:
    st.session_state.next_display_time = 0

def start_timer():
    st.session_state.timer_started = True
    st.session_state.next_display_time = time.time() + random.randint(300, 1200)  # 5 to 20 minutes in seconds

# Start/stop timer button
if st.session_state.timer_started:
    st.button("Stop Timer", on_click=lambda: st.session_state.update({"timer_started": False}))
else:
    st.button("Start Timer", on_click=start_timer)

# Display a random prize if the timer has elapsed
if st.session_state.timer_started and time.time() >= st.session_state.next_display_time:
    prize = get_random_prize()
    if prize:
        st.balloons()  # Simulate a pop-up with balloons
        st.success(f"🎉 The randomly selected prize is: {prize} 🎉")
        # Schedule the next display time
        st.session_state.next_display_time = time.time() + random.randint(300, 1200)  # Set next interval

# Refresh page to simulate timer countdown
if st.session_state.timer_started:
    st.experimental_rerun()
