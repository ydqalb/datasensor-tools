# UPDATED: 2 May 2022
import pickle
import RecoveryAccount, RecoveryKeyword, duplicateMedia, addnews
import main_
import pyautogui
import datetime, re, yaml, time
import numpy as np
import streamlit as st
import pandas as pd
import mysql.connector
import helper as h
import streamlit_authenticator as stauth
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from pathlib import Path
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
from streamlit_extras.altex import line_chart, get_stocks_data, sparkline_chart
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_elements import elements, mui, html, nivo
# https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu
# https://icons.getbootstrap.com/



st.set_page_config(page_title='DataSensor-Tools', layout='wide')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

def home():
    today = datetime.date.today()
    colored_header(
        label=f"Data Link Clipper V2 [ {today} ]",
        description="",
        color_name="blue-90",
        )
    
    dbv2 = mysql.connector.connect(
            host = "159.65.134.198",
            user = "sc",
            port = "33569",
            password = "Rahasia@sc",
            database = "clipper"
        )
    
    cursorCount = dbv2.cursor()
    cursorCount.execute(f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'on_progress' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkOnProgress = cursorCount.fetchone()
    cursorCount.execute(f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'failed' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkFailed = cursorCount.fetchone()
    cursorCount.execute(f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'done' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkDone = cursorCount.fetchone()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="On Progress", value=linkOnProgress[0])
    col2.metric(label="Failed", value=linkFailed[0])
    col3.metric(label="Done", value=linkDone[0])
    style_metric_cards()

    cursorv2 = dbv2.cursor()
    cursorv2.execute(f"SELECT count(*), created_at, status FROM clipper.job where type = 'link' AND status IN ('on_progress', 'failed', 'done') AND created_at between '{today} 00:00:00' AND '{today} 23:59:59' group by status, created_at")
    linkStatus = cursorv2.fetchall()

    countData = []
    created_at = []
    status = []
    # dfv2 = []

    for datav2 in linkStatus:
        countData.append(datav2[0])
        created_at.append(re.sub(".*\-[0-9]+|\:[0-9]+$", "", str(datav2[1])))
        status.append(datav2[2])
        # task_id.append(datav2[2])
        # datadb = f'{datav2[0]}, {datav2[1]}'
        # dfv2.append(datadb)

    dfsc = pd.DataFrame({
        'value': countData,
        'created_at': created_at,
        'status': status,
        })

    stocks = dfsc
    line_chart(
        data=stocks,
        x="created_at",
        y="value",
        color="status",
        rolling=20,
        height=300
    )

    stathttpd, statcrond = st.columns(2)
    with stathttpd:
        st.success("[2023-09-26 15:00:00] 192.168.150.114 - httpd is running...")
    with statcrond:
        st.success("[2023-09-26 15:00:00] 192.168.150.16 - crond is running...")
    
    server1, server2 = st.columns(2)
    with server1:
        labels1 = ['Used', 'Available']
        clipperndc = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        clippercloud = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        specs1 = [[{'type':'domain'}, {'type':'domain'}]]
        fig1 = make_subplots(rows=1, cols=2, specs=specs1)

        # Define pie charts
        fig1.add_trace(go.Pie(labels=labels1, values=[80, 20], name='Clipper 114', marker_colors=clipperndc, hole = 0.7,), 1, 1)
        fig1.add_trace(go.Pie(labels=labels1, values=[60, 40], name='Clipper 137', marker_colors=clippercloud, hole = 0.7,), 1, 2)

        # Tune layout and hover info
        fig1.update_traces(hoverinfo='label+percent+name', textinfo='none')
        fig1.update(layout_title_text='Server Usage',
                layout_showlegend=False)

        fig1 = go.Figure(fig1)
        st.plotly_chart(fig1)

    with server2:
        labels2 = ['Used', 'Available']
        clipperv2 = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        pusher =  ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        specs2 = [[{'type':'domain'}, {'type':'domain'}]]
        fig2 = make_subplots(rows=1, cols=2, specs=specs2)

        # Define pie charts
        fig2.add_trace(go.Pie(labels=labels2, values=[40, 60], name='Clipper V2', marker_colors=clipperv2, hole = 0.7,), 1, 1)
        fig2.add_trace(go.Pie(labels=labels2, values=[20, 80], name='Pusher 16', marker_colors=pusher, hole = 0.7,), 1, 2)

        # Tune layout and hover info
        fig2.update_traces(hoverinfo='label+percent+name', textinfo='none')
        fig2.update(layout_showlegend=False)

        fig2 = go.Figure(fig2)
        st.plotly_chart(fig2)


def do_upload_tasks():
    st.subheader('Input CSV')
    uploaded_file = st.file_uploader("Choose a file")

def recovery_account():
    st.markdown("<b><small>SELECT PLATFORM :</small></b>", unsafe_allow_html=True)
    add_select_box = st.selectbox("",
                                  ("Instagram",
                                   "Twitter",
                                   "Facebook",
                                   "Youtube",
                                   "Tiktok"
                                   ),
                                  label_visibility="collapsed")
    if add_select_box == "Instagram":
        RecoveryAccount.instagram_func()
    if add_select_box == "Twitter":
        RecoveryAccount.twitter_func()
    if add_select_box == "Facebook":
        RecoveryAccount.facebook_func()
    if add_select_box == "Youtube":
        RecoveryAccount.youtube_func()
    if add_select_box == "Tiktok":
        RecoveryAccount.tiktok_func()

def recovery_keyword():
    RecoveryKeyword.recovery_keyword_func()

def profile():
    with st.form("form edit"):
        st.markdown("<h4 style='text-align: center; color: black;'>Edit Profile</h4>",
                    unsafe_allow_html=True)
        st.text_input("Full Name", f"{name}")
        st.text_input("Username", "rifqi")
        st.text_input("Password", "abc", type="password")
        st.form_submit_button("Change")
        
    authenticator.logout('Logout', 'main')

def do_logs():
    st.text_input('Search Media :')

def add_news():
    addnews.addnews_func()

def duplicate_media():
    duplicateMedia.duplicate_func()



styles = {
    "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch",
                  "background-color": "#191919"},
    "icon": {"font-size": "17px"},
    "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#6e6e6e"},
    "nav-link-selected": {"background-color": "#4F70D4", "font-size": "17px", "font-weight": "normal",
                          "color": "white", }
}

