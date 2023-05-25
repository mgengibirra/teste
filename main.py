import os
import streamlit as st

st.title("File Manager")

selected_dir = st.text_input("Enter the path to your directory:")

st.write("diretório = " + selected_dir)

if selected_dir:
    try:
        abs_dir = os.path.abspath(selected_dir)
        os.chdir(abs_dir)
        st.success("Current working directory set to: " + os.getcwd())
    except OSError:
        st.error("Invalid directory path.")

'''

        

# Streamlit app    
    
# Directory selection

if selected_dir:
    try:
        os.chdir(selected_dir)
        st.success("Current working directory set to: " + os.getcwd())
    except OSError:
        st.error("Invalid directory path.")

# File selection
file_list = os.listdir(os.getcwd())
selected_file = st.selectbox("Choose a file to open", file_list)
if selected_file:
    try:
        with open(selected_file, 'r') as file:
            contents = file.read()
        st.write(contents)
    except FileNotFoundError:
        st.error(f"File '{selected_file}' not found.")

'''
