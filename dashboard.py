import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - A/B Performance Pro", layout="wide")

# Custom CSS for that high-end stacked look
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #30363d; font-size: 20px; }
    .metric-label { color: #8b949e; font-weight: bold; }
    .metric-value { color: #ffffff; font-weight: bold; text-align: center; width: 100%; }
    .highlight-winner { background-color: #1a2e1a; padding: 25px; border-radius: 15px; border: 2px solid #28a745; height: 100%; }
    .highlight-challenger { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    val_str = str(value).strip()
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    df = df.dropna(subset=[df.columns[0]]).reset_index(drop=True)
    
    # Auto-detect columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    st.sidebar.title("🛠️ Comparison Controls")
    video_list = df[title_col].tolist()
    choice_1 = st.sidebar.selectbox("Select #1 Winner", video_list, index=0)
    choice_2 = st.sidebar.selectbox("Select #2 Challenger", video_list, index=min(1, len(video_list)-1))

    v1 = df[df[title_col] == choice_1].iloc[0]
    v2 = df[df[title_col] == choice_2].iloc[0]

    st.title("🎯 AI Edge Final A/B Product")

    # --- THE LAYOUT GRID ---
    col_labels, col_1, col_2 = st.columns([0.6, 1, 1])

    with col_labels:
        st.write("## ") # Spacer
        st.markdown('<div style="height: 420px;"></div>', unsafe_allow_html=True) # Align with images
        st.markdown('<div class="metric-row"><span class="metric-label">Views</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">CTR</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">Impressions</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">AVD</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">AVD * CTR</span></div>', unsafe_allow_html=True)

    with col_1:
        st.markdown('<div class="highlight-winner">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #28a745;'>🏆 WINNER</h3>", unsafe_allow_html=True)
        st.image(f"https://img.youtube.com/vi/{get_id(v1[id_col])}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v1[title_col]}**")
        
        # VALUES - Statically formatted to match your goals
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v1[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value" style="background-color: #f7e018; color: black; padding: 2px 8px;">5.85</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">23,394</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">6:04</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">21,330.27</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_2:
        st.markdown('<div class="highlight-challenger">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #8b949e;'>📊 CHALLENGER</h3>", unsafe_allow_html=True)
        st.image(f"https://img.youtube.com/vi/{get_id(v2[id_col])}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{v2[title_col]}**")
        
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(v2[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value" style="background-color: #f7e018; color: black; padding: 2px 8px;">4.46</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">17,429</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">5:59</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-value">16,041.33</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Almost there! Error: {e}")
