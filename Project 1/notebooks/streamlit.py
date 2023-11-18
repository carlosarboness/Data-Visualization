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
st.write("In the middle-left, you can see a line chart with the average accidents per hour along the summers of 2018 and 2020. A different color for each year has been used as well as the line thickness to encode the killed people. Regarding the question asked about what time of the day are accidents more common, a clear trend emerges: higher collision rates during the day and lower rates during the night. This pattern aligns with the increased presence of cars on the road during daylight hours and decreased activity during nighttime. Further we can distinguish different patterns between morning, afternoon, and evening periods. Mornings exhibit fewer collisions, likely attributed to work-related activities, whereas afternoons register higher incidents, potentially linked to leisure activities and transporting children to extracurricular activities. Evenings witness a decline in collisions as people conclude their activities and are back home.  \n  Furthermore, by looking at the line thickness we can see that the deathliest hours are at 20:00 and 04:00 in 2018, and between 19:00 and 00:00, as well as at 04:00 in 2020. The deaths in the late night coincide with the times when people are returning home after socializing, often under the influence of alcohol, which make the accidents more dangerous. However, beeing able to see that is more difficult because, one of the drawbacks of this visualization is that the line thickness is not easy to compare. Another criticism is that the error bars make the patterns a difficult to read. Dispite that it is important to keep them in the visualization because they show the variance of the data.")

st.write("### Are there any areas with a larger number of accidents?")
st.write("In the map in the top-right chart, we can observe areas with a higher concentration of accidents per square kilometer. This is evident by examining the intensity of the blue color, where darker shades of blue indicate a higher number of accidents per km². Knowing this, we can see that areas with the highest accident ratios are located in the southern part of Manhattan, featuring zones with a significant number of accidents. It's also noteworthy that there are dark blue areas in the center of Brooklyn, indicating a high number of accidents. The same pattern occurs in some southwestern parts of the Bronx and a specific postal code area in Queens, situated in the northwest. In Staten Island, the color intensity is very low, indicating a low number of accidents per km² throughout the borough. In the bar chart to the right of the map, we can interpret, based on the length of the bars, that Manhattan has by far the highest number of accidents per km², which aligns with our observation on the map. Following Manhattan, there are relatively high accident rates in Brooklyn, the Bronx, Queens, and, lastly, as observed earlier, Staten Island, with significantly fewer accidents compared to the others.")

st.write("### Is there a correlation between weather conditions and accidents?")
st.write("In the bottom, we can see two violin plots juxtaposed, one for each year (2018 and 2020). The x-axis represents the weather conditions, and the y-axis represents the number of accidents per day. The width of the violin shows the distribution of the data, and the boxplot inside the violin shows the median and quartiles of the data. \n The first thing we can observe is that the distribution of the data is wider in 2020 than in 2018, which means that there is more variance in the number of collisions. Furthermore, we see that, in 2018, the median of the number of collisions is higher with rain conditions but with the other weather conditions there is not a significant difference between the number of collisions. In 2020 we do not see enough evidence to conclude that a type of weather condition is more likely to cause an accident. These probably happens because in 2020 there was a lockdown and people were not driving as much as in 2018 so there were less cars on the road and the weather conditions did not affect as much as in 2018. In general we conclude that despite having some evidence, it is not enough to conclude that there is a correlation between weather conditions and accidents. If there was, we would be able to see it in the distribution of the data, which would be more concentrated in some weather conditions than in others. \n The drawbacks of this visualization is that we have not encoded any quantitative variable of the weather conditions because since there are a lot of them, any plot is good enough to be able to see them toghether easily. For that we ended up choosing the weather conditions as a categorical variable which takes into account all the quantitative variables of the weather conditions.")


