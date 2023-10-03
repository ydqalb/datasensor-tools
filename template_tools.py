# UPDATED: 2 May 2022

import streamlit as st
# https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu
# https://icons.getbootstrap.com/
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Muti-page app example', layout='wide')


def do_upload_tasks():
    st.markdown('### Upload task file')


def do_view_tasks():
    st.markdown('### Taxing tasks')
    st.markdown('''
    * Task1
    * Task2
    * Task3
    ''')


def do_manage_tasks():
    st.markdown('### Ticking tasks')
    st.checkbox('Task1', False)
    st.checkbox('Task2', True)
    st.checkbox('Task3', False)
    c1, c2, c3, _ = st.columns([1, 1, 1, 7])
    c1.button('Update tasks')
    c2.button('Add new task...')
    c3.button('Delete selected tasks')


def do_credentials():
    st.markdown('### Security rules')


def do_logs():
    st.markdown('### Blah, blah, blah, ....')


styles = {
    "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch",
                  "background-color": "#fafafa"},
    "icon": {"color": "black", "font-size": "20px"},
    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "lightblue", "font-size": "20px", "font-weight": "normal",
                          "color": "black", },
}

menu = {
    'title': 'Todo App',
    'items': {
        'Home': {
            'action': None, 'item_icon': 'house', 'submenu': {
                'title': None,
                'items': {
                    'View Tasks': {'action': do_view_tasks, 'item_icon': 'list-task', 'submenu': None},
                    'Manage Tasks': {'action': do_manage_tasks, 'item_icon': 'list-check', 'submenu': None},
                    'Upload Tasks': {'action': do_upload_tasks, 'item_icon': 'cloud-upload-fill', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        },
        'Settings': {
            'action': None, 'item_icon': 'gear', 'submenu': {
                'title': None,
                'items': {
                    'Manage Credentials': {'action': do_credentials, 'item_icon': 'key', 'submenu': None},
                    'View Logs': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
                },
                'menu_icon': None,
                'default_index': 0,
                'with_view_panel': 'main',
                'orientation': 'horizontal',
                'styles': styles
            }
        }
    },
    'menu_icon': 'clipboard2-check-fill',
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
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")

    if menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])

    if menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()


show_menu(menu)
