import streamlit as st
import streamlit.components.v1 as components

# This launches your 8R Stealth visual
with open("index.html", "r") as f:
    html_code = f.read()
    components.html(html_code, height=1000, scrolling=True) 
