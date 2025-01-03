import streamlit as st

def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Italiana&family=Quicksand:wght@300..700&display=swap');
    
    .title{
        font-family: 'Italiana', serif;
        font-weight: bold;
        font-size: 80px;
    }
    
    .subheading1{
        font-family: "Quicksand", serif;
        font-optical-sizing: auto;
        font-weight: 300;
        font-style: normal;
    }
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)