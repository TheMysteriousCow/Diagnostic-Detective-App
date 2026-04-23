import secrets
import streamlit as st
import streamlit_authenticator as stauth
import base64
import os
from utils.data_manager import DataManager


# =========================
# Logo Funktion
# =========================
def set_logo_top_right(image_file: str):
    if not os.path.exists(image_file):
        st.warning(f"Bild konnte nicht geladen werden. Pfad: {image_file}")
        return

    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    .logo-container {{
        position: fixed;
        top: 60px;   /* 👈 bewusst tiefer gesetzt */
        right: 30px;
        z-index: 100;
    }}
    .logo-img {{
        width: 110px;
        height: auto;
        opacity: 0.95;
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{encoded}" class="logo-img">
    </div>
    """

    st.markdown(css, unsafe_allow_html=True)


# =========================
# Login Manager
# =========================
class LoginManager:
    def __new__(cls, *args, **kwargs):
        if 'login_manager' in st.session_state:
            return st.session_state.login_manager

        instance = super(LoginManager, cls).__new__(cls)
        st.session_state.login_manager = instance
        return instance

    def __init__(
        self,
        data_manager: DataManager = None,
        auth_credentials_file: str = 'credentials.yaml',
        auth_cookie_name: str = 'bmld_inf2_streamlit_app'
    ):
        if hasattr(self, 'authenticator'):
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

    # =========================
    # Hauptsteuerung
    # =========================
    def login_register(self, login_title='Login', register_title='Register new user'):
        if st.session_state.get("authentication_status") is True:
            with st.sidebar:
                st.write(f"Angemeldet als: **{st.session_state.get('name')}**")
                self.authenticator.logout()
        else:
            self._login_register_page(login_title, register_title)
            st.stop()

    # =========================
    # Login/Register Seite
    # =========================
    def _login_register_page(self, login_title, register_title):
        # 👉 robuster Pfad (funktioniert lokal + cloud)
        image_path = os.path.join(os.getcwd(), "images", "logo.png")

        # 👉 Logo hier platzieren (richtiger Ort!)
        set_logo_top_right(image_path)

        login_tab, register_tab = st.tabs((login_title, register_title))

        with login_tab:
            self._login()

        with register_tab:
            self._register()

    # =========================
    # Login
    # =========================
    def _login(self):
        self.authenticator.login()

        status = st.session_state.get("authentication_status")

        if status is False:
            st.error("Username/password is incorrect")
        elif status is None:
            st.warning("Please enter your username and password")

    # =========================
    # Registrierung
    # =========================
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