import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd

# Data
weather = pd.read_csv('data/weather2018.csv')
weather = weather[['datetime', 'icon']] # keep only datetime and icon columns
weather['datetime'] = pd.to_datetime(weather['datetime']) # convert datetime column to datetime type

collisions = pd.read_csv('data/preprocessed-collisions-2.csv') # read preprocessed collisions data
collisions['CRASH_DATETIME'] = pd.to_datetime(collisions['CRASH_DATETIME'])
collisions['MONTH'] = collisions['CRASH_DATETIME'].dt.month_name() 
collisions['HOUR'] = collisions['CRASH_DATETIME'].dt.hour
collisions['DAY_WEEK'] = collisions['CRASH_DATETIME'].dt.day_name()
collisions['DAY'] = collisions['CRASH_DATETIME'].dt.day
collisions = collisions[['BOROUGH', 'ZIP_CODE', 'LATITUDE', 'LONGITUDE', 
                         'CONTRIBUTING_FACTOR_VEHICLE1', 'VEHICLE_TYPE_CODE1',
                         'CRASH_DATETIME', 'MONTH', 'HOUR', 'DAY_WEEK', 'DAY']]
collisions = collisions.merge(weather, how='left', left_on=collisions['CRASH_DATETIME'].dt.date, right_on=weather['datetime'].dt.date)
collisions = collisions.drop(columns=['key_0', 'datetime']) # drop redundant columns

# Selection parameters
options_month = list(collisions['MONTH'].unique()) # ['June', 'July', 'August', 'September']

input_dropdown_month = alt.binding_select(options=options_month + [None], labels=options_month + ['All'], name='Month:  ')
selection_month = alt.selection_point(fields=['MONTH'], bind=input_dropdown_month)


options_day_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

input_dropdown_day_week = alt.binding_select(options=options_day_week + [None], labels=options_day_week + ['All'], name='Day of the week:  ')
selection_day_week = alt.selection_point(fields=['DAY_WEEK'], bind=input_dropdown_day_week)


options_borough = list(collisions['BOROUGH'].unique()) # ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']

input_dropdown_borough = alt.binding_select(options=options_borough + [None], labels=options_borough + ['All'], name='Borough:  ')
selection_borough = alt.selection_point(fields=['BOROUGH'], bind=input_dropdown_borough)


options_vehicle = list(collisions['VEHICLE_TYPE_CODE1'].unique()) # ['Taxi', 'Ambulance', 'Fire truck']

input_dropdown_vehicle = alt.binding_select(options=options_vehicle + [None], labels=options_vehicle + ['All'], name='Vehicle type:  ')
selection_vehicle = alt.selection_point(fields=['VEHICLE_TYPE_CODE1'], bind=input_dropdown_vehicle)


options_weather = list(collisions['icon'].unique()) # ['rain', 'clear-day', 'partly-cloudy-day', 'cloudy']

input_dropdown_weather = alt.binding_select(options=options_weather + [None], labels=options_weather + ['All'], name='Weather:  ')
selection_weather = alt.selection_point(fields=['icon'], bind=input_dropdown_weather)


select_hour = alt.selection_point(name="hour", fields=['HOUR'], 
                                  bind=alt.binding_range(min=0, max=23, step=1, name="Hour: "))
bind_checkbox = alt.binding_checkbox(name='All Hours:  ')
param_checkbox = alt.param(bind=bind_checkbox)


select_day = alt.selection_point(name="day", fields=['DAY'], 
                                 bind=alt.binding_range(min=1, max=31, step=1, name="Day: "))

bind_checkbox_day = alt.binding_checkbox(name='All Days:  ')
param_checkbox_day = alt.param(bind=bind_checkbox_day)

