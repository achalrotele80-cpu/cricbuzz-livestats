import streamlit as st


st.title("🏠 About Cricbuzz LiveStats")

st.markdown("""
## Project Overview

**Cricbuzz LiveStats** is an interactive cricket analytics platform
that integrates live cricket data with a SQL database.

The application provides:

- ⚡ Real-time match updates
- 📊 Player performance statistics
- 🔍 SQL-driven cricket analytics
- 🛠️ CRUD database operations
- 📈 Interactive visualizations
""")

st.divider()

st.subheader("💼 Business Use Cases")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📺 Sports Media
    - Live match information
    - Player performance analysis
    - Historical trends
    """)

    st.markdown("""
    ### 🎮 Fantasy Cricket
    - Player form
    - Head-to-head statistics
    - Recent performance
    """)

with col2:
    st.markdown("""
    ### 📈 Cricket Analytics
    - Player evaluation
    - Performance trends
    - Statistical analysis
    """)

    st.markdown("""
    ### 🎓 Education
    - SQL practice
    - Database operations
    - API integration
    """)

st.divider()

st.subheader("🛠️ Technology Stack")

st.write(
    "Python • Streamlit • SQL • SQLite • Pandas • REST API • "
    "Requests • Plotly"
)