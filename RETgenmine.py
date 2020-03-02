from __future__ import division
import pandas as pd
from pylab import *

# read the data from csv file
df = pd.read_csv("Statement.csv", usecols=['timeStamp', 'elapsed', 'allThreads', 'success'])

# convert timestamp
df = df.set_index(['timeStamp'])
df.index = pd.to_datetime(df.index, unit='ms')

# re-sample data per 15 seconds
df = df.resample('15S').mean()

# get throughput
df['throughput'] = df['allThreads'] / df['elapsed'] * 1000

# get all the failed requests
df['errors'] = np.where(df['success'] == 'false', '1', '0')

# convert everything to int
df[['throughput', 'elapsed', 'errors']] = df[['throughput', 'elapsed', 'errors']].astype(int)

# multiple line plot
fig = plt.figure()
fig.show()
ax = fig.add_subplot(111)
ax.plot(df['throughput'], data=df, marker='o', color='green', linewidth=2, label="throughput")
ax.plot(df['elapsed'], data=df, marker='', color='blue', linewidth=2, label="response time")
ax.plot(df['errors'], data=df, marker='', color='red', linewidth=2, linestyle='dashed', label="errors")
plt.xlabel('test duration')
plt.ylabel('TPS/Errors/Responses')
plt.title('Test Summary')
plt.legend()

# print the graph
plt.show()

