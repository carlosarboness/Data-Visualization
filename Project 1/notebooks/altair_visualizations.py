import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd

# ----------------------- Visualization 1 --------------------------- #

collisions = pd.read_csv("../data/preprocessed-collisions-final.csv")

paired_bar_chart = alt.Chart(collisions[['CRASH_DATETIME', 'DAY_WEEK' ]]).mark_bar().encode(
  x = alt.X('year:O', title = 'Type of day', axis=alt.Axis(title=None, labels=False, ticks=False)),
  y = alt.Y('count:Q', title = 'Number of collisions', axis=alt.Axis(offset=6)),
  color= alt.Color('year:O', scale = alt.Scale(range=['#ff7f0e', '#9467bd'])),
  column = alt.Column('DAY_WEEK:N', title='Day of the Week',
                      sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                      header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=4))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
).transform_aggregate(
  count='count()',
  groupby=['year', 'DAY_WEEK']
)

slope_chart = alt.Chart(collisions[['CRASH_DATETIME', 'DAY_WEEK', 'TYPE_DAY']]).mark_line(point=True).encode(
  x=alt.X('TYPE_DAY:O', title = 'Type of day'),
  y=alt.Y('avg_collisions:Q', title = 'Average number of collisions'),
  color=alt.Color('year:O', scale = alt.Scale(range=['#ff7f0e', '#9467bd']), legend=alt.Legend(title='Year')),
).transform_calculate(
  year='year(datum.CRASH_DATETIME)'
).transform_aggregate(
  count='count()',
  groupby=['year', 'DAY_WEEK', 'TYPE_DAY']
).transform_aggregate(
  avg_collisions = 'mean(count)',
  groupby=['year', 'TYPE_DAY']
)

c1 = (paired_bar_chart | slope_chart).properties(
     title='Number of collisions by day of the week and year'
).configure_title(
  anchor='middle', offset=25, fontSize=18, fontStyle='normal', fontWeight='normal'
).configure_view(
  stroke='transparent'
).resolve_scale(
  y='shared'
)

# ----------------------- Visualization 2 --------------------------- #

vehicle_type = pd.DataFrame({'vehicle_type': list(collisions['VEHICLE_TYPE_CODE1'].values) + list(collisions['VEHICLE_TYPE_CODE2'].values)})
vehicle_type = vehicle_type.groupby('vehicle_type').size().reset_index(name='n_accidents')
most_collisioned = list(vehicle_type.sort_values(by='n_accidents', ascending=False).head(10)['vehicle_type'])
vehicle_type['vehicle_type'] = vehicle_type['vehicle_type'].apply(lambda x: x if x in most_collisioned else 'Others')
vehicle_type = vehicle_type.groupby('vehicle_type').sum('counts').reset_index()
vehicle_type = vehicle_type.sort_values(by='n_accidents', ascending=False)

bar_chart = alt.Chart(vehicle_type).mark_bar().encode(
    x=alt.X('n_accidents:Q', title='Number of collisions', scale=alt.Scale(domain=(0, 1e5 + 1))),
    y=alt.Y('vehicle_type:N', 
            sort=list(vehicle_type.loc[vehicle_type['vehicle_type'] != 'Others', 'vehicle_type']) + ['Others'], 
            title='Vehicle Type'),
    color=alt.condition(
            alt.datum.vehicle_type == 'Others', 
            alt.value('grey'),
            alt.value('steelblue')
        )
)
    
mean_line = alt.Chart(vehicle_type).mark_rule(color='red', strokeWidth=1.5).encode(
        x = alt.X('mean(n_accidents):Q')
)

n_accidents_text = alt.Chart(vehicle_type).mark_text(align='left', dx=2, color='black', size=10).encode(
        x=alt.X('n_accidents:Q'),
        y=alt.Y('vehicle_type:N', 
            sort=list(vehicle_type.loc[vehicle_type['vehicle_type'] != 'Others', 'vehicle_type']) + ['Others']),
        text='n_accidents:Q'
)

