import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - A/B Test Pro", layout="wide")

# Exact CSS for the professional Iman Gadzhi look
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #30363d; font-size: 20px; }
    .metric-label { color: #8b949e; font-weight: bold; }
    .metric-value { color: #ffffff; font-weight: bold; text-align: center; width: 100%; }
    .ctr-highlight { background-color: #f7e018; color: black; padding: 4px 10px; border-radius: 4px; font-weight: bold; }
    .winner-box { background-color: #1a2e1a; padding: 25px; border-radius: 15px; border: 2px solid #28a745; height: 100%; }
    .challenger-box { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    val_str = str(value).strip()
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    # 1. Load and Clean (CRITICAL: removes 'nan' rows)
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    df = df.dropna(how='all').dropna(subset=[df.columns[0]]).reset_index(drop=True)
    
    # Auto-detect columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    # 2. Sidebar Controls
    st.sidebar.title("🛠️ Comparison Controls")
    video_list = df[title_col].tolist()
    choice_1 = st.sidebar.selectbox("Select #1 Winner", video_list, index=0)
    choice_2 = st.sidebar.selectbox("Select #2 Challenger", video_list, index=min(1, len(video_list)-1))

    v1 = df[df[title_col] == choice_1].iloc[0]
    v2 = df[df[title_col] == choice_2].iloc[0]

    st.title("🎯 AI Edge Content A/B Performance")

    #
