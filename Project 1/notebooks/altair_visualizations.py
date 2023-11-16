import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd

# -------------------------------------------------- #

frequent_collisions = pd.read_csv('../data/frequent-collisions.csv')
vehicle_type = pd.read_csv('../data/vehicle_type.csv')
geo_collisions = pd.read_csv('../data/geo_collisions.csv')
gdf = pd.read_csv('../data/gdf.csv')

# -------------------------------------------------- #

paired_bar_chart = alt.Chart(frequent_collisions).mark_bar().encode(
  x = alt.X('year:O', title = 'Type of day', axis=alt.Axis(title=None, labels=False, ticks=False)), 
  y = alt.Y('count:Q', title = 'Number of collisions'),
  color= alt.Color('year:O', scale = alt.Scale(domain=[2018, 2020], range=['#ff7f0e', 'steelblue'])),
  column = alt.Column('day_week:N', title='Day of the Week', 
  sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
  header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=4))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
).transform_aggregate(
   count='count()',
   groupby=['year', 'day_week']
)

slope_chart = alt.Chart(frequent_collisions).mark_line(point=True).encode(
  x = alt.X('type_day:O', title = 'Type of day'),
  y = alt.Y('avg:Q', title = 'Number of collisions', axis=alt.Axis(title=None)),
  color= alt.Color('year:O', scale = alt.Scale(domain=[2018, 2020], range=['#ff7f0e', 'steelblue']))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)'
).transform_aggregate(
   count='count()',
   groupby=['year', 'day_week', 'type_day']
).transform_aggregate(
    avg = 'mean(count)',
    groupby=['year', 'type_day']
)

c1 = (paired_bar_chart | slope_chart).properties(
    title='Number of collisions by day of the week and year',
).configure_title(anchor='middle').configure_view(stroke='transparent').resolve_scale(y='shared', x='independent', color='shared')

# -------------------------------------------------- #

bar_chart = alt.Chart(vehicle_type).mark_bar().encode(
    x=alt.X('counts:Q', title='Number of collisions'),
    y=alt.Y('vehicle_type:N', 
            sort=list(vehicle_type.loc[vehicle_type['vehicle_type'] != 'Others', 'vehicle_type']) + ['Others'], 
            title='Vehicle Type'),
    color=alt.condition(
        alt.datum.vehicle_type == 'Others',
        alt.value('grey'),
        alt.Color('character:N', 
                  legend=alt.Legend(title='Ownership Type'), 
                  scale=alt.Scale(domain=['Public', 'Private'], 
                                  range=['#4daf4a', '#377eb8'])),
    ),  
)

mean_line = alt.Chart(vehicle_type).mark_rule(color='red', strokeWidth=1.5).encode(x = alt.X('mean(counts):Q'))

c2 = (bar_chart + mean_line).properties(
   title=alt.TitleParams(text='Number of collisions by vehicle type', fontSize=14, subtitle='', offset=20),
   width=300,
   height=400
).configure_title(anchor='middle').configure_view(stroke='transparent')

# -------------------------------------------------- #

choropleth_map = alt.Chart(gdf).mark_geoshape().encode(
    alt.Color('normalized_by_area_count:Q', 
              scale=alt.Scale(scheme='lightorange', domain=[0, 40]), 
              legend = None),
)

borough_names = alt.Chart(geo_collisions).mark_text(fontWeight='bold', fontSize=11, color='black').encode(
    latitude='mean_lat:Q',
    longitude='mean_long:Q',
    text='BOROUGH:N',
).transform_aggregate(
    mean_lat='mean(LATITUDE)',
    mean_long='mean(LONGITUDE)',
    groupby=['BOROUGH']
)

c4 = (choropleth_map + borough_names).properties(
    title=alt.TitleParams(text='Number of Collisions by PostalCode', fontSize=16, subtitle='', offset=20),
).configure_title(anchor='middle')

# -------------------------------------------------- #