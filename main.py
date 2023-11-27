# import RecoveryAccount, RecoveryKeyword, duplicateMedia, addnews
# from controller.duplicateMedia import duplicate_func
import datetime, re, yaml, time
import numpy as np
import streamlit as st
import pandas as pd
import mysql.connector
import helper as h
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

st.set_page_config(page_title='DataSensor-Tools', layout='wide')


def style_metric_cards(
        background_color: str = "#191919",
        border_size_px: int = 1,
        border_color: str = "#CCC",
        border_radius_px: int = 5,
        border_left_color: str = "#4f70d4",
        box_shadow: bool = True,
):
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def home():
    today = datetime.date.today()
    colored_header(
        label=f"Data Link Clipper V2 [ {today} ]",
        description="",
        color_name="blue-90",
    )

    dbv2 = mysql.connector.connect(
        host="159.65.134.198",
        user="sc",
        port="33569",
        password="Rahasia@sc",
        database="clipper"
    )

    cursorCount = dbv2.cursor()
    cursorCount.execute(
        f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'on_progress' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkOnProgress = cursorCount.fetchone()
    cursorCount.execute(
        f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'failed' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkFailed = cursorCount.fetchone()
    cursorCount.execute(
        f"SELECT count(status) FROM clipper.job where type = 'link' AND status = 'done' AND created_at between '{today} 00:00:00' AND '{today} 23:59:59'")
    linkDone = cursorCount.fetchone()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="On Progress", value=linkOnProgress[0])
    col2.metric(label="Failed", value=linkFailed[0])
    col3.metric(label="Done", value=linkDone[0])
    style_metric_cards()

    cursorv2 = dbv2.cursor()
    cursorv2.execute(
        f"SELECT count(*), created_at, status FROM clipper.job where type = 'link' AND status IN ('on_progress', 'failed', 'done') AND created_at between '{today} 00:00:00' AND '{today} 23:59:59' group by status, created_at")
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
        st.text('Service httpd')
        with open('../log/checkstatushttpdchandate_114.txt', 'r') as httpd114:
            st.warning(f"{httpd114.readlines()[-1]}")
        with open('../log/checkstatushttpdchandate_137.txt', 'r') as httpd137:
            st.warning(f"{httpd137.readlines()[-1]}")
    with statcrond:
        st.text('Service crond')
        with open('../log/checkstatuscrondchandate_114.txt', 'r') as crond114:
            st.warning(f"{crond114.readlines()[-1]}")
        with open('../log/checkstatuscrondchandate_137.txt', 'r') as crond137:
            st.warning(f"{crond137.readlines()[-1]}")
        with open('../log/checkstatuscrondchandate_16.txt', 'r') as crond16:
            st.warning(f"{crond16.readlines()[-1]}")

    server1, server2 = st.columns(2)
    with server1:
        labels1 = ['Used', 'Available']
        clipperndc = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        clippercloud = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        specs1 = [[{'type': 'domain'}, {'type': 'domain'}]]
        fig1 = make_subplots(rows=1, cols=2, specs=specs1)

        # Define pie charts
        fig1.add_trace(
            go.Pie(labels=labels1, values=[80, 20], name='Clipper 114', marker_colors=clipperndc, hole=0.7, ), 1, 1)
        fig1.add_trace(
            go.Pie(labels=labels1, values=[60, 40], name='Clipper 137', marker_colors=clippercloud, hole=0.7, ), 1, 2)

        # Tune layout and hover info
        fig1.update_traces(hoverinfo='label+percent+name', textinfo='none')
        fig1.update(layout_title_text='Server Usage',
                    layout_showlegend=False)

        fig1 = go.Figure(fig1)
        st.plotly_chart(fig1)

    with server2:
        labels2 = ['Used', 'Available']
        clipperv2 = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        pusher = ['rgb(79, 112, 212)', 'rgb(147, 151, 147)']
        specs2 = [[{'type': 'domain'}, {'type': 'domain'}]]
        fig2 = make_subplots(rows=1, cols=2, specs=specs2)

        # Define pie charts
        fig2.add_trace(go.Pie(labels=labels2, values=[40, 60], name='Clipper V2', marker_colors=clipperv2, hole=0.7, ),
                       1, 1)
        fig2.add_trace(go.Pie(labels=labels2, values=[20, 80], name='Pusher 16', marker_colors=pusher, hole=0.7, ), 1,
                       2)

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


def do_logs():
    st.text_input('Search Media :')


def add_news():
    addnews.addnews_func()


def duplicate_media():
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
    # duplicate_func()


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
                    'Compare Data Printed': {'action': do_upload_tasks, 'item_icon': 'arrows-angle-contract',
                                             'submenu': None},
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


if __name__ == "__main__":
    show_menu(menu)