menu = {
    'title': 'DataSensor-Tools',
    'items': {
        'Home': {
            'action': home, 'item_icon': 'house-door', 'submenu': None
        },
        'Clipper': {
            'action': None, 'item_icon': 'scissors', 'submenu': {
                'title': None,
                'items': {
                    'Duplicate Media': {'action': duplicate_media, 'item_icon': 'files', 'submenu': None},
                    'Add News': {'action': add_news, 'item_icon': 'cloud-plus', 'submenu': None}
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
        'SmartCrawler': {
            'action': None, 'item_icon': 'journal-code', 'submenu': {
                'title': None,
                'items': {
                    'Recovery Account': {'action': recovery_account, 'item_icon': 'person-lines-fill', 'submenu': None},
                    'Recovery Keyword': {'action': recovery_keyword, 'item_icon': 'key', 'submenu': None},
                    'Get ID': {'action': do_upload_tasks, 'item_icon': '123', 'submenu': None},
                    'Delete Img Analysis': {'action': do_upload_tasks, 'item_icon': 'trash-fill', 'submenu': None},
                    'Compare Data Printed': {'action': do_upload_tasks, 'item_icon': 'arrows-angle-contract', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
        # 'Settings': {
        #     'action': None, 'item_icon': 'gear', 'submenu': {
        #         'title': None,
        #         'items': {
        #             'Manage Credentials': {'action': do_logs, 'item_icon': 'key', 'submenu': None},
        #             'View Logs': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
        #         },
        #         'menu_icon': None,
        #         'default_index': 0,
        #         'with_view_panel': 'main',
        #         'orientation': 'horizontal',
        #         'styles': styles
        #     }
        # },
        f'{name}': {
            'action': None, 'item_icon': 'person-circle', 'submenu': {
                'title': None,
                'items': {
                    'Profile': {'action': profile, 'item_icon': 'person-circle', 'submenu': None},
                    # 'View Logs': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
    },
    'menu_icon': 'cast',
    'default_index': 0,
    'with_view_panel': 'sidebar',
    'orientation': 'vertical',
    'styles': styles
}


def show_menu(menu):
    def _get_options(menu):
        options = list(menu['items'].keys())
        return options

    def _get_icons(menu):
        icons = [v['item_icon'] for _k, v in menu['items'].items()]
        return icons

    kwargs = {
        'menu_title': menu['title'],
        'options': _get_options(menu),
        'icons': _get_icons(menu),
        'menu_icon': menu['menu_icon'],
        'default_index': menu['default_index'],
        'orientation': menu['orientation'],
        'styles': menu['styles']
    }

    with_view_panel = menu['with_view_panel']
    if with_view_panel == 'sidebar':
        with st.sidebar:
            menu_selection = option_menu(**kwargs)
            # authenticator.logout('Logout', 'main')
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")

    if menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])

    if menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()


if st.session_state["authentication_status"]:
    show_menu(menu)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
