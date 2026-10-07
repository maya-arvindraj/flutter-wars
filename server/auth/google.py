from google.oauth2 import id_token
from google.auth.transport import requests


def verify_google_token(token: str):
    try:
        google_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
        )

        return {
            "google_subject": google_info["sub"],
            "email": google_info["email"],
        }

    except ValueError:
        return None