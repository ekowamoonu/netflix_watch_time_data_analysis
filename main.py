import pandas as pd
import requests
from io import StringIO

import matplotlib

# fetch csv from URL provided in demo
url = 'https://www.dataquest.io/wp-content/uploads/2020/11/ViewingActivity-sample.csv'
response = requests.get(url)

# StringIO converts response text into a file-like object
data = StringIO(response.text)

# get all columns to display in terminal
pd.options.display.max_columns = None

df = pd.read_csv(data)

# We only want to know how much we have watched of a certain movie and when so we drop all unecessary columns to keep things cleaner
df = df.drop(
    ['Profile Name', 'Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'],
    axis=1)

""" 
All three remaining columns after dropping are strings. That's okay for the Title column but we need to change the two time related
columns to their correct datatypes before we can work with them
So we convert:
1. Convert Start Time -> datetime
2. Convert Start Time from UTC -> to our local timezone (My timezone is UTC so I'll leave this as it is since its the default format from Netflix)
3. Convert Duration to timedelta (a time duration format pandas can understand and perform calculations with)
"""

df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)

#Now, doing a df.dtypes print out shows that Start Time is now in UTC datetime format
#If you need to convert to another Timezone, you can follow th commented code below to do the appropriate conversions

"""
#change the Start Time column into the dataframe's index
df = df.set_index('Start Time')

#convert from UTC timezone to your timezone
df.index = df.index.tz_convert('Your timezone')

#reset the index so that Start Time becomes a column again
df = df.reset_index()
"""

df['Duration'] = pd.to_timedelta(df["Duration"])

#Next, we are going to filter the Title column so that we can analyze only views of 'The Office'
#There way will approach it in this tutorial is to create a new dataframe and populate it with only rows where the Title
#contains 'The Office (U.S)'

#regex=False tells the function that the previous argument is a string not a regex expression
office = df[df['Title'].str.contains('The Office (U.S.)', regex=False)]

"""
To test if the new dataframe we have created is actually correct, we can sample X number of rows from the 
dataframe and check if all rows contain 'The Office'

print(office.sample(20))
"""

"""
Next, we know that, those short episode seconds previews on Netflix actually count into your watching time. So we will further
sort our dataframe to only include rows where the Duration is at least 1 minute
"""

office = office[office["Duration"] > '0 days 00:01:00']

"""
Now to the fun part of analyzing the data.
How much time have I spent watching The Office?
"""

total_time_spent = office['Duration'].sum()
print(total_time_spent)

"""
On which days of the week have I watched the most Office episodes?
During which hours of the day do I most often start Office episodes?
"""

office['Weekday'] = office['Start Time'].dt.weekday
office['Hour'] = office['Start Time'].dt.hour


"""
Time to do generate some nice charts. We will use matplotlib
- Total number of hours of movies watched
- Days I watch Netflix the most
- Longest movies I have watched
"""

%matplotlib inline