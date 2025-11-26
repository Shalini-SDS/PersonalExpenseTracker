"""
Personal Expense Tracker
A command-line application to log, view, and manage daily expenses with data persistence.
Features include adding expenses, viewing summaries by category and time period, and saving data to JSON.
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
DATA_FILE = "expenses.json"

def load_expenses():
    """
    Load expenses from the JSON file.
    Returns a list of expense dictionaries. If file doesn't exist, returns empty list.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("⚠️  Could not read the expense file. Starting with empty list.")
            return []
    return []


def save_expenses(expenses):
    """
    Save expenses to the JSON file.
    Args:
        expenses (list): List of expense dictionaries to save
    """
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(expenses, file, indent=4)
        print("✓ Expenses saved successfully!")
    except IOError as e:
        print(f"❌ Error saving expenses: {e}")


def add_expense(expenses):
    """
    Add a new expense to the list.
    Prompts user for amount, category, and optional date.
    Args:
        expenses (list): List of current expenses
    """
    try:
        print("\n--- Add New Expense ---")
        
        # Get amount
        while True:
            try:
                amount = float(input("Enter amount (₹): "))
                if amount <= 0:
                    print("❌ Amount must be positive!")
                    continue
                break
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
        
        # Get category
        categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        
        while True:
            try:
                choice = int(input("Select category (1-8) or enter custom name: "))
                if 1 <= choice <= len(categories):
                    category = categories[choice - 1]
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(categories)}.")
            except ValueError:
                category = input("Enter custom category name: ").strip()
                if category:
                    break
                print("❌ Category cannot be empty.")
        
        # Get date
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if date_input:
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                date = date_input
            except ValueError:
                print("❌ Invalid date format. Using today's date.")
                date = datetime.now().strftime("%Y-%m-%d")
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Get optional description
        description = input("Enter description (optional): ").strip() or "No description"
        
        # Create expense entry
        expense = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        expenses.append(expense)
        print(f"✓ Expense added: ₹{amount:.2f} in {category} on {date}")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")


def view_summary(expenses):
    """
    Display summary of expenses with multiple viewing options.
    Allows viewing by category, time period, or overall summary.
    Args:
        expenses (list): List of expense dictionaries
    """
    if not expenses:
        print("❌ No expenses recorded yet.")
        return
    
    while True:
        print("\n--- View Summary ---")
        print("1. Summary by Category")
        print("2. Total Overall Spending")
        print("3. Daily Summary")
        print("4. Weekly Summary")
        print("5. Monthly Summary")
        print("6. View All Expenses")
        print("7. Back to Main Menu")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            summary_by_category(expenses)
        elif choice == "2":
            overall_summary(expenses)
        elif choice == "3":
            daily_summary(expenses)
        elif choice == "4":
            weekly_summary(expenses)
        elif choice == "5":
            monthly_summary(expenses)
        elif choice == "6":
            view_all_expenses(expenses)
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice. Please try again.")


def summary_by_category(expenses):
    """Display total spending by category."""
    category_totals = defaultdict(float)
    
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
    
    print("\n--- Spending by Category ---")
    total = 0
    for category in sorted(category_totals.keys()):
        amount = category_totals[category]
        total += amount
        percentage = (amount / sum(category_totals.values())) * 100
        print(f"  {category:<15} ₹{amount:>8.2f} ({percentage:>5.1f}%)")
    print(f"  {'-'*35}")
    print(f"  {'TOTAL':<15} ₹{total:>8.2f} (100.0%)")


def overall_summary(expenses):
    """Display overall spending statistics."""
    total = sum(exp["amount"] for exp in expenses)
    avg = total / len(expenses) if expenses else 0
    
    amounts = [exp["amount"] for exp in expenses]
    max_expense = max(amounts) if amounts else 0
    min_expense = min(amounts) if amounts else 0
    
    print("\n--- Overall Spending Summary ---")
    print(f"  Total Spending:     ₹{total:.2f}")
    print(f"  Number of Expenses: {len(expenses)}")
    print(f"  Average Expense:    ₹{avg:.2f}")
    print(f"  Highest Expense:    ₹{max_expense:.2f}")
    print(f"  Lowest Expense:     ₹{min_expense:.2f}")


