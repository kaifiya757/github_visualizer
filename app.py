import streamlit as st
import pandas as pd
from utils import get_user, get_repos

st.title("GitHub Profile Visualizer")

username = st.text_input("Enter GitHub Username", "google")

if username:
    user = get_user(username)
    repos_data = get_repos(username)

    # 🔥 Profile Section
    st.subheader("Profile Info")

    col1, col2 = st.columns(2)

    with col1:
        st.image(user["avatar_url"], width=150)

    with col2:
        st.write("Name:", user.get("name"))
        st.write("Followers:", user["followers"])
        st.write("Following:", user["following"])
        st.write("Public Repos:", user["public_repos"])

    # 📊 Repo Data
    repo_names = []
    stars = []
    languages = []

    for repo in repos_data:
        repo_names.append(repo['name'])
        stars.append(repo['stargazers_count'])
        languages.append(repo['language'])

    df = pd.DataFrame({
        "Repository": repo_names,
        "Stars": stars,
        "Language": languages
    })

    df = df.dropna()
    df = df.sort_values(by="Stars", ascending=False).head(10)

    st.subheader("Top Repositories by Stars")
    st.bar_chart(df.set_index("Repository")["Stars"])

    # 🌍 Language Distribution
    st.subheader("Language Distribution")
    lang_df = df["Language"].value_counts()
    st.bar_chart(lang_df)