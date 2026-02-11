import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge Content Tracker", layout="wide")
st.title("📊 AI Edge Content Tracker")

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Calculate main metrics using raw YouTube column names
    total_views = df['Views'].sum()
    total_videos = len(df)
    avg_views = df['Views'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Views", f"{total_views:,}")
    col2.metric("Videos Tracked", total_videos)
    col3.metric("Avg. Views", f"{int(avg_views):,}")

    st.subheader("Top 10 Videos by Views")
    # Sort by the 'Views' column in your Excel sheet
    top_10 = df[['Video title', 'Views']].sort_values(by='Views', ascending=False).head(10)
    st.bar_chart(data=top_10, x='Video title', y='Views')
    
    st.dataframe(df)

except Exception as e:
    st.error(f"Error loading data: {e}")
    