def daily_summary(expenses):
    """Display daily spending summary for a specific date or range."""
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    
    if not date_input:
        date_input = datetime.now().strftime("%Y-%m-%d")
    
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return
    
    day_expenses = [exp for exp in expenses if exp["date"] == date_input]
    
    if not day_expenses:
        print(f"❌ No expenses found for {date_input}")
        return
    
    total = sum(exp["amount"] for exp in day_expenses)
    print(f"\n--- Expenses for {date_input} ---")
    for exp in sorted(day_expenses, key=lambda x: x["amount"], reverse=True):
        print(f"  {exp['category']:<15} ₹{exp['amount']:>8.2f} - {exp['description']}")
    print(f"  {'-'*50}")
    print(f"  {'DAILY TOTAL':<15} ₹{total:>8.2f}")


def weekly_summary(expenses):
    """Display weekly spending summary."""
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    week_expenses = []
    for exp in expenses:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d").date()
        if week_start <= exp_date <= week_end:
            week_expenses.append(exp)
    
    if not week_expenses:
        print(f"❌ No expenses found for this week ({week_start} to {week_end})")
        return
    
    # Group by date
    daily_totals = defaultdict(float)
    for exp in week_expenses:
        daily_totals[exp["date"]] += exp["amount"]
    
    total = sum(daily_totals.values())
    print(f"\n--- Weekly Summary ({week_start} to {week_end}) ---")
    for date in sorted(daily_totals.keys()):
        print(f"  {date}: ₹{daily_totals[date]:>8.2f}")
    print(f"  {'-'*30}")
    print(f"  {'WEEKLY TOTAL':<15} ₹{total:>8.2f}")


def monthly_summary(expenses):
    """Display monthly spending summary."""
    today = datetime.now().date()
    month = input("Enter month (YYYY-MM) or leave blank for current month: ").strip()
    
    if not month:
        month = today.strftime("%Y-%m")
    
    month_expenses = [exp for exp in expenses if exp["date"].startswith(month)]
    
    if not month_expenses:
        print(f"❌ No expenses found for {month}")
        return
    
    # Group by category
    category_totals = defaultdict(float)
    for exp in month_expenses:
        category_totals[exp["category"]] += exp["amount"]
    
    total = sum(category_totals.values())
    print(f"\n--- Monthly Summary ({month}) ---")
    print(f"  Total Expenses: {len(month_expenses)}")
    print("\n  By Category:")
    for category in sorted(category_totals.keys()):
        amount = category_totals[category]
        percentage = (amount / total) * 100
        print(f"    {category:<15} ₹{amount:>8.2f} ({percentage:>5.1f}%)")
    print(f"  {'-'*40}")
    print(f"  {'MONTHLY TOTAL':<15} ₹{total:>8.2f}")


def view_all_expenses(expenses):
    """Display all recorded expenses in a formatted table."""
    if not expenses:
        print("❌ No expenses recorded.")
        return
    
    print("\n--- All Expenses ---")
    print(f"{'Date':<12} {'Category':<15} {'Amount':<12} {'Description'}")
    print("-" * 70)
    
    for exp in sorted(expenses, key=lambda x: x["date"], reverse=True):
        print(f"{exp['date']:<12} {exp['category']:<15} ₹{exp['amount']:>8.2f}  {exp['description']}")


