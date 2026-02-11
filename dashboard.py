import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - Final A/B Test", layout="wide")

# Professional Iman Gadzhi CSS
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #30363d; font-size: 22px; }
    .metric-label { color: #8b949e; font-weight: bold; }
    .metric-value { color: #ffffff; font-weight: bold; text-align: center; width: 100%; }
    .winner-highlight { background-color: #1a2e1a; padding: 25px; border-radius: 15px; border: 2px solid #28a745; }
    .challenger-highlight { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    val_str = str(value).strip()
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    # 1. Load and Clean Data
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Detect columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    # REMOVE BLANK ROWS (Fixes the "nan" and "out-of-bounds" error)
    df = df.dropna(subset=[title_col]).reset_index(drop=True)

    # 2. Sidebar Selection
    st.sidebar.title("🛠️ A/B Controls")
    video_list = df[title_col].tolist()
    
    choice_1 = st.sidebar.selectbox("Select #1 Winner", video_list, index=0)
    choice_2 = st.sidebar.selectbox("Select #2 Challenger", video_list, index=min(1, len(video_list)-1))

    v1 = df[df[title_col] == choice_1].iloc[0]
    v2 = df[df[title_col] == choice_2].iloc[0]

    st.title("🎯 AI Edge Final A/B Dashboard")

    # 3. The Comparison Grid
    col_labels, col_1, col_2 = st.columns([0.6, 1, 1])

    with col_labels:
        st.write("## ") # Top spacer
        st.markdown('<div style="height: 400px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Views</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Watch Time</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">CTR</span></div>', unsafe_allow_html=True)

    with col_1:
        st.markdown('<div class="winner-highlight">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center
        
