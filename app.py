import streamlit as st
import pandas as pd
from utils import get_user, get_repos
import matplotlib.pyplot as plt

st.set_page_config(page_title="GitHub Visualizer", layout="wide")

st.title("GitHub Profile Visualizer")

# 🔥 Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# 🔍 Input
username = st.text_input("Enter GitHub Username", "google")

if username and username not in st.session_state.history:
    st.session_state.history.append(username)

# 📂 Sidebar
st.sidebar.title("Search History")

selected_user = None
for user in st.session_state.history:
    if st.sidebar.button(user):
        selected_user = user

if st.sidebar.button("Clear History"):
    st.session_state.history = []

if selected_user:
    username = selected_user

# 🚀 Main
if username:
    user = get_user(username)
    repos_data = get_repos(username)

    if "message" in user:
        st.error("User not found")
    else:
        # 👤 Profile
        st.subheader("Profile Info")

        col1, col2 = st.columns(2)

        with col1:
            st.image(user.get("avatar_url"), width=150)

        with col2:
            st.write("Name:", user.get("name"))
            st.write("Followers:", user.get("followers"))
            st.write("Following:", user.get("following"))
            st.write("Public Repos:", user.get("public_repos"))

        # 📊 Data
        repo_names, stars, languages, dates = [], [], [], []

        for repo in repos_data:
            repo_names.append(repo.get('name'))
            stars.append(repo.get('stargazers_count'))
            languages.append(repo.get('language'))
            dates.append(repo.get('created_at'))

        df = pd.DataFrame({
            "Repository": repo_names,
            "Stars": stars,
            "Language": languages,
            "Created": dates
        })

        df = df.dropna()

        # 🎯 Filter slider
        min_stars = st.slider("Filter by minimum stars", 0, int(df["Stars"].max()), 0)
        df = df[df["Stars"] >= min_stars]

        # ⭐ Top Repo Highlight
        if not df.empty:
            top_repo = df.sort_values(by="Stars", ascending=False).iloc[0]
            st.success(f"Top Repo: {top_repo['Repository']} ⭐ {top_repo['Stars']}")

        # 📈 Top Repos Chart
        st.subheader("Top Repositories")
        top_df = df.sort_values(by="Stars", ascending=False).head(10)

        if not top_df.empty:
            st.bar_chart(top_df.set_index("Repository")["Stars"])
        else:
            st.write("No data available")

        # 🌍 Language Chart
        st.subheader("Language Distribution")
        if not df.empty:
            lang_df = df["Language"].value_counts()
            st.bar_chart(lang_df)

        # 📅 Repo Creation Trend
        st.subheader("Repo Creation Trend")

        if not df.empty:
            df["Created"] = pd.to_datetime(df["Created"])
            df["Month"] = df["Created"].dt.to_period("M")

            trend = df["Month"].value_counts().sort_index()

            st.line_chart(trend)

        # 📥 Download CSV
        st.subheader("Download Data")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Repo Data as CSV",
            data=csv,
            file_name=f"{username}_repos.csv",
            mime='text/csv',
        )