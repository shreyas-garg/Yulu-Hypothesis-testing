# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ePoJndLbrRTkFKOQKcO4Uw1P8ssIzqU8

##Yulu - Hypothesis Testing
About Yulu
Yulu is India’s leading micro-mobility service provider, which offers unique vehicles for the daily commute. Starting off as a mission to eliminate traffic congestion in India, Yulu provides the safest commute solution through a user-friendly mobile app to enable shared, solo and sustainable commuting.

Yulu zones are located at all the appropriate locations (including metro stations, bus stands, office spaces, residential areas, corporate offices, etc) to make those first and last miles smooth, affordable, and convenient!

Yulu has recently suffered considerable dips in its revenues. They have contracted a consulting company to understand the factors on which the demand for these shared electric cycles depends. Specifically, they want to understand the factors affecting the demand for these shared electric cycles in the Indian market.

Problem Statement
The company wants to know:

Which variables are significant in predicting the demand for shared electric cycles in the Indian market?

How well those variables describe the electric cycle demands
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import scipy.stats as spy

dataset = pd.read_csv(r"https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/428/original/bike_sharing.csv?1642089089")

dataset.shape

dataset.columns

dataset.head()

dataset.tail()

dataset.dtypes

dataset.isnull().sum()

for i in dataset.columns:
  print(i, ':', dataset[i].nunique())

"""Season, holiday, working day, and weather represent categorical or discrete variables. In contrast, the remaining features such as temperature, 'feels like' temperature, humidity, wind speed, and the counts of casual, registered, and total bike rentals are continuous variables."""

dataset.describe()

"""1.Half of the dataset entries were logged during autumn, while approximately three-quarters were recorded in winter, with fewer entries in summer.

2.Holiday-related data is minimally present in the dataset.

3.About half of the entries are categorized as non-working days.

4.Cloudy days dominate the weather data, constituting approximately 75% of the dataset, while clear or partially cloudy days make up around 50%.

5.The median temperature recorded is 20.5 degrees Celsius, with three-quarters of the data showing temperatures up to 26.24 degrees Celsius.

6.The 'feels like' temperature has a median of 24.24 degrees Celsius, with 75% of readings reaching up to 31.06 degrees Celsius.

7.Humidity levels have a median of 62%, with three-quarters of the entries recording up to 77% humidity.

8.Wind speeds in the dataset have a median of 12.998, with the upper three-quarters reaching up to 16.997.

9.Casual user data indicates a median of 17 users, with the 75th percentile at 49 users, and an average of 36.02 users, peaking at 367.

10.Registered user counts show a median of 118, with the upper quartile reaching up to 222 users, averaging at 155.552 users, with a maximum of 886.

11.Combined casual and registered users have a median count of 145, with the 75th percentile at 284, and an average of 191.574 users, with the maximum at 977.
"""

dataset['season'].value_counts(normalize=True)

dataset['holiday'].value_counts(normalize=True)

dataset['workingday'].value_counts(normalize=True)

dataset['weather'].value_counts(normalize=True)

dataset['temp'].describe()

"""The mean temperature across the dataset is 20.23 degrees Celsius, with the median temperature also being 20.5 degrees Celsius.
Temperatures ranged from a low of 0.82 degrees Celsius up to a high of 41 degrees Celsius.
"""

dataset['windspeed'].describe()

dataset['humidity'].describe()

dataset['casual'].describe()

dataset['registered'].describe()

dataset['count'].describe()

dataset.groupby(by='season')['holiday'].sum().sort_values(ascending=False)

dataset.groupby(by='season')['workingday'].sum().sort_values(ascending=False)

dataset.groupby(by='season')['temp'].describe()

dataset.groupby(by='season')['atemp'].describe()

dataset.groupby(by='season')['humidity'].describe()

dataset.groupby(by='season')['windspeed'].describe()

dataset.groupby(by='season')['registered'].describe()

dataset.groupby(by='season')['count'].describe()

dataset.groupby(by='weather')['registered'].describe()

dataset.groupby(by='weather')['count'].describe()

dataset_copy = dataset.copy()

plt.figure(figsize=(15,8))
sns.countplot(data=dataset, x='season', palette="Set2")
plt.show()

