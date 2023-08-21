import streamlit as st
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, engine,Client, MatierePremiere, BonReceptionMatierePremiere

Session = sessionmaker(bind=engine)
session = Session()

if "liste_tole_entre" not in st.session_state:
    st.session_state["liste_tole_entre"] = []
    


st.title('Clients')



col = st.columns([2,1])
with col[1]:
    a = st.container()
    st.write('## Ajout client')
    nom = st.text_input('nom')
    adresse = st.text_area('adresse')
    if st.button('Valider'):
        client = Client(nom=nom,adresse=adresse)
        session.add(client)
        session.commit()
        st.success("added {client}")
with col[0]:
    "## liste clients"
    client = st.selectbox('Clients',map(str,session.query(Client).all()))
    client1 = session.query(Client).filter(Client.nom == client).first()
    date_entre = st.date_input('Date')
    bon_reception = BonReceptionMatierePremiere(date_reception=date_entre,client=client1)
    
    with st.form('tole_entre_details'):
        nom = st.text_input("genre")
        description = st.text_input("epaisseur")
        quantite_stock = st.number_input('qty')
        unite_mesure = st.text_input('unité')
        date_expiration = st.date_input('date')
        if st.form_submit_button():
            mp = MatierePremiere(
            nom = nom,
            description = description ,
            quantite_stock = quantite_stock,
            unite_mesure = unite_mesure,
            date_expiration = date_expiration,
            bon_reception = bon_reception
            )
            st.session_state["liste_tole_entre"].append(mp)
            
    for i in st.session_state["liste_tole_entre"]:
        a.write(i)
        
    
    
    bon_reception.matieres_premieres_recues = st.session_state["liste_tole_entre"]
    if st.button("valider"):
        session.add(bon_reception)
        session.add(st.session_state["liste_tole_entre"])
        session.commit()
        st.success("ok")
        pass


session.close()