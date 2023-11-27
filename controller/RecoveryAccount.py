import streamlit as st
import helper as h
import main_
import pyautogui
import time

input_upload = ["📝 Input", "📤 Upload"]


# Instagram
def instagram_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Instagram </h4>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(input_upload)
    with st.form("my_form"):
        col1, col2 = st.columns(2)
        with col1:
            with tab1:
                identity = "Username Instagram"
                username_ig = h.input_text(identity=identity)
            with tab2:
                file_upload = st.file_uploader("Import Username Instagram :")
                h.upload_file(file_upload=file_upload)

            track_comment = st.selectbox("Take Comments",
                                         ("Yes", "No"))
            if track_comment == "Yes":
                track_comment = True
            else:
                track_comment = False

        with col2:
            since_form = st.date_input("Start Since from :").strftime('%Y-%m-%d')
            since_until = st.date_input("until :").strftime('%Y-%m-%d')

        st.markdown("""---""")

        def in_submit():
            try:
                with st.spinner('Wait for it...'):
                    main_.list_input.extend(username_ig)
                    main_.platforms.extend(["instagram_account"])
                    main_.job_account(since=since_form, until=since_until, track_comment=track_comment)
                    for i in username_ig:
                        st.info(f"success recovery {i}")
                st.success('Done!')
                time.sleep(3)
                pyautogui.hotkey("ctrl", "F5")
            except:
                st.warning('Recovery Filed')
                username_ig.clear()
                main_.list_input.clear()
                time.sleep(1)
                pyautogui.hotkey("ctrl", "F5")

        if st.form_submit_button("Recovery"):
            if not username_ig:
                if not file_upload:
                    st.warning("Input / Upload Username Instagram")
                else:
                    in_submit()
            else:
                in_submit()


# Twitter
def twitter_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Twitter </h4>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(input_upload)
    with st.form("my_form"):
        with tab1:
            identity = "Username Twitter"
            username_tw = h.input_text(identity=identity)
        with tab2:
            file_upload = st.file_uploader("Import Username Twitter :")
            h.upload_file(file_upload=file_upload)

        since_twitter = h.input_since()

        st.markdown("""---""")

        def in_submit():
            try:
                with st.spinner('Wait for it...'):
                    time.sleep(5)
                st.success('Done!')
                main_.list_input.extend(username_tw)
                main_.platforms.extend(["twitter_history_account"])
                main_.job_account(since=since_twitter)
                pyautogui.hotkey("ctrl", "F5")
            except:
                st.warning('Recovery Filed')
                username_tw.clear()
                main_.list_input.clear()
                time.sleep(1)
                pyautogui.hotkey("ctrl", "F5")

        if st.form_submit_button("Recovery"):
            if not username_tw:
                if not file_upload:
                    st.warning("Input / Upload Username Twitter")
                else:
                    in_submit()
            else:
                in_submit()


# Facebook
def facebook_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Facebook </h4>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(input_upload)
    with st.form("my_form"):
        with tab1:
            identity = "ID Facebook"
            id_facebook = h.input_text(identity=identity)
        with tab2:
            file_upload = st.file_uploader("Import ID Facebook :")
            h.upload_file(file_upload=file_upload)

        type_fb = st.selectbox("Type :", ("Personal", "page"))
        if type_fb == "Personal":
            type_fb = ["fb_feed_personal"]
        else:
            type_fb = ["fb_feed_page"]

        since_facebook = h.input_since()

        st.markdown("""---""")

        def in_submit():
            try:
                with st.spinner('Wait for it...'):
                    time.sleep(5)
                st.success('Done!')
                main_.list_input.extend(id_facebook)
                main_.platforms.extend(type_fb)
                main_.job_account(since=since_facebook)
                pyautogui.hotkey("ctrl", "F5")
            except:
                st.warning('Recovery Filed')
                id_facebook.clear()
                main_.list_input.clear()
                time.sleep(1)
                pyautogui.hotkey("ctrl", "F5")

        if st.form_submit_button("Recovery"):
            if not id_facebook:
                if not file_upload:
                    st.warning("Input / Upload ID Facebook")
                else:
                    in_submit()
            else:
                in_submit()


# Youtube
def youtube_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Youtube </h4>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(input_upload)
    with st.form("my_form"):
        with tab1:
            identity = "ID Youtube"
            id_youtube = h.input_text(identity=identity)
        with tab2:
            file_upload = st.file_uploader("Import ID Youtube :")
            h.upload_file(file_upload=file_upload)

        since_youtube = h.input_since()

        st.markdown("""---""")

        def in_submit():
            try:
                with st.spinner('Wait for it...'):
                    time.sleep(5)
                st.success('Done!')
                main_.list_input.extend(id_youtube)
                main_.platforms.extend(["youtube_post_alt"])
                main_.job_account(since=since_youtube)
                pyautogui.hotkey("ctrl", "F5")
            except:
                st.warning('Recovery Filed')
                id_youtube.clear()
                main_.list_input.clear()
                time.sleep(1)
                pyautogui.hotkey("ctrl", "F5")

        if st.form_submit_button("Recovery"):
            if not id_youtube:
                if not file_upload:
                    st.warning("Input / Upload Channel ID")
                else:
                    in_submit()
            else:
                in_submit()


# Tiktok
def tiktok_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Instagram </h4>",
                unsafe_allow_html=True)
    st.info("Coming soon!")
