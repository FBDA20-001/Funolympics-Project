# Importing necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Olympics Broadcast Dashboard",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Olympics dataset
df = pd.read_csv('Olympics.csv')

st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"],
[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}
</style>
""")



# Sidebar
with st.sidebar:
    st.title('Olympics Broadcast Dashboard')

    sports_list = df['Sport'].unique().tolist()
    selected_sport = st.selectbox('Select a sport', sports_list)
    
    country_list = df['country'].unique().tolist()
    selected_country = st.selectbox('Select a country', country_list)

# Plots
# Visualization of average viewership per continent per sportcode
@st.cache_data
def average_viewership_per_continent():
    avg_viewership = df.groupby(['continent', 'Sport']).size().reset_index(name='Viewership')  # Perform count
    return avg_viewership

avg_viewership_data = average_viewership_per_continent()
avg_viewership_fig = px.bar(avg_viewership_data, x='Sport', y='Viewership', color='continent',
                            title='Average Viewership per Continent per Sport')

# Visualization of viewership trends over time per continent per sportcode
@st.cache_data
def viewership_trends_over_time():
    viewership_trends = px.line(df, x='Date', y='Sport', color='continent', facet_row='Sport',
                                title='Viewership Trends Over Time per Continent per Sport')
    return viewership_trends

# Visualization of distribution of viewership and Gender per sportcode
@st.cache_data
def viewership_and_gender_distribution():
    viewership_gender = px.histogram(df, x='Sport', color='gender', facet_col='Sport',
                                     title='Distribution of Viewership and Gender per Sport')
    return viewership_gender

# Visualization of viewership by country per sportcode
@st.cache_data
def viewership_by_country():
    viewership_by_country = px.bar(df, x='country', y='Sport', color='Sport',
                                    title='Viewership by Country per Sport')
    return viewership_by_country

# Visualization of relationship between age and viewership per sportcode
@st.cache_data
def age_vs_viewership():
    age_viewership = px.scatter(df, x='Age', y='Sport', color='Sport',
                                title='Relationship between Age and Viewership per Sport')
    return age_viewership

# Visualization of viewership across countries and continent per age
@st.cache_data
def viewership_across_countries_and_continent_per_age():
    viewership_across_countries = px.scatter(df, x='Age', y='Sport', color='continent',
                                             title='Viewership across Countries and Continent per Age')
    return viewership_across_countries

# Visualization of countries on the viewership rates to identify areas of low and high interests
@st.cache_data
def countries_viewership_rates():
    countries_viewership = px.choropleth(df, locations='country', color='Sport', 
                                          title='Viewership Rates by Country',
                                          locationmode='country names')
    return countries_viewership

# Main Panel
st.title('Olympics Broadcast Dashboard')

# Visualizations
st.subheader('Average Viewership per Continent per Sport')
st.plotly_chart(avg_viewership_fig)

st.subheader('Viewership Trends Over Time per Continent per Sport')
st.plotly_chart(viewership_trends_over_time())

st.subheader('Distribution of Viewership and Gender per Sport')
st.plotly_chart(viewership_and_gender_distribution())

st.subheader('Viewership by Country per Sport')
st.plotly_chart(viewership_by_country())

st.subheader('Relationship between Age and Viewership per Sport')
st.plotly_chart(age_vs_viewership())

st.subheader('Viewership across Countries and Continent per Age')
st.plotly_chart(viewership_across_countries_and_continent_per_age())

st.subheader('Viewership Rates by Country')
st.plotly_chart(countries_viewership_rates())

# Custom CSS for responsive layout and styling
st.markdown(
    """
    <style>
    .stPlotlyChart {
        width: 100%;
    }
    .stDataFrame {
        width: 100%;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
