import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd

# -------------------------------------------------- #

frequent_collisions = pd.read_csv('../data/frequent-collisions.csv')
vehicle_type = pd.read_csv('../data/vehicle_type.csv')
geo_collisions = pd.read_csv('../data/geo_collisions.csv')
gdf = pd.read_csv('../data/gdf.csv')
collisions = pd.read_csv("../data/preprocessed-collisions-final.csv")

# -------------------------------------------------- #

paired_bar_chart = alt.Chart(frequent_collisions).mark_bar().encode(
  x = alt.X('year:O', title = 'Type of day', axis=alt.Axis(title=None, labels=False, ticks=False)), 
  y = alt.Y('count:Q', title = 'Number of collisions'),
  color= alt.Color('year:O', scale = alt.Scale(scheme='tableau10')),
  column = alt.Column('DAY_WEEK:N', title='Day of the Week', 
  sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
  header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=4))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
).transform_aggregate(
   count='count()',
   groupby=['year', 'DAY_WEEK']
)

slope_chart = alt.Chart(frequent_collisions).mark_line(point=True).encode(
  x = alt.X('TYPE_DAY:O', title = 'Type of day'),
  y = alt.Y('avg:Q', title = 'Number of collisions', axis=alt.Axis(title=None)),
  color= alt.Color('year:O', scale = alt.Scale(scheme='tableau10')),
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)'
).transform_aggregate(
   count='count()',
   groupby=['year', 'DAY_WEEK', 'TYPE_DAY']
).transform_aggregate(
    avg = 'mean(count)',
    groupby=['year', 'TYPE_DAY']
)

c1 = (paired_bar_chart | slope_chart).properties(
     title='Number of collisions by day of the week and year'
).configure_title(anchor='middle').configure_view(stroke='transparent').resolve_scale(y='shared', x='independent', color='shared')

# -------------------------------------------------- #

bar_chart = alt.Chart(vehicle_type).mark_bar().encode(
    x=alt.X('counts:Q', title='Number of collisions'),
    y=alt.Y('vehicle_type:N', 
            sort=list(vehicle_type.loc[vehicle_type['vehicle_type'] != 'Others', 'vehicle_type']) + ['Others'], 
            title='Vehicle Type'),
    color=alt.condition(
        alt.datum.vehicle_type == 'Others',
        alt.value('brown'),
        alt.Color('character:N', legend=alt.Legend(title='Ownership Type'), 
                  scale=alt.Scale(domain=['Public', 'Private'], range=['#4daf4a', 'grey'])),
    ),  
)

mean_line = alt.Chart(vehicle_type).mark_rule(color='red', strokeWidth=1.5).encode(x = alt.X('mean(counts):Q'))

c2 = (bar_chart + mean_line).properties(
   title=alt.TitleParams(text='Number of collisions by vehicle type', fontSize=14, subtitle='', offset=20),
   width=300,
   height=300
).configure_title(anchor='middle').configure_view(stroke='transparent')

# -------------------------------------------------- #

error_bar = alt.Chart(collisions).mark_errorbar(ticks=True).encode(
    x=alt.X('hours:Q'),
    y=alt.Y('count:Q',axis=alt.Axis(title=None), scale=alt.Scale(zero=False)),
    color = alt.Color('year:O', scale = alt.Scale(scheme='tableau10'))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
  hours = 'hours(datum.CRASH_DATETIME)'
).transform_aggregate(
   count='count()',
   groupby=['year', 'hours', 'CRASH_DATE']
)

avg_deaths_line = alt.Chart(collisions).mark_trail().encode(
    x = alt.X('hours:Q', title='Time of day'),
    y = alt.Y('avg_collisions:Q', title='Average number of collisions'),
    color = alt.Color('year:O', scale = alt.Scale(scheme='tableau10'), title='Year'),
    size = alt.Size('avg_killed:Q', title='Average deaths')
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
  hours = 'hours(datum.CRASH_DATETIME)'
).transform_aggregate(
   count_collisions='count()',
   count_killed='sum(TOTAL_KILLED)',
   groupby=['year', 'hours', 'CRASH_DATE']
).transform_aggregate(
    avg_collisions='mean(count_collisions)',
    avg_killed='mean(count_killed)',
    groupby=['year', 'hours']
)

c3 = (avg_deaths_line + error_bar).properties(
    title='Average collisions and deaths over time',
    width=600,
    height=400
    ).configure_title(
      anchor='middle', offset=25, fontSize=18, fontStyle='normal', fontWeight='normal'
    )

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

weather_original = pd.read_csv("../data/weather.csv")
weather = weather_original[['datetime', 'temp', 'precip', 'windspeed', 
                            'humidity', 'cloudcover', 'conditions', 'visibility']]
weather['datetime'] = pd.to_datetime(weather['datetime'])
coll_weather = pd.DataFrame({'datetime': collisions["CRASH_DATE"]})
coll_weather['datetime'] = pd.to_datetime(coll_weather['datetime'])
coll_weather = coll_weather.groupby(['datetime']).size().reset_index(name='collisions')
coll_weather = pd.merge(coll_weather, weather, on='datetime')
coll_weather['year'] = coll_weather['datetime'].dt.year
coll_weather['conditions'] = coll_weather['conditions'].apply(lambda x: 'Rain, Overcast' if x=='Overcast' else x)

coll_weather_2018 = coll_weather[coll_weather['year']==2018]
coll_weather_2020 = coll_weather[coll_weather['year']==2020]

boxplot = alt.Chart().mark_boxplot(color='black').encode(
    alt.Y(f'collisions:Q')
).properties(width=100)

violin = alt.Chart().transform_density(
    'collisions',
    as_=['collisions', 'density'],
    extent=[0, 1000],
    groupby=['conditions']
).mark_area(orient='horizontal').encode(
    y='collisions:Q',
    color=alt.Color('conditions:N', legend=None, scale=alt.Scale(scheme='set2')),
    x=alt.X(
        'density:Q',
        stack='center',
        impute=None,
        title=None,
        scale=alt.Scale(nice=False, zero=False),
        axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
    ),
).properties(
    width=100,
    height=400
)

facet = lambda coll_weather, title: alt.layer(violin, boxplot, data=coll_weather).facet(column='conditions:N').\
    resolve_scale(x=alt.ResolveMode("independent")).properties(title=alt.TitleParams(text=title, anchor="middle", align="center"))

c5 = alt.hconcat(facet(coll_weather_2018, "Summer 2018"),facet(coll_weather_2020, "Sumer 2020")).configure_facet(
    spacing=0,
).configure_header(
    titleOrient='bottom',
    labelOrient='bottom'
).configure_view(
    stroke=None
).properties(
    title='Collisions distribution for weather conditions',
).configure_title(
      anchor='middle', offset=25, fontSize=18, fontStyle='normal', fontWeight='normal'
    )