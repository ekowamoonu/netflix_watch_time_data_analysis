import pandas as pd
import requests
from io import StringIO

import matplotlib.pyplot as plt

"""
You can either fetch your ViewingActivityCSV from your own URL or from your local.
# fetch csv from URL 
# StringIO converts response text into a file-like object
# get all columns to display in terminal
"""

url = 'https://yoururl.csv'
response = requests.get(url)
data = StringIO(response.text)
pd.options.display.max_columns = None

#df = pd.read_csv(data) OR
df = pd.read_csv("ViewingActivity.csv")  #from local

""" 
We only want to know how much we have watched of a certain movie and when so we drop all unecessary columns in dataframe to keep things cleaner.
All three remaining columns after dropping are strings. That's okay for the Title column but we need to change the two time related
columns to their correct datatypes before we can work with them
So we convert:
1. Convert Start Time -> datetime
2. Convert Start Time from UTC -> to our local timezone (My timezone is UTC so I'll leave this as it is since its the default format from Netflix)
3. Convert Duration to timedelta (a time duration format pandas can understand and perform calculations with)
"""

df = df.drop(
    ['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'],
    axis=1)

df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)


"""
#Now, doing a df.dtypes print out shows that Start Time is now in UTC datetime format
#If you need to convert to another Timezone, you can follow the commented code below to do the appropriate conversions

#change the Start Time column into the dataframe's index
df = df.set_index('Start Time')

#convert from UTC timezone to your timezone
df.index = df.index.tz_convert('Your timezone')

#reset the index so that Start Time becomes a column again
df = df.reset_index()
"""

df['Duration'] = pd.to_timedelta(df["Duration"])

"""
#Next, we are going to filter the Title column so that we can analyze only views belonging to my profile "Ekow". 
#There way will approach it is to create a new dataframe and populate it with only rows where the Title
#contains the profile name 'Ekow'

#regex=False tells the function that the previous argument is a string not a regex expression
"""

movie = df[df['Profile Name'].str.contains('Ekow', regex=False)]

"""
To test if the new dataframe we have created is actually correct, we can sample X number of rows from the 
dataframe: 
print(movie.sample(20))

Next, we know that, those short episode seconds previews on Netflix actually count into your watching time. So we will further
sort our dataframe to only include rows where the Duration is at least 1 minute
"""

movie = movie[movie["Duration"] > '0 days 00:01:00']
total_time_spent = movie['Duration'].sum()

movie['Weekday'] = movie['Start Time'].dt.strftime('%A')
movie['Hour'] = movie['Start Time'].dt.hour

"""
Time to do generate some nice charts. We will use matplotlib
"""

"""
Viewing hours categorised for each day of the week ---------------------------------------------------------------------
"""
movie['Weekday'] = pd.Categorical(movie['Weekday'], categories = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

#create movie_by_day and count the rows for each weekday, assigning the result to the variable
movie_by_day = movie['Weekday'].value_counts()

#sort
movie_by_day = movie_by_day.sort_index()

#optional: Increase font size of chart
plt.rcParams.update({'font.size':16})

movie_by_day.plot(kind='bar', figsize=(10,5), title=f'Total Number of Watch Hours By Day ({total_time_spent} in total)')
plt.subplots_adjust(bottom=0.22)
plt.xticks(rotation=45)
plt.show()


"""
Time of the day I have watched the most movies -------------------------------------------------------------------------
"""
movie['Hour'] = pd.Categorical(movie['Hour'],categories=list(range(24)), ordered=True)
movie_by_hour = movie['Hour'].value_counts()
movie_by_hour = movie_by_hour.sort_index()
movie_by_hour.plot(kind='bar', figsize=(20,10), title='Movies Watched By The Hour')
plt.show()
