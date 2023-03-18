import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import folium as fol


overall_data = pd.read_csv('assets/overall_data.csv')


overall_data["pickup_datetime"] = pd.to_datetime(overall_data['pickup_datetime'])
overall_data['dropoff_datetime'] = pd.to_datetime(overall_data['dropoff_datetime'])


covid_df  = pd.read_csv('assets/covidreportsbystate.csv')

covid_df['submission_date'] = pd.to_datetime(covid_df['submission_date'])
covid_df['created_at'] = pd.to_datetime(covid_df['created_at'])

covid_df.drop(columns=['consent_cases', 'consent_deaths', 'prob_cases', 'new_case', 'pnew_case', 'prob_death', 'new_death', 'pnew_death', 'conf_cases', 'conf_death'], inplace=True)

covid_df['year'] = covid_df['submission_date'].dt.year

#create a graph of the average number of passengers per ride per year rounded to two decimal places
passenger_count = overall_data.groupby('year')['passenger_count'].mean()
passenger_count.plot(kind='bar', ylabel="Passengers", title='Average Passenger Count by Year', color='blue')

#plot the tot_cases by day where state = NY
covid_df[covid_df['state'] == 'NY'].plot(kind='area',x='submission_date', y='tot_cases', title='Total Cases in NY by Day', xlabel='Date', ylabel='Total Cases', figsize=(20, 10)).ticklabel_format(style='plain', axis='y')

#did cash payments increase or decrease in 2020?
cash_2020 = overall_data[overall_data['payment_type'] == 'cash']
cash_2020 = cash_2020.groupby('year')['payment_type'].count()
cash_2020

#did credit card payments increase or decrease in 2020?
credit_2020 = overall_data[overall_data['payment_type'] == 'credit_card']
credit_2020 = credit_2020.groupby('year')['payment_type'].count()
credit_2020

#plot the number of rides that paid with credit card in 2019
credit_2019 = overall_data[overall_data['payment_type'] == 'credit_card']
credit_2019 = credit_2019.groupby('year')['payment_type'].count()


#plot the number of rides that paid with cash after 2019
cash_2019 = overall_data[overall_data['payment_type'] == 'cash']
cash_2019 = cash_2019.groupby('year')['payment_type'].count()


#overlay cash_2019 and credit_2019 side by side to compare on the same graph with a legend
fig, ax = plt.subplots()
credit_2019.plot(title='Credit Card Payments', color='blue', ax=ax)
cash_2019.plot(title='Cash  vs. Credit Payments', color='red', ax=ax)
ax.legend(['Credit Card', 'Cash'])


#plot the average fare amount per year
fare_amount = overall_data.groupby('year')['fare_amount'].mean()
fare_amount.plot(title='Average Fare Amount by Year', color='blue', ylabel='Fare Amount')


borough_data = pd.read_csv('assets/taxi_zone_lookup.csv')


#convert PU location ID in overall_data to borough based on borough_data
borough_data = borough_data[['LocationID', 'Borough']]
borough_data = borough_data.rename(columns={'LocationID': 'PULocationID'})
overall_data = overall_data.merge(borough_data, on='PULocationID', how='left')
overall_data = overall_data.rename(columns={'Borough': 'PUBorough'})


overall_data = overall_data.loc[overall_data['PUBorough'] != 'EWR']
overall_data = overall_data.loc[overall_data['PUBorough'] != 'Unknown']


#reset index of overall_data by puborough
map_data = overall_data.set_index('PUBorough')
map_data


#make the map interactive with a mouseover
map = fol.Map(location=[40.7128, -74.0060], zoom_start=10)
map.choropleth(geo_data='assets/new-york-city-boroughs.geojson', data=overall_data, columns=['PUBorough', 'trip_distance'], key_on='feature.properties.name', fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2, legend_name='Average Distance in Miles', highlight=True)
map


#calculate the average distance per borough per year and plot it
borough_distance = overall_data.groupby(['PUBorough', 'year'])['trip_distance'].mean()
borough_distance = borough_distance.reset_index()
borough_distance = borough_distance.pivot(index='PUBorough', columns='year', values='trip_distance')
borough_distance.plot(kind='bar', title='Average Distance by Borough by Year', ylabel='Distance in Miles')
#make the graph wider
plt.gcf().set_size_inches(25, 5)



#average tip amount per borough
borough_tip = overall_data[overall_data['PUBorough'] != 'EWR']
borough_tip = overall_data.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip


#average tip amount in 2020
borough_tip_2020 = overall_data[overall_data['year'] == 2020]
borough_tip_2020 = borough_tip_2020.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2020


#average tip amount in 2019
borough_tip_2019 = overall_data[overall_data['year'] == 2019]
borough_tip_2019 = borough_tip_2019.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2019


#average tip amount in 2021
borough_tip_2021 = overall_data[overall_data['year'] == 2021]
borough_tip_2021 = borough_tip_2021.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2021


#average tip amount in 2022
borough_tip_2022 = overall_data[overall_data['year'] == 2022]
borough_tip_2022 = borough_tip_2022.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2022


#plot the change in average tip amount per borough from 2019 to 2020
fig, ax = plt.subplots()
borough_tip_2019.plot(title='Average Tip Amount by Borough', color='blue', ax=ax)
borough_tip_2020.plot(title='Average Tip Amount by Borough', color='red', ax=ax)
borough_tip_2021.plot(title='Average Tip Amount by Borough', color='green', ax=ax)
borough_tip_2022.plot(title='Average Tip Amount by Borough', color='orange', ax=ax)
ax.legend(['2019', '2020', '2021', '2022'])



#display the map in a panel with the other plots

fig, ax = plt.subplots(2, 2, figsize=(30, 20))
passenger_count.plot(kind='bar', title='Average Passenger Count by Year', color='blue', ax=ax[0,0], xlabel='Year', ylabel='Passenger Count')
borough_distance.plot(kind='bar', title='Distance Traveled', colormap='Paired', ax=ax[0,1], xlabel='Borough', ylabel='Distance in Miles')
borough_tip_2019.plot(title='Average Tip Amount by Borough', color='blue', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2020.plot(title='Average Tip Amount by Borough', color='red', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2021.plot(title='Average Tip Amount by Borough', color='green', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2022.plot(title='Average Tip Amount by Borough', color='orange', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
cash_2019.plot(title='Cash  vs. Credit Payments', color='red', ax=ax[1,1], ylabel='Number of Payments', xlabel='Year')
credit_2019.plot(title='Cash  vs. Credit Payments', color='blue', ax=ax[1,1], ylabel='Number of Payments', xlabel='Year')
ax[0,0].legend(['Average Passenger Count'])
ax[0,1].legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fancybox=True, shadow=True, title='Borough', title_fontsize='large',    borderpad=1, labelspacing=1, handlelength=1, handletextpad=1, borderaxespad=1, columnspacing=1)
ax[1,0].legend(['2019', '2020', '2021', '2022'])
ax[1,1].legend(['Cash', 'Credit Card'])



for container in ax[0,0].containers:
    ax[0,0].bar_label(container, label_type='edge', fmt='%.2f')