"""
Personal Dashboard App
A web interface for tracking habits, finances, and debt.
Can be hosted on Raspberry Pi.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
from database import init_database, get_db_session, Habit, HabitEntry, Expense, Card

# Initialize the database on first run
init_database()

# Page configuration
st.set_page_config(
    page_title="Personal Dashboard",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title("📊 Personal Dashboard")

# Create tabs for different sections
# For now, we'll focus on the main page with Habit Tracker and Finance sections
st.markdown("---")


# ============================================
# HABIT TRACKER SECTION (Idea 1)
# ============================================
st.header("✅ Habit Tracker")

# Create a database session
db = get_db_session()


def add_new_habit(habit_name):
    """
    Add a new habit to the database.

    Args:
        habit_name (str): Name of the habit to add
    """
    new_habit = Habit(name=habit_name)
    db.add(new_habit)
    db.commit()


def delete_habit(habit_id):
    """
    Delete a habit from the database.

    Args:
        habit_id (int): ID of the habit to delete
    """
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()


def toggle_habit_completion(habit_id, date):
    """
    Toggle habit completion for a specific date.
    If entry exists and is completed, delete it (uncheck).
    If entry doesn't exist, create it (check).

    Args:
        habit_id (int): ID of the habit
        date (datetime.date): Date to toggle
    """
    # Check if entry already exists for this habit and date
    entry = db.query(HabitEntry).filter(
        HabitEntry.habit_id == habit_id,
        HabitEntry.date == date
    ).first()

    if entry:
        # Entry exists, delete it (unchecking)
        db.delete(entry)
    else:
        # Entry doesn't exist, create it (checking)
        new_entry = HabitEntry(habit_id=habit_id, date=date, completed=True)
        db.add(new_entry)

    db.commit()


def is_habit_completed(habit_id, date):
    """
    Check if a habit is completed on a specific date.

    Args:
        habit_id (int): ID of the habit
        date (datetime.date): Date to check

    Returns:
        bool: True if habit is completed, False otherwise
    """
    entry = db.query(HabitEntry).filter(
        HabitEntry.habit_id == habit_id,
        HabitEntry.date == date
    ).first()
    return entry is not None and entry.completed


# Add new habit dialog (Change 2)
@st.dialog("Add New Habit")
def add_habit_dialog():
    """
    Display popup dialog for adding a new habit.
    """
    new_habit_name = st.text_input("Habit Name", key="new_habit_input")
    if st.button("Add Habit"):
        if new_habit_name.strip():
            add_new_habit(new_habit_name.strip())
            st.success(f"Habit '{new_habit_name}' added successfully!")
            st.rerun()
        else:
            st.error("Please enter a habit name")


# Add new habit button
if st.button("➕ Add New Habit"):
    add_habit_dialog()

# Initialize session state for month/year if not exists
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = datetime.now().month
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = datetime.now().year

# Get all habits from database
all_habits = db.query(Habit).all()

if all_habits:
    # Get number of days in selected month
    num_days = calendar.monthrange(st.session_state.selected_year, st.session_state.selected_month)[1]

    # Create horizontal scrollable habit tracker
    st.markdown("### Monthly Habit View")

    # Create a container for the habit tracker with horizontal scroll
    with st.container():
        # Create header row with day numbers (Change 1: More space for habit names, Change 5: No wrapping for day numbers)
        header_cols = st.columns([4] + [1] * num_days)
        header_cols[0].markdown("**Habit**")
        for day in range(1, num_days + 1):
            # Prevent day numbers from wrapping
            header_cols[day].markdown(f'<div style="white-space: nowrap; text-align: center;"><strong>{day}</strong></div>', unsafe_allow_html=True)

        # Display each habit with checkboxes for each day
        for habit in all_habits:
            habit_cols = st.columns([4] + [1] * num_days)

            # Habit name column with delete button (Change 1: No text wrapping)
            with habit_cols[0]:
                col_a, col_b = st.columns([5, 1])
                # Use markdown to prevent text wrapping
                col_a.markdown(f'<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{habit.name}</div>', unsafe_allow_html=True)
                if col_b.button("🗑️", key=f"del_{habit.id}"):
                    delete_habit(habit.id)
                    st.rerun()

            # Checkbox columns for each day
            for day in range(1, num_days + 1):
                date_obj = datetime(
                    st.session_state.selected_year,
                    st.session_state.selected_month,
                    day
                ).date()

                # Check if habit is completed on this date
                is_completed = is_habit_completed(habit.id, date_obj)

                # Create unique key for checkbox
                checkbox_key = f"habit_{habit.id}_day_{day}_{st.session_state.selected_month}_{st.session_state.selected_year}"

                # Display checkbox
                if habit_cols[day].checkbox("", value=is_completed, key=checkbox_key):
                    if not is_completed:
                        # Was unchecked, now checked
                        toggle_habit_completion(habit.id, date_obj)
                        st.rerun()
                else:
                    if is_completed:
                        # Was checked, now unchecked
                        toggle_habit_completion(habit.id, date_obj)
                        st.rerun()

    # Month and Year selector placed BELOW the habits display
    st.markdown("---")
    st.markdown("**Select Month & Year:**")

    col_month, col_year, col_spacer = st.columns([2, 2, 6])

    with col_month:
        # Month selector with unique key
        months = list(calendar.month_name)[1:]  # Skip empty first element
        selected_month_name = st.selectbox(
            "Month",
            months,
            index=st.session_state.selected_month - 1,
            key="month_selector"
        )
        # Update session state if changed
        new_month = months.index(selected_month_name) + 1
        if new_month != st.session_state.selected_month:
            st.session_state.selected_month = new_month
            st.rerun()

    with col_year:
        # Year selector with unique key
        current_year = datetime.now().year
        years = list(range(current_year - 5, current_year + 6))
        selected_year = st.selectbox(
            "Year",
            years,
            index=years.index(st.session_state.selected_year),
            key="year_selector"
        )
        # Update session state if changed
        if selected_year != st.session_state.selected_year:
            st.session_state.selected_year = selected_year
            st.rerun()

else:
    st.info("No habits added yet. Add your first habit above!")

st.markdown("---")


# ============================================
# FINANCE TRACKER SECTION (Idea 2 & 3)
# ============================================
st.header("💰 Finance Tracker")


def add_expense(date, amount, card_used, category, description):
    """
    Add a new expense to the database.

    Args:
        date (datetime.date): Date of expense
        amount (float): Amount spent
        card_used (str): Card used for payment
        category (str): Category of spending
        description (str): Description of expense
    """
    new_expense = Expense(
        date=date,
        amount=amount,
        card_used=card_used,
        category=category,
        description=description
    )
    db.add(new_expense)
    db.commit()


def update_card_debt(card_name, amount):
    """
    Update debt for a specific card.
    If card doesn't exist, create it.

    Args:
        card_name (str): Name of the card
        amount (float): Amount to add to debt
    """
    card = db.query(Card).filter(Card.card_name == card_name).first()
    if card:
        card.debt += amount
    else:
        new_card = Card(card_name=card_name, debt=amount)
        db.add(new_card)
    db.commit()


def delete_expense(expense_id):
    """
    Delete an expense from the database and update card debt.

    Args:
        expense_id (int): ID of the expense to delete
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        # Update card debt by subtracting the expense amount
        card = db.query(Card).filter(Card.card_name == expense.card_used).first()
        if card:
            card.debt -= expense.amount

        # Delete the expense
        db.delete(expense)
        db.commit()


