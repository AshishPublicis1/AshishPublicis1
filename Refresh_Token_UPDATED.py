import argparse

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPE = "https://www.googleapis.com/auth/adwords"


def main(client_secrets_path, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path, scopes=scopes
    )

    flow.run_console()

    print("Access token: %s" % flow.credentials.token)
    print("Refresh token: %s" % flow.credentials.refresh_token)


if __name__ == "__main__":


    configured_scopes = [SCOPE]

    main(r'C:\Users\ashsingh42\Downloads\secret.json', configured_scopes)