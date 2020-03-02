import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
st.title('Performance Result Analysis')

# read the data from csv file


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a csv file', filenames)
    return os.path.join(folder_path, selected_filename)


filename = file_selector()
st.write('You selected `%s`' % filename)


@st.cache(allow_output_mutation=True)
def get_data():
    data = pd.read_csv(filename)
    return data


data_load_state = st.text('Loading data...')
df = get_data()
data_load_state.text('')

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
