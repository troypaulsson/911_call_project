import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reads and takes a quick look at the data
df = pd.read_csv('911.csv')
df.info()
print(df.head())

# Prints the top 5 zip codes, the top 5 townships, and the number of unique titles 
print(df['zip'].value_counts().head(5))
print(df['twp'].value_counts().head(5))
print(df['title'].nunique())

# A function that takes the title of the call, finds the main reason, and returns it
# Another answer I found later : df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
def titleToReason(title): #my answer
    if title[0] == 'E':
        return 'EMS'
    elif title[0]=='T':
        return 'Traffic'
    else:
        return 'Fire'
    
# Adds it to a new column titled Reason and counts occurences of each reason
df['Reason'] = df['title'].apply(titleToReason)
print(df['Reason'].value_counts())

# Creates a countplot of 911 calls by 'Reason' column
sns.countplot(x='Reason',data=df)
plt.show()

# Finds data type of objects in 'timeStamp' column
print(type(df['timeStamp'].iloc[0]))

# Uses pd.to_datetime() method to convert the column from strings to DateTime objects.
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Uses lambda expressions and the .apply() method to create 3 new columns called Hour, Month, and Day of Week, based off of the timeStamp column
df['Hour'] = df['timeStamp'].apply(lambda date: date.hour)
df['Month'] = df['timeStamp'].apply(lambda date: date.month)
df['Day of Week'] = df['timeStamp'].apply(lambda date: date.isoweekday())
print(df['Hour'])
print(df['Month'])
print(df['Day of Week'])

# Converts the days of the week from numbers to names using a dictionary and the .map() method
dmap = {1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat',7:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)
print(df['Day of Week'])

# Creates a countplot of the 'Day of Week' and 'Month' columns with the hue based off of the Reason column
sns.countplot(x='Day of Week',hue='Reason',data=df)
plt.tight_layout()
plt.show()
sns.countplot(x='Month',hue='Reason',data=df)
plt.tight_layout()
plt.show()

# Creates a groupby object called byMonth, grouped by the 'Month' column and aggregated using the .count() method
byMonth = df.groupby('Month').count()
print(byMonth.head())

# Creates a simple plot indicating the count of calls per month.
byMonth['twp'].plot()
plt.show()

# Resets the index of byMonth and creates a linear fit on the number of calls per month
sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())
plt.show()

# Creates a new column called 'Date' that contains the date from the timeStamp column, using a lambda expression and .date()
df['Date'] = df['timeStamp'].apply(lambda date: date.date())
print(df['Date'])

# Creates a plot after grouping by date and aggregating with .count()
byDate = df.groupby('Date').count()['twp'].plot()
plt.show()

# Creates three plots grouped by date, and separated by the reason of the call
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

# Restructures the dataframe so that the columns become the Hours and the Index becomes the Day of the Week
dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
print(dayHour.head())

# Creates a HeatMap using the new dataframe
sns.heatmap(dayHour,cmap='viridis')
plt.show()

# Creates a clustermap
sns.clustermap(dayHour,cmap='viridis')
plt.show()

# Repeats the last three steps but uses the 'Month' as the column
dayMonth = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
sns.heatmap(dayMonth,cmap='viridis')
plt.show()
sns.clustermap(dayMonth,cmap='viridis')
plt.show()
