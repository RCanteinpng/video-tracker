import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Edge Video Tracker", layout="wide")

# --- CONSTANTS ---
FILE_PATH = 'Master_Video_Tracker.xlsx'

# --- LOAD DATA ---
@st.cache_data
def load_data():
    if not os.path.exists(FILE_PATH):
        return None
    try:
        # Load Excel file
        df = pd.read_excel(FILE_PATH)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_data()

# --- HEADER ---
st.title("📊 AI Edge Content Tracker")
st.markdown("Tracking video performance for **AI Edge** and related topics.")

if df is None:
    st.warning(f"⚠️ Could not find '{FILE_PATH}'. Please ensure the Excel file is in the repository.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")

# Filter by Category if column exists
if 'Category' in df.columns:
    categories = st.sidebar.multiselect(
        "Select Category",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )
    df_selection = df.query("Category == @categories")
else:
    df_selection = df

# --- KEY METRICS ---
# Calculate totals safely
total_views = df_selection['Views'].sum() if 'Views' in df_selection.columns else 0
total_videos = len(df_selection)
avg_views = df_selection['Views'].mean() if 'Views' in df_selection.columns else 0

# Check for Revenue column (matches standard YouTube export)
rev_col = [c for c in df_selection.columns if 'revenue' in c.lower()]
total_revenue = df_selection[rev_col[0]].sum() if rev_col else 0

# Display Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Views", f"{total_views:,.0f}")
col2.metric("Videos Tracked", total_videos)
col3.metric("Avg. Views", f"{avg_views:,.0f}")
col4.metric("Est. Revenue", f"${total_revenue:,.2f}")

st.markdown("---")

# --- CHARTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Performance by Category")
    if 'Category' in df_selection.columns:
        fig_cat = px.pie(df_selection, values='Views', names='Category', hole=0.4)
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Category column not found.")

with col_right:
    st.subheader("Top 10 Videos")
    if 'Video title' in df_selection.columns and 'Views' in df_selection.columns:
        top_videos = df_selection.sort_values(by="Views", ascending=False).head(10)
        fig_bar = px.bar(
            top_videos, 
            x='Views', 
            y='Video title', 
            orientation='h',
            text_auto='.2s'
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Video title or Views column not found.")

# --- RAW DATA TABLE ---
with st.expander("📂 View Raw Data"):
    st.dataframe(df_selection)