import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_option_menu import option_menu

def main():
    st.title("Data Sensor Tools")
    __login__obj = __login__(auth_token = "courier_auth_token", 
                        company_name = "Shims",
                        width = 200, height = 250, 
                        logout_button_name = 'Logout', hide_menu_bool = False, 
                        hide_footer_bool = False, 
                        lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN == True:
        st.title("Home")
        st.markdown("Your Streamlit Application Begins here!")

        # show_pages(
        #         [
        #             Page(f"{home()}", "Home", "🏠"),
        #             Page("myapp.py", "MyApp", "🈸"),
        #         ]
        # )

def home():
    st.markdown("Your Streamlit Application Begins here!")



if __name__ == "__main__":
    main()