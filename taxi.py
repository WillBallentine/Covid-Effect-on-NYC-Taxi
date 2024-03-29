
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas as gpd
import folium as fol

overall_data = pd.read_csv('Covid-Effect-on-NYC-Taxi/assets/sample.csv')

overall_data["pickup_datetime"] = pd.to_datetime(overall_data['pickup_datetime'])
overall_data['dropoff_datetime'] = pd.to_datetime(overall_data['dropoff_datetime'])

drop_list = (list(np.where(overall_data['trip_distance'] > 100)))

for i in drop_list:
    overall_data.drop(i, inplace=True)

covid_df  = pd.read_csv('Covid-Effect-on-NYC-Taxi/assets/covidreportsbystate.csv')

covid_df['submission_date'] = pd.to_datetime(covid_df['submission_date'])
covid_df['created_at'] = pd.to_datetime(covid_df['created_at'])

covid_df.drop(columns=['consent_cases', 'consent_deaths', 'prob_cases', 'new_case', 'pnew_case', 'prob_death', 'new_death', 'pnew_death', 'conf_cases', 'conf_death'], inplace=True)

covid_df['year'] = covid_df['submission_date'].dt.year

passenger_count = overall_data.groupby('year')['passenger_count'].mean()
passenger_count.plot(kind='bar', ylabel="Passengers", title='Average Passenger Count by Year', color='blue')


passenger_count_2019 = overall_data[overall_data['year'] == 2019]['passenger_count'].mean()
passenger_count_2020 = overall_data[overall_data['year'] == 2020]['passenger_count'].mean()
passenger_count_2013 = overall_data[overall_data['year'] == 2013]['passenger_count'].mean()

passenger_count_2019, passenger_count_2020, passenger_count_2013

covid_df[covid_df['state'] == 'NY'].plot(kind='area',x='submission_date', y='tot_cases', title='Total Cases in NY', xlabel='Date', ylabel='Total Cases', figsize=(20, 10)).ticklabel_format(style='plain', axis='y')

credit = overall_data[overall_data['payment_type'] == 'credit_card']
credit = credit.groupby('year')['payment_type'].count()


cash = overall_data[overall_data['payment_type'] == 'cash']
cash = cash.groupby('year')['payment_type'].count()


cash_2019 = overall_data[(overall_data['payment_type'] == 'cash') & (overall_data['year'] == 2019)]['payment_type'].count()
print(f"2019 cash payments: {cash_2019}")

credit_2019 = overall_data[(overall_data['payment_type'] == 'credit_card') & (overall_data['year'] == 2019)]['payment_type'].count()
print(f"2019 credit card payments: {credit_2019}")

cash_2020 = overall_data[(overall_data['payment_type'] == 'cash') & (overall_data['year'] == 2020)]['payment_type'].count()
print(f"2020 cash payments: {cash_2020}")

credit_2020 = overall_data[(overall_data['payment_type'] == 'credit_card') & (overall_data['year'] == 2020)]['payment_type'].count()
print(f"2020 credit card payments: {credit_2020}")

cash_2019 / (cash_2019 + credit_2019)

credit_2019 / (cash_2019 + credit_2019)


cash_2020 / (cash_2020 + credit_2020)

credit_2020 / (cash_2020 + credit_2020)

fig, ax = plt.subplots()
credit.plot(title='Credit Card Payments', color='blue', ax=ax)
cash.plot(title='Cash  vs. Credit Payments', color='red', ax=ax)
ax.legend(['Credit Card', 'Cash'])


labels = ['Cash', 'Credit']
sizes = [cash_2019 / (cash_2019 + credit_2019), credit_2019 / (cash_2019 + credit_2019)]
sizes2 = [cash_2020 / (cash_2020 + credit_2020), credit_2020 / (cash_2020 + credit_2020)]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.title('2019 Cash vs. Credit Payments')
plt.show()

fig2, ax2 = plt.subplots()
ax2.pie(sizes2, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax2.axis('equal')
plt.title('2020 Cash vs. Credit Payments')
plt.show()


fare_amount = overall_data.groupby('year')['fare_amount'].mean()
fare_amount.plot(title='Average Fare Amount by Year', color='blue', ylabel='Fare Amount')


fare_amount_2011 = overall_data[overall_data['year'] == 2011]['fare_amount'].mean()
print(f"2011 average fare amount: ${fare_amount_2011:.2f}")

fare_amount_2019 = overall_data[overall_data['year'] == 2019]['fare_amount'].mean()
print(f"2019 average fare amount: ${fare_amount_2019:.2f}")

fare_amount_2020 = overall_data[overall_data['year'] == 2020]['fare_amount'].mean()
print(f"2020 average fare amount: ${fare_amount_2020:.2f}")


fare_amount_2021 = overall_data[overall_data['year'] == 2021]['fare_amount'].mean()
print(f"2021 average fare amount: ${fare_amount_2021:.2f}")


fare_amount = overall_data[overall_data['year'] >= 2019].groupby('year')['fare_amount'].mean()
fare_amount.plot(title='Average Fare Amount by Year', color='blue', ylabel='Fare Amount')
ax = plt.gca()
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.0f}'))



