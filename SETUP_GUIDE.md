# Personal Expense Tracker - Setup & Quick Start Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [First Run](#first-run)
4. [Basic Operations](#basic-operations)
5. [Advanced Features](#advanced-features)
6. [FAQs](#faqs)

---

## Quick Start

### Minimal Setup (1 minute)
```bash
# Navigate to project directory
cd PersonalExpenseTracker-1

# Run the program
python expense_tracker.py
```

That's it! The program will create `expenses.json` automatically on first save.

---

## Installation

### System Requirements
- **Python**: 3.6 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: Minimal (~5MB)

### Check Python Version
```bash
python --version
# or
python3 --version
```

### Install Dependencies

#### Required
- None! The program uses only Python standard library by default.

#### Optional (For Charts)
```bash
pip install matplotlib
```

**Windows:**
```powershell
pip install matplotlib
```

**macOS/Linux:**
```bash
pip3 install matplotlib
```

---

## First Run

### Step 1: Navigate to Project
```bash
cd path/to/PersonalExpenseTracker-1
```

### Step 2: Start the Program
```bash
python expense_tracker.py
```

### Step 3: Add Your First Expense
1. Select menu option `1` (Add Expense)
2. Enter amount: `100`
3. Choose category: Select from list or enter custom
4. Enter date: Press Enter for today
5. Add description: "First expense"
6. The program automatically saves!

### Step 4: View Your Data
1. Select menu option `2` (View Summary)
2. Choose view type:
   - `2` for Overall Summary
   - `1` for Category Summary
   - `6` to see all expenses

---

## Basic Operations

### Adding an Expense
```
Main Menu → 1 (Add Expense)
├─ Amount: Enter positive number
├─ Category: Choose from list or custom
├─ Date: Format YYYY-MM-DD (or press Enter)
└─ Description: Add optional note
```

**Example:**
```
Amount: 250.50
Category: Food
Date: 2024-11-26
Description: Weekly groceries
✓ Saved automatically
```

### Viewing Spending Summary

#### By Category
```
Menu → 2 → 1
Shows:
- Food: ₹1,000 (40%)
- Transport: ₹500 (20%)
- Entertainment: ₹400 (16%)
- Bills: ₹300 (12%)
- Shopping: ₹200 (8%)
- Total: ₹2,400
```

#### Overall Statistics
```
Menu → 2 → 2
Shows:
- Total Spending: ₹5,000
- Number of Expenses: 50
- Average Expense: ₹100
- Highest Expense: ₹1,500
- Lowest Expense: ₹10
```

#### Daily View
```
Menu → 2 → 3
Enter Date: 2024-11-26
Shows all expenses for that day
```

#### Weekly View
```
Menu → 2 → 4
Shows day-by-day breakdown for current week
```

#### Monthly View
```
Menu → 2 → 5
Shows category breakdown for selected month
```

### Editing an Expense
```
Main Menu → 3 (Edit Expense)
├─ Select expense number from list
├─ Choose field to modify:
│  ├─ 1: Amount
│  ├─ 2: Category
│  ├─ 3: Date
│  └─ 4: Description
└─ Enter new value
```

### Deleting an Expense
```
Main Menu → 4 (Delete Expense)
├─ Select expense number from list
└─ ✓ Expense removed
```

### Visualizing Expenses (Charts)
```
Main Menu → 5 (Visualize)
Displays:
- Pie chart: Spending distribution
- Bar chart: Total by category
```

*Requires: `pip install matplotlib`*

---

## Advanced Features

### Working with Data Files

#### Using Sample Data
```bash
# Copy sample file to use it
cp expenses_sample.json expenses.json
python expense_tracker.py
```

#### Backup Your Data
```bash
# Windows PowerShell
Copy-Item expenses.json expenses_backup.json

# macOS/Linux
cp expenses.json expenses_backup.json
```

#### Edit Data Directly
You can edit `expenses.json` in any text editor. Format:
```json
{
    "amount": 100.50,
    "category": "Food",
    "date": "2024-11-26",
    "description": "Lunch",
    "timestamp": "2024-11-26T12:30:00"
}
```

### Custom Categories
The program supports any category. When adding an expense:
- Choose option from pre-defined list, OR
- Enter custom category name (e.g., "Pet Care", "Hobby")

### Date Formats
- **Supported**: YYYY-MM-DD (e.g., 2024-11-26)
- **Fallback**: Defaults to today if invalid
- **Example**: 2024-01-15

### Amount Input
- **Format**: Decimal numbers (e.g., 100.50, 50, 1000.99)
- **Validation**: Must be positive
- **Currency**: Uses ₹ (can be changed in code)

---

## FAQs

### Q: Where is my data stored?
**A:** In `expenses.json` in the same directory as the program.

### Q: Can I move the expenses.json file?
**A:** Yes, but keep it in the same folder as `expense_tracker.py` or edit the `DATA_FILE` variable in the code.

### Q: How do I backup my data?
**A:** Copy `expenses.json` to a safe location:
```bash
cp expenses.json expenses_backup_$(date +%Y%m%d).json
```

### Q: Can I import data from CSV?
**A:** Not built-in, but you can edit `expenses.json` directly or ask for this feature.

### Q: What if the program crashes?
**A:** Your data is saved in `expenses.json`. Restart and it will load automatically.

### Q: How do I uninstall?
**A:** Simply delete the folder. Data in `expenses.json` won't be affected if you keep a copy.

### Q: Can I use this on multiple devices?
**A:** Yes, copy `expenses.json` between devices or use cloud storage.

### Q: Is my data encrypted?
**A:** No. Keep `expenses.json` in a secure location if privacy is important.

### Q: Can I change the currency?
**A:** Yes, edit the `₹` symbol throughout the code to your currency symbol.

### Q: What's the maximum number of expenses?
**A:** No practical limit; depends on your storage.

### Q: Can I export as CSV?
**A:** Not built-in, but `expenses.json` can be converted using Excel or Python scripts.

---

## Keyboard Shortcuts

| Action | How |
|--------|-----|
| Cancel operation | Press Ctrl+C or enter 0 when prompted |
| Go back to menu | Select option for previous menu |
| Exit program | Choose 6 from main menu |

---

## Common Workflows

### Weekly Review
```
1. Main Menu → 2 (View Summary)
2. Choose 4 (Weekly Summary)
3. Identify high-spending categories
4. Plan next week's budget
```

### Monthly Reporting
```
1. Main Menu → 2 → 5 (Monthly Summary)
2. Analyze spending patterns
3. Export or screenshot results
4. Share with others if needed
```

### Quick Expense Entry
```
1. Open program
2. Press 1 (Add Expense)
3. Enter amount, category, date
4. Exit (Saves automatically)
```

### Finding a Specific Expense
```
1. Main Menu → 2 → 6 (View All Expenses)
2. Scan for your expense
3. Note the line number
4. Use Edit or Delete if needed
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'json'"
- This shouldn't happen as json is built-in. Reinstall Python.

### Issue: "matplotlib not found" when visualizing
```bash
pip install matplotlib
```

### Issue: "Permission denied" saving file
- Check folder permissions
- Try running as administrator (Windows)

### Issue: Expenses not saving
- Check if `expenses.json` exists in the same folder
- Ensure write permissions on the folder
- Close other programs editing the file

### Issue: Date format errors
- Use format: YYYY-MM-DD
- Example: 2024-11-26 ✓ | 26-11-2024 ✗

---

## Performance Tips

1. **Large datasets** (1000+ expenses): Summaries may take a moment
2. **Optimize searches**: Use Monthly/Weekly summaries instead of viewing all
3. **Archive old data**: Move old expenses to separate backup file
4. **Regular saves**: Program auto-saves, but manual backup recommended

---

## Support & Help

### Need Help?
1. Check this guide first
2. Review the README.md file
3. Check expense_tracker.py comments
4. Verify your data format in expenses.json

### Report Issues
- Describe what happened
- Include error messages
- Share the data if possible (anonymize if needed)

---

## Version Information

- **Program**: Personal Expense Tracker v1.0
- **Language**: Python 3.6+
- **Data Format**: JSON
- **File Size**: ~50KB (program) + data file size
- **Last Updated**: November 26, 2024

---

**Happy Tracking! 💰**
