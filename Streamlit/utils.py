import streamlit as st
# from PIL import Image

from streamlit_extras.app_logo import add_logo

# im = Image.open("logo.png")
# im1 = im.resize(([100,100]))

def logo():
    add_logo("logo120.png",height=80)
    
def Title():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Co-Creator";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )