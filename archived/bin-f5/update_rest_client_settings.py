#!/usr/bin/env python3
"""Update the rest client settings."""
import json
import os
import pathlib


def main():
    """ Entry """
    symbols_path = os.getenv("TESTRUN_SYMBOLS")
    if symbols_path is None:
        raise SystemExit("Need to define TESTRUN_SYMBOLS")

    with open(symbols_path) as stream:
        symbols = json.load(stream)

    settings_path = pathlib.Path("~/Library/Application Support/Code/User/settings.json").expanduser()
    if not settings_path.exists():
        raise SystemExit(f"{settings_path} does not exist")

    with open(settings_path) as stream:
        settings = json.load(stream)

    username = symbols["ctrl_admin_username"]
    password = symbols["ctrl_admin_pass"]
    host = symbols["control_host_ips"][0]
    version = "v1"
    root = f"https://{host}/api"

    rest_client_settings = settings.setdefault("rest-client.environmentVariables", {})
    shared = rest_client_settings.setdefault("$shared", {})
    shared["adm"] = f"{root}/adm/{version}"
    shared["platform"] = f"{root}/platform/{version}"
    shared["hostname"] = host
    shared["admin_auth"] = f'Basic {username}:{password}'

    # Add OIDC Keycloak Information
    kc_symbols_path = os.getenv("OIDC_KEYCLOAK_SYMBOLS")
    if kc_symbols_path:
        with open(kc_symbols_path, "r", encoding="utf-8") as stream:
            kc = json.load(stream)

        shared.update({
            key: kc[key]
            for key in [
                "keycloak_oidc_authorization_endpoint",
                "keycloak_oidc_token_endpoint",
                "keycloak_oidc_jwks_uri",
                "keycloak_oidc_wellknown_endpoint",
            ]
        })

        # Hard code these for now
        shared["client_id"] = "adm-dataplane"
        shared["client_secret"] = "f790ea9d-db28-4ef8-9081-366a17c7f654"


    with open(settings_path, "w", encoding="utf-8") as stream:
        json.dump(settings, stream, indent=4)


if __name__ == '__main__':
    main()