# c1
base = alt.Chart(collisions).mark_arc().encode(
    alt.Theta('icon:N', scale=alt.Scale(domain=list(collisions['icon'].unique())), stack=True),
    alt.Radius('sum(count):Q', scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color=alt.Color('icon:N', title='Weather', scale=alt.Scale(domain=list(collisions['icon'].unique()))),
    tooltip=['icon:N', 'sum(count):Q']
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather & (select_day | param_checkbox_day)
).properties(
    title='Number of collisions by type of weather',
)

c1 = base.mark_arc(innerRadius=20, stroke="#fff") + base.mark_text(radiusOffset=10).encode(text="sum(count):Q")


# c2
base = alt.Chart(collisions).encode(
    x=alt.X('VEHICLE_TYPE_CODE1:N', sort='-y', scale=alt.Scale(domain=options_vehicle), title='Vehicle Type', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(count):Q', title='Number of Collisions'),
    tooltip=['VEHICLE_TYPE_CODE1:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather & (select_day | param_checkbox_day)
).properties(
    title='Number of collisions by vehicle type',
    width=200,
    height=350,
)

c2 = base.mark_bar() + base.mark_text(dy=-10, size=15).encode(text="sum(count):Q", color=alt.value('black'))


# c3
base = alt.Chart(collisions).encode(
    x=alt.X('HOUR:O', title='Hour of Day', scale=alt.Scale(domain=np.arange(0, 24)), axis=alt.Axis(labelAngle=0)),
    y=alt.Y('MONTH:N', title='Month', scale=alt.Scale(domain=options_month)),
    tooltip=['HOUR:O', 'MONTH:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather & (select_day | param_checkbox_day)
).properties(
    title='Number of collisions by hour of day and month',
)

heatmap = base.mark_rect().encode(
    color=alt.Color('sum(count):Q', title='Number of Collisions', scale=alt.Scale(scheme='greenblue'))
)

c3 = heatmap + base.mark_text(baseline='middle', color='white').encode(text='sum(count):Q')


# c4
raw_github_url = 'https://raw.githubusercontent.com/benetraco/ny_map/main/ny_city_map.geojson'
ny_city_map = alt.Data(url=raw_github_url, format=alt.DataFormat(property='features'))
ny_city = alt.Chart(ny_city_map).mark_geoshape(fill='lightgray', stroke='white', strokeWidth=1.3, opacity=0.4).encode(tooltip=alt.value(None)) # create base map

c4 = alt.Chart(collisions).mark_point(size=3, opacity=0.7, filled=True).encode(
    latitude='LATITUDE:Q',
    longitude='LONGITUDE:Q',
    color=alt.Color('BOROUGH:N', scale=alt.Scale(domain=options_borough), title='Borough'),
    tooltip=['BOROUGH:N', 'VEHICLE_TYPE_CODE1:N', 'icon:N', 'HOUR:O', 'MONTH:N', 'DAY_WEEK:N', 'DAY:O'],
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather & (select_day | param_checkbox_day)
).properties(
    title='Location of collisions',
).properties(
    width=400,
    height=400
)

(ny_city + c4)

# c5
c5 = alt.Chart(collisions).mark_line(point=True).encode(
    x=alt.X('DAY:O', title='Day of Month', scale=alt.Scale(domain=np.arange(1, 32)), axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(count):Q', title='Number of Collisions'),
    color=alt.condition((select_day | param_checkbox_day), alt.value('red'), alt.value('lightgray')),
    tooltip=['DAY:O', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather 
).properties(
    title='Number of collisions by hour of day',
)

# c6
base = alt.Chart(collisions).encode(
    y=alt.Y('DAY_WEEK:N', title='Day of Week', 
            sort=options_day_week, 
            scale=alt.Scale(domain=options_day_week)),
    x=alt.X('sum(count):Q', title='Number of Collisions'),
    color=alt.value('teal'), 
    tooltip=['DAY_WEEK:N', 'sum(count):Q'],
).transform_aggregate(
    count = 'count()',
    groupby=['MONTH', 'DAY_WEEK', 'BOROUGH', 'VEHICLE_TYPE_CODE1', 'HOUR', 'icon', 'DAY']
).add_params(
    selection_month, selection_day_week, selection_borough, selection_vehicle, select_hour, param_checkbox, selection_weather, select_day, param_checkbox_day
).transform_filter(
    selection_month & selection_day_week & selection_borough & selection_vehicle & (select_hour | param_checkbox) & selection_weather & (select_day | param_checkbox_day)
).properties(
    title='Number of collisions by day of week',
    width=500
)

c6 = base.mark_point(filled=True) + base.mark_rule()


# Selections
selection_type_vehicle = alt.selection_interval(encodings=['x']) # selection for vehicle type
selection_day_week = alt.selection_interval(encodings=['y']) # selection for day of week
selection_day_month = alt.selection_interval(encodings=['x']) # selection for day of month
selection_hour = alt.selection_interval(encodings=['x']) # selection for hour of day
point_weather = alt.selection_point(fields=['icon']) # selection for weather
brush_map = alt.selection_interval() # selection for map


# We add the parameters inside the charts where they will be used.
c1 = c1.add_params(point_weather)
c2 = c2.encode(color=alt.condition(selection_type_vehicle, alt.value('steelblue'), alt.value('lightgray'))).add_params(selection_type_vehicle)
c3 = c3.add_params(selection_hour)
c4 = c4.add_params(brush_map)
c5 = c5.add_params(selection_day_month)
c6 = c6.encode(color=alt.condition(selection_day_week, alt.value('teal'), alt.value('lightgray'))).add_params(selection_day_week)


# We incorporate transformations into the other charts to create these interactions across different visualizations.
c1 = c1.transform_filter(selection_type_vehicle & selection_day_week & selection_day_month & point_weather & brush_map & selection_hour)
c2 = c2.transform_filter(selection_day_week & selection_day_month & point_weather & brush_map & selection_hour)
c3 = c3.transform_filter(selection_type_vehicle & selection_day_week & selection_day_month & point_weather & brush_map)
c4 = ny_city + c4.transform_filter(selection_type_vehicle & selection_day_week & selection_day_month & point_weather & selection_hour)
c5 = c5.transform_filter(selection_type_vehicle & selection_day_week & point_weather & brush_map & selection_hour)
c6 = c6.transform_filter(selection_type_vehicle & selection_day_month & point_weather & brush_map & selection_hour)