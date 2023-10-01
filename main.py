import streamlit as st
from scrape import GithubClient
import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()
CLOUD_TRANSLATION_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"

# Map between Google API language codes and language names
language_labels = dict(
    zip(
        ["fr", "hi", "zh", "ar", "es"],
        ["Français", "हिंदी", "中国人", "عربي", "Español"]
    )
)

def get_translation(texts : list, from_lang : str = "en", to_lang : str = "en"):
    resp = requests.post(
        GOOGLE_TRANSLATE_ENDPOINT, 
        {
            "q" : texts, 
            "source" : from_lang, 
            "target" : to_lang,
            "key" : CLOUD_TRANSLATION_API_KEY
        }
    )
    translate_json = resp.json()
    translations = [t["translatedText"] for t in translate_json["data"]["translations"]]
    return translations

def show_readmes():
    # Displays READMEs stored in session state
    if st.session_state["visible_repos"]: 
        with st.form("translation_form", clear_on_submit=False):
            st.form_submit_button("Translate", on_click = show_translated_readmes)

            for i in st.session_state["visible_repos"]:
                summary = st.session_state["repos"][i]
                with st.expander(label = summary["title"]):
                    st.checkbox(label = "Translate this README", key=f"checkbox_{i}")
                    st.markdown(summary["readme_html"], unsafe_allow_html=True)

# Handles translate button logic to update session state READMEs and then calls show_readmes
def show_translated_readmes():
    st.title("Git Global 🌎")
    translated_readmes = []
    for i in st.session_state["visible_repos"]:
        summary = st.session_state["repos"][i]
        if st.session_state[f"checkbox_{i}"]:
            t_segments = get_translation(summary["readme_text"], to_lang = st.session_state["target_language"])            
            t_readme = summary["readme_html"]
            for english_text, translated_text in zip(summary["readme_text"], t_segments):
                t_readme = t_readme.replace(english_text, translated_text)
            summary["readme_html"] = t_readme
            translated_readmes.append(summary)
    n_translated = len(translated_readmes)
    st.session_state["repos"] = translated_readmes
    st.session_state["visible_repos"] = [i for i in range(n_translated)]

    show_readmes()       
    st.sidebar.download_button(
        label = "Download READMEs",
        file_name = f"README - {st.session_state['username']} - {language_labels[st.session_state['target_language']]}.json",
        mime = "json",
        data = json.dumps(st.session_state["repos"])
    )

def show_finetuned_repos():
    show_keyword_form()
    st.title("Git Global 🌎")

    keyword = st.session_state["keyword"]
    translated_keyword = get_translation(
        [keyword], 
        from_lang = st.session_state["target_language"]
    )[0]
    print(translated_keyword)

    finetuned_indices = []
    for i, summary in enumerate(st.session_state["repos"]):
        if translated_keyword in summary["readme_html"]:
            finetuned_indices.append(i)
    st.session_state["visible_repos"] = finetuned_indices
    print(finetuned_indices, "repositories visible after keyword searching.")
    show_readmes()

def show_searched_repos():
    show_keyword_form()
    st.title("Git Global 🌎")
    
    username = st.session_state["username"]
    user_type = st.session_state["user_type"]
    repo_limit = st.session_state["repo_limit"]

    with st.spinner(f"Fetching READMEs from user {username}..."):
        repo_summaries = GithubClient.get_user_repo_summaries(
            username=username, 
            user_type=user_type,
            link_limit=int(repo_limit) if repo_limit else float("inf")
        )
    n_repos = len(repo_summaries)
    st.session_state["repos"] = repo_summaries
    st.session_state["visible_repos"] = [i for i in range(n_repos)]
    show_readmes()

# Setup sidebar search fields
def show_search_form():
    with st.sidebar.form("search_form", clear_on_submit = False):
        st.text_input(
            "Github name",
            key="username"
        )
        st.radio(
            label="User type",
            options=("user", "org"),
            format_func=lambda opt: "Individual User" if opt == "user" else "Organization",
            key="user_type"
        )
        st.text_input(
            "Repository limit",
            key="repo_limit",
        )
        st.form_submit_button(
            label = "Search",
            on_click = show_searched_repos
        )

def reset_views():
    show_keyword_form()
    n_repos = len(st.session_state["repos"])
    st.session_state["visible_repos"] = range(n_repos)
    show_readmes()

def show_keyword_form():
    st.sidebar.button("Reset", on_click=reset_views)
    with st.sidebar.form("keyword_search", clear_on_submit=False):
        st.selectbox(
            label = "Preferred language",
            options = language_labels.keys(),
            format_func=lambda opt: language_labels[opt],
            key = "target_language"
        )
        st.text_input(
            "Keyword search", 
            key="keyword"
        )
        st.form_submit_button(
            label = "Finetune", 
            on_click = show_finetuned_repos,
        )

if __name__ == '__main__':
    if "repos" not in st.session_state:
        st.title("Git Global 🌎")
    show_search_form()