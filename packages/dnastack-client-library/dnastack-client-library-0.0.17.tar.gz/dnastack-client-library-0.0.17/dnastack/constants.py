import os

auth_params = {
    "wallet_uri": "https://wallet.prod.dnastack.com/",
    "redirect_uri": "https://wallet.prod.dnastack.com/",
    "client_id": "publisher-cli",
    "client_secret": "xBmI87BDGdDkiVoJRJm1RgnHGy1MxpN1",
}


cli_directory = f"{os.path.expanduser('~')}/.dnastack"
config_file_path = f"{cli_directory}/config.yaml"
downloads_directory = f"{os.getcwd()}"

ACCEPTED_CONFIG_KEYS = [
    "data-connect-url",
    "drs-url",
    "personal_access_token",
    "email",
    "oauth_token",
    "wallet-url",
    "client-id",
    "client-secret",
    "client-redirect-uri",
    "collections-url",
]

auth_scopes = "openid drs-object:write drs-object:access dataconnect:info dataconnect:data dataconnect:query"