def delete_expense(expenses):
    """
    Delete an expense from the list.
    Shows all expenses and lets user select which one to delete.
    Args:
        expenses (list): List of expense dictionaries
    """
    if not expenses:
        print("❌ No expenses to delete.")
        return
    
    print("\n--- Delete Expense ---")
    print("All Expenses:")
    for i, exp in enumerate(expenses, 1):
        print(f"  {i}. {exp['date']} - {exp['category']:<15} ₹{exp['amount']:.2f} - {exp['description']}")
    
    try:
        choice = int(input("Enter expense number to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(expenses):
            deleted = expenses.pop(choice - 1)
            print(f"✓ Deleted: ₹{deleted['amount']:.2f} from {deleted['category']} on {deleted['date']}")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Invalid input.")


def edit_expense(expenses):
    """
    Edit an existing expense.
    Allows user to modify amount, category, date, or description.
    Args:
        expenses (list): List of expense dictionaries
    """
    if not expenses:
        print("❌ No expenses to edit.")
        return
    
    print("\n--- Edit Expense ---")
    print("All Expenses:")
    for i, exp in enumerate(expenses, 1):
        print(f"  {i}. {exp['date']} - {exp['category']:<15} ₹{exp['amount']:.2f} - {exp['description']}")
    
    try:
        choice = int(input("Enter expense number to edit (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(expenses):
            expense = expenses[choice - 1]
            
            print("\nEdit options:")
            print("1. Amount")
            print("2. Category")
            print("3. Date")
            print("4. Description")
            print("5. Cancel")
            
            edit_choice = input("What would you like to edit? (1-5): ").strip()
            
            if edit_choice == "1":
                new_amount = float(input("Enter new amount: "))
                if new_amount > 0:
                    expense["amount"] = new_amount
                    print("✓ Amount updated!")
                else:
                    print("❌ Amount must be positive.")
            
            elif edit_choice == "2":
                new_category = input("Enter new category: ").strip()
                if new_category:
                    expense["category"] = new_category
                    print("✓ Category updated!")
            
            elif edit_choice == "3":
                new_date = input("Enter new date (YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    expense["date"] = new_date
                    print("✓ Date updated!")
                except ValueError:
                    print("❌ Invalid date format.")
            
            elif edit_choice == "4":
                new_desc = input("Enter new description: ").strip()
                if new_desc:
                    expense["description"] = new_desc
                    print("✓ Description updated!")
            
            elif edit_choice == "5":
                print("❌ Edit cancelled.")
            else:
                print("❌ Invalid choice.")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Invalid input.")


def visualize_expenses(expenses):
    """
    Create a visual chart of expenses using matplotlib (bonus feature).
    Displays pie chart for spending by category.
    Args:
        expenses (list): List of expense dictionaries
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("❌ matplotlib not installed. Install with: pip install matplotlib")
        return
    
    if not expenses:
        print("❌ No expenses to visualize.")
        return
    
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct="%1.1f%%", startangle=90)
    plt.title("Expense Distribution by Category")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()
    
    # Create bar chart for top expenses by category
    plt.figure(figsize=(10, 6))
    categories = sorted(category_totals.keys())
    amounts = [category_totals[cat] for cat in categories]
    plt.bar(categories, amounts, color="skyblue")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.title("Total Spending by Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main_menu():
    """
    Display and handle the main menu.
    Allows user to navigate all features of the expense tracker.
    """
    print("\n" + "="*50)
    print("   💰 PERSONAL EXPENSE TRACKER 💰".center(50))
    print("="*50)
    print("1. Add Expense")
    print("2. View Summary")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Visualize Expenses (Chart)")
    print("6. Exit")
    print("="*50)


def main():
    """
    Main program loop.
    Loads expenses, displays menu, and processes user commands.
    """
    print("\n🚀 Loading Personal Expense Tracker...")
    expenses = load_expenses()
    print(f"✓ Loaded {len(expenses)} expense(s)")
    
    while True:
        main_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            add_expense(expenses)
            save_expenses(expenses)
        
        elif choice == "2":
            view_summary(expenses)
        
        elif choice == "3":
            edit_expense(expenses)
            if expenses:
                save_expenses(expenses)
        
        elif choice == "4":
            delete_expense(expenses)
            if expenses:
                save_expenses(expenses)
        
        elif choice == "5":
            visualize_expenses(expenses)
        
        elif choice == "6":
            print("\n✓ Thank you for using Personal Expense Tracker!")
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