# Add expense dialog (Change 3)
@st.dialog("Add New Expense")
def add_expense_dialog():
    """
    Display popup dialog for adding new expenses.
    User can add multiple expenses before closing.
    """
    with st.form("expense_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            # Date input
            expense_date = st.date_input("Date", value=datetime.now())

            # Amount input
            expense_amount = st.number_input("Amount Spent", min_value=0.0, step=0.01)

        with col2:
            # Card used input
            expense_card = st.text_input("Card Used")

            # Category input
            expense_category = st.selectbox(
                "Category",
                ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Education", "Other"]
            )

        with col3:
            # Description input
            expense_description = st.text_area("Description")

        # Submit button
        col_submit, col_close = st.columns([1, 1])
        with col_submit:
            submit_expense = st.form_submit_button("Add Expense", use_container_width=True)

        if submit_expense:
            if expense_amount > 0 and expense_card.strip():
                # Add expense to database
                add_expense(
                    expense_date,
                    expense_amount,
                    expense_card.strip(),
                    expense_category,
                    expense_description
                )
                # Update card debt
                update_card_debt(expense_card.strip(), expense_amount)
                st.success("Expense added successfully! You can add another or close this window.")
                st.rerun()
            else:
                st.error("Please fill in Amount and Card Used fields")

    # Close button outside the form
    if st.button("Close Window", use_container_width=True):
        st.rerun()


# Add expense button
if st.button("📝 Add New Expense"):
    add_expense_dialog()

st.markdown("---")

# Spending Pie Chart by Category (Idea 2)
st.subheader("📊 Spending by Category (Current Year)")

# Get current year
current_year = datetime.now().year

# Query expenses for current year
year_expenses = db.query(Expense).filter(
    Expense.date >= datetime(current_year, 1, 1).date(),
    Expense.date <= datetime(current_year, 12, 31).date()
).all()

if year_expenses:
    # Create DataFrame from expenses
    expenses_df = pd.DataFrame([
        {
            'date': exp.date,
            'amount': exp.amount,
            'card_used': exp.card_used,
            'category': exp.category,
            'description': exp.description
        }
        for exp in year_expenses
    ])

    # Group by category and sum amounts
    category_spending = expenses_df.groupby('category')['amount'].sum().reset_index()

    # Create pie chart
    fig_category = px.pie(
        category_spending,
        values='amount',
        names='category',
        title=f'Spending by Category - {current_year}',
        hole=0.3  # Donut chart style
    )

    st.plotly_chart(fig_category, use_container_width=True)

    # Display summary table
    st.write("**Category Summary:**")
    category_spending['amount'] = category_spending['amount'].apply(lambda x: f"₹{x:.2f}")
    st.dataframe(category_spending, hide_index=True, use_container_width=True)

else:
    st.info("No expenses recorded for this year yet.")

st.markdown("---")

# Debt Pie Chart by Card (Idea 3)
st.subheader("💳 Debt by Card")

# Query all cards with debt
all_cards = db.query(Card).all()

if all_cards and any(card.debt > 0 for card in all_cards):
    # Create DataFrame from cards
    cards_df = pd.DataFrame([
        {
            'card_name': card.card_name,
            'debt': card.debt
        }
        for card in all_cards
        if card.debt > 0
    ])

    # Calculate total debt
    total_debt = cards_df['debt'].sum()

    # Create pie chart
    fig_debt = px.pie(
        cards_df,
        values='debt',
        names='card_name',
        title=f'Debt by Card (Total: ₹{total_debt:.2f})',
        hole=0.3
    )

    st.plotly_chart(fig_debt, use_container_width=True)

    # Display summary table
    st.write("**Card Debt Summary:**")
    cards_df['debt'] = cards_df['debt'].apply(lambda x: f"₹{x:.2f}")
    st.dataframe(cards_df, hide_index=True, use_container_width=True)

else:
    st.info("No card debt recorded yet.")

st.markdown("---")

# Recent Expenses Section (Change 4)
st.subheader("📋 Recent Expenses")

# Query recent expenses (latest 20)
recent_expenses = db.query(Expense).order_by(Expense.date.desc(), Expense.id.desc()).limit(20).all()

if recent_expenses:
    st.write("*Click the bin button to delete an expense*")

    # Header row
    header_cols = st.columns([2, 2, 2, 2, 3, 1])
    header_cols[0].markdown("**Date**")
    header_cols[1].markdown("**Amount**")
    header_cols[2].markdown("**Card**")
    header_cols[3].markdown("**Category**")
    header_cols[4].markdown("**Description**")
    header_cols[5].markdown("**Delete**")

    # Display expenses in a table format with delete buttons
    for expense in recent_expenses:
        cols = st.columns([2, 2, 2, 2, 3, 1])

        # Display expense details
        cols[0].write(expense.date.strftime('%Y-%m-%d'))
        cols[1].write(f"₹{expense.amount:.2f}")
        cols[2].write(expense.card_used)
        cols[3].write(expense.category)
        cols[4].write(expense.description if expense.description else "-")

        # Delete button
        if cols[5].button("🗑️", key=f"del_expense_{expense.id}"):
            delete_expense(expense.id)
            st.success("Expense deleted successfully!")
            st.rerun()

    st.markdown("---")
    st.caption(f"Showing {len(recent_expenses)} most recent expenses")

else:
    st.info("No expenses recorded yet.")

# Close database session
db.close()

# Footer
st.markdown("---")
st.markdown("*Personal Dashboard - Track your habits, finances, and goals*")
