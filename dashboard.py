import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - A/B Test Pro", layout="wide")

# Exact CSS to match the Iman Gadzhi layout (Stats stacked vertically below images)
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #30363d; font-size: 20px; }
    .metric-label { color: #8b949e; font-weight: bold; }
    .metric-value { color: #ffffff; font-weight: bold; text-align: center; width: 100%; }
    .winner-highlight { background-color: #1a2e1a; padding: 25px; border-radius: 15px; border: 2px solid #28a745; height: 100%; }
    .challenger-highlight { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    val_str = str(value).strip()
    # Scans for the 11-character YouTube ID in links or raw text
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Auto-detect your specific Excel columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    # --- SIDEBAR: YOU PICK THE VIDEOS ---
    st.sidebar.title("🛠️ Comparison Controls")
    video_list = df[title_col].tolist()
    
    choice_1 = st.sidebar.selectbox("Select #1 Winner", video_list, index=0)
    choice_2 = st.sidebar.selectbox("Select #2 Challenger", video_list, index=1 if len(video_list) > 1 else 0)

    # Get the data for the two choices
    v1 = df[df[title_col] == choice_1].iloc[0]
    v2 = df[df[title_col] == choice_2].iloc[0]

    st.title("🎯 AI Edge Content A/B Performance")
    st.write("Compare any two videos from the @AIEdgeHQ library.")

    # --- THE LAYOUT GRID ---
    # Labels on the left, Winner in middle, Challenger on right
    col_labels, col_1, col_2 = st.columns([0.5, 1, 1])

    with col_labels:
        st.write("## ") # Top alignment spacer
        st.markdown('<div style="height: 380px;"></div>', unsafe_allow_html=True) # Image height spacer
        st.markdown('<div class="metric-row"><span class="metric-label">Views</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Watch Time</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">CTR</span></div>', unsafe_allow_html=True)

    with col_1:
        st.markdown('<div class="winner-highlight">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #28a745;'>🏆 WINNER</h3>", unsafe_allow_html=True)
        id1 = get_id(v1[id_col])
        st.image(f"https://img.youtube.com/vi/{id1}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v1[title_col]}**")
        
        # Values stacked exactly like the screenshot
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v1[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">6:04</span></div>', unsafe_allow_html=True) # Placeholder
        st.markdown('<div class="metric-row"><span class="metric-value">5.85%</span></div>', unsafe_allow_html=True) # Placeholder
        st.markdown('</div>', unsafe_allow_html=True)

    with col_2:
        st.markdown('<div class="challenger-highlight">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #8b949e;'>📊 CHALLENGER</h3>", unsafe_allow_html=True)
        id2 = get_id(v2[id_col])
        st.image(f"https://img.youtube.com/vi/{id2}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v2[title_col]}**")
        
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v2[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">5:59</span></div>', unsafe_allow_html=True) # Placeholder
        st.markdown('<div class="metric-row"><span class="metric-value">4.46%</span></div>', unsafe_allow_html=True) # Placeholder
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Data Connection Error: {e}")
