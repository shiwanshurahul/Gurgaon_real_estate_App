
import streamlit as st
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

import warnings

warnings.filterwarnings("ignore")  # Suppress all warnings globally

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

#1. geo map of gurgaon:
st.header('Sector Price per Sqft Geomap')

new_df = pd.read_csv('datasets/data_viz1.csv')

group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

fig = px.scatter_map(
    group_df, 
    lat="latitude", 
    lon="longitude", 
    color="price_per_sqft", 
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire, 
    zoom=10,
    map_style="open-street-map",
    text=group_df.index
)

st.plotly_chart(fig,use_container_width=True)

#2. word cloud of ameneties:
st.header('Features Wordcloud')

feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))   #features str

wordcloud = WordCloud(width = 800, height = 800,
          background_color ='black',
          stopwords = set(['s']),  # Any stopwords you'd like to exclude
          min_font_size = 10).generate(feature_text)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot()

#3. scatter plot -> area vs price:
st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])  #take i/p

if(property_type == 'house'):
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)

#4. pie chart bedroom filter by sector:
st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()   #get unique sector to be selected on UI
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)  #take input

if(selected_sector == 'overall'):
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

#5. side by side boxplot bedroom price:
st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)

#6. displot of price of flat and house:
st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()

st.pyplot(fig3)



