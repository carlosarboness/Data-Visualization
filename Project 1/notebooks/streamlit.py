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


with st.container():
    
    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(c1, use_container_width=True)
        st.altair_chart(c3, use_container_width=True)

    with col2: 
        st.image('../data/c4.png', use_column_width=True)
        st.altair_chart(c2, use_container_width=True)

with st.container():    
    
    left_co, cent_co, last_co = st.columns([1, 5, 5])
    cent_co.altair_chart(c5, use_container_width=True)

st.markdown("---")

st.write("## Questions")

st.write("### Are accidents more frequent during weekdays or weekends? Is there any difference between before COVID-19 and after?")
st.write("In the top-left chart, orange bars represent data from the year 2018, while blue bars represent data from 2020 (before and after COVID, respectively). Analyzing the length of the bars reveals a consistent trend: on all days of the week, the total number of accidents occurring on each day is considerably higher (more than double in all cases) before COVID compared to after. Furthermore, in the right slope chart, where colors correspond to those in the paired bar chart, a decreasing trend is evident in the number of accidents on weekdays versus weekends. Weekends consistently exhibit a lower average number of accidents both before and after COVID. Notably, this difference intensifies before COVID, indicating a more pronounced contrast. However, in 2020, the difference is not as significant. From this graph, we can infer that the number of traffic accidents has decreased post-COVID, and this reduction in accidents on weekends has followed a similar trend, with a slight decrease in the decline. One possible explanation is the reduced use of both public and private transportation on weekends due to decreased overall activity (work, school, etc.).")

st.write("### Is there any type of vehicle more prone to participate in accidents?")
st.write("In the middle-right chart, we can observe the number of accidents involving different types of vehicles in both 2018 and 2020 (from June to September). In this case, we cannot directly answer the question about which vehicles are more prone to accidents, as it would require knowledge of the number of vehicles of each type in New York (or circulating in New York). Quantifying this is a challenging task since, for example, although we see that Sedans have the highest number of accidents, there are likely also many more Sedan-type cars on the roads in New York. The same may be true for SUVs. By examining the length of the bars or directly looking at the numbers at the end of each bar, we can note that sedans and SUVs are the vehicle types most frequently involved in accidents, overshadowing other vehicles such as taxis, pickups, bicycles, etc. Despite the difficulty in quantifying the total number of each vehicle type, what we can conclude is that Sedans and SUVs mentioned earlier contribute to a significant percentage of accidents in New York. By observing that the bars are well to the right of the red bar (mean accidents), it's evident that these values are well above the average accidents per vehicle. It's also noteworthy that taxis, although likely fewer in number, still have a notable frequency of accidents.")

st.write("### At what time of the day are accidents more common?")
st.write("In the map in the top-right chart, we can observe areas with a higher concentration of accidents per square kilometer. This is evident by examining the intensity of the blue color, where darker shades of blue indicate a higher number of accidents per km². Knowing this, we can see that areas with the highest accident ratios are located in the southern part of Manhattan, featuring zones with a significant number of accidents. It's also noteworthy that there are dark blue areas in the center of Brooklyn, indicating a high number of accidents. The same pattern occurs in some southwestern parts of the Bronx and a specific postal code area in Queens, situated in the northwest. In Staten Island, the color intensity is very low, indicating a low number of accidents per km² throughout the borough. In the bar chart to the right of the map, we can interpret, based on the length of the bars, that Manhattan has by far the highest number of accidents per km², which aligns with our observation on the map. Following Manhattan, there are relatively high accident rates in Brooklyn, the Bronx, Queens, and, lastly, as observed earlier, Staten Island, with significantly fewer accidents compared to the others.")

st.write("### Are there any areas with a larger number of accidents?")
st.write("Respuesta")

st.write("### Is there a correlation between weather conditions and accidents?")
st.write("Respuesta")


