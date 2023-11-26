import streamlit as st

st.set_page_config(layout="wide")

st.title("🚗 New York Collisions Study 🗽")

st.subheader("Visualizing collisions dataset from New York City")

st.markdown("---")

with st.sidebar:
    st.sidebar.title("👨‍💻 About")
    st.sidebar.info(
        """
        This web app was created by Carlos Arbonés and Benet Ramió, two students from the GCED degree at UPC.
        
        **Gmail:**
        carlos.arbones@estudiantat.upc.edu
        benet.ramio@estudiantat.upc.edu
        
        Source code: [GitHub](https://github.com/carlosarboness/Data-Visualization)
        """
    )