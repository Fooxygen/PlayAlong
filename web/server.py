
#   PlayAlong
#   Copyright (c) 2026 Fooxygen.
#   With BaseTUT.
#   Licensed under the MIT License.

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from   http.server  import SimpleHTTPRequestHandler, ThreadingHTTPServer
from   pathlib      import Path
from   typing       import Any
from   urllib.parse import parse_qs, urlparse

WEB_DIR = Path(__file__).resolve().parent
REPO_ROOT = WEB_DIR.parent
DEFAULT_PORT = 8787
DIFY_USER = "playalong-web"


class ApiError(Exception):
    """Expected API error returned to the browser as JSON."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def load_env(path: Path) -> None:
    """Load a simple KEY=VALUE .env file without overriding existing variables."""

    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ApiError(500, f"Missing environment variable: {name}")
    return value


def require_scope() -> str:
    value = os.environ.get("PC_SCOPE") or os.environ.get("PC_CASE_SCOPE")
    if not value:
        raise ApiError(500, "Missing environment variable: PC_SCOPE or PC_CASE_SCOPE")
    return value


def post_json(url: str, payload: dict[str, Any], token: str) -> dict[str, Any]:
    # Use ASCII escaping for the outer payload to avoid codepage issues.
    data = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise ApiError(502, f"Upstream returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise ApiError(502, f"Cannot reach upstream: {error.reason}") from error

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ApiError(502, "Upstream returned non-JSON content") from error
    if not isinstance(result, dict):
        raise ApiError(502, "Upstream JSON is not an object")
    return result


def load_case_library() -> dict[str, dict[str, Any]]:
    """Read the full case library from PowerContext, keyed by pack_id."""

    data = post_json(
        require_env("PC_URL").rstrip("/") + "/v1/memory/entries/list",
        {"scope_id": require_scope()},
        require_env("PC_TOKEN"),
    )

    library: dict[str, dict[str, Any]] = {}
    for entry in data.get("entries", []):
        if entry.get("kind") != "playalong.case":
            continue

        text = entry.get("text")
        if not isinstance(text, str):
            continue

        try:
            case = json.loads(text)
        except json.JSONDecodeError:
            continue

        pack_id = str(case.get("pack_id", ""))
        if pack_id:
            library[pack_id] = case

    return library


def get_cases() -> list[dict[str, Any]]:
    """Read the case catalog from PowerContext and return non-spoiler summaries."""

    cases: list[dict[str, Any]] = []
    for case in load_case_library().values():
        profile = case.get("profile")
        if not isinstance(profile, dict):
            profile = {}

        cases.append(
            {
                "pack_id": str(case.get("pack_id", "")),
                "title": str(case.get("title", "")),
                "description": str(case.get("description", "")),
                "difficulty": int(case.get("difficulty", 0)),
                "rounds": int(case.get("rounds", 0)),
                "name": str(profile.get("name", "")),
                "occupation": str(profile.get("occupation", "")),
                "disappearance": str(profile.get("disappearance", "")),
            }
        )

    cases.sort(key=lambda item: item["pack_id"])
    return cases


def get_memory_catalog(pack_id: str) -> dict[str, Any]:
    """Return fragment titles only. Fragment text must be recalled one by one."""

    case = load_case_library().get(pack_id)
    if not case:
        raise ApiError(404, f"Unknown case: {pack_id}")

    items: list[dict[str, str]] = []
    for fragment in case.get("fragments") or []:
        if not isinstance(fragment, dict):
            continue
        items.append(
            {
                "id": str(fragment.get("id", "")),
                "title": str(fragment.get("title", "")),
            }
        )

    return {"pack_id": pack_id, "items": items}


def recall_memory(pack_id: str, fragment_id: str) -> dict[str, str]:
    """Return the text of a single fragment."""

    case = load_case_library().get(pack_id)
    if not case:
        raise ApiError(404, f"Unknown case: {pack_id}")

    for fragment in case.get("fragments") or []:
        if not isinstance(fragment, dict):
            continue
        if fragment.get("id") == fragment_id:
            return {
                "id": fragment_id,
                "title": str(fragment.get("title", "")),
                "text": str(fragment.get("text", "")),
            }

    raise ApiError(404, f"Unknown fragment: {fragment_id}")


def chat(query: str, conversation_id: str, pack_id: str = "") -> dict[str, str]:
    """Forward a player message to Dify Chatflow and return the conversation id."""

    data = post_json(
        require_env("DIFY_API_BASE").rstrip("/") + "/chat-messages",
        {
            "inputs": {"pack_id": pack_id},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": DIFY_USER,
        },
        require_env("DIFY_API_KEY"),
    )

    return {
        "answer": str(data.get("answer", "")),
        "conversation_id": str(data.get("conversation_id", "")),
        "message_id": str(data.get("message_id", "")),
    }


class Handler(SimpleHTTPRequestHandler):
    server_version = "PlayAlongWeb/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(f"[web] {fmt % args}\n")

    def reply(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ApiError(400, "Invalid Content-Length") from error

        if length <= 0 or length > 1_000_000:
            raise ApiError(400, "Request body is empty or too large")

        raw = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ApiError(400, "Request body is not valid JSON") from error

        if not isinstance(body, dict):
            raise ApiError(400, "Request body must be a JSON object")
        return body

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.reply({"ok": True})
            return

        if path == "/api/cases":
            try:
                self.reply({"cases": get_cases()})
            except ApiError as error:
                self.reply({"error": error.message}, error.status)
            return

        if path == "/api/memory":
            try:
                pack_id = parse_qs(parsed.query).get("pack_id", [""])[0].strip()
                if not pack_id:
                    raise ApiError(400, "pack_id must not be empty")
                self.reply(get_memory_catalog(pack_id))
            except ApiError as error:
                self.reply({"error": error.message}, error.status)
            return

        if path == "/" and not (WEB_DIR / "index.html").is_file():
            self.reply({"error": "Frontend is not ready"}, 503)
            return

        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/api/memory/recall":
            try:
                body = self.read_json()
                pack_id = str(body.get("pack_id", "")).strip()
                fragment_id = str(body.get("fragment_id", "")).strip()
                if not pack_id or not fragment_id:
                    raise ApiError(400, "pack_id and fragment_id must not be empty")
                self.reply(recall_memory(pack_id, fragment_id))
            except ApiError as error:
                self.reply({"error": error.message}, error.status)
            except Exception:
                self.reply({"error": "Internal server error"}, 500)
            return

        if path != "/api/chat":
            self.reply({"error": "Not found"}, 404)
            return

        try:
            body = self.read_json()
            query = str(body.get("query", "")).strip()
            conversation_id = str(body.get("conversation_id", "")).strip()
            pack_id = str(body.get("pack_id", "")).strip()

            if not query:
                raise ApiError(400, "query must not be empty")

            self.reply(chat(query, conversation_id, pack_id))
        except ApiError as error:
            self.reply({"error": error.message}, error.status)
        except Exception:
            self.reply({"error": "Internal server error"}, 500)


def main() -> None:
    load_env(REPO_ROOT / ".env")

    for name in ("PC_URL", "PC_TOKEN", "DIFY_API_BASE", "DIFY_API_KEY"):
        if not os.environ.get(name):
            print(f"Missing environment variable: {name}", file=sys.stderr)
            raise SystemExit(2)

    if not os.environ.get("PC_SCOPE") and not os.environ.get("PC_CASE_SCOPE"):
        print("Missing environment variable: PC_SCOPE or PC_CASE_SCOPE", file=sys.stderr)
        raise SystemExit(2)

    try:
        port = int(os.environ.get("WEB_PORT", DEFAULT_PORT))
    except ValueError:
        print("WEB_PORT must be an integer", file=sys.stderr)
        raise SystemExit(2)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"PlayAlong Web: http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
