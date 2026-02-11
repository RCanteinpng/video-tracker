import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - Final Dashboard", layout="wide")
st.title("🚀 AI Edge Content Dashboard")

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # --- AUTO-DETECT COLUMNS ---
    # This finds the Video ID even if the column is named 'Video' or 'ID'
    id_col = next((c for c in df.columns if 'video' in c.lower() or 'id' in c.lower()), None)
    view_col = next((c for c in df.columns if 'view' in c.lower()), 'Views')
    title_col = next((c for c in df.columns if 'title' in c.lower()), 'Video title')

    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Views", f"{df[view_col].sum():,}")
    m2.metric("Total Videos", len(df))
    m3.metric("Avg Views", f"{int(df[view_col].mean()):,}")

    # --- BIG PERFORMANCE CHART ---
    st.subheader("📈 Video Performance")
    st.bar_chart(df, x=title_col, y=view_col, height=500, use_container_width=True)

    # --- THUMBNAIL GALLERY ---
    st.divider()
    st.subheader("🖼️ AI Edge Content Catalog")
    
    cols = st.columns(3) 
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Extracts just the ID if the cell contains a full link
            raw_id = str(row[id_col])
            video_id = raw_id.split('/')[-1].split('=')[-1] if '/' in raw_id else raw_id
            
            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            st.image(thumb_url, use_container_width=True)
            st.write(f"**{row[title_col]}**")
            st.caption(f"📈 Views: {row[view_col]:,}")
            st.divider()

except Exception as e:
    st.error(f"Almost there! Just a small data error: {e}")