borough_data = pd.read_csv('Covid-Effect-on-NYC-Taxi/assets/taxi_zone_lookup.csv')


borough_data = borough_data[['LocationID', 'Borough']]
borough_data = borough_data.rename(columns={'LocationID': 'PULocationID'})
overall_data = overall_data.merge(borough_data, on='PULocationID', how='left')
overall_data = overall_data.rename(columns={'Borough': 'PUBorough'})

overall_data = overall_data.loc[overall_data['PUBorough'] != 'EWR']
overall_data = overall_data.loc[overall_data['PUBorough'] != 'Unknown']

map_data = overall_data.set_index('PUBorough')
map_data


map = fol.Map(location=[40.7128, -74.0060], zoom_start=10)
map.choropleth(geo_data='Covid-Effect-on-NYC-Taxi/assets/new-york-city-boroughs.geojson', data=overall_data, columns=['PUBorough', 'trip_distance'], key_on='feature.properties.name', fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2, legend_name='Average Distance in Miles', highlight=True, labels='feature.properties.name')
map


borough_distance = overall_data.groupby(['PUBorough', 'year'])['trip_distance'].mean()
borough_distance = borough_distance.reset_index()
borough_distance = borough_distance.pivot(index='PUBorough', columns='year', values='trip_distance')
borough_distance.plot(kind='bar', title='Average Distance by Borough by Year', ylabel='Distance in Miles')

plt.gcf().set_size_inches(25, 5)


borough_tip = overall_data[overall_data['PUBorough'] != 'EWR']
borough_tip = overall_data.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip

borough_tip_2020 = overall_data[overall_data['year'] == 2020]
borough_tip_2020 = borough_tip_2020.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2020


borough_tip_2019 = overall_data[overall_data['year'] == 2019]
borough_tip_2019 = borough_tip_2019.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2019

borough_tip_2021 = overall_data[overall_data['year'] == 2021]
borough_tip_2021 = borough_tip_2021.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2021

borough_tip_2022 = overall_data[overall_data['year'] == 2022]
borough_tip_2022 = borough_tip_2022.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_2022


borough_tip_queens = overall_data[overall_data['PUBorough'] == 'Queens']
borough_tip_queens = borough_tip_queens.groupby(['PUBorough'])['tip_amount'].mean()
borough_tip_queens


tip_change = (borough_tip_2020 - borough_tip_2019) / borough_tip_2019
tip_change = tip_change * 100
tip_change

tot_change = 0

for i in tip_change:
    tot_change += i

tot_change = tot_change / 5
tot_change


fig, ax = plt.subplots()
borough_tip_2019.plot(title='Average Tip Amount by Borough', color='blue', ax=ax)
borough_tip_2020.plot(title='Average Tip Amount by Borough', color='red', ax=ax)
borough_tip_2021.plot(title='Average Tip Amount by Borough', color='green', ax=ax)
borough_tip_2022.plot(title='Average Tip Amount by Borough', color='orange', ax=ax)
ax.legend(['2019', '2020', '2021', '2022'])



fig, ax = plt.subplots(2, 2, figsize=(30, 20))
passenger_count.plot(kind='bar', title='Average Passenger Count by Year', color='blue', ax=ax[0,0], xlabel='Year', ylabel='Passenger Count')
borough_distance.plot(kind='bar', title='Distance Traveled', colormap='Paired', ax=ax[0,1], xlabel='Borough', ylabel='Distance in Miles')
borough_tip_2019.plot(title='Average Tip Amount by Borough', color='blue', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2020.plot(title='Average Tip Amount by Borough', color='red', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2021.plot(title='Average Tip Amount by Borough', color='green', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
borough_tip_2022.plot(title='Average Tip Amount by Borough', color='orange', ax=ax[1,0], xlabel='Borough', ylabel='Tip Amount in USD')
cash.plot(title='Cash  vs. Credit Payments', color='red', ax=ax[1,1], ylabel='Number of Payments', xlabel='Year')
credit.plot(title='Cash  vs. Credit Payments', color='blue', ax=ax[1,1], ylabel='Number of Payments', xlabel='Year')
ax[0,0].legend(['Average Passenger Count'])
ax[0,1].legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fancybox=True, shadow=True, title='Borough', title_fontsize='large',    borderpad=1, labelspacing=1, handlelength=1, handletextpad=1, borderaxespad=1, columnspacing=1)
ax[1,0].legend(['2019', '2020', '2021', '2022'])
ax[1,1].legend(['Cash', 'Credit Card'])



for container in ax[0,0].containers:
    ax[0,0].bar_label(container, label_type='edge', fmt='%.2f')


