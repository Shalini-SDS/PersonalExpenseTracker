# Testing Guide & Examples

## 📝 Test Cases

### Test 1: Add Expense with All Features

**Objective**: Verify adding expense with amount, category, date, and description

**Steps**:
```
1. Run: python expense_tracker.py
2. Select: 1 (Add Expense)
3. Amount: 250.50
4. Category: 1 (Food)
5. Date: 2024-11-26
6. Description: Lunch with friends
7. Verify: "✓ Expense added" message
8. Open expenses.json - confirm data saved
```

**Expected Result**: ✅ Expense appears in expenses.json with all details

---

### Test 2: View Category Summary

**Objective**: Verify category summary shows correct totals and percentages

**Setup**: Add 3 expenses in different categories

**Steps**:
```
1. Add:
   - Food: ₹100
   - Transport: ₹50
   - Food: ₹150
   
2. Select: 2 (View Summary)
3. Select: 1 (Summary by Category)
```

**Expected Result**: ✅
```
Food: ₹250 (76.9%)
Transport: ₹50 (15.4%)
Other: ₹25 (7.7%)
TOTAL: ₹325
```

---

### Test 3: View Overall Summary

**Objective**: Verify statistics calculations

**Setup**: Have at least 5 expenses

**Steps**:
```
1. Select: 2 (View Summary)
2. Select: 2 (Total Overall)
```

**Expected Result**: ✅ Shows:
- Total Spending
- Number of Expenses
- Average (Total ÷ Count)
- Highest
- Lowest

---

### Test 4: Daily Summary

**Objective**: Filter expenses by date

**Steps**:
```
1. Select: 2 (View Summary)
2. Select: 3 (Daily Summary)
3. Enter: 2024-11-26
```

**Expected Result**: ✅ Shows only expenses from 2024-11-26

---

### Test 5: Edit Expense

**Objective**: Modify existing expense

**Setup**: Have at least 1 expense

**Steps**:
```
1. Select: 3 (Edit Expense)
2. Select expense #1
3. Choose: 1 (Edit Amount)
4. Enter: 500
5. Verify: Amount changed
```

**Expected Result**: ✅ Amount updated in expenses.json

---

### Test 6: Delete Expense

**Objective**: Remove expense from list

**Steps**:
```
1. Note expense count: python -c "import json; print(len(json.load(open('expenses.json'))))"
2. Select: 4 (Delete Expense)
3. Select expense to delete
4. Verify: Count decreased by 1
```

**Expected Result**: ✅ Expense removed from expenses.json

---

### Test 7: Data Persistence

**Objective**: Verify data loads on restart

**Steps**:
```
1. Add expense with unique description: "TEST_PERSISTENCE_12345"
2. Exit program (6)
3. Restart: python expense_tracker.py
4. Select: 2 → 6 (View All)
5. Search for: "TEST_PERSISTENCE_12345"
```

**Expected Result**: ✅ Expense appears after restart

---

### Test 8: Invalid Input Handling

**Objective**: Verify error handling

**Test Cases**:
```
Amount Input:
- Input: -50 → "Amount must be positive!"
- Input: abc → "Invalid amount..."
- Input: 0 → "Amount must be positive!"

Date Input:
- Input: 13-11-2024 → Uses today's date
- Input: 2024-13-45 → Invalid date
- Input: empty → Uses today's date

Category Input:
- Input: empty → Prompts again
- Input: Custom123 → Accepts and saves
```

**Expected Result**: ✅ All cases handled gracefully

---

### Test 9: Multiple Categories

**Objective**: Test all pre-defined categories

**Steps**:
```
Add 8 expenses with each category:
1. Food
2. Transport
3. Entertainment
4. Shopping
5. Bills
6. Health
7. Education
8. Other

View: 2 → 1 (Summary by Category)
```

**Expected Result**: ✅ All 8 categories appear with correct amounts

---

### Test 10: Large Dataset Performance

**Objective**: Test with 100+ expenses

**Steps**:
```
1. Copy expenses_sample.json to expenses.json
2. Add 50 more expenses
3. View: 2 → 6 (All expenses)
4. View: 2 → 5 (Monthly summary)
5. Time the operations
```

**Expected Result**: ✅ Responds in <2 seconds

---

### Test 11: Receipt OCR & AI Auto-Categorization (Streamlit)

**Objective**: Verify receipt upload extracts amount/date/description and AI suggests categories

**Steps**:
```
1. Run: streamlit run app.py
2. Open page: ➕ Add Expense
3. Ensure: Sidebar toggles 'Enable AI features' and 'Enable OCR' are turned ON
4. Upload a clear receipt image containing a total amount and date
5. Click: 📸 Process Receipt
6. Verify: Amount, Date, and Description fields are prefilled (or partially filled)
7. Click: 🔍 Suggest Category and inspect suggestion
8. Click: 💾 Save Expense and confirm it's saved with the chosen category
```

**Expected Result**: ✅ OCR reads amount/date (best-effort); AI suggests a reasonable category and expense is saved

---

## 🎯 Sample Test Data

### Scenario 1: Student Budget Tracking

```
Add these expenses:
- Food: ₹300 (Breakfast)
- Food: ₹250 (Lunch)
- Food: ₹150 (Dinner)
- Transport: ₹500 (Monthly pass)
- Entertainment: ₹200 (Movie)
- Education: ₹1000 (Books)
- Shopping: ₹400 (Clothes)
```

**Expected Summary**:
```
Total: ₹2,800
Food: ₹700 (25%)
Transport: ₹500 (17.9%)
Entertainment: ₹200 (7.1%)
Education: ₹1000 (35.7%)
Shopping: ₹400 (14.3%)
```

