import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Real estate App")

with open('datasets/df.pkl','rb') as file:
    df = pickle.load(file)
 
# st.dataframe(df)    
    
with open('datasets/pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)

st.header('Enter your inputs:')

# Property -> str
property_type = st.selectbox('Property Type',['flat','house'])

# sector -> str
sector = st.selectbox('sector', sorted(df['sector'].unique().tolist() ) )

# bedRoom -> float
bedroom = float(st.selectbox('No. of bedRoom', sorted(df['bedRoom'].unique().tolist() ) ))

# bathroom -> float
bathroom = float(st.selectbox('No. of bathroom', sorted(df['bathroom'].unique().tolist() ) ))

# balcony -> str
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist() ) )

# property_age -> str
property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

# built_up_area -> float
built_up_area = float(st.number_input('Built Up Area'))

# servant_room -> float
servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))

# store_room -> float
store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

# furnishing_type -> str
furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

# luxury_category -> str
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

# floor_category -> str
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))


if st.button('Predict', type="primary", icon=":material/search:"):
    status_text = st.empty()
    status_text.write("Performing calculations...")

    time.sleep(2)
    
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    
    # st.dataframe(one_df)

    # predict:
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # display:
    status_text.empty()   # remove the status_text msg
    st.text("The price of the flat is between {} Cr and {} Cr".format(round(low,2),round(high,2)))

    