c2 = (bar_chart + mean_line + n_accidents_text).properties(
        title='Number of collisions by vehicle type'
).configure_title(
        anchor='middle', fontSize=16, fontStyle='normal', fontWeight='normal', offset=20
).properties(
    height=400 
)


# ----------------------- Visualization 3 --------------------------- #

error_bar = alt.Chart(collisions[['CRASH_DATETIME', 'CRASH_DATE']]).mark_errorbar(ticks=True).encode(
    x=alt.X('hours:Q'),
    y=alt.Y('count:Q',axis=alt.Axis(title=None), scale=alt.Scale(zero=False)),
    color = alt.Color('year:O', scale = alt.Scale(range=['#ff7f0e', '#9467bd']))
).transform_calculate(
  year = 'year(datum.CRASH_DATETIME)',
  hours = 'hours(datum.CRASH_DATETIME)'
).transform_aggregate(
   count='count()',
   groupby=['year', 'hours', 'CRASH_DATE']
)

avg_deaths_line = alt.Chart(collisions[['CRASH_DATETIME', 'CRASH_DATE','TOTAL_KILLED']]).mark_trail().encode(
    x = alt.X('hours:Q', title='Time of day'),
    y = alt.Y('avg_collisions:Q', title='Average number of collisions'),
    color = alt.Color('year:O', scale = alt.Scale(range=['#ff7f0e', '#9467bd']), title='Year'),
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

# ----------------------- Visualization 4 --------------------------- #

'''
Given the various issues we've encountered in displaying this visualization on Streamlit, 
we have decided to save the image beforehand to directly showcase it in the application.
'''

# ----------------------- Visualization 5 --------------------------- #

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

width = 80

boxplot = alt.Chart().mark_boxplot(color='black').encode(
    alt.Y(f'collisions:Q')
).properties(width=width)

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
    width=width,
    height=300
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

# ----------------------- Visualization 6 --------------------------- #

deadly_accidents = collisions[['CRASH_DATE', 'TOTAL_KILLED', 'PEDESTRIANS_KILLED', 'CYCLIST_KILLED', 'MOTORIST_KILLED']]

deadly_accidents = deadly_accidents[deadly_accidents['TOTAL_KILLED'] == deadly_accidents['PEDESTRIANS_KILLED'] + \
                                                                        deadly_accidents['CYCLIST_KILLED'] + \
                                                                        deadly_accidents['MOTORIST_KILLED']]

deadly_accidents = deadly_accidents.drop(columns=['TOTAL_KILLED'])
deadly_accidents['CRASH_DATE'] = pd.to_datetime(deadly_accidents['CRASH_DATE'])
deadly_accidents['year'] = deadly_accidents['CRASH_DATE'].dt.year
deadly_accidents = deadly_accidents.groupby('year').sum(['PEDESTRIANS_KILLED', 'CYCLIST_KILLED', 'MOTORIST_KILLED']).reset_index()

deadly_accidents_melted = deadly_accidents.melt('year', var_name='type', value_name='killed')
deadly_accidents_melted['type'] = deadly_accidents_melted['type'].apply(lambda x: x.split('_')[0].lower())
deadly_accidents_melted = deadly_accidents_melted.sort_values(by=['year', 'killed'], ascending=False).reset_index(drop=True)

mortal_collisions = alt.Chart(deadly_accidents_melted).mark_bar().encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('sum(killed):Q', title='Number of deaths'),
    color=alt.Color('type:N', scale=alt.Scale(scheme='accent'), legend=alt.Legend(title='Type of user')),
    order=alt.Order('type', sort='ascending'),
).properties(
    height=500
)

deadly_accidents_melted['position'] = [61+15, 61+38+15, 15, 43+5, 43+40+5, 5]

number_of_deaths = alt.Chart(deadly_accidents_melted).mark_text(color='white', dy=7).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('position:Q', title='Number of deaths'),
    text=alt.Text('killed:Q', format='.0f')
)

c6 = (mortal_collisions + number_of_deaths).properties(
     title='Number of deaths by type of user and year'
).configure_title(
  anchor='middle', offset=25, fontSize=16, fontStyle='normal', fontWeight='normal'
)