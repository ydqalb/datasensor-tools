import streamlit as st
from streamlit_tags import st_tags
import main_


def upload_file(file_upload):
    if st.button("upload"):
        if not file_upload:
            st.warning("No data uploaded")
        try:
            if file_upload is not None:
                for upload in file_upload:
                    msg = str(upload, "utf-8")
                    main_.list_input.append(msg)
                st.info("Data Uploaded")
        except:
            st.warning("Upload Filed")


def input_text(identity):
    return st_tags(label=identity,
                   text='Press enter to add more',
                   maxtags=100,
                   key='1')


def input_since():
    return st.date_input("Since from :").strftime('%Y-%m-%d')

