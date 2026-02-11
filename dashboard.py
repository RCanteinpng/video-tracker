import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="AI Edge - A/B Performance", layout="wide")

# This creates the green "Winner" box from the Iman Gadzhi tweet
st.markdown("""
    <style>
    .winner-box { background-color: #1a2e1a; border: 2px solid #28a745; padding: 20px; border-radius: 15px; }
    .challenger-box { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

def get_id(value):
    """Force-extracts a YouTube ID from any string or link"""
    val_str = str(value)
    if 'v=' in val_str: return val_str.split('v=')[1][:11]
    if 'be/' in val_str: return val_str.split('be/')[1][:11]
    return val_str[:11]

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Auto-detect Columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), df.columns[1])
    title_col = next((c for c in df.columns if 'title' in c.lower()), df.columns[0])
    id_col = next((c for c in df.columns if any(x in c.lower() for x in ['id', 'video', 'content'])), df.columns[0])

    df = df.sort_values(by=view_col, ascending=False).reset_index(drop=True)
    winner = df.iloc[0]
    challengers = df.iloc[1:5]

    st.title("🎯 AI Edge Content A/B Testing")

    # --- THE COMPARISON LAYOUT ---
    col1, spacer, col2 = st.columns([1.2, 0.1, 1.5])

    with col1:
        st.markdown('<div class="winner-box">', unsafe_allow_html=True)
        st.subheader("🏆 THE WINNER")
        w_id = get_id(winner[id_col])
        st.image(f"https://img.youtube.com/vi/{w_id}/maxresdefault.jpg", use_container_width=True)
        st.markdown(f"### {winner[title_col]}")
        st.metric("Views", f"{int(winner[view_col]):,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("📊 CHALLENGERS")
        for _, row in challengers.iterrows():
            st.markdown('<div class="challenger-box">', unsafe_allow_html=True)
            c1, c2 = st.columns([0.4, 0.6])
            with c1:
                c_id = get_id(row[id_col])
                st.image(f"https://img.youtube.com/vi/{c_id}/mqdefault.jpg", use_container_width=True)
            with c2:
                st.write(f"**{row[title_col]}**")
                st.write(f"📈 {int(row[view_col]):,} views")
            st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Almost there! Error: {e}")
    
