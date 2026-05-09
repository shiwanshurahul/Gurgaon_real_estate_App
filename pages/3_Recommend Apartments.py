
import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

location_df = pickle.load(open('datasets/location_distance.pkl','rb'))

cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))

# TopFacilities -> cosine_sim1
# PriceDetails -> cosine_sim2
# LocationAdvantages -> cosine_sim3

def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    list_of_no = [1,2,3,4,5]
    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'Recommendations': list_of_no
    })
    
    return recommendations_df
    

recommend_properties_with_scores('DLF The Camellias') #functn call

st.title('Select Location and Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list())) #col me landmark ha

radius = st.number_input('Radius in Kms')

if st.button('Search', help='Search Apartments in given radius from the above location', icon=":material/search:"):
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    # apart_dist = []
    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + ' kms')

    # st.radio("Select anyone for recommendation:", apart_dist)
    
st.title('Recommend Apartments')
selected_apartment = st.selectbox('Select an apartment',sorted(location_df.index.to_list())) #idx me apartment ha

if st.button('Recommend', help='Display Apartments similar to the selected one.', icon=":material/apartment:"):
    recommendation_df = recommend_properties_with_scores(selected_apartment)

    st.dataframe(recommendation_df)