# Personal Expense Tracker 💰

A comprehensive command-line application to log, manage, and analyze your daily expenses with automatic data persistence.

## Features

### ✅ Core Features (Required)

1. **Add Expense**
   - Log new expenses with amount, category, and date
   - 8 pre-defined categories: Food, Transport, Entertainment, Shopping, Bills, Health, Education, Other
   - Support for custom categories
   - Optional automatic date (uses today's date)
   - Add expense descriptions for better tracking

2. **View Summary**
   - **By Category**: See total spending for each category with percentages
   - **Overall Summary**: Total spending, average, highest, and lowest expenses
   - **Daily Summary**: View all expenses for a specific date
   - **Weekly Summary**: See expenses grouped by day for the current week
   - **Monthly Summary**: Analyze spending by category for a specific month
   - **View All**: Display all recorded expenses in a formatted table

3. **Data Persistence**
   - Automatically saves expenses to `expenses.json`
   - Loads previous expenses on program startup
   - JSON format for easy editing and backup

### 🎁 Bonus Features

4. **Edit Expense**
   - Modify amount, category, date, or description of existing expenses
   - Select from numbered list for easy editing

5. **Delete Expense**
   - Remove unwanted expense records
   - Confirmation before deletion

6. **Visualize Expenses**
   - **Pie Chart**: Shows spending distribution by category
   - **Bar Chart**: Displays total spending by category
   - Requires: `pip install matplotlib`

## Installation

### Prerequisites
- Python 3.6+
- matplotlib (optional, for visualization features)

### Setup

1. **Clone or download the repository**
   ```bash
   cd PersonalExpenseTracker-1
   ```

2. **Install optional dependencies**
   ```bash
   pip install matplotlib
   ```

## Usage

### Running the Program

```bash
python expense_tracker.py
```

### Main Menu Options

```
1. Add Expense           - Log a new expense
2. View Summary          - View various expense summaries
3. Edit Expense          - Modify an existing expense
4. Delete Expense        - Remove an expense record
5. Visualize Expenses    - Display charts and graphs
6. Exit                  - Save and exit the program
```

### Example Workflows

#### Adding an Expense
```
Choice: 1
Amount: 150
Category: (Choose from list or enter custom)
Date: 2024-11-26 (or press Enter for today)
Description: Dinner at restaurant
```

#### Viewing a Category Summary
```
Choice: 2
→ 1 (Summary by Category)
```

#### Viewing Weekly Expenses
```
Choice: 2
→ 4 (Weekly Summary)
```

#### Editing an Expense
```
Choice: 3
Select expense number to edit
Choose field to modify (Amount, Category, Date, Description)
```

#### Deleting an Expense
```
Choice: 4
Select expense number to delete
```

#### Visualizing Expenses
```
Choice: 5
(Displays pie chart and bar chart)
```

## Data Format

Expenses are stored in `expenses.json`:

```json
[
    {
        "amount": 150.00,
        "category": "Food",
        "date": "2024-11-26",
        "description": "Dinner at restaurant",
        "timestamp": "2024-11-26T19:30:45.123456"
    }
]
```

## Program Structure

### Main Functions

| Function | Purpose |
|----------|---------|
| `load_expenses()` | Load expenses from JSON file |
| `save_expenses()` | Save expenses to JSON file |
| `add_expense()` | Add new expense entry |
| `view_summary()` | Display summary menu and options |
| `summary_by_category()` | Show spending by category |
| `overall_summary()` | Display overall statistics |
| `daily_summary()` | Show expenses for specific date |
| `weekly_summary()` | Display week's expenses |
| `monthly_summary()` | Show month's expenses |
| `view_all_expenses()` | Display all expenses table |
| `edit_expense()` | Modify existing expense |
| `delete_expense()` | Remove expense record |
| `visualize_expenses()` | Generate charts (matplotlib) |
| `main()` | Main program loop |

## Features in Detail

### Categories

**Pre-defined Categories:**
- 🍽️ Food
- 🚗 Transport
- 🎬 Entertainment
- 🛍️ Shopping
- 💳 Bills
- 🏥 Health
- 📚 Education
- 📌 Other

You can also create custom categories when adding expenses.

### Summary Types

1. **Category Summary**: Breakdown of total spending per category with percentages
2. **Overall Summary**: Statistics including total, average, max, and min expenses
3. **Daily Summary**: All expenses for a specific date with category details
4. **Weekly Summary**: Day-by-day breakdown for the current week
5. **Monthly Summary**: Category breakdown for a specific month
6. **All Expenses**: Complete list of all recorded transactions

### Data Validation

- ✓ Amount must be positive
- ✓ Date format validation (YYYY-MM-DD)
- ✓ Category must not be empty
- ✓ Invalid input handling with user feedback

## Error Handling

The program handles various error scenarios:

- **Missing or corrupted JSON file**: Starts with empty expense list
- **Invalid date format**: Falls back to today's date or prompts again
- **Non-numeric amount input**: Prompts for valid number
- **Missing matplotlib**: Displays helpful error message with installation instructions
- **File I/O errors**: Catches and reports file operation failures

## Tips for Best Results

1. **Regular Backups**: Keep backups of `expenses.json` for data safety
2. **Consistent Categories**: Use consistent category names for better analysis
3. **Detailed Descriptions**: Add descriptions for future reference
4. **Regular Review**: Use summaries to monitor spending patterns
5. **Use Visualizations**: Charts help identify spending trends

## Customization

### Adding More Categories

Edit the `categories` list in the `add_expense()` function:

```python
categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Custom1", "Custom2"]
```

### Changing Currency Symbol

Change `₹` to your preferred currency symbol throughout the code:
- `$` for USD
- `€` for EUR
- `£` for GBP

### File Storage Location

Change the `DATA_FILE` variable:
```python
DATA_FILE = "path/to/your/expenses.json"
```

## Requirements Met

✅ **Add Expense**: Multiple input options with validation
✅ **View Summary**: Five different summary types
✅ **Data Persistence**: JSON file storage and loading
✅ **User Menu**: Interactive command-line interface
✅ **Bonus Features**: Delete, Edit, and Visualization capabilities
✅ **Clean Code**: Well-commented, modular functions
✅ **Error Handling**: Comprehensive input validation

## Troubleshooting

### "matplotlib not installed"
```bash
pip install matplotlib
```

### "expenses.json not found"
- Normal on first run; will create automatically on first save

### Chart not displaying
- Ensure matplotlib is installed and display server is available
- On remote systems, you may need to configure matplotlib backend

## Future Enhancements

Potential improvements for future versions:
- 📊 Budget tracking and alerts
- 📈 Trend analysis with forecasting
- 💾 CSV export functionality
- 🔐 Password protection for data
- 📱 Mobile app version
- 📧 Email spending reports
- 🏦 Bank account integration

## License

This project is provided as-is for educational purposes.

## Support

For issues or improvements, review the code comments or reach out to the development team.

---

**Version**: 1.0
**Last Updated**: November 26, 2024
**Author**: Your Name

Happy tracking! 💰
