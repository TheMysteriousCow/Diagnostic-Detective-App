import secrets
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_manager import DataManager


class LoginManager:

    def __new__(cls, *args, **kwargs):
        if "login_manager" in st.session_state:
            return st.session_state.login_manager

        instance = super(LoginManager, cls).__new__(cls)
        st.session_state.login_manager = instance
        return instance

    def __init__(
        self,
        data_manager: DataManager = None,
        auth_credentials_file: str = "credentials.yaml",
        auth_cookie_name: str = "bmld_inf2_streamlit_app"
    ):
        if hasattr(self, "authenticator"):
            return

        if data_manager is None:
            return

        self.data_manager = data_manager
        self.auth_credentials_file = auth_credentials_file
        self.auth_cookie_name = auth_cookie_name
        self.auth_cookie_key = secrets.token_urlsafe(32)

        self.auth_credentials = self._load_auth_credentials()

        self.authenticator = stauth.Authenticate(
            self.auth_credentials,
            self.auth_cookie_name,
            self.auth_cookie_key
        )

    def _load_login_css(self):
        st.markdown("""
        <style>
        .stApp {
            background-color: white;
        }

        html, body, p, div, span, label,
        h1, h2, h3, h4, h5, h6,
        .stMarkdown,
        .stText,
        .stCaption,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"],
        [data-testid="stText"] {
            color: #5C4033 !important;
        }

        div[data-baseweb="input"] {
            background-color: #EAEAEA !important;
            border-radius: 14px !important;
            border: none !important;
        }

        div[data-baseweb="input"] > div {
            background-color: #EAEAEA !important;
            border-radius: 14px !important;
        }

        div[data-baseweb="input"] input {
            background-color: #EAEAEA !important;
            color: #5C4033 !important;
        }

        input {
            color: #5C4033 !important;
        }

        input::placeholder {
            color: #8B6F63 !important;
        }

        button[data-baseweb="tab"] {
            color: #5C4033 !important;
            font-weight: 600 !important;
        }

        div.stButton > button {
            width: 100%;
            height: 50px;
            background-color: #D9D9D9 !important;
            color: #5C4033 !important;
            border: none !important;
            border-radius: 14px !important;
            font-size: 1rem;
            font-weight: 600;
        }

        div.stButton > button:hover {
            background-color: #CFCFCF !important;
            color: #5C4033 !important;
        }

        .stAlert {
            color: #5C4033 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def _load_auth_credentials(self):
        return self.data_manager.load_app_data(
            self.auth_credentials_file,
            initial_value={"usernames": {}}
        )

    def _save_auth_credentials(self):
        self.data_manager.save_app_data(
            self.auth_credentials,
            self.auth_credentials_file
        )

    def login_register(self, login_title="Login", register_title="Register new user"):
        if st.session_state.get("authentication_status") is True:
            with st.sidebar:
                st.write(f"Angemeldet als: **{st.session_state.get('name')}**")
                self.authenticator.logout()
        else:
            self._load_login_css()
            self._login_register_page(login_title, register_title)
            st.stop()

    def _login_register_page(self, login_title, register_title):
        login_tab, register_tab = st.tabs((login_title, register_title))

        with login_tab:
            self._login()

        with register_tab:
            self._register()

    def _login(self):
        self.authenticator.login()

        status = st.session_state.get("authentication_status")

        if status is False:
            st.error("Username/password is incorrect")
        elif status is None:
            st.warning("Please enter your username and password")

    def _register(self):
        st.info("""
        Password requirements:

        - 8-20 characters
        - at least one uppercase letter
        - one lowercase letter
        - one digit
        - one special character (@$!%*?&)
        """)

        res = self.authenticator.register_user()

        if res[1] is not None:
            st.success(f"User {res[1]} registered successfully")

            try:
                self._save_auth_credentials()
                st.success("Credentials saved successfully")
            except Exception as e:
                st.error(f"Failed to save credentials: {e}")