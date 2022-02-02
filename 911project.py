import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('911.csv')
df.info()
print(df.head())

#What are the top 5 zipcodes for 911 calls?
print(df['zip'].value_counts().head(5))
#What are the top 5 townships (twp) for 911 calls?
print(df['twp'].value_counts().head(5))
#Take a look at the 'title' column, how many unique title codes are there?
print(df['title'].nunique())

#In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic.
#Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.

def titleToReason(title): #my answer
    if title[0] == 'E':
        return 'EMS'
    elif title[0]=='T':
        return 'Traffic'
    else:
        return 'Fire'

df['Reason'] = df['title'].apply(titleToReason)
print(df['Reason'].value_counts())

#book answer: df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])

# Now use seaborn to create a countplot of 911 calls by Reason.
sns.countplot(x='Reason',data=df)
plt.show()

#Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column?
print(type(df['timeStamp'].iloc[0]))
#You should have seen that these timestamps are still strings. Use pd.to_datetime to convert the column from strings to DateTime objects.
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
#You can now grab specific attributes from a Datetime object by calling them. For example:
time = df['timeStamp'].iloc[0]
time.hour
#Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Hour, Month, and Day of Week.
#You will create these columns based off of the timeStamp column, reference the solutions if you get stuck on this step.
print(df['timeStamp'][0])

df['Hour'] = df['timeStamp'].apply(lambda date: date.hour)
df['Month'] = df['timeStamp'].apply(lambda date: date.month)
df['Day of Week'] = df['timeStamp'].apply(lambda date: date.isoweekday())
print(df['Hour'])
print(df['Month'])
print(df['Day of Week'])
#Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week
dmap = {1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat',7:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)
print(df['Day of Week'])

#Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column.
sns.countplot(x='Day of Week',hue='Reason',data=df)
plt.tight_layout()
plt.show()
#Now do the same for Month
sns.countplot(x='Month',hue='Reason',data=df)
plt.tight_layout()
plt.show()

#Now create a groupby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame.
byMonth = df.groupby('Month').count()
print(byMonth.head())

#Now create a simple plot off of the dataframe indicating the count of calls per month.
byMonth['twp'].plot()
plt.show()

#Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column.
sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())
plt.show()

#Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method.
df['Date'] = df['timeStamp'].apply(lambda date: date.date())
print(df['Date'])

#Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls
byDate = df.groupby('Date').count()['twp'].plot()
plt.show()

# Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.show()

df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()
plt.show()

df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()
plt.show()

#Now let's move on to creating heatmaps with seaborn and our data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week.
dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
print(dayHour.head())

#Now create a HeatMap using this new DataFrame.
sns.heatmap(dayHour,cmap='viridis')
plt.show()

#Now create a clustermap using this DataFrame
sns.clustermap(dayHour,cmap='viridis')
plt.show()

#Now repeat these same plots and operations, for a DataFrame that shows the Month as the column.
dayMonth = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
sns.heatmap(dayMonth,cmap='viridis')
plt.show()
sns.clustermap(dayMonth,cmap='viridis')
plt.show()
