import streamlit as st
import pandas as pd

# Set page to wide mode to fit everything like the screenshot
st.set_page_config(page_title="AI Edge - Content Dashboard", layout="wide")

# Custom CSS to make the title look professional
st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: #FFFFFF; }
    .metric-card { background-color: #1E1E1E; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 AI Edge Performance Dashboard")

# Load your Excel data
try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # --- 1. TOP LINE METRICS ---
    total_views = df['Views'].sum()
    total_videos = len(df)
    avg_views = df['Views'].mean()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Channel Views", f"{total_views:,}")
    m2.metric("Videos Tracked", total_videos)
    m3.metric("Avg. Views/Video", f"{int(avg_views):,}")
    m4.metric("Active Status", "LIVE")

    # --- 2. MAIN PERFORMANCE CHART ---
    st.subheader("📈 Views Comparison")
    # Making the chart big and readable
    st.bar_chart(df, x="Video title", y="Views", height=500, use_container_width=True)

    # --- 3. THE THUMBNAIL GALLERY (Final Product) ---
    st.divider()
    st.subheader("🖼️ AI Edge Content Catalog")

    # This creates a grid of thumbnails
    cols = st.columns(3) 
    
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Use the Video ID from your Excel to pull the real YouTube thumbnail
            video_id = str(row['Video ID']).strip()
            thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            # Displaying the image and the specific stats for that video
            st.image(thumb_url, use_container_width=True)
            st.markdown(f"**{row['Video title']}**")
            st.caption(f"👀 Views: {row['Views']:,}")
            st.divider()

    # --- 4. RAW DATA TABLE ---
    with st.expander("View Raw Data Table"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
    st.info("Check that your Excel file has 'Video title', 'Views', and 'Video ID' columns.")
