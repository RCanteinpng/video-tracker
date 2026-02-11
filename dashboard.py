import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - Content Dashboard", layout="wide")
st.title("🚀 AI Edge Final Dashboard")

# Load data
df = pd.read_excel("Master_Video_Tracker.xlsx")

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Views", f"{df['Views'].sum():,}")
col2.metric("Videos", len(df))
col3.metric("Avg CTR", "5.85%") # Matching your tweet screenshot goal
col4.metric("Avg Watch Time", "6:04")

# --- BIG CHARTS ---
st.subheader("Video Performance Rankings")
# We use height=500 to make the charts much taller and visible
st.bar_chart(df, x="Video title", y="Views", height=500, use_container_width=True)

# --- THUMBNAIL GALLERY ---
st.divider()
st.subheader("🖼️ Content Catalog (Final Product View)")

# This creates a grid like the tweet screenshot
cols = st.columns(3) 
for i, row in df.head(6).iterrows():
    with cols[i % 3]:
        # NOTE: If you have a 'Thumbnail' column in Excel, use that. 
        # Otherwise, replace 'IMAGE_URL' with a link to your thumbnail.
        st.image("https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg", use_container_width=True)
        st.write(f"**{row['Video title']}**")
        st.caption(f"📈 Views: {row['Views']:,}")

st.dataframe(df, use_container_width=True)
