import streamlit as st
from altair_visualizations import *

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


col1, col2 = st.columns(2)

with col1:
    st.altair_chart(c1, use_container_width=True)
    st.altair_chart(c2, use_container_width=True)

with col2: 

    st.altair_chart(c4, use_container_width=True)
    st.altair_chart(c1, use_container_width=True)