plt.figure(figsize=(15,8))
sns.countplot(data=dataset, x='holiday', palette="twilight")
plt.show()

plt.figure(figsize=(15,8))
sns.countplot(data=dataset, x='workingday', palette="Set3")
plt.show()

plt.figure(figsize=(15,8))
sns.countplot(data=dataset, x='weather', palette="Set1")
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='temp', palette="twilight", aspect=2, color="m")
plt.axvline(x=dataset['temp'].mean(), linestyle=":", color='g', label="temp_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='atemp', palette="twilight", aspect=2, color="brown")
plt.axvline(x=dataset['atemp'].mean(), linestyle=":", color='g', label="atemp_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='windspeed', palette="twilight", aspect=2, color="b")
plt.axvline(x=dataset['windspeed'].mean(), linestyle=":", color='g', label="windspeed_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='humidity', palette="twilight", aspect=2, color="r")
plt.axvline(x=dataset['humidity'].mean(), linestyle=":", color='g', label="humidity_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='casual', palette="twilight", aspect=2, color="b")
plt.axvline(x=dataset['casual'].mean(), linestyle=":", color='g', label="casual_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='registered', palette="twilight", aspect=2, color="m")
plt.axvline(x=dataset['registered'].mean(), linestyle=":", color='g', label="registered_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(15,8))
sns.displot(data=dataset, x='count', palette="twilight", aspect=2, color="black")
plt.axvline(x=dataset['count'].mean(), linestyle=":", color='g', label="count_mean", alpha=0.9)
plt.legend()
plt.show()

plt.figure(figsize=(20,8))
sns.ecdfplot(data=dataset, x="casual", palette="copper", legend=True, label="casual")
sns.ecdfplot(data=dataset, x="registered", palette="copper", legend=True, label="registered")
sns.ecdfplot(data=dataset, x="count", palette="copper", legend=True, label="count")
plt.legend()
plt.title("CDF of Casual, Registered and Count")

plt.figure(figsize=(20,8))
categorical_columns = ['season', 'holiday', 'workingday', 'weather']

fig, ax = plt.subplots(2, 2, figsize=(23, 12))
axes = ax.ravel()

for index, column in enumerate(categorical_columns):
  sns.boxplot(data=dataset, x=column, y="count", palette="terrain", ax=axes[index])
  axes[index].set_title(f"Demand of total vechiles by {column}", )



"""##Season
The median demand in the summer, fall, and winter seasons is nearly identical, while the median is very low in the spring season.

The outliers in countable demand can be seen for all the seasons, probably lot of outliers in spring season. All the outliers are in the upper range of Inter Quartile Range (IQR).

##Holiday
The median counted demand is nearly identical during holidays and non-holidays.

There are no outliers in the counted demand for holidays, whereas there are outliers in the non-holiday demand, and that too, in the upper Inter Quartile Range (IQR).

##workingday
The median difference between a working day and a non-working day is only marginally significant.

There are outliers in vehicle demand on working and non-working days.

##Weather
For clear/few clouds and misty/cloudy conditions, the median demand for counted vehicles is nearly identical.

The demand for counted vehicles during light snow/light rain is less than during clear and mist conditions.

There is only one data point for heavy rain and thunder storms, which makes sense as nobody would prefer to ride in these heavy conditions.

There are outliers in the upper IQR for all the conditions, except heavy rain.
"""

categorical_columns = ['season', 'holiday', 'workingday', 'weather']

fig, ax = plt.subplots(2, 2, figsize=(23, 12))
axes = ax.ravel()

for index, column in enumerate(categorical_columns):
  sns.boxplot(data=dataset, x=column, y="registered", palette="ocean", ax=axes[index])
  axes[index].set_title(f"Demand of registered vechiles by {column}", )

categorical_columns = ['season', 'holiday', 'workingday', 'weather']

fig, ax = plt.subplots(2, 2, figsize=(23, 12))
axes = ax.ravel()

for index, column in enumerate(categorical_columns):
  sns.boxplot(data=dataset, x=column, y="casual", palette="Pastel1", ax=axes[index])
  axes[index].set_title(f"Demand of casual vechiles by {column}", )

continous_columns = ['casual', 'registered', 'count']

sns.relplot(data=dataset, x="temp", y="casual", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between casual vechile demand and temperature")

"""Casual vehicle demand is linear beginning at 5 degrees Celsius and peaks at 35 and 40 degrees Celsius."""

sns.relplot(data=dataset, x="temp", y="registered", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between registered vechile demand and temperature")

sns.relplot(data=dataset, x="temp", y="count", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between counted vechile demand and temperature")

sns.relplot(data=dataset, x="windspeed", y="casual", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between casual vechile demand and windspeed")

sns.relplot(data=dataset, x="windspeed", y="registered", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between registered vehicle demand and windspeed")

sns.relplot(data=dataset, x="windspeed", y="count", palette="tab10", kind='line', aspect=3)
plt.title("Relationship between counted vehicle demand and windspeed")

days = ['workingday', 'holiday']

fig, ax = plt.subplots(1, 2, figsize=(30, 8))
axes = ax.ravel()

for index, day in enumerate(days):
  sns.pointplot(x="season", y="count", hue=day, data=dataset, palette="seismic", ax=axes[index])
  axes[index].set_title(f"Total vechile demand curve for {day} for different season w.r.t count")

days = ['workingday', 'holiday']

fig, ax = plt.subplots(1, 2, figsize=(30, 8))
axes = ax.ravel()
for index, day in enumerate(days):
  sns.pointplot(x="weather", y="count", hue=day, data=dataset, palette="inferno", ax=axes[index])
  axes[index].set_title(f"Total vechile demand curve for {day} for different season w.r.t count")

"""Working Day -
The total demand for vehicles is drastically reduced from clear skies to cloudy mist and is further reduced to light snow or light rain for both working and non-working days.

Holiday -
The total demand curve is increasing from clear skies to cloudy mist and is reduced in light snow or light rain.

The graph shows an interesting contrast between clear skies and cloudy mist during holidays and non-holidays.*italicised text*
"""

from scipy.stats import ttest_ind

working_day_count = dataset[(dataset['workingday'] == 1)]['count']
non_working_day_count = dataset[(dataset['workingday'] == 0)]['count']

t_stat, p_value = np.round(ttest_ind(working_day_count, non_working_day_count, random_state=42), 2)
print(f"T-test statistic is {t_stat} and p_value is {p_value}")

"""##Conclusion

This results in a p-value of 0.23, which is below the defined significance level of 5%. The T-test is therefore not significant and the NULL HYPOTHESIS is CONFIRMED.

##Analysis of Variance (ANOVA)

To check if No. of cycles rented is similar or different in different

Weather
Season

##Assumptions
The samples are independent.

Each sample is from a normally distributed population.

The population standard deviations of the groups are all equal. This property is known as homoscedasticity.
"""

from scipy.stats import f_oneway


spring_season = dataset[dataset['season'] == 1]['count']
summer_season = dataset[dataset['season'] == 2]['count']
fall_season = dataset[dataset['season'] == 3]['count']
winter_season = dataset[dataset['season'] == 4]['count']

f_stat, p_value = f_oneway(spring_season, summer_season, fall_season, winter_season)
print(f"F-test statistic is {f_stat} and p_value is {p_value}")

fig, ax = plt.subplots(1, 4, figsize=(25, 6))
axes = ax.ravel()

seasons = [1, 2, 3, 4]
colors = ['r','g','b','m']
for index, season in enumerate(seasons):
  sns.histplot(dataset[dataset['season'] == season]['count'], ax=axes[index], kde=True, color=colors[index], label=f'weather_{season}', )
  axes[index].legend()

from scipy.stats import boxcox

season_1_transformed = boxcox(dataset[dataset['season'] == 1]['count'])
season_2_transformed = boxcox(dataset[dataset['season'] == 2]['count'])
season_3_transformed = boxcox(dataset[dataset['season'] == 3]['count'])
season_4_transformed = boxcox(dataset[dataset['season'] == 4]['count'])

fig, ax = plt.subplots(1, 4, figsize=(27, 6))
axes = ax.ravel()

transformed_seasons = [season_1_transformed, season_2_transformed, season_3_transformed, season_4_transformed]
colors = ['r','g','b', 'm']
for index, season in enumerate(transformed_seasons):
  sns.histplot(season[0], ax=axes[index], kde=True, color=colors[index], label=f'season_{index}_transformed', )
  axes[index].legend()

weather_1 = dataset[dataset['weather'] == 1]['count']
weather_2 = dataset[dataset['weather'] == 2]['count']
weather_3 = dataset[dataset['weather'] == 3]['count']
weather_4 = dataset[dataset['weather'] == 4]['count']


fig, ax = plt.subplots(1, 4, figsize=(25, 6))
axes = ax.ravel()

weathers = [1, 2, 3, 4]
colors = ['r','g','b','m']
for index, weather in enumerate(weathers):
  sns.histplot(dataset[dataset['weather'] == weather]['count'], ax=axes[index], kde=True, color=colors[index], label=f'weather_{weather}', )
  axes[index].legend()

from scipy.stats import boxcox

weather_1_transformed = boxcox(dataset[dataset['weather'] == 1]['count'])
weather_2_transformed = boxcox(dataset[dataset['weather'] == 2]['count'])
weather_3_transformed = boxcox(dataset[dataset['weather'] == 3]['count'])

fig, ax = plt.subplots(1, 3, figsize=(25, 6))
axes = ax.ravel()

transformed_weathers = [weather_1_transformed, weather_2_transformed, weather_3_transformed]
colors = ['r','g','b']
for index, weather in enumerate(transformed_weathers):
  sns.histplot(weather[0], ax=axes[index], kde=True, color=colors[index], label=f'weather_{index}_transformed', )
  axes[index].legend()

"""##Conclusion

This results in a p-value of 3.486e-181, which is below the defined significance level of 5%. The ANNOVA test for weather is therefore significant and the NULL HYPOTHESIS is NOT CONFIRMED.

##x^2 Test

Note: An often quoted guideline for the validity of this calculation is that the test should be used only if the observed and expected frequencies in each cell are at least 5.

##Assumptions Reference

The data in the cells should be frequencies, or counts of cases rather than percentages or some other transformation of the data.

The levels (or categories) of the variables are mutually exclusive.

The study groups must be independent. This means that a different test must be used if the two groups are related.

The value of the cell expecteds should be 5 or more in at least 80% of the cells, and no cell should have an expected of less than one.

##Null Hypothesis:

The impact of weather is independent of seasons.
Alternative Hypothesis:
The impact of weather has a different impact depending on the season.
"""

from scipy.stats.contingency import chi2_contingency


plt.figure(figsize=(18, 5))
contingency_table = pd.crosstab(dataset['season'], dataset['weather'])
values = np.array([contingency_table.iloc[0][:4], contingency_table.iloc[1][:4], contingency_table.iloc[2][:4]])
sns.heatmap(contingency_table, annot=True, fmt='.6g', cmap="gist_stern")
plt.show()

"""##Insights
1.A 2-sample T-test comparing user counts on working versus non-working days suggests no significant difference in average counts between these two categories.

2.ANOVA tests across seasons indicate variations in bike usage, with different seasons showing distinct population means.

4.Another ANOVA test across various weather conditions, excluding one condition, suggests consistent bike usage across different weather conditions.

5.A Chi2 test reveals a relationship between seasonal changes and weather patterns, indicating that weather influences vary with the seasons.

6.The median recorded temperature is 20.5 degrees Celsius, with 75% of temperatures recorded up to 26.24 degrees Celsius, and an average temperature of 20.36 degrees Celsius.

7.The median user count is 145, with 75% of observations below 284 and an average count of 191.574, peaking at 977.

8.Working days constitute 68% of the data, suggesting higher bike usage on these days due to increased public transportation use.

9.Data points during light snow or light rain are scarce, reflecting reduced service use during adverse weather conditions.

10.The mean temperature observed is 20.23 degrees Celsius, occurring 50% of the time as the median value.

11.Strong positive correlations exist between casual and total user counts, as well as between registered users and total counts.

##Recommendations:

1.Offer special promotions or fitness competitions on non-working days and holidays to boost vehicle usage.

2.Introduce biweekly or monthly discounts during low-demand months (January to June) to incentivize more usage.

3.Provide personalized referral discounts based on bike model for first-time users.

4.Attract fitness enthusiasts by offering prizes for using bikes during off-peak hours (midnight to 8 AM).

5.Implement seasonal discounts during the spring to increase bike usage during this period of reduced demand.
"""