---

### Scenario 2: Monthly Household Expenses

```
Add these expenses:
- Bills: ₹5000 (Electricity)
- Bills: ₹3000 (Internet)
- Bills: ₹2500 (Water)
- Food: ₹2000 (Groceries)
- Health: ₹500 (Medicine)
- Entertainment: ₹1000 (Streaming)
- Transport: ₹1500 (Fuel)
- Other: ₹500 (Miscellaneous)
```

**Expected Summary**:
```
Total: ₹16,000
Bills: ₹10,500 (65.6%)
Food: ₹2000 (12.5%)
Transport: ₹1500 (9.4%)
Entertainment: ₹1000 (6.3%)
Health: ₹500 (3.1%)
Other: ₹500 (3.1%)
```

---

## 🔍 Verification Checklist

- [ ] Program starts without errors
- [ ] Can add expense successfully
- [ ] Expenses.json created on first save
- [ ] Data persists after restart
- [ ] Category summary calculates correctly
- [ ] Overall summary shows accurate stats
- [ ] Daily filter works correctly
- [ ] Weekly summary groups properly
- [ ] Monthly summary by category works
- [ ] Can edit expense amount
- [ ] Can edit expense category
- [ ] Can edit expense date
- [ ] Can edit expense description
- [ ] Can delete expense
- [ ] View All displays all expenses
- [ ] Invalid inputs handled gracefully
- [ ] Negative amounts rejected
- [ ] Invalid dates handled
- [ ] Empty descriptions allowed
- [ ] Custom categories work
- [ ] Timestamps recorded
- [ ] File permissions work
- [ ] Large datasets perform well

---

## 📊 Output Examples

### Sample Console Output

```
==================================================
   💰 PERSONAL EXPENSE TRACKER 💰
==================================================
1. Add Expense
2. View Summary
3. Edit Expense
4. Delete Expense
5. Visualize Expenses (Chart)
6. Exit
==================================================
Enter your choice (1-6): 1

--- Add New Expense ---
Enter amount (₹): 250.50
Enter amount (₹): 

Available categories:
  1. Food
  2. Transport
  3. Entertainment
  4. Shopping
  5. Bills
  6. Health
  7. Education
  8. Other
Select category (1-8) or enter custom name: 1
Enter date (YYYY-MM-DD) or press Enter for today: 2024-11-26
Enter description (optional): Lunch with friends
✓ Expense added: ₹250.50 in Food on 2024-11-26
```

### Category Summary Output

```
--- Spending by Category ---
  Bills            ₹10500.00 ( 65.6%)
  Food             ₹2000.00 ( 12.5%)
  Transport        ₹1500.00 (  9.4%)
  Entertainment    ₹1000.00 (  6.3%)
  Health           ₹500.00 (  3.1%)
  Other            ₹500.00 (  3.1%)
  ------------------------------------
  TOTAL            ₹16000.00 (100.0%)
```

### Overall Summary Output

```
--- Overall Spending Summary ---
  Total Spending:     ₹16000.00
  Number of Expenses: 23
  Average Expense:    ₹695.65
  Highest Expense:    ₹5000.00
  Lowest Expense:     ₹150.00
```

### Weekly Summary Output

```
--- Weekly Summary (2024-11-24 to 2024-11-30) ---
  2024-11-24: ₹1500.00
  2024-11-25: ₹2300.50
  2024-11-26: ₹890.00
  2024-11-27: ₹650.00
  2024-11-28: ₹2100.00
  2024-11-29: ₹3200.00
  2024-11-30: ₹1500.00
  ------------------------------------
  WEEKLY TOTAL        ₹12140.50
```

---

## 🚀 Performance Benchmarks

| Operation | Dataset | Time |
|-----------|---------|------|
| Add 1 expense | - | <100ms |
| View category summary | 100 expenses | <50ms |
| View overall summary | 100 expenses | <50ms |
| View all expenses | 100 expenses | <100ms |
| Monthly summary | 100 expenses | <100ms |
| Edit expense | - | <50ms |
| Delete expense | 100 expenses | <50ms |
| Load from file | 500 expenses | <100ms |
| Save to file | 500 expenses | <150ms |

---

## 🐛 Known Issues & Workarounds

### Issue: Matplotlib window doesn't appear
**Cause**: Display server not configured
**Workaround**: Ensure you have a display server or use SSH X11 forwarding

### Issue: Special characters in descriptions
**Cause**: JSON encoding issues
**Workaround**: Use UTF-8 encoding or simple ASCII characters

### Issue: Date sorting issues
**Cause**: Locale settings
**Workaround**: Always use YYYY-MM-DD format

---

## ✅ Quality Assurance

### Code Quality Checks
- [ ] All functions have docstrings
- [ ] Comments explain complex logic
- [ ] Variable names are descriptive
- [ ] No hardcoded values
- [ ] Error handling present
- [ ] Code follows PEP 8 style

### Functionality Tests
- [ ] All menu options work
- [ ] All data operations succeed
- [ ] Edge cases handled
- [ ] Invalid inputs rejected
- [ ] Data integrity maintained

---

## 📝 Test Results Template

```
Test Date: _______________
Tester Name: _____________
Platform: OS: ______ Python: ______

Passed Tests:
☐ Add Expense
☐ View Summary (All Types)
☐ Edit Expense
☐ Delete Expense
☐ Data Persistence
☐ Error Handling
☐ Large Dataset
☐ Visualizations

Failed Tests:
1. ________________
2. ________________

Notes:
________________________________
```

---

**Happy Testing! 🎉**
