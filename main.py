# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration

st.set_page_config(page_title= "Airbnb Data Visualization | By Rafadh Rafeek",
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                  )


# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("Enter your connection string")
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('data.csv')


st.sidebar.title("Airbnb Data Visualization")
st.sidebar.text("By Rafadh Rafeek")
country = st.sidebar.selectbox('Select a Country',sorted(df.Country.unique()))
df_country = df[df['Country']==country]
room = st.sidebar.selectbox('Select Room_type',sorted(df_country.Room_type.unique()))
df_room = df_country[df_country['Room_type']==room]
prop = st.sidebar.multiselect('Select Property_type',sorted(df_room.Property_type.unique()),sorted(df_room.Property_type.unique()))
price = st.sidebar.slider('Select Price',df_country.Price.min(),df_country.Price.max(),(df_country.Price.min(),df_country.Price.max()))


#quaries
query = f'`Property_type` in {str(prop)} & `Price` >= {price[0]} & `Price` <= {price[1]}'
query1 = f'`Property_type` in {str(prop)}'


#------------------------------------genearal geo location-----------------
geo1_df = df.groupby(['Country']).size().reset_index(name="Total_Listings")
geo1_df.index += 1
fig = px.choropleth(geo1_df,
                    title='Total Listings by Country',
                    locations='Country',
                    locationmode='country names',
                    color='Total_Listings',
                    color_continuous_scale=px.colors.sequential.Blackbody
                    )
st.plotly_chart(fig,use_container_width=True)
st.write(geo1_df)


#------------------------------------Availablity by Property barchart-----------------
st.divider()

df1 = df_country.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)



fig = px.bar(df1,
            title='Availablity by Property Types',
            x='Listings',
            y='Property_type',
            orientation='h',
            color='Property_type',
            color_continuous_scale=px.colors.sequential.Agsunset)
st.plotly_chart(fig,use_container_width=True)
st.write(df1)

#------------------------------------pie chart-----------------
st.divider()
df3 = df_country.groupby(["Property_type"]).size().reset_index(name="counts")
fig = px.pie(df3,
            title='Total Listings of  each Property Types by Country',
            names='Property_type',
            values='counts',
            color_discrete_sequence=px.colors.sequential.Rainbow
                )
fig.update_traces(textposition='outside', textinfo='value+label')
st.plotly_chart(fig,use_container_width=True)


#------------------------------------property type geo-----------------
st.divider()

geo2_df =  df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
geo2_df.index += 1
fig = px.choropleth(geo2_df,
                    title='Property Type Availablity by Country',
                    locations='Country',
                    locationmode='country names',
                    color='Total_Listings',
                    color_continuous_scale=px.colors.sequential.Plasma
                    )
st.plotly_chart(fig,use_container_width=True)
st.write(geo2_df)


#------------------------------------price comparison barchart-----------------
st.divider()

df2 = df_country.groupby(["Property_type"])['Price'].mean().reset_index(name="Average_Price").sort_values(by='Average_Price',ascending=False)
fig2 = px.bar(df2,
        title='Price Comparison by Property Type',
        x='Property_type',
        y='Average_Price',
        color='Property_type',
        color_continuous_scale=px.colors.sequential.Agsunset)
st.plotly_chart(fig2,use_container_width=True)


#------------------------------------availability geoloc-----------------
st.divider()

country_df = df.groupby('Country',as_index=False)['Availability_365'].mean()
country_df.Availability_365 = country_df.Availability_365.astype(int)
fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color= 'Availability_365', 
                                    hover_data=['Availability_365'],
                                    locationmode='country names',
                                    size='Availability_365',
                                    title= 'Avg Availability in each Country',
                                    color_continuous_scale='agsunset'
                        )
st.plotly_chart(fig,use_container_width=True)



#------------------------------------location by cordinates-----------------

location_df = df[df['Country']==country]
continent_mapping = {
    'Australia': 'world',
    'Brazil': 'south america',
    'Canada': 'north america',
    'China': 'asia',
    'Portugal': 'europe',
    'Turkey': 'asia',
    'United States': 'usa',
    'Spain': 'europe',
    'Hong Kong': 'asia'
}

fig_5 = px.choropleth(data_frame=location_df,
                                    locationmode='country names',
                                    title= 'Exact Location By Property Type',
                                    scope=continent_mapping[country]
                        )
x = 0
while True:
        try:
                fig_5.add_trace(
                px.scatter_geo(
                        data_frame=location_df,
                        lat='Latitude',  # Column name for latitude
                        lon='Longitude',  # Column name for longitude
                        color='Property_type',
                        hover_data=['Price']
                ).data[x]
                )
                x += 1
        except:
                break

st.plotly_chart(fig_5,use_container_width=True)












