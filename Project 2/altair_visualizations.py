import pandas as pd
import numpy as np
import altair as alt

collisions = pd.read_csv('data/preprocessed-collisions-final.csv') 

options_month = ['June', 'July', 'August', 'September']
input_dropdown_month = alt.binding_select(options=options_month + [None], labels=options_month + ['All'], name='Month:  ')
selection_month = alt.selection_point(fields=['MONTH'], bind=input_dropdown_month)

# -------------------------------  c1  -------------------------------------

selection_weather = alt.selection_point(encodings=['x'])

c1 = alt.Chart(collisions).mark_bar().encode(
  x=alt.X('icon:N', title='Weather', sort='-y', axis=alt.Axis(labelAngle=0)),
  y=alt.Y('sum(count):Q', title='Number of Accidents'),
  color=alt.condition(selection_weather, 
                      alt.Color('CASUALTIES:N', scale=alt.Scale(range=['teal', 'orange'])), 
                      alt.value('lightgray')), 
).transform_aggregate(
  count = 'count()',
  groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY', 'CASUALTIES']
).add_params( 
  selection_month, selection_weather
).transform_filter(
  selection_month
).properties(
    title='Number of collisions by type of weather',
    height=300, 
    width=275
)

# -------------------------------  c2  -------------------------------------

selection_vehicle = alt.selection_point(encodings=['x'])

vehicle_type_to_emoji = {
    'Taxi': '🚕',
    'Ambulance': '🚑',
    'Fire truck': '🚒'
}

collisions['vehicle_emoji'] = collisions['VEHICLE_TYPE_CODE1'].map(vehicle_type_to_emoji)

base = alt.Chart(collisions).encode(
    x=alt.X('VEHICLE_TYPE_CODE1:N', sort='-y', title='Vehicle Type', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(count):Q', title='Number of Collisions'),
    color = alt.condition(selection_vehicle, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['VEHICLE_TYPE_CODE1:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY', 'vehicle_emoji']
).add_params(
    selection_month, selection_vehicle
).transform_filter(
    selection_month 
).properties(
    title='Number of collisions by vehicle type',
    width=200,
    height=300
)

c2 = base.mark_bar() + base.mark_text(dy=-10, size=30).encode(text='vehicle_emoji:N')

collisions = collisions.drop(columns=['vehicle_emoji'])

# -------------------------------  c3  -------------------------------------

selection_day = alt.selection_interval(encodings=['x'])

base = alt.Chart(collisions).encode(
    x=alt.X('DAY:O', title='Day of the month', scale=alt.Scale(domain=np.arange(1, 32)), axis=alt.Axis(labelAngle=0)),
    y=alt.Y('MONTH:N', title='Month', scale=alt.Scale(domain=options_month)),
    tooltip=['DAY:O', 'MONTH:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day
).transform_filter(
    selection_month 
).properties(
    title='Number of collisions by day of the month',
)

heatmap = base.mark_rect().encode(
    color = alt.condition(selection_day, 
                          alt.Color('sum(count):Q', scale=alt.Scale(scheme='lightgreyred'), legend=None),
                          alt.value('lightgray'), legend=None),
).properties(
    width=550,
    height=175
)

c3 = heatmap + base.mark_text(baseline='middle').encode(
    text='sum(count):Q', 
    color = alt.condition(selection_day, 
                          alt.value('black'), 
                          alt.value('lightgray')))

# -------------------------------  c4  -------------------------------------

raw_github_url = 'https://raw.githubusercontent.com/benetraco/ny_map/main/ny_city_map.geojson'
ny_city_map = alt.Data(url=raw_github_url, format=alt.DataFormat(property='features'))
ny_city = alt.Chart(ny_city_map).mark_geoshape(fill='lightgray', stroke='white', strokeWidth=1.3, opacity=0.4).encode(tooltip=alt.value(None)) 

brush_map = alt.selection_interval()

c4 = alt.Chart(collisions).mark_point(size=3, opacity=0.7, filled=True).encode(
    latitude='LATITUDE:Q',
    longitude='LONGITUDE:Q',
    color = alt.condition(brush_map, 
                          alt.Color('BOROUGH:N', legend=None, scale=alt.Scale(scheme='dark2')), 
                          alt.value('lightgray')),
    tooltip=['BOROUGH:N', 'VEHICLE_TYPE_CODE1:N', 'icon:N', 'HOUR:O', 'MONTH:N', 'DAY_WEEK:N', 'DAY:O'],
).add_params(
    selection_month, brush_map
).transform_filter(
    selection_month 
).properties(
    title='Number of collisions by borough',
).properties(
    height=400, 
    width=350
)

# -------------------------------  c41  ------------------------------------

selection_borough = alt.selection_point(fields=['BOROUGH'])

c41 = alt.Chart(collisions).mark_bar().encode(
  x=alt.X('sum(count):Q', title='Number of Collisions'),
  y=alt.Y('BOROUGH:N', title='Borough', sort='-x', axis=alt.Axis(labelAngle=0)),
  color=alt.condition(selection_borough, alt.Color('BOROUGH:N'), alt.value('lightgray')),
  tooltip=['BOROUGH:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_borough
).transform_filter(
    selection_month & brush_map
).properties(
    width=500,
    height=175
)

# -------------------------------- c5 ------------------------------------

selection_hour = alt.selection_interval(encodings=['x'])
selection_hour_point = alt.selection_point(encodings=['x'])

c5  = alt.Chart(collisions).mark_line(point=True).encode(
    x=alt.X('HOUR:O', title='Hour of Day', scale=alt.Scale(domain=np.arange(1, 24)), axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(count):Q', title='Number of Collisions'),
    color=alt.condition(selection_hour & selection_hour_point, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['HOUR:O', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_hour, selection_hour_point
).transform_filter(
    selection_month 
).properties(
    title='Number of collisions by hour of day',
    width=550,
    height=175
)

# -------------------------------  c6 ------------------------------------

selection_dayweek = alt.selection_point(encodings=['y'])
days_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

base = alt.Chart(collisions).encode(
    y=alt.Y('DAY_WEEK:N', title='Day of Week', 
            sort='-x'),
    x=alt.X('sum(count):Q', title='Number of Collisions'),
    color=alt.condition(selection_dayweek, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['DAY_WEEK:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_dayweek, 
).transform_filter(
    selection_month
).properties(
    title='Number of collisions by day of week',
    width=500,
    height=175
)

c6 = base.mark_point(filled=True) + base.mark_rule()


# Interactions

c1 = c1.transform_filter(selection_vehicle & selection_borough & selection_dayweek & selection_hour & brush_map & selection_day & selection_hour_point)
c2 = c2.transform_filter(selection_weather & selection_borough & selection_dayweek & selection_hour & brush_map & selection_day & selection_hour_point)
c3 = c3.transform_filter(selection_vehicle & selection_weather & selection_dayweek & selection_hour & brush_map & selection_weather & selection_hour_point)
c4 = c4.transform_filter(selection_vehicle & selection_borough & selection_dayweek & selection_hour & selection_day & selection_weather & selection_hour_point)
c41 = c41.transform_filter(selection_vehicle & selection_dayweek & selection_hour & selection_day & selection_weather & brush_map & selection_hour_point)
c5 = c5.transform_filter(selection_vehicle & selection_borough & selection_dayweek & selection_day & selection_weather & brush_map)
c6 = c6.transform_filter(selection_vehicle & selection_borough & selection_hour & selection_day & selection_weather & brush_map & selection_hour_point)

# Final chart

final_chart = (((((ny_city + c4) & c41) & c6) | ((c1 | c2) & c3 & c5)).configure_title(anchor='middle'))