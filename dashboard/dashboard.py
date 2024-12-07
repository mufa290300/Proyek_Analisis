import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/mufa290300/Proyek_Analisis/main/dashboard/hour_2.csv")
df['date'] = pd.to_datetime(df['date'])

df.head()

df.info()

st.set_page_config(page_title="Bike Sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "Total_count": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "date": "yearmonth",
        "Total_count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    return monthly_users_df
def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "Total_count": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "Total_count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')

    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])

    seasonly_users_df = seasonly_users_df.sort_values('season')

    return seasonly_users_df
def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "Total_count": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "Total_count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')

    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    weekday_users_df = weekday_users_df.sort_values('weekday')

    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hour").agg({
        "casual": "sum",
        "registered": "sum",
        "Total_count": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "Total_count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    return hourly_users_df

min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar:
  st.image("https://raw.githubusercontent.com/mufa290300/Proyek_Analisis/main/images.png")
  st.sidebar.header("Filter:")
  start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
  )

st.sidebar.header("Nama Lengkap:")

st.sidebar.markdown("Muhamad Fahrudin")

main_df = df[
    (df["date"] >= str(start_date)) &
    (df["date"] <= str(end_date))
]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

st.title(":bar_chart: Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['Total_count'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')
fig2 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by weekday').update_layout(xaxis_title='', yaxis_title='Total Rides')
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig = px.line(hourly_users_df,
              x='hour',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["skyblue", "orange"],
              markers=True,
              title='Count of bikeshare rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
