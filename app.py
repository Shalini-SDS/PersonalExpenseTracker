"""
Personal Expense Tracker - Streamlit Frontend
A web-based dashboard to visualize and manage expenses with interactive charts.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import plotly.graph_objects as go
import plotly.express as px

# Configuration
DATA_FILE = "expenses.json"

# Page configuration
st.set_page_config(
    page_title="💰 Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #2E86AB;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== Data Functions ====================

@st.cache_data
def load_expenses():
    """Load expenses from JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            st.warning("Could not read expense file. Starting fresh.")
            return []
    return []


def save_expenses(expenses):
    """Save expenses to JSON file."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(expenses, file, indent=4)
        st.success("✓ Expenses saved successfully!")
        st.cache_data.clear()
    except IOError as e:
        st.error(f"Error saving expenses: {e}")


def convert_to_dataframe(expenses):
    """Convert expenses list to pandas DataFrame."""
    if not expenses:
        return pd.DataFrame()
    
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date', ascending=False)


# ==================== Dashboard Components ====================

def dashboard():
    """Main dashboard view."""
    st.markdown("<h1 class='header-title'>💰 Personal Expense Tracker</h1>", unsafe_allow_html=True)
    
    expenses = load_expenses()
    
    if not expenses:
        st.info("📊 No expenses yet. Add your first expense to get started!")
        return
    
    df = convert_to_dataframe(expenses)
    
    # Key Metrics
    st.subheader("📈 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    total = df['amount'].sum()
    avg = df['amount'].mean()
    max_exp = df['amount'].max()
    count = len(df)
    
    with col1:
        st.metric("Total Spending", f"₹{total:,.2f}")
    with col2:
        st.metric("Average Expense", f"₹{avg:,.2f}")
    with col3:
        st.metric("Highest Expense", f"₹{max_exp:,.2f}")
    with col4:
        st.metric("Total Expenses", count)
    
    # Charts Section
    st.subheader("📊 Charts & Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Category Breakdown", "Trends", "Time Analysis", "Details"])
    
    with tab1:
        category_summary(df)
    
    with tab2:
        spending_trends(df)
    
    with tab3:
        time_analysis(df)
    
    with tab4:
        detailed_expenses(df)


def category_summary(df):
    """Display category-wise spending breakdown."""
    st.markdown("### Spending by Category")
    
    col1, col2 = st.columns(2)
    
    # Category totals
    category_data = df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)
    category_data.columns = ['Total', 'Count', 'Average']
    category_data = category_data.sort_values('Total', ascending=False)
    
    with col1:
        # Pie Chart
        fig_pie = px.pie(
            df,
            values='amount',
            names='category',
            title="Expense Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar Chart
        fig_bar = px.bar(
            category_data.reset_index(),
            x='category',
            y='Total',
            title="Total Spending by Category",
            color='Total',
            color_continuous_scale='Blues',
            labels={'Total': 'Amount (₹)', 'category': 'Category'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed table
    st.markdown("#### Category Statistics")
    st.dataframe(
        category_data.reset_index().rename(columns={
            'category': 'Category',
            'Total': 'Total (₹)',
            'Count': 'Transactions',
            'Average': 'Avg (₹)'
        }),
        use_container_width=True,
        hide_index=True
    )


def spending_trends(df):
    """Display spending trends over time."""
    st.markdown("### Spending Trends")
    
    # Daily spending trend
    daily_spending = df.groupby(df['date'].dt.date)['amount'].sum().reset_index()
    daily_spending.columns = ['Date', 'Amount']
    
    fig_line = px.line(
        daily_spending,
        x='Date',
        y='Amount',
        title="Daily Spending Trend",
        markers=True,
        color_discrete_sequence=['#2E86AB']
    )
    fig_line.update_xaxes(title_text="Date")
    fig_line.update_yaxes(title_text="Amount (₹)")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Weekly/Monthly comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Weekly spending
        df['week'] = df['date'].dt.to_period('W')
        weekly = df.groupby('week')['amount'].sum().reset_index()
        weekly['week'] = weekly['week'].astype(str)
        
        fig_weekly = px.bar(
            weekly,
            x='week',
            y='amount',
            title="Weekly Spending",
            color='amount',
            color_continuous_scale='Greens',
            labels={'amount': 'Amount (₹)', 'week': 'Week'}
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    with col2:
        # Monthly spending
        df['month'] = df['date'].dt.to_period('M')
        monthly = df.groupby('month')['amount'].sum().reset_index()
        monthly['month'] = monthly['month'].astype(str)
        
        fig_monthly = px.bar(
            monthly,
            x='month',
            y='amount',
            title="Monthly Spending",
            color='amount',
            color_continuous_scale='Oranges',
            labels={'amount': 'Amount (₹)', 'month': 'Month'}
        )
        st.plotly_chart(fig_monthly, use_container_width=True)


def time_analysis(df):
    """Analyze expenses by time periods."""
    st.markdown("### Time-Based Analysis")
    
    # Time period selector
    time_option = st.radio(
        "Select Time Period",
        ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"],
        horizontal=True
    )
    
    if time_option == "Daily":
        time_period = df['date'].dt.date
        period_name = "Date"
    elif time_option == "Weekly":
        time_period = df['date'].dt.to_period('W')
        period_name = "Week"
    elif time_option == "Monthly":
        time_period = df['date'].dt.to_period('M')
        period_name = "Month"
    elif time_option == "Quarterly":
        time_period = df['date'].dt.to_period('Q')
        period_name = "Quarter"
    else:
        time_period = df['date'].dt.to_period('Y')
        period_name = "Year"
    
    # Group data
    time_data = df.copy()
    time_data['period'] = time_period.astype(str)
    grouped = time_data.groupby('period').agg({
        'amount': ['sum', 'count', 'mean', 'min', 'max']
    }).round(2)
    grouped.columns = ['Total', 'Count', 'Average', 'Min', 'Max']
    
    # Display table
    st.dataframe(grouped.reset_index().rename(columns={'period': period_name}), use_container_width=True)
    
    # Visualization
    fig = px.bar(
        grouped.reset_index().rename(columns={'period': period_name}),
        x=period_name,
        y='Total',
        title=f"Total Spending by {time_option}",
        color='Total',
        color_continuous_scale='Viridis',
        labels={'Total': 'Amount (₹)'}
    )
    st.plotly_chart(fig, use_container_width=True)


def detailed_expenses(df):
    """Display detailed expense table."""
    st.markdown("### Expense Details")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.multiselect(
            "Filter by Category",
            df['category'].unique(),
            default=df['category'].unique()
        )
    
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(df['date'].min().date(), df['date'].max().date()),
            max_value=datetime.now().date()
        )
    
    with col3:
        amount_range = st.slider(
            "Amount Range (₹)",
            float(df['amount'].min()),
            float(df['amount'].max()),
            (float(df['amount'].min()), float(df['amount'].max())),
            step=10.0
        )
    
    # Apply filters
    filtered_df = df[
        (df['category'].isin(category_filter)) &
        (df['date'].dt.date >= date_range[0]) &
        (df['date'].dt.date <= date_range[1]) &
        (df['amount'] >= amount_range[0]) &
        (df['amount'] <= amount_range[1])
    ].copy()
    
    # Display table
    display_df = filtered_df[[
        'date', 'category', 'amount', 'description'
    ]].copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df.columns = ['Date', 'Category', 'Amount (₹)', 'Description']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Summary
    st.markdown("#### Filtered Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", f"₹{filtered_df['amount'].sum():,.2f}")
    with col2:
        st.metric("Count", len(filtered_df))
    with col3:
        st.metric("Average", f"₹{filtered_df['amount'].mean():,.2f}")


# ==================== Add/Manage Expenses ====================

def add_expense_page():
    """Page to add new expenses."""
    st.subheader("➕ Add New Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=0.01,
            step=1.0
        )
    
    with col2:
        date = st.date_input(
            "Date",
            value=datetime.now().date()
        )
    
    categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]
    category = st.selectbox(
        "Category",
        categories
    )
    
    description = st.text_area(
        "Description (optional)",
        placeholder="Enter expense details..."
    )
    
    if st.button("💾 Add Expense", key="add_btn", type="primary"):
        if amount > 0:
            expenses = load_expenses()
            new_expense = {
                "amount": amount,
                "category": category,
                "date": str(date),
                "description": description or "No description",
                "timestamp": datetime.now().isoformat()
            }
            expenses.append(new_expense)
            save_expenses(expenses)
            st.success(f"✓ Added ₹{amount:.2f} in {category}")
        else:
            st.error("Amount must be greater than 0")


def manage_expenses_page():
    """Page to edit/delete expenses."""
    st.subheader("✏️ Manage Expenses")
    
    expenses = load_expenses()
    
    if not expenses:
        st.info("No expenses to manage")
        return
    
    df = convert_to_dataframe(expenses)
    
    # Create editable dataframe
    st.markdown("#### Edit or Delete Expenses")
    
    # Display with options to delete
    col_exp, col_del = st.columns([10, 1])
    
    with col_exp:
        for idx, (i, row) in enumerate(df.iterrows()):
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
            
            with col1:
                st.write(f"📅 {row['date'].strftime('%Y-%m-%d')}")
            with col2:
                st.write(f"₹{row['amount']:.2f}")
            with col3:
                st.write(row['category'])
            with col4:
                st.write(row['description'])
            with col5:
                if st.button("🗑️", key=f"del_{idx}"):
                    expenses.pop(i)
                    save_expenses(expenses)
                    st.rerun()


def statistics_page():
    """Advanced statistics and analytics."""
    st.subheader("📊 Advanced Statistics")
    
    expenses = load_expenses()
    
    if not expenses:
        st.info("No data available for statistics")
        return
    
    df = convert_to_dataframe(expenses)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top spending categories
        st.markdown("#### Top Spending Categories")
        top_categories = df.groupby('category')['amount'].sum().nlargest(5)
        fig = px.bar(
            x=top_categories.index,
            y=top_categories.values,
            title="Top 5 Categories",
            color=top_categories.values,
            color_continuous_scale='Reds',
            labels={'x': 'Category', 'y': 'Amount (₹)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Spending distribution
        st.markdown("#### Spending Distribution")
        percentiles = df['amount'].quantile([0.25, 0.5, 0.75, 0.9])
        dist_data = pd.DataFrame({
            'Range': ['0-25%', '25-50%', '50-75%', '75-90%', '90%+'],
            'Count': [
                len(df[df['amount'] <= percentiles[0.25]]),
                len(df[(df['amount'] > percentiles[0.25]) & (df['amount'] <= percentiles[0.5])]),
                len(df[(df['amount'] > percentiles[0.5]) & (df['amount'] <= percentiles[0.75])]),
                len(df[(df['amount'] > percentiles[0.75]) & (df['amount'] <= percentiles[0.9])]),
                len(df[df['amount'] > percentiles[0.9]])
            ]
        })
        
        fig = px.pie(
            dist_data,
            values='Count',
            names='Range',
            title="Distribution by Amount Range",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Category analysis
    st.markdown("#### Category Analysis")
    category_analysis = df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean', 'min', 'max', 'std']
    }).round(2)
    category_analysis.columns = ['Total', 'Transactions', 'Mean', 'Min', 'Max', 'Std Dev']
    st.dataframe(category_analysis.reset_index(), use_container_width=True)


# ==================== Main App ====================

def main():
    """Main application entry point."""
    
    # Sidebar navigation
    st.sidebar.markdown("### 📱 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Dashboard", "➕ Add Expense", "✏️ Manage", "📈 Statistics"],
        label_visibility="collapsed"
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Data Management")
    
    expenses = load_expenses()
    st.sidebar.metric("Total Expenses", len(expenses))
    
    if expenses:
        df = convert_to_dataframe(expenses)
        st.sidebar.metric("Total Spending", f"₹{df['amount'].sum():,.2f}")
    
    # Data controls
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Refresh", key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📥 Export CSV", key="export_btn"):
            if expenses:
                df = convert_to_dataframe(expenses)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export")
    
    # Sample data option
    if st.sidebar.checkbox("📊 Load Sample Data"):
        if os.path.exists("expenses_sample.json"):
            with open("expenses_sample.json", 'r') as f:
                sample_expenses = json.load(f)
            
            if st.sidebar.button("Load Samples"):
                current = load_expenses()
                current.extend(sample_expenses)
                save_expenses(current)
                st.sidebar.success("✓ Sample data loaded!")
                st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📚 About
    **Personal Expense Tracker v1.0**
    
    Track your daily expenses with visual analytics.
    
    **Features:**
    - 📊 Interactive charts
    - 📈 Trend analysis
    - 📅 Time-based filtering
    - 💾 Auto-save
    """)
    
    # Main content
    if page == "📊 Dashboard":
        dashboard()
    elif page == "➕ Add Expense":
        add_expense_page()
    elif page == "✏️ Manage":
        manage_expenses_page()
    elif page == "📈 Statistics":
        statistics_page()


if __name__ == "__main__":
    main()
