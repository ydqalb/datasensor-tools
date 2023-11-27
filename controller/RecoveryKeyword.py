import streamlit as st
from streamlit_tags import st_tags
import main_
import pyautogui
import time


# st.set_page_config(
#     page_title="Recovery Keyword"
# )
def recovery_keyword_func():
    st.markdown("<h4 style='text-align: left; color: black;'>Recovery Keyword </h4>",
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Input", "📤 Upload"])

    with st.form("my_form"):
        with tab1:
            keywords = st_tags(
                label="keyword :",
                text='Press enter to add more',
                maxtags=100,
                key='1')

        with tab2:
            uploaded_files = st.file_uploader("Import Keyword :")
            if st.button("upload"):
                if not uploaded_files:
                    st.warning("No data uploaded")
                try:
                    if uploaded_files is not None:
                        for upload in uploaded_files:
                            msg = str(upload, "utf-8")
                            main_.list_input.append(msg)
                        st.info("Data Uploaded")
                except:
                    st.warning("Upload Filed")

        since = st.date_input(  # since
            "since :",
            key="since"
        )
        format_since = since.strftime('%Y-%m-%d')

        if 'dummy_data' not in st.session_state.keys():
            dummy_data = ['youtube', 'instagram', 'twitter', 'tiktok', 'helo']
            st.session_state['dummy_data'] = dummy_data
        else:
            dummy_data = st.session_state['dummy_data']

        def checkbox_container(data):
            st.write('select platform :')
            cols = st.columns(5)
            if cols[0].form_submit_button('Select All'):
                for i in data:
                    st.session_state[i + '_dynamic_checkbox'] = True
                st.experimental_rerun()
            if cols[1].form_submit_button('UnSelect All'):
                for i in data:
                    st.session_state[i + '_dynamic_checkbox'] = False
                st.experimental_rerun()
            for i in data:
                st.checkbox(i, key=i + '_dynamic_checkbox')

        def get_selected_checkboxes():
            return [i.replace('_dynamic_checkbox', '\_.*keyword') for i in st.session_state.keys() if
                    i.endswith('_dynamic_checkbox') and st.session_state[i]]

        def in_submit():
            try:
                with st.spinner('Wait for it...'):
                    time.sleep(5)
                st.success('Done!')
                main_.list_input.extend(keywords)
                main_.platforms.extend(get_selected_checkboxes())
                main_.job_keyword(since=format_since)
                pyautogui.hotkey("ctrl", "F5")
            except:
                st.warning('Recovery Filed')
                keywords.clear()
                main_.list_input.clear()
                time.sleep(1)
                pyautogui.hotkey("ctrl", "F5")

        checkbox_container(dummy_data)
        # st.write(get_selected_checkboxes())
        st.markdown("""---""")

        send_submit = st.form_submit_button("Recovery")
        if send_submit:
            if not keywords:
                if not uploaded_files:
                    st.warning("Input / Upload Keyword")

                elif uploaded_files:
                    if not get_selected_checkboxes():
                        st.warning("Choose platform")
                    elif get_selected_checkboxes():
                        in_submit()
            elif keywords:
                if not get_selected_checkboxes():
                    st.warning("Choose platform")
                elif get_selected_checkboxes():
                    in_submit()
