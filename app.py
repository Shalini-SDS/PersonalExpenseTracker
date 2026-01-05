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
import re
from PIL import Image
try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False
try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except Exception:
    DATEUTIL_AVAILABLE = False

# Configuration
DATA_FILE = "expenses.json"
# Vibrant modern palette for charts and UI accents
CHART_COLORS = ['#0066FF', '#00C49A', '#FF8926', '#FF4D6D', '#9B6BFF', '#FF61AF', '#00A3E0']  # vibrant palette

# Page configuration
st.set_page_config(
    page_title="ExpenseTracker Pro",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS and UI polish (fonts, Lottie animation, improved cards)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
    }

    /* Header */
    .header-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #0066FF, #00A3E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }

    .header-sub { color: #475569; margin-top: 6px; font-weight: 500; }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 18px !important;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.06);
        border: 1px solid rgba(15,23,42,0.04);
        transition: transform 0.35s ease, box-shadow 0.35s ease;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(15,23,42,0.08); }

    div[data-testid="stMetric"] label { font-weight: 600 !important; color: #64748b !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-weight: 800 !important; color: #0f172a !important; font-size: 1.25rem; }

    /* Button Styling */
    .stButton>button { border-radius: 10px; font-weight: 700; transition: all 0.18s ease; padding: 0.55rem 1rem; }
    .stButton>button[kind="primary"] { background: linear-gradient(135deg, #0066FF 0%, #00A3E0 100%); color: white; }

    /* Card Styling */
    .content-card { background-color: #ffffff; padding: 1.6rem; border-radius: 18px; border: 1px solid rgba(15,23,42,0.04); margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(15,23,42,0.03); }

    /* Tabs */
    .stTabs [data-baseweb="tab"] { background-color: transparent; color: #475569; border-radius: 8px; padding: 6px 18px; }
    .stTabs [aria-selected="true"] { background-color: rgba(0,102,255,0.08) !important; color: #0066FF !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: transparent; }

    /* Utilities */
    .section-header { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 1.5rem 0 1rem; display:flex; align-items:center; gap:10px; }

    /* Small animations */
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(8px);} to { opacity:1; transform: translateY(0);} }
    .animate-fade { animation: fadeInUp 0.6s ease both; }

    </style>

    <!-- Lottie for header animation -->
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
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


def apply_custom_chart_style(fig, height=420):
    """Apply consistent styling to plotly charts."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Poppins, Inter, sans-serif', 'color': '#0f172a', 'size': 13},
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter"
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        transition=dict(duration=800, easing='cubic-in-out'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_layout(height=height)
    return fig


# ------------------- AI & OCR Helpers -------------------

def parse_amount_from_text(text):
    """Try to extract a numeric amount from arbitrary text."""
    if not text:
        return None
    # Common currency patterns: ₹, Rs, plain numbers; pick the largest plausible number
    matches = re.findall(r'₹\s?[\d,]+(?:\.\d{1,2})?|Rs\.?\s?[\d,]+(?:\.\d{1,2})?|\b[0-9][0-9,]*\.?[0-9]{0,2}\b', text)
    nums = []
    for m in matches:
        m_clean = re.sub(r'[₹,Rs\.\s]', '', m)
        try:
            nums.append(float(m_clean))
        except Exception:
            continue
    if not nums:
        return None
    # Return the largest numeric-looking match (works well for receipts with totals)
    return max(nums)


def parse_date_from_text(text):
    """Try to extract a date from text using dateutil when available."""
    if not text or not DATEUTIL_AVAILABLE:
        return None
    try:
        dt = date_parser.parse(text, fuzzy=True, dayfirst=False)
        return dt.date()
    except Exception:
        return None


def ocr_extract_text(uploaded_file):
    """Use pytesseract to extract text from an uploaded image file-like object."""
    if not OCR_AVAILABLE:
        return ""
    try:
        img = Image.open(uploaded_file)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        st.warning(f"OCR read error: {e}")
        return ""


def auto_categorize(description, expenses_list=None):
    """Simple heuristic categorizer: keyword matching + historical lookup."""
    desc = (description or "").lower()
    keywords = {
        'Food': ['restaurant','cafe','grocery','supermarket','zomato','swiggy','dine','meal'],
        'Transport': ['uber','ola','taxi','bus','metro','petrol','fuel','auto','parking'],
        'Entertainment': ['netflix','movie','ticket','spotify','concert','streaming'],
        'Shopping': ['flipkart','amazon','mall','shopping','store','clothing','shoes'],
        'Bills': ['electricity','internet','bill','water','subscription','rent','emi'],
        'Health': ['doctor','hospital','pharmacy','clinic','medicine'],
        'Education': ['course','college','tuition','books','class'],
    }
    for cat, kws in keywords.items():
        for kw in kws:
            if kw in desc:
                return cat
    # Fallback: historical simple matching by token
    if expenses_list:
        try:
            hist_df = convert_to_dataframe(expenses_list)
            for token in desc.split():
                matches = hist_df[hist_df['description'].str.lower().str.contains(token, na=False)]
                if not matches.empty:
                    return matches['category'].mode().iloc[0]
        except Exception:
            pass
    return 'Other'


def inject_theme_css(theme='Dark'):
    """Inject CSS for Light or Dark themes using CSS variables for consistent switching."""
    palettes = {
        'Dark': {
            'bg': '#0b0f14',
            'surface': '#0f1724',
            'muted': '#94a3b8',
            'primary': '#0066FF',
            'accent': '#00A3E0',
            'text': '#e6eef8',
            'card': '#0b1320'
        },
        'Light': {
            'bg': 'linear-gradient(135deg,#f5f7ff 0%, #eef2ff 100%)',
            'surface': '#ffffff',
            'muted': '#64748b',
            'primary': '#0066FF',
            'accent': '#00A3E0',
            'text': '#0f172a',
            'card': '#ffffff'
        }
    }

    theme_vals = palettes.get(theme, palettes['Dark'])

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Poppins', sans-serif;
        background: {theme_vals['bg']};
        color: {theme_vals['text']};
    }}

    /* Animated header gradient */
    .header-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, {theme_vals['primary']}, {theme_vals['accent']});
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite;
    }}

    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .header-sub {{ color: {theme_vals['muted']}; margin-top: 6px; font-weight: 500; }}

    /* Metric Card Styling */
    div[data-testid="stMetric"] {{
        background-color: {theme_vals['card']};
        padding: 18px !important;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.5);
        border: 1px solid rgba(255,255,255,0.02);
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        animation: fadeInUp 0.6s ease both;
    }}
    div[data-testid="stMetric"]:hover {{ transform: translateY(-6px); box-shadow: 0 16px 40px rgba(2,6,23,0.45); }}

    div[data-testid="stMetric"] label {{ font-weight: 600 !important; color: {theme_vals['muted']} !important; }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{ font-weight: 800 !important; color: {theme_vals['text']} !important; font-size: 1.25rem; }}

    /* Button Styling */
    .stButton>button {{ border-radius: 10px; font-weight: 700; transition: all 0.18s ease; padding: 0.55rem 1rem; }}
    .stButton>button[kind="primary"] {{ background: linear-gradient(135deg, {theme_vals['primary']} 0%, {theme_vals['accent']} 100%); color: white; }}

    /* Card Styling */
    .content-card {{ background-color: {theme_vals['surface']}; padding: 1.6rem; border-radius: 18px; border: 1px solid rgba(15,23,42,0.04); margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(2,6,23,0.25); }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{ background-color: transparent; color: {theme_vals['muted']}; border-radius: 8px; padding: 6px 18px; }}
    .stTabs [aria-selected="true"] {{ background-color: rgba(0,102,255,0.08) !important; color: {theme_vals['primary']} !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{ background-color: rgba(255,255,255,0.01); }}

    /* Utilities */
    .section-header {{ font-size: 1.15rem; font-weight: 700; color: {theme_vals['text']}; margin: 1.5rem 0 1rem; display:flex; align-items:center; gap:10px; }}

    /* Small animations */
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(8px);}} to {{ opacity:1; transform: translateY(0);}} }}
    .animate-fade {{ animation: fadeInUp 0.6s ease both; }}

    /* Make Plotly tooltips and traces look crisp */
    .js-plotly-plot .legendtoggle {{ cursor: pointer; }}
    </style>

    <!-- Lottie for header animation -->
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    """, unsafe_allow_html=True)


# ==================== Dashboard Components ====================

def dashboard():
    """Main dashboard view."""
    st.markdown("""
    <div style="display:flex;align-items:center;gap:18px;margin-bottom:10px;">
        <div style="width:84px;height:84px;">
            <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"  background="transparent"  speed="1"  loop  autoplay style="width:100%;height:100%;"></lottie-player>
        </div>
        <div>
            <h1 class='header-title'>ExpenseTracker Pro</h1>
            <div class='header-sub'>Beautiful analytics with animated charts & smart insights</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    expenses = load_expenses()
    
    if not expenses:
        st.info("📊 No expenses yet. Add your first expense to get started!")
        return
    
    df = convert_to_dataframe(expenses)
    
    # Key Metrics
    st.markdown("<div class='section-header'><span>📈</span> Overview</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><span>📊</span> Analytics</div>", unsafe_allow_html=True)
    
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
            color_discrete_sequence=CHART_COLORS,
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            pull=[0.06] * len(df['category'].unique()),
            marker=dict(line=dict(color='rgba(255,255,255,0.08)', width=2))
        )
        apply_custom_chart_style(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar Chart
        fig_bar = px.bar(
            category_data.reset_index(),
            x='category',
            y='Total',
            title="Total Spending by Category",
            color='category',
            color_discrete_sequence=CHART_COLORS,
            labels={'Total': 'Amount (₹)', 'category': 'Category'}
        )
        apply_custom_chart_style(fig_bar)
        fig_bar.update_layout(showlegend=False)
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
    """Display spending trends over time with an animated cumulative chart."""
    st.markdown("<div class='section-header'><span>📉</span> Spending Trends</div>", unsafe_allow_html=True)

    # Daily spending trend and cumulative animation
    daily_spending = df.groupby(df['date'].dt.date)['amount'].sum().reset_index()
    daily_spending.columns = ['Date', 'Amount']
    daily_spending = daily_spending.sort_values('Date')
    daily_spending['Cumulative'] = daily_spending['Amount'].cumsum()

    # Build animation frames: for each frame show cumulative up to that date
    frames = []
    for frame_date in daily_spending['Date'].unique():
        subset = daily_spending[daily_spending['Date'] <= frame_date].copy()
        subset['Frame'] = frame_date
        frames.append(subset)
    anim_df = pd.concat(frames)

    fig_anim = px.area(
        anim_df,
        x='Date',
        y='Cumulative',
        animation_frame='Frame',
        title='Cumulative Spending Over Time',
        color_discrete_sequence=[CHART_COLORS[0]]
    )
    fig_anim.update_traces(line=dict(width=3), marker=dict(size=6))
    apply_custom_chart_style(fig_anim, height=480)
    # Show plotly animation controls with a comfortable size
    st.plotly_chart(fig_anim, use_container_width=True, height=480)

    # Weekly/Monthly comparison (cleaner colors & sizes)
    col1, col2 = st.columns(2)

    with col1:
        df['week'] = df['date'].dt.to_period('W')
        weekly = df.groupby('week')['amount'].sum().reset_index()
        weekly['week'] = weekly['week'].astype(str)

        fig_weekly = px.bar(
            weekly,
            x='week',
            y='amount',
            title='Weekly Aggregates',
            color_discrete_sequence=[CHART_COLORS[1]]
        )
        fig_weekly.update_layout(xaxis_title='Week', yaxis_title='Amount (₹)')
        apply_custom_chart_style(fig_weekly, height=380)
        st.plotly_chart(fig_weekly, use_container_width=True)

    with col2:
        df['month'] = df['date'].dt.to_period('M')
        monthly = df.groupby('month')['amount'].sum().reset_index()
        monthly['month'] = monthly['month'].astype(str)

        fig_monthly = px.bar(
            monthly,
            x='month',
            y='amount',
            title='Monthly Aggregates',
            color_discrete_sequence=[CHART_COLORS[2]]
        )
        fig_monthly.update_layout(xaxis_title='Month', yaxis_title='Amount (₹)')
        apply_custom_chart_style(fig_monthly, height=380)
        st.plotly_chart(fig_monthly, use_container_width=True)


def time_analysis(df):
    """Analyze expenses by time periods."""
    st.markdown("<div class='section-header'><span>📅</span> Period Analysis</div>", unsafe_allow_html=True)
    
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
    
    # Visualization
    fig = px.bar(
        grouped.reset_index().rename(columns={'period': period_name}),
        x=period_name,
        y='Total',
        title=f"Spending Breakdown: {time_option}",
        color='Total',
        color_continuous_scale='Viridis',
        labels={'Total': 'Amount (₹)'}
    )
    apply_custom_chart_style(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Display table
    st.markdown("#### Period Statistics")
    st.dataframe(grouped.reset_index().rename(columns={'period': period_name}), use_container_width=True, hide_index=True)


def detailed_expenses(df):
    """Display detailed expense table."""
    st.markdown("<div class='section-header'><span>📋</span> Expense Details</div>", unsafe_allow_html=True)
    
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
        min_amt = float(df['amount'].min())
        max_amt = float(df['amount'].max())
        
        # Handle cases where min and max are the same
        if min_amt == max_amt:
            amount_range = (min_amt, max_amt)
            st.write(f"Amount: ₹{min_amt:,.2f}")
        else:
            amount_range = st.slider(
                "Amount Range (₹)",
                min_amt,
                max_amt,
                (min_amt, max_amt),
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
    """Page to add new expenses with optional OCR receipt upload and AI auto-categorization."""
    st.markdown("<div class='section-header'><span>➕</span> Add New Expense</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # Prefill values from OCR if available
        pre_amount = st.session_state.get('ocr_amount', None)
        pre_date = st.session_state.get('ocr_date', None)
        pre_category = st.session_state.get('ocr_category', None)
        pre_description = st.session_state.get('ocr_description', '')
        
        with col1:
            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                value=float(pre_amount) if pre_amount else 0.01,
                step=1.0
            )
        
        with col2:
            date = st.date_input(
                "Date",
                value=pre_date if pre_date else datetime.now().date()
            )
        
        categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Education", "Other"]
        default_cat = pre_category if pre_category in categories else categories[0]
        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(default_cat)
        )
        
        description = st.text_area(
            "Description (optional)",
            value=pre_description,
            placeholder="Enter expense details..."
        )

        # Receipt upload and OCR
        st.markdown("---")
        st.markdown("#### Upload Receipt (optional)")
        uploaded = st.file_uploader("Upload image of receipt (PNG/JPG/TIFF)", type=['png','jpg','jpeg','tiff','bmp'], key='receipt_upload')
        if uploaded:
            if st.session_state.get('ocr_enabled', OCR_AVAILABLE) and OCR_AVAILABLE:
                if st.button("📸 Process Receipt", key='process_receipt'):
                    text = ocr_extract_text(uploaded)
                    parsed_amount = parse_amount_from_text(text)
                    parsed_date = parse_date_from_text(text)
                    parsed_desc = text.strip().replace('\n', ' ')[:400]
                    parsed_category = None
                    if st.session_state.get('ai_enabled', True):
                        parsed_category = auto_categorize(parsed_desc, load_expenses())
                    if parsed_amount:
                        st.session_state['ocr_amount'] = parsed_amount
                    if parsed_date:
                        st.session_state['ocr_date'] = parsed_date
                    if parsed_category:
                        st.session_state['ocr_category'] = parsed_category
                    st.session_state['ocr_description'] = parsed_desc
                    st.success("OCR processed — fields prefilled. Edit before saving if needed.")
                    st.experimental_rerun()
            else:
                st.warning("OCR is not available. Enable OCR in the sidebar and ensure Tesseract is installed on your system.")

        # Suggest category using AI
        if st.session_state.get('ai_enabled', True):
            if st.button("🔍 Suggest Category", key='suggest_cat'):
                suggested = auto_categorize(description, load_expenses())
                st.info(f"Suggested Category: **{suggested}**")

        # Save
        if st.button("💾 Save Expense", key="add_btn", type="primary"):
            if amount > 0:
                # If AI enabled and category is 'Other', attempt auto-categorize
                if st.session_state.get('ai_enabled', True) and (not category or category == 'Other'):
                    suggested = auto_categorize(description, load_expenses())
                    if suggested and suggested != 'Other':
                        category = suggested
                        st.info(f"Auto-categorized as {category}")

                expenses = load_expenses()
                new_expense = {
                    "amount": float(amount),
                    "category": category,
                    "date": str(date),
                    "description": description or "No description",
                    "timestamp": datetime.now().isoformat()
                }
                expenses.append(new_expense)
                save_expenses(expenses)
                # Clear OCR session prefills after successful save
                for k in ['ocr_amount','ocr_date','ocr_category','ocr_description']:
                    if k in st.session_state:
                        del st.session_state[k]
                st.success(f"✓ Added ₹{amount:.2f} in {category}")
                st.experimental_rerun()
            else:
                st.error("Amount must be greater than 0")
        st.markdown("</div>", unsafe_allow_html=True)


def manage_expenses_page():
    """Page to edit/delete expenses."""
    st.markdown("<div class='section-header'><span>✏️</span> Manage Expenses</div>", unsafe_allow_html=True)
    
    expenses = load_expenses()
    
    if not expenses:
        st.info("No expenses to manage")
        return
    
    df = convert_to_dataframe(expenses)
    
    # Create editable dataframe
    st.markdown("#### Edit or Delete Expenses")
    
    # Display with options to delete
    for idx, (i, row) in enumerate(df.iterrows()):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
            
            with col1:
                st.markdown(f"**📅 {row['date'].strftime('%Y-%m-%d')}**")
            with col2:
                st.write(f"₹{row['amount']:.2f}")
            with col3:
                st.write(f"🏷️ {row['category']}")
            with col4:
                st.write(f"📝 {row['description']}")
            with col5:
                if st.button("🗑️", key=f"del_{idx}"):
                    expenses.pop(i)
                    save_expenses(expenses)
                    st.rerun()
            st.markdown("---")


def statistics_page():
    """Advanced statistics and analytics."""
    st.markdown("<div class='section-header'><span>📊</span> Advanced Analytics</div>", unsafe_allow_html=True)
    
    expenses = load_expenses()
    
    if not expenses:
        st.info("No data available for statistics")
        return
    
    df = convert_to_dataframe(expenses)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top spending categories
        top_categories = df.groupby('category')['amount'].sum().nlargest(5)
        fig = px.bar(
            x=top_categories.index,
            y=top_categories.values,
            title="Top 5 Spending Categories",
            color=top_categories.index,
            color_discrete_sequence=CHART_COLORS,
            labels={'x': 'Category', 'y': 'Amount (₹)'}
        )
        apply_custom_chart_style(fig)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Spending distribution
        percentiles = df['amount'].quantile([0.25, 0.5, 0.75, 0.9])
        dist_data = pd.DataFrame({
            'Range': ['Budget (0-25%)', 'Normal (25-50%)', 'Moderate (50-75%)', 'High (75-90%)', 'Premium (90%+)'],
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
            title="Transaction Value Distribution",
            color_discrete_sequence=CHART_COLORS,
            hole=0.4
        )
        apply_custom_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category analysis
    st.markdown("#### Deep Dive: Category Analysis")
    category_analysis = df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean', 'min', 'max', 'std']
    }).round(2)
    category_analysis.columns = ['Total Spend', 'Transactions', 'Average', 'Minimum', 'Maximum', 'Std Dev']
    st.dataframe(category_analysis.reset_index(), use_container_width=True, hide_index=True)


def ai_insights_page():
    """AI-powered recommendations, suggestions, and risk factors."""
    st.markdown("<div class='section-header'><span>🤖</span> AI Smart Insights</div>", unsafe_allow_html=True)
    
    if not st.session_state.get('ai_enabled', True):
        st.info("AI features are disabled. Enable 'Enable AI features' in the sidebar to use AI insights.")
        return

    expenses = load_expenses()
    if not expenses or len(expenses) < 5:
        st.info("🤖 AI needs at least 5 transactions to start providing meaningful insights.")
        return
    
    df = convert_to_dataframe(expenses)
    total_amt = df['amount'].sum()
    
    # AI Summary Card
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0066FF 0%, #00A3E0 100%); padding: 18px; border-radius: 20px; color: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0, 102, 255, 0.14); display:flex; gap:18px; align-items:center;'>
            <div style='width:80px; height:80px; flex:0 0 80px;'>
                <lottie-player src="https://assets6.lottiefiles.com/packages/lf20_jbrw3hcz.json"  background="transparent"  speed="1"  loop  autoplay style="width:100%;height:100%;"></lottie-player>
            </div>
            <div>
                <h2 style='margin: 0; font-weight: 700; color: white;'>AI Financial Assistant</h2>
                <p style='opacity: 0.95; font-size: 1.03rem; margin-top: 8px;'>I've analyzed {len(df)} transactions to provide you with personalized financial guidance.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 1. Recommendations & Suggestions
    with col1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("### 💡 Recommendations")
        
        # Analyze top category
        cat_sums = df.groupby('category')['amount'].sum()
        top_cat = cat_sums.idxmax()
        top_amt = cat_sums.max()
        pct = (top_amt / total_amt) * 100
        
        if pct > 40:
            st.warning(f"**Heavy Spending:** Your spending in **{top_cat}** accounts for {pct:.1f}% of your total. Setting a limit here could save you ₹{(top_amt * 0.2):,.2f} monthly.")
        else:
            st.success(f"**Balanced Budget:** Your spending is well-distributed. No single category dominates your budget.")
            
        # Specific suggestions
        if 'Food' in df['category'].values:
            food_total = df[df['category'] == 'Food']['amount'].sum()
            if food_total > total_amt * 0.3:
                st.info("🍳 **Quick Tip:** Reducing restaurant visits by 25% could significantly boost your savings.")
        
        if 'Entertainment' in df['category'].values:
            st.info("🎬 **Subscription Check:** Review your monthly digital subscriptions for any unused services.")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Risk Factors
    with col2:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("### ⚠️ Financial Risks")
        
        # Risk: Recent spike
        recent_date = df['date'].max()
        last_7_days = df[df['date'] >= (recent_date - timedelta(days=7))]
        prev_7_days = df[(df['date'] < (recent_date - timedelta(days=7))) & (df['date'] >= (recent_date - timedelta(days=14)))]
        
        if not prev_7_days.empty:
            curr_sum = last_7_days['amount'].sum()
            prev_sum = prev_7_days['amount'].sum()
            if curr_sum > prev_sum * 1.5:
                st.error(f"**Spending Spike:** Your spending jumped by {((curr_sum/prev_sum)-1)*100:.1f}% this week.")
            elif curr_sum < prev_sum * 0.8:
                st.success("**Optimization:** You're spending significantly less this week. Keep it up!")
        
        # Risk: High single transaction
        max_exp = df['amount'].max()
        avg_exp = df['amount'].mean()
        if max_exp > avg_exp * 5:
            st.warning(f"**Outlier Detected:** A single transaction of ₹{max_exp:,.2f} is significantly higher than your average.")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Monthly Prediction
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("### 🔮 Predictive Analysis")
    
    # Calculate daily average
    days_tracked = (df['date'].max() - df['date'].min()).days + 1
    daily_avg = total_amt / max(days_tracked, 1)
    projected_monthly = daily_avg * 30
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Daily Average Spend:** ₹{daily_avg:,.2f}")
        st.write(f"**Estimated Monthly Burn:** ₹{projected_monthly:,.2f}")
    
    with col_b:
        # Assuming 15k as a baseline target for health visualization
        target = 15000
        progress = min(total_amt / target, 1.0) 
        st.write(f"**Budget Usage ({total_amt:,.0f} / {target:,.0f})**")
        st.progress(progress)
        if progress > 0.8:
            st.error("🚨 Critical: You are close to your monthly budget limit!")
        elif progress > 0.5:
            st.warning("⚠️ Warning: You've used over half of your typical budget.")
        else:
            st.success("✅ Healthy: Your spending is well within limits.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== Main App ====================

def main():
    """Main application entry point."""
    
    # Sidebar navigation
    st.sidebar.markdown("### 📱 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Dashboard", "➕ Add Expense", "✏️ Manage", "📈 Statistics", "🤖 AI Insights"],
        label_visibility="collapsed"
    )

    # Theme selector (Light / Dark / Auto)
    theme_choice = st.sidebar.selectbox("Theme", ["Auto", "Light", "Dark"], index=0)
    # Determine which explicit theme to apply; 'Auto' maps to Dark for now (can be extended to detect system)
    theme_to_apply = 'Dark' if theme_choice == 'Auto' else theme_choice
    inject_theme_css(theme_to_apply)

    # AI & OCR toggles
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 AI & OCR")
    st.sidebar.checkbox("Enable AI features", value=st.session_state.get('ai_enabled', True), key='ai_enabled')
    st.sidebar.checkbox("Enable OCR (Receipt Upload)", value=st.session_state.get('ocr_enabled', OCR_AVAILABLE), key='ocr_enabled')
    if not OCR_AVAILABLE:
        st.sidebar.markdown("⚠️ OCR not available: install Tesseract and the `pytesseract` Python package. See the guide/REQUIREMENTS.md for details.")

    
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
    elif page == "🤖 AI Insights":
        ai_insights_page()


if __name__ == "__main__":
    main()
