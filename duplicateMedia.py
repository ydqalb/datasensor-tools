import streamlit as st
import pandas as pd
import helper as h
import main_
import mysql.connector
import pyautogui
import time
import re


def duplicate_func():
    with st.form('my_form'):
        media = st.text_input('Search Baselink :')
        st.form_submit_button('Search')

    dbsc = mysql.connector.connect(
            host = "159.65.134.198",
            user = "sc",
            port = "33569",
            password = "Rahasia@sc",
            database = "smart_crawler"
        )
    cursorsc = dbsc.cursor()
    cursorsc.execute(f"SELECT * FROM master_media_tag_ON WHERE baselink LIKE '%{media}%' limit 5")
    rowsc = cursorsc.fetchall()
    
    dbv2 = mysql.connector.connect(
            host = "159.65.134.198",
            user = "sc",
            port = "33569",
            password = "Rahasia@sc",
            database = "clipper"
        )
    cursorv2 = dbv2.cursor()
    cursorv2.execute(f"SELECT * FROM media WHERE base_url LIKE '%{media}%' limit 5")
    rowv2 = cursorv2.fetchall()
    
    mediasc = []
    screen_name = []
    baselinksc = []

    id_mediav2 = []
    mediav2 = []
    baselinkv2 = []
    created_at = []
    lastUpdateV2 = []

    for datasc in rowsc:
        mediasc.append(datasc[0])
        screen_name.append(datasc[1])
        baselinksc.append(datasc[3])
    
    for datav2 in rowv2:
        id_mediav2.append(datav2[0])
        mediav2.append(datav2[1])
        baselinkv2.append(datav2[3])
        created_at.append(datav2[8])
        lastUpdateV2.append(datav2[9])

    if bool(rowsc) is True or bool(rowv2) is True:
        statSC, statV2 = st.columns(2)
        with statSC:
            st.warning("Database SC")
            dfsc = pd.DataFrame({
            'Media': mediasc,
            'Screen Name': screen_name,
            'Baselink': baselinksc,
            })
            st.write(dfsc)
        
        with statV2:
            st.warning("Database V2")
            dfv2 = pd.DataFrame({
            'ID Media': id_mediav2,
            'Media ': mediav2,
            'Baselink': baselinkv2,
            'Created At': created_at,
            'Last Update': lastUpdateV2
            })
            st.write(dfv2)
    elif bool(rowsc) is False or bool(rowv2) is False:
        pass
    else:
        st.error('Media tidak ditemukan!')

    