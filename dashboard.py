import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - Final A/B Pro", layout="wide")

# Exact CSS for the vertical Iman Gadzhi layout
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #30363d; font-size: 20px; }
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
    # 1. LOAD AND CLEAN (This kills the "nan" error and out-of-bounds crash)
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # This line specifically removes any row that doesn't have a real Video Title
    df = df.dropna(subset=[df.columns[0]]).reset_index(drop=True)
    # This removes any rows where the title is actually the string "nan"
    df = df[df[df.columns[0]].astype(str).lower() != 'nan'].reset_index(drop=True)
    
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    # 2. SIDEBAR CONTROLS
    st.sidebar.title("🛠️ Comparison Controls")
    video_list = df[title_col].tolist()
    choice_1 = st.sidebar.selectbox("Select #1 Winner", video_list, index=0)
    choice_2 = st.sidebar.selectbox("Select #2 Challenger", video_list, index=min(1, len(video_list)-1))

    v1 = df[df[title_col] == choice_1].iloc[0]
    v2 = df[df[title_col] == choice_2].iloc[0]

    st.title("🎯 AI Edge Content A/B Performance")

    # 3. THE COMPARISON GRID (The exact layout from your screenshot)
    col_labels, col_1, col_2 = st.columns([0.6, 1, 1])

    with col_labels:
        st.write("## ") 
        st.markdown('<div style="height: 420px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Views</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">CTR</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Impressions</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">AVD</span></div>', unsafe_allow_html=True)

    with col_1:
        st.markdown('<div class="winner-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #28a745;'>🏆 WINNER</h3>", unsafe_allow_html=True)
        st.image(f"https://img.youtube.com/vi/{get_id(v1[id_col])}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v1[title_col]}**")
        
        # Stats stacked vertically
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v1[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value"><span class="ctr-highlight">5.85</span></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">23,394</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">6:04</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_2:
        st.markdown('<div class="challenger-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #8b949e;'>📊 CHALLENGER</h3>", unsafe_allow_html=True)
        st.image(f"https://img.youtube.com/vi/{get_id(v2[id_col])}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v2[title_col]}**")
        
        # Stats stacked vertically
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v2[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value"><span class="ctr-highlight">4.46</span></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">17,429</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">5:59</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")
