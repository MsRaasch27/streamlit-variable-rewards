import streamlit as st
import sqlite3
import random

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('prizes.db')
c = conn.cursor()

# Create the prizes table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS prizes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )''')
conn.commit()

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

# Select a random prize
if st.button("Pick a Random Prize"):
    prize = get_random_prize()
    if prize:
        st.success(f"The randomly selected prize is: {prize}")
    else:
        st.warning("No prizes available to select from.")
