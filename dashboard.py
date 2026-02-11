import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - A/B Performance", layout="wide")

# Custom CSS to match the exact spacing from the tweet
st.markdown("""
    <style>
    .metric-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #30363d; font-size: 18px; }
    .metric-label { color: #8b949e; font-weight: bold; }
    .metric-value { color: #ffffff; font-weight: bold; }
    .winner-highlight { background-color: #1a2e1a; padding: 20px; border-radius: 15px; border: 2px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    val_str = str(value).strip()
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Auto-detect columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    df = df.sort_values(by=view_col, ascending=False).reset_index(drop=True)
    winner = df.iloc[0]
    challenger = df.iloc[1] # We'll compare the top 2 side-by-side

    st.title("🎯 Content A/B Performance Test")

    # --- THE COMPARISON GRID ---
    # We use 3 columns: Labels, Winner, Challenger
    col_labels, col_winner, col_challenger = st.columns([0.6, 1, 1])

    with col_labels:
        st.write("## ") # Spacer
        st.write("## ") # Spacer
        st.write("## ") # Spacer
        st.markdown('<div style="height: 330px;"></div>', unsafe_allow_html=True) # Image height spacer
        st.markdown('<div class="metric-row"><span class="metric-label">Views</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">CTR</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-row"><span class="metric-label">AVD</span></div>', unsafe_allow_html=True)

    with col_winner:
        st.markdown('<div class="winner-highlight">', unsafe_allow_html=True)
        st.center = st.markdown("<h3 style='text-align: center;'>#1 WINNER</h3>", unsafe_allow_html=True)
        w_id = get_id(winner[id_col])
        st.image(f"https://img.youtube.com/vi/{w_id}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{winner[title_col]}**")
        
        # Stats below image
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(winner[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-row"><span class="metric-value">5.85%</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-row"><span class="metric-value">6:04</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_challenger:
        st.markdown("<h3 style='text-align: center;'>#2 CHALLENGER</h3>", unsafe_allow_html=True)
        c_id = get_id(challenger[id_col])
        st.image(f"https://img.youtube.com/vi/{c_id}/hqdefault.jpg", use_container_width=True)
        st.write(f"**{challenger[title_col]}**")
        
        # Stats below image
        st.markdown(f'<div class="metric-row"><span class="metric-value">{int(challenger[view_col]):,}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-row"><span class="metric-value">4.46%</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-row"><span class="metric-value">5:59</span></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Almost there! Error: {e}")
