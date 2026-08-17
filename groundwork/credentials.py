"""Connection config. `.env` in the working directory is loaded once, on import
of the providers package. Each provider resolves its own credentials.

ChatGPT OAuth (the `openai-codex` provider) follows the Kernos pattern:

- Groundwork's own credential file: `.credentials/openai-codex.json`
  with the shape {"access": str, "refresh": str, "expires": ms-epoch, "accountId": str}
- The Codex CLI (`codex login`) writes `~/.codex/auth.json` with a different
  schema. On resolve, if the CLI file is newer and carries different tokens,
  it is synced into Groundwork's file — so `codex login` is all a user needs.
- Expired access tokens refresh via OAuth; a refresh-401 (rotated by a fresh
  `codex login`) recovers from the CLI file before giving up.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import TypedDict


class CodexCredential(TypedDict):
    access: str
    refresh: str
    expires: int       # ms since epoch
    accountId: str


CODEX_CREDS_PATH = ".credentials/openai-codex.json"
CODEX_CLI_AUTH_PATH = "~/.codex/auth.json"
_OAUTH_TOKEN_URL = "https://auth.openai.com/oauth/token"
_OAUTH_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"


class CredentialError(Exception):
    pass


def _decode_jwt_claim(token: str, *claims: str):
    """Walk `claims` into the JWT payload; returns None on any failure."""
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        node = json.loads(base64.urlsafe_b64decode(payload_b64))
        for c in claims:
            node = node.get(c, {})
        return node or None
    except Exception:
        return None


def _read_cli_auth() -> CodexCredential | None:
    try:
        with open(os.path.expanduser(CODEX_CLI_AUTH_PATH)) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    tokens = data.get("tokens") or {}
    access, refresh = tokens.get("access_token", ""), tokens.get("refresh_token", "")
    if not access or not refresh:
        return None
    exp = _decode_jwt_claim(access, "exp")
    expires = int(exp) * 1000 if exp else int((time.time() + 3600) * 1000)
    account_id = tokens.get("account_id") or _decode_jwt_claim(
        access, "https://api.openai.com/auth", "chatgpt_account_id") or ""
    return CodexCredential(access=access, refresh=refresh, expires=expires, accountId=account_id)


def _persist(creds: CodexCredential) -> None:
    os.makedirs(os.path.dirname(CODEX_CREDS_PATH), exist_ok=True)
    with open(CODEX_CREDS_PATH, "w") as f:
        json.dump(dict(creds), f, indent=2)


def resolve_codex_credential() -> CodexCredential:
    """Groundwork file, resynced from the CLI file when that one is newer."""
    creds_path = CODEX_CREDS_PATH
    cli_path = os.path.expanduser(CODEX_CLI_AUTH_PATH)

    cli_mtime = os.path.getmtime(cli_path) if os.path.exists(cli_path) else 0.0
    own_mtime = os.path.getmtime(creds_path) if os.path.exists(creds_path) else 0.0
    if cli_mtime > own_mtime:
        cli_creds = _read_cli_auth()
        if cli_creds is not None:
            _persist(cli_creds)

    try:
        with open(creds_path) as f:
            data = json.load(f)
        return CodexCredential(
            access=data["access"], refresh=data["refresh"],
            expires=data.get("expires", 0),
            accountId=data.get("accountId")
            or _decode_jwt_claim(data["access"], "https://api.openai.com/auth", "chatgpt_account_id")
            or "",
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError):
        pass

    cli_creds = _read_cli_auth()
    if cli_creds is not None:
        _persist(cli_creds)
        return cli_creds

    raise CredentialError(
        "No ChatGPT OAuth credentials. Run `codex login` (writes ~/.codex/auth.json), "
        f"or create {CODEX_CREDS_PATH} with access/refresh tokens."
    )


def refresh_codex_credential(creds: CodexCredential) -> CodexCredential:
    form = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh"],
        "client_id": _OAUTH_CLIENT_ID,
    }).encode()
    req = urllib.request.Request(
        _OAUTH_TOKEN_URL, method="POST", data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            # `codex login` rotated the refresh token — recover from the CLI file.
            cli_creds = _read_cli_auth()
            if cli_creds is not None and cli_creds["access"] != creds["access"]:
                _persist(cli_creds)
                return cli_creds
        raise CredentialError(f"Codex token refresh failed: {exc}") from exc
    except urllib.error.URLError as exc:
        raise CredentialError(f"Codex token refresh failed: {exc}") from exc

    access = result.get("access_token", "")
    if not access:
        raise CredentialError("Codex token refresh returned no access_token")
    new = CodexCredential(
        access=access,
        refresh=result.get("refresh_token", creds["refresh"]),
        expires=int((time.time() + result.get("expires_in", 3600)) * 1000),
        accountId=_decode_jwt_claim(access, "https://api.openai.com/auth", "chatgpt_account_id")
        or creds["accountId"],
    )
    _persist(new)
    return new
