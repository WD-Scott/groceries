'''
helpers.py
==========
'''
import streamlit as st
import sqlite3

DB = "meal_planner.db"

def init_db():
    with get_connection() as conn:
        #conn.execute("DROP TABLE IF EXISTS meal_plan")  # Drop old table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meal_plan (
                id INTEGER PRIMARY KEY,
                day TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                meal TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grocery_list (
                id INTEGER PRIMARY KEY,
                item TEXT,
                checked BOOLEAN
            )
        """)
        conn.commit()


def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

def get_grocery_items():
    with get_connection() as conn:
        return conn.execute("SELECT id, item, checked FROM grocery_list").fetchall()

def add_grocery_item(item):
    with get_connection() as conn:
        conn.execute("INSERT INTO grocery_list (item, checked) VALUES (?, 0)", (item,))
        conn.commit()

def toggle_item_status(item_id, status):
    with get_connection() as conn:
        conn.execute("UPDATE grocery_list SET checked = ? WHERE id = ?", (status, item_id))
        conn.commit()

def delete_grocery_item(item_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM grocery_list WHERE id = ?", (item_id,))
        conn.commit()

def set_meal(day, meal_type, meal):
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM meal_plan WHERE day = ? AND meal_type = ?",
            (day, meal_type)
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE meal_plan SET meal = ? WHERE day = ? AND meal_type = ?",
                (meal, day, meal_type)
            )
        else:
            conn.execute(
                "INSERT INTO meal_plan (day, meal_type, meal) VALUES (?, ?, ?)",
                (day, meal_type, meal)
            )
        conn.commit()


def get_meal_plan():
    with get_connection() as conn:
        return conn.execute(
            "SELECT day, meal_type, meal FROM meal_plan ORDER BY day, meal_type"
        ).fetchall()
