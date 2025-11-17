# 📊 Personal Dashboard App

A comprehensive web-based dashboard for tracking habits, finances, and debt. Perfect for hosting on Raspberry Pi!

## ✨ Features

### 1. Habit Tracker
- Track multiple habits across any month and year
- Visual monthly calendar view with checkboxes for each day
- Scroll through days while habit names stay fixed
- Add or delete habits anytime
- Persistent storage in database
- View habits across past, present, and future dates

### 2. Finance Tracker
- Add expenses with detailed information (Date, Amount, Card, Category, Description)
- Visual pie chart showing spending by category for current year
- Category breakdown summary table
- Automatic card debt tracking

### 3. Debt Tracker
- Visual pie chart showing debt distribution across cards
- Total debt calculation
- Debt automatically updates when expenses are added

## 🛠️ Technology Stack

- **Python 3.12**
- **Streamlit** - Web interface
- **SQLAlchemy** - Database ORM
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **SQLite** - Local database

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- pip or uv package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HabitTracker
   ```

2. **Install dependencies**

   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

   Using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - Open your browser and go to: `http://localhost:8501`
   - On Raspberry Pi, access from other devices using: `http://<raspberry-pi-ip>:8501`

## 🚀 Usage Guide

### Habit Tracker

1. **Add a New Habit**
   - Click on "➕ Add New Habit" expander
   - Enter habit name (e.g., "Exercise", "Read", "Meditate")
   - Click "Add Habit" button

2. **Track Daily Habits**
   - Select month and year from dropdowns
   - Check/uncheck boxes for each day to mark habit completion
   - Changes are saved automatically to database

3. **Delete a Habit**
   - Click the 🗑️ button next to habit name
   - Habit and all its entries will be permanently deleted

### Finance Tracker

1. **Add an Expense**
   - Fill in the expense form:
     - **Date**: Select the date of expense
     - **Amount Spent**: Enter the amount (decimal values allowed)
     - **Card Used**: Enter card name (e.g., "Visa Gold", "HDFC Credit")
     - **Category**: Select from predefined categories
     - **Description**: Add optional details about the expense
   - Click "Add Expense" button
   - Expense will be added and card debt will be updated automatically

2. **View Spending by Category**
   - Pie chart displays spending distribution for current year
   - Summary table shows exact amounts per category

3. **View Debt by Card**
   - Pie chart displays debt distribution across all cards
   - Summary table shows exact debt per card
   - Total debt is displayed in chart title

## 🗄️ Database Structure

The app uses SQLite database (`dashboard.db`) with the following tables:

### habits
- `id`: Unique identifier
- `name`: Habit name
- `created_date`: Date when habit was created

### habit_entries
- `id`: Unique identifier
- `habit_id`: Reference to habit
- `date`: Date of completion
- `completed`: Boolean flag

### expenses
- `id`: Unique identifier
- `date`: Expense date
- `amount`: Amount spent
- `card_used`: Card name
- `category`: Expense category
- `description`: Details

### cards
- `id`: Unique identifier
- `card_name`: Card name (unique)
- `debt`: Total debt on card

## 🔧 Configuration for Raspberry Pi

To run on Raspberry Pi and access from other devices:

1. **Install on Raspberry Pi**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Run with network access**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

3. **Access from any device**
   - Find your Raspberry Pi IP address: `hostname -I`
   - Open browser on any device: `http://<raspberry-pi-ip>:8501`

4. **Optional: Run on startup**
   - Create a systemd service or add to crontab
   - Example crontab entry:
     ```
     @reboot cd /path/to/HabitTracker && streamlit run app.py --server.address 0.0.0.0
     ```

## 📝 Code Documentation

All code is thoroughly documented with:
- Function docstrings explaining purpose, arguments, and return values
- Inline comments for complex logic
- Clear variable names following Python conventions

## 🐛 Troubleshooting

**Issue**: Database not found
- **Solution**: The database is created automatically on first run. Make sure you have write permissions in the app directory.

**Issue**: Changes not saving
- **Solution**: Check that `dashboard.db` file has write permissions.

**Issue**: Can't access from other devices
- **Solution**: Make sure you're using `--server.address 0.0.0.0` flag and firewall allows port 8501.

## 🔮 Future Enhancements

- Reminders module
- To-do lists and tasks
- Export data to Excel/CSV
- Dark mode theme
- Mobile-responsive design improvements

## 📄 License

This project is for personal use.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
