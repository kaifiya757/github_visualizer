import streamlit as st
import pandas as pd
from utils import get_user, get_repos

st.set_page_config(page_title="GitHub Visualizer", layout="wide")

st.title("GitHub Profile Visualizer")

# 🔥 Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# 🔍 Input box
username = st.text_input("Enter GitHub Username", "google")

# ➕ Add to history
if username and username not in st.session_state.history:
    st.session_state.history.append(username)

# 🔥 Sidebar - Search History
st.sidebar.title("Search History")

selected_user = None

for user in st.session_state.history:
    if st.sidebar.button(user):
        selected_user = user

# Clear history button
if st.sidebar.button("Clear History"):
    st.session_state.history = []

# If user clicked from history
if selected_user:
    username = selected_user

# 🚀 Main Logic
if username:
    user = get_user(username)
    repos_data = get_repos(username)

    # ❌ Handle invalid user
    if "message" in user:
        st.error("User not found. Try another username.")
    else:
        # 👤 Profile Section
        st.subheader("Profile Info")

        col1, col2 = st.columns(2)

        with col1:
            st.image(user.get("avatar_url"), width=150)

        with col2:
            st.write("Name:", user.get("name"))
            st.write("Followers:", user.get("followers"))
            st.write("Following:", user.get("following"))
            st.write("Public Repos:", user.get("public_repos"))

        # 📊 Repo Data
        repo_names = []
        stars = []
        languages = []

        for repo in repos_data:
            repo_names.append(repo.get('name'))
            stars.append(repo.get('stargazers_count'))
            languages.append(repo.get('language'))

        df = pd.DataFrame({
            "Repository": repo_names,
            "Stars": stars,
            "Language": languages
        })

        # Clean data
        df = df.dropna()
        df = df.sort_values(by="Stars", ascending=False).head(10)

        # 📈 Top Repos
        st.subheader("Top Repositories by Stars")
        if not df.empty:
            st.bar_chart(df.set_index("Repository")["Stars"])
        else:
            st.write("No data available")

        # 🌍 Language Distribution
        st.subheader("Language Distribution")
        if not df.empty:
            lang_df = df["Language"].value_counts()
            st.bar_chart(lang_df)
        else:
            st.write("No language data available")