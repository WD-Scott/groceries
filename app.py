'''
app.py
======
'''

import streamlit as st
import helpers as h

# --- Page Setup ---
st.set_page_config(page_title="Meal & Grocery Planner", layout="centered")

# --- Inject Custom CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Initialize Database ---
h.init_db()

# --- App Title ---
st.title("Meal & Grocery Planner")

# --- Tabs ---
tabs = st.tabs(["Meal Plan", "Grocery List"])


# ────────────────────────
# MEAL PLAN TAB
# ────────────────────────
with tabs[0]:
    st.subheader("Plan the Week")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_types = ["breakfast", "lunch", "dinner"]

    for day in days:
        with st.expander(day):
            cols = st.columns(3)
            for i, meal_type in enumerate(meal_types):
                with cols[i]:
                    meal = st.text_input(
                        f"{meal_type.title()}",
                        key=f"{day}_{meal_type}"
                    )
                    if meal:
                        h.set_meal(day, meal_type, meal)


    st.markdown("### Weekly Meal Plan")
    meal_plan = h.get_meal_plan()

    if meal_plan:
        grouped = {}
        for day, meal_type, meal in meal_plan:
            grouped.setdefault(day, {})[meal_type] = meal

        for day in days:
            if day in grouped:
                st.markdown(f"#### {day}")
                meals = grouped[day]
                for meal_type in meal_types:
                    meal = meals.get(meal_type, "—")
                    st.markdown(f"- **{meal_type.title()}**: {meal}")
    else:
        st.info("No meals planned yet.")


# ────────────────────────
# GROCERY LIST TAB
# ────────────────────────
with tabs[1]:
    st.subheader("Grocery List")

    with st.form("add_grocery"):
        new_item = st.text_input(
            "Add Item",
            placeholder="",
            label_visibility="visible"
        )
        submitted = st.form_submit_button("Add to List")
        if submitted and new_item.strip():
            h.add_grocery_item(new_item.strip())
            st.rerun()

    st.divider()

    items = h.get_grocery_items()
    if not items:
        st.info("Your grocery list is empty!")
    else:
        for item_id, item, checked in items:
            col1, col2, col3 = st.columns([0.1, 0.75, 0.15])
            with col1:
                st.checkbox(
                    "",
                    value=bool(checked),
                    key=f"chk_{item_id}",
                    on_change=h.toggle_item_status,
                    args=(item_id, not checked),
                )
            with col2:
                style_class = "checked grocery-item" if checked else "grocery-item"
                st.markdown(f"<div class='{style_class}'>{item}</div>", unsafe_allow_html=True)
            with col3:
                st.button("🗑️", key=f"del_{item_id}", on_click=h.delete_grocery_item, args=(item_id,))
