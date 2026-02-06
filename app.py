# -----------------------------------------
# FIX PYTHON PATH
# -----------------------------------------
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# -----------------------------------------
# IMPORTS
# -----------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime

from ingestion.file_uploader import load_file
from analytics.risk_engine import assign_risk
from database.db_loader import load_to_db

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Credit Card Misuse Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# CUSTOM CSS (Power BI Style)
# -----------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');
    
    /* Main Background - Dark Blue like Power BI */
    .stApp {
        background: linear-gradient(135deg, #0d2847 0%, #1a3a5c 50%, #0d2847 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', sans-serif !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    p, div, span, label {
        font-family: 'Segoe UI', sans-serif !important;
        color: #e0e0e0 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #0d2847 100%);
        border-right: 1px solid #2d4a6d;
    }
    
    /* Metric Cards - Power BI Style */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6d 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #00bcf2;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 188, 242, 0.2);
        border-left-color: #00d4ff;
    }
    
    [data-testid="stMetric"] label {
        font-size: 11px !important;
        font-weight: 400 !important;
        color: #b8c7d9 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    
    /* Chart Containers */
    .chart-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6d 100%);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        border: 1px solid #2d4a6d;
    }
    
    .chart-title {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Select Boxes */
    .stSelectbox > div > div {
        background: #2d4a6d !important;
        border: 1px solid #3d5a7d !important;
        border-radius: 4px;
        color: #ffffff !important;
    }
    
    .stSelectbox label {
        color: #b8c7d9 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #2d4a6d;
        padding: 20px;
        border-radius: 8px;
        border: 2px dashed #3d5a7d;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #00bcf2;
        background: #1e3a5f;
    }
    
    /* Data Table */
    .dataframe {
        background: #1e3a5f !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    .dataframe th {
        background: #0d2847 !important;
        color: #00bcf2 !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        color: #e0e0e0 !important;
    }
    
    /* Search Box */
    .stTextInput > div > div > input {
        background: #2d4a6d !important;
        border: 1px solid #3d5a7d !important;
        border-radius: 4px;
        color: #ffffff !important;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(90deg, #0d2847 0%, #1e3a5f 100%);
        padding: 20px 30px;
        border-radius: 8px;
        border-left: 4px solid #00bcf2;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    
    .main-subtitle {
        font-size: 13px;
        color: #b8c7d9;
        margin: 5px 0 0 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d2847;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d4a6d;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3d5a7d;
    }
    
    /* Multi-select styling */
    .stMultiSelect > div > div {
        background: #2d4a6d !important;
        border: 1px solid #3d5a7d !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: #1e4d3a !important;
        color: #00ff88 !important;
        border-left: 4px solid #00ff88 !important;
    }
    
    .stError {
        background: #4d1e1e !important;
        color: #ff4444 !important;
        border-left: 4px solid #ff4444 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------
engine = create_engine(
    "mysql+pymysql://root:mysql123@localhost/card_misuse_analytics"
)

# -----------------------------------------
# SIDEBAR
# -----------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>💳</div>
            <h2 style='margin: 0; font-size: 18px; color: #00bcf2;'>Card Analytics</h2>
            <p style='margin: 5px 0 0 0; font-size: 11px; color: #7d8a9e;'>Misuse Detection System</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: none; border-top: 1px solid #2d4a6d; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Upload Section
    st.markdown("**📤 UPLOAD DATASET**")
    uploaded_file = st.file_uploader(
        "Choose CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner("Processing data..."):
            df_new = load_file(uploaded_file)
            df_new = assign_risk(df_new)
            load_to_db(df_new, uploaded_file.name)
        st.success("✓ Data uploaded successfully!")
        st.rerun()
    
    st.markdown("<hr style='border: none; border-top: 1px solid #2d4a6d; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Info Section
    st.markdown("""
        <div style='padding: 15px; background: #1e3a5f; border-radius: 8px; border-left: 3px solid #00bcf2;'>
            <p style='font-size: 11px; margin: 0; color: #b8c7d9;'>
                <b>Last Updated:</b><br>
                Real-time data from database
            </p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# LOAD DATA FROM DATABASE
# -----------------------------------------
@st.cache_data(ttl=60)
def load_data():
    return pd.read_sql("SELECT * FROM vw_latest_transactions", engine)

df = load_data()

# -----------------------------------------
# HEADER
# -----------------------------------------
st.markdown("""
    <div class='main-header'>
        <div class='main-title'>💳 Credit Card Misuse Analytics</div>
        <div class='main-subtitle'>Real-time transaction monitoring and fraud detection dashboard</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------
# SEARCH & FILTERS
# -----------------------------------------
st.markdown("### 🔍 Filters & Search")

# Search box
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    search_term = st.text_input("🔎 Search transactions", placeholder="Search by customer ID, city, or channel...", label_visibility="collapsed")

# Apply search filter
if search_term:
    df = df[
        df['customer_id'].astype(str).str.contains(search_term, case=False, na=False) |
        df['city'].astype(str).str.contains(search_term, case=False, na=False) |
        df['channel'].astype(str).str.contains(search_term, case=False, na=False)
    ]

# Filter section
st.markdown("<div style='margin: 15px 0;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    customer = st.selectbox(
        "Customer ID",
        ["All"] + sorted(df["customer_id"].dropna().unique().tolist())
    )

with col2:
    risk = st.selectbox(
        "Risk Level",
        ["All"] + sorted(df["risk_level"].dropna().unique().tolist())
    )

with col3:
    channel = st.selectbox(
        "Channel",
        ["All"] + sorted(df["channel"].dropna().unique().tolist())
    )

with col4:
    city = st.selectbox(
        "City",
        ["All"] + sorted(df["city"].dropna().unique().tolist())
    )

# Apply filters
if customer != "All":
    df = df[df["customer_id"] == customer]
if risk != "All":
    df = df[df["risk_level"] == risk]
if channel != "All":
    df = df[df["channel"] == channel]
if city != "All":
    df = df[df["city"] == city]

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------
# KEY METRICS ROW
# -----------------------------------------
st.markdown("<div style='margin: 20px 0;'>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

total_txns = len(df)
total_amount = df['amount'].sum()
normal_txns = (df["risk_level"] == "Normal").sum() if "Normal" in df["risk_level"].values else 0
high_risk_txns = (df["risk_level"] == "High Risk").sum()

with m1:
    st.metric("Total Transactions", f"{total_txns:,}")

with m2:
    st.metric("Normal Txns", f"{normal_txns:,}")

with m3:
    st.metric("Total Amount", f"₹{total_amount:,.0f}")

with m4:
    st.metric("High Risk Txns", f"{high_risk_txns:,}")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------
# CHARTS ROW 1: Donut Chart + Bar Chart
# -----------------------------------------
chart_col1, chart_col2 = st.columns([1, 1])

# DONUT CHART - Risk Level Distribution
with chart_col1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Count of transaction_id by risk_level</div>", unsafe_allow_html=True)
    
    risk_counts = df['risk_level'].value_counts()
    
    # Power BI colors
    colors = {
        'Normal': '#00bcf2',
        'Medium Risk': '#ffa500',
        'High Risk': '#ff4444'
    }
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.6,
        marker=dict(
            colors=[colors.get(label, '#999999') for label in risk_counts.index],
            line=dict(color='#0d2847', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=11, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
    )])
    
    fig_donut.update_layout(
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            font=dict(color='white', size=10),
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5
        ),
        annotations=[dict(
            text=f'{risk_counts.sum()}<br>Total',
            x=0.5, y=0.5,
            font=dict(size=20, color='white', family='Segoe UI'),
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig_donut, use_container_width=True, key='donut_risk')
    st.markdown("</div>", unsafe_allow_html=True)

# BAR CHART - Transaction by Year
with chart_col2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Count of transaction_id by Year</div>", unsafe_allow_html=True)
    
    # Assuming you have a date column
    if 'transaction_date' in df.columns or 'date' in df.columns:
        date_col = 'transaction_date' if 'transaction_date' in df.columns else 'date'
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['year'] = df[date_col].dt.year
        year_counts = df['year'].value_counts().sort_index()
    else:
        # If no date column, create sample data
        year_counts = pd.Series([total_txns], index=[2024])
    
    fig_year = go.Figure(data=[
        go.Bar(
            x=year_counts.index,
            y=year_counts.values,
            marker=dict(
                color='#00bcf2',
                line=dict(color='#0d2847', width=1)
            ),
            text=year_counts.values,
            textposition='outside',
            textfont=dict(color='white', size=11)
        )
    ])
    
    fig_year.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(
            showgrid=False,
            showline=False,
            color='white',
            title='Year'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=False,
            color='white',
            title='Count'
        )
    )
    
    st.plotly_chart(fig_year, use_container_width=True, key='bar_year')
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------
# CHARTS ROW 2: City Bar Chart + Channel Breakdown
# -----------------------------------------
chart_col3, chart_col4 = st.columns([2, 1])

# BAR CHART - Transactions by City
with chart_col3:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>Count of transaction_id by city</div>", unsafe_allow_html=True)
    
    city_counts = df['city'].value_counts().head(10)
    
    fig_city = go.Figure(data=[
        go.Bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            marker=dict(
                color='#00bcf2',
                line=dict(color='#0d2847', width=1)
            ),
            text=city_counts.values,
            textposition='outside',
            textfont=dict(color='white', size=10)
        )
    ])
    
    fig_city.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=20, r=60, t=20, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=False,
            color='white'
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            color='white'
        )
    )
    
    st.plotly_chart(fig_city, use_container_width=True, key='bar_city')
    st.markdown("</div>", unsafe_allow_html=True)

# CHANNEL LIST
with chart_col4:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chart-title'>channel</div>", unsafe_allow_html=True)
    
    channel_list = df['channel'].dropna().unique().tolist()
    
    for ch in sorted(channel_list):
        count = (df['channel'] == ch).sum()
        st.markdown(f"""
            <div style='padding: 8px; margin: 5px 0; background: #1e3a5f; border-radius: 4px; border-left: 3px solid #00bcf2;'>
                <input type='checkbox' style='margin-right: 8px;'>
                <span style='color: #ffffff; font-size: 13px;'>{ch} ({count})</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------
# TRANSACTION TABLE
# -----------------------------------------
st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
st.markdown("<div class='chart-title'>📋 Transaction Details</div>", unsafe_allow_html=True)

# Format the dataframe for display
display_cols = [col for col in df.columns if col not in ['year']]
st.dataframe(
    df[display_cols].head(100),
    use_container_width=True,
    height=400
)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
    <div style='text-align: center; padding: 30px 0; color: #7d8a9e; font-size: 11px;'>
        © 2024 Credit Card Analytics • Powered by Streamlit & MySQL
    </div>
""", unsafe_allow_html=True)