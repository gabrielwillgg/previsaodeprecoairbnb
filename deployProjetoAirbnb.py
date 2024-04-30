@st.cache_resource
import pandas as pd
import streamlit as st
import joblib as jb

def run():
    st.set_page_config(
        page_title="Previsão de Preços",
    )
    image1 = r"https://gabrielwill.com.br/assets/images/logo2.png"
    image2 = r"https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_Bélo.svg/512px-Airbnb_Logo_Bélo.svg.png"

    st.image([image1,image2], width=100)
        
    """
    # Ferramenta de previsão de preços de diárias - Airbnb Rio de Janeiro

    Este projeto foi realizado por Gabriel Will, a fim de estudos.\n
    Site: [gabrielwill.com.br](https://gabrielwill.com.br)\n
    Linkedin: [Gabriel Will](https://www.linkedin.com/in/gabrielwillgg/)\n
    Notebook no Kaggle do Modelo de Previsão: [Kaggle](https://www.kaggle.com/code/gabrielwillgg/projeto-ferramenta-de-previsao-de-preco-de-imovel)

    """

    x_number = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
                'minimum_nights': 0, 'year': 0, 'month': 0, 'amenities_quantity': 0, 'host_listings_count': 0}

    x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

    x_lists = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Others', 'Serviced apartment'],
                'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
                'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period'],
                'bed_type': [ 'Real Bed', 'Others']
                }

    for item in x_number:
        if item == 'latitude':
            value = st.number_input(f'{item}', step=0.00001, value=-22.96486, format='%.5f')
        elif item == 'longitude':
            value = st.number_input(f'{item}', step=0.00001, value=-43.17562, format='%.5f')
        elif item == 'extra_people':
            value = st.number_input(f'{item}', step=0.01, value=0.0)
        else:
            value = st.number_input(f'{item}', step=1, value=0)
        x_number[item] = value

    for item in x_tf:
        value = st.selectbox(f'{item}', ('Sim', 'Não'))
        if value == 'Sim':
            x_tf[item] = 1
        else:
            x_tf[item] = 0

    dic_xlists = {}
    for item in x_lists:
        for value in x_lists[item]:
            dic_xlists[f'{item}_{value}'] = 0

    for item in x_lists:
        value = st.selectbox(f'{item}', x_lists[item])
        dic_xlists[f'{item}_{value}'] = 1

    button = st.button('Prever valor')

    if button:
        st.write("Isso pode demorar um pouco, por favor aguarde.")
        dic_xlists.update(x_number)
        dic_xlists.update(x_tf)
        values_df = pd.DataFrame(dic_xlists, index=[0])
        values_df = values_df.reindex(columns=['year', 'month', 'host_is_superhost', 'host_listings_count',
        'latitude', 'longitude', 'accommodates', 'bathrooms', 'bedrooms',
        'beds', 'extra_people', 'minimum_nights', 'instant_bookable',
        'amenities_quantity', 'property_type_Apartment',
        'property_type_Bed and breakfast', 'property_type_Condominium',
        'property_type_Guest suite', 'property_type_Guesthouse',
        'property_type_Hostel', 'property_type_House',
        'property_type_Loft', 'property_type_Others',
        'property_type_Serviced apartment', 'room_type_Entire home/apt',
        'room_type_Hotel room', 'room_type_Private room',
        'room_type_Shared room','bed_type_Others', 'bed_type_Real Bed',
        'cancellation_policy_flexible', 'cancellation_policy_moderate',
        'cancellation_policy_strict', 'cancellation_policy_strict_14_with_grace_period'])

        model = jb.load('model.joblib')
        price = model.predict(values_df)

        st.write(f"O valor justo para a diária de sua acomodação é de: R${price[0]}")

if __name__ == "__main__":
    run()
