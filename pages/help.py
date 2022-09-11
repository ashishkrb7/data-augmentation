from pathlib import Path
import streamlit as st
import os

PAGE_CONFIG = {
    "page_icon": "🤖",
    "page_title": "Augment",
    "layout": "wide",
    "initial_sidebar_state": "auto",
}
st.set_page_config(**PAGE_CONFIG)

st.markdown(
    """ <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}header {visibility: hidden;}</style>""",
    unsafe_allow_html=True,
)

# Remove whitespace from the top of the page and sidebar
st.markdown(
    """
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


path_st = os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")).replace(
    "\\", "/"
)  # Working directory


def styling_css_call(file_name):
    """To call CSS"""
    try:
        with open(path_st + "/pages/assets/" + file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass


styling_css_call("global.css")


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


intro_markdown = read_markdown_file(f"{path_st}/README.md")
st.markdown(intro_markdown, unsafe_allow_html=True)
