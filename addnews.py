import streamlit as st
import pandas as pd
import helper as h
import main_
import pyautogui
import time
import mysql.connector
import requests
import json
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
    }

def addnews_func():
    with st.form('my_form'):
        id_media = st.text_input('Search ID Media :')
        st.form_submit_button('Search')

    dbsc = mysql.connector.connect(
            host = "159.65.134.198",
            user = "sc",
            port = "33569",
            password = "Rahasia@sc",
            database = "clipper"
        )
    cursorsc = dbsc.cursor()
    cursorsc.execute(f"SELECT * FROM media WHERE id = '{id_media}'")
    rowsc = cursorsc.fetchone()

    print(rowsc)
    if bool(rowsc) is True:
        st.success(f'Media *{rowsc[1]}* ditemukan!')
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, delimiter='\t', names=['Link', 'Status'])
            for link in df['Link']:
                url = 'http://192.168.21.110:31831/job/create'
                media_id = rowsc[0]
                link = re.sub("[\[\]\']", "", link)

                data = {"data": json.dumps([{"media_id": f'{media_id}', "link": f'{link}'}])}
                response = requests.post(url, data=data, headers=HEADERS)
                df['Status'] = 'Pushed!'
                print(data)
                print(response.content)

            st.write(df)
            st.success('Completed Pushed!')
        else:
            st.info('☝️ Upload a txt file')
    else:
        st.info('Masukan ID Media!')
