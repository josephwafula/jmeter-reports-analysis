import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Performance Result Analysis')


# read the data from csv file
def file_selector():
    uploaded_file = st.file_uploader("Choose an image...", type=['csv', 'jtl'])
    if uploaded_file is not None:
        return uploaded_file


filename = file_selector()


def get_data():
    if filename is None:
        st.warning('No file selected.')
        column_names = ['timeStamp', 'elapsed', 'responseCode', 'threadName', 'success', 'allThreads']
        data = pd.DataFrame(columns=column_names)
    else:
        data = pd.read_csv(filename)
    return data


# data_load_state = st.text('Loading data...')
df = get_data()
# data_load_state.text('')

# create copy of data for later
origin_df = df

# convert timestamp
df = df.set_index(['timeStamp'])
df.index = pd.to_datetime(df.index, unit='ms')

# re-sample data every 15 seconds
df = df.resample('15S').mean()

# get throughput
df['throughput'] = df['allThreads'] / df['elapsed'] * 1000

# get all the failed requests
df['errors'] = np.where(df['success'] == 'false', '1', '0')

# convert everything to int
df[['throughput', 'elapsed', 'errors']] = df[['throughput', 'elapsed', 'errors']].astype(int)

# multiple line plot
columns = st.multiselect(
    label='What column to you want to display', options=df.columns)

# st.write(df[columns])
st.line_chart(df[columns])

if st.checkbox('Show response time scatter chart'):

    # create figure using plotly express
    origin_df['timeStamp'] = pd.to_datetime(origin_df['timeStamp'], unit='ms')
    fig = px.scatter(origin_df, x='timeStamp', y='elapsed', color='elapsed')

    # Plot!
    st.plotly_chart(fig)
