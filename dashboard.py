import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Edge - A/B Performance", layout="wide")

# Dark Theme Styling
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .metric-box { border: 1px solid #4f4f4f; padding: 15px; border-radius: 10px; background: #161b22; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = pd.read_excel("Master_Video_Tracker.xlsx")
    
    # Auto-detect columns
    view_col = next((c for c in df.columns if 'view' in c.lower()), 'Views')
    title_col = next((c for c in df.columns if 'title' in c.lower()), 'Video title')
    id_col = next((c for c in df.columns if 'video' in c.lower() or 'id' in c.lower()), 'Video ID')

    # Sort to find the "Winner"
    df = df.sort_values(by=view_col, ascending=False)
    winner = df.iloc[0]
    others = df.iloc[1:4] # Get the next 3 for comparison

    st.title("🎯 Content A/B Performance Comparison")
    st.write("Comparing your top-performing 'Winner' against recent uploads.")

    # --- THE COMPARISON LAYOUT ---
    col_a, vs, col_b = st.columns([1, 0.2, 1])

    with col_a:
        st.subheader("🏆 THE WINNER")
        vid_id = str(winner[id_col]).split('/')[-1].split('=')[-1]
        st.image(f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg", use_container_width=True)
        st.markdown(f"### {winner[title_col]}")
        st.info(f"📈 Total Views: {winner[view_col]:,}")

    with vs:
        st.markdown("<h1 style='text-align: center; padding-top: 100px;'>VS</h1>", unsafe_allow_html=True)

    with col_b:
        st.subheader("📊 CHALLENGERS")
        for i, row in others.iterrows():
            c1, c2 = st.columns([0.4, 0.6])
            with c1:
                o_id = str(row[id_col]).split('/')[-1].split('=')[-1]
                st.image(f"https://img.youtube.com/vi/{o_id}/mqdefault.jpg", use_container_width=True)
            with c2:
                st.write(f"**{row[title_col]}**")
                st.caption(f"Views: {row[view_col]:,}")
            st.divider()

    # --- BIG CHART AT BOTTOM ---
    st.subheader("📈 Performance Benchmarks")
    st.bar_chart(df.head(10), x=title_col, y=view_col, height=400, use_container_width=True)

except Exception as e:
    st.error(f"Layout Error: {e}")
