
#   PlayAlong
#   Copyright (c) 2026 Fooxygen.
#   With BaseTUT.
#   Licensed under the MIT License.

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES_DIR = REPO_ROOT / "cases" / "json"
CASE_KIND = "playalong.case"
DEFAULT_SCOPE_KEY = "playalong-case-library-v2"
DEFAULT_TITLE = "PlayAlong Case Library"
DEFAULT_SUMMARY = "PlayAlong case library managed by scripts/seed_cases.py."
DEFAULT_MAX_BYTES = 8192

TOP_KEYS = {"pack_id", "title", "version", "profile", "npcs", "fragments"}
PROFILE_KEYS = {
    "name",
    "age",
    "occupation",
    "personality",
    "appearance",
    "disappearance",
    "secret",
}
NPC_KEYS = {
    "id",
    "name",
    "relation",
    "age",
    "personality",
    "speech_style",
    "opening",
    "greeting_hint",
    "questions",
    "facts",
}
QUESTION_KEYS = {"id", "content", "topic", "targets"}
FACT_KEYS = {
    "id",
    "topic",
    "text",
    "accepts",
    "keywords",
    "weight",
    "reaction_if_missed",
    "source_fragment",
}
FRAGMENT_KEYS = {"id", "title", "text", "certainty", "keywords"}
REQUIRES_KEYS = {"npc", "mentions"}


class SeedError(RuntimeError):
    """可预期的配置或数据错误。"""


def load_dotenv(path: Path) -> None:
    """读取简单的 KEY=VALUE .env；不覆盖已经存在的环境变量。"""

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


def read_env(name: str, fallback: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value:
        return value
    if fallback:
        return os.environ.get(fallback)
    return None


def update_env_scope(path: Path, scope_id: str) -> bool:
    """把 PC_CASE_SCOPE 写回 .env，保留其他内容和原有换行风格。"""

    line_value = f"PC_CASE_SCOPE={scope_id}"
    try:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        newline = "\r\n" if "\r\n" in text else "\n"
        lines = text.splitlines(keepends=True)
        output: list[str] = []
        replaced = False

        for line in lines:
            stripped = line.strip()
            if stripped.split("=", 1)[0].strip() == "PC_CASE_SCOPE":
                if not replaced:
                    ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
                    output.append(line_value + ending)
                    replaced = True
                continue
            output.append(line)

        if not replaced:
            if output and not output[-1].endswith(("\n", "\r")):
                output[-1] += newline
            output.append(line_value + newline)

        path.write_text("".join(output), encoding="utf-8", newline="")
        return True
    except OSError:
        return False


def fail(message: str) -> int:
    print("无法继续", file=sys.stderr)
    for line in str(message).splitlines():
        print(f"  {line}", file=sys.stderr)
    return 1


def post_json(base_url: str, token: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    # 外层用 ASCII 转义，避免 Windows / WSL 不同终端编码影响中文正文。
    data = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SeedError(f"POST {path} 失败：HTTP {error.code}：{detail}") from error
    except urllib.error.URLError as error:
        raise SeedError(f"POST {path} 失败：{error.reason}") from error

    if not raw:
        return {}
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SeedError(f"POST {path} 返回了非 JSON 内容") from error
    if not isinstance(result, dict):
        raise SeedError(f"POST {path} 返回的 JSON 不是对象")
    return result


def check_keys(
    value: Any,
    required: set[str],
    label: str,
    errors: list[str],
    *,
    optional: set[str] | None = None,
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label} 必须是对象")
        return False
    optional = optional or set()
    missing = required - set(value)
    extra = set(value) - required - optional
    if missing:
        errors.append(f"{label} 缺少字段：{', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{label} 多出字段：{', '.join(sorted(extra))}")
    return not missing and not extra


def check_string(value: Any, label: str, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, str):
        errors.append(f"{label} 必须是字符串")
    elif not allow_empty and not value.strip():
        errors.append(f"{label} 不能为空")


def check_string_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{label} 必须是字符串数组")


def check_int(value: Any, label: str, errors: list[str], *, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        errors.append(f"{label} 必须是 >= {minimum} 的整数")


def validate_case(case: Any, source: Path, max_bytes: int) -> list[str]:
    errors: list[str] = []
    label = source.name
    if not check_keys(case, TOP_KEYS, f"{label} 顶层", errors):
        return errors

    check_string(case["pack_id"], f"{label}.pack_id", errors)
    check_string(case["title"], f"{label}.title", errors)
    check_int(case["version"], f"{label}.version", errors, minimum=1)

    if check_keys(case["profile"], PROFILE_KEYS, f"{label}.profile", errors):
        profile = case["profile"]
        for key in ("name", "occupation", "personality", "appearance", "disappearance", "secret"):
            check_string(profile[key], f"{label}.profile.{key}", errors)
        check_int(profile["age"], f"{label}.profile.age", errors, minimum=1)

    fragments = case["fragments"]
    fragment_ids: set[str] = set()
    if not isinstance(fragments, list) or not fragments:
        errors.append(f"{label}.fragments 必须是非空数组")
        fragments = []
    for index, fragment in enumerate(fragments):
        fragment_label = f"{label}.fragments[{index}]"
        if not check_keys(fragment, FRAGMENT_KEYS, fragment_label, errors, optional={"requires"}):
            continue
        check_string(fragment["id"], f"{fragment_label}.id", errors)
        check_string(fragment["title"], f"{fragment_label}.title", errors)
        check_string(fragment["text"], f"{fragment_label}.text", errors)
        check_string_list(fragment["keywords"], f"{fragment_label}.keywords", errors)
        if fragment["certainty"] not in {"accurate", "inaccurate"}:
            errors.append(f"{fragment_label}.certainty 只能是 accurate 或 inaccurate")
        fragment_id = fragment.get("id")
        if isinstance(fragment_id, str):
            if fragment_id in fragment_ids:
                errors.append(f"{label} 中 fragment id 重复：{fragment_id}")
            fragment_ids.add(fragment_id)

    npcs = case["npcs"]
    npc_ids: set[str] = set()
    if not isinstance(npcs, list) or not npcs:
        errors.append(f"{label}.npcs 必须是非空数组")
        npcs = []
    for npc_index, npc in enumerate(npcs):
        npc_label = f"{label}.npcs[{npc_index}]"
        if not check_keys(npc, NPC_KEYS, npc_label, errors):
            continue
        check_string(npc["id"], f"{npc_label}.id", errors)
        check_string(npc["name"], f"{npc_label}.name", errors)
        check_string(npc["relation"], f"{npc_label}.relation", errors)
        check_string(npc["personality"], f"{npc_label}.personality", errors)
        check_string(npc["speech_style"], f"{npc_label}.speech_style", errors)
        check_string(npc["opening"], f"{npc_label}.opening", errors)
        check_string(npc["greeting_hint"], f"{npc_label}.greeting_hint", errors)
        check_int(npc["age"], f"{npc_label}.age", errors, minimum=1)
        npc_id = npc.get("id")
        if isinstance(npc_id, str):
            if npc_id in npc_ids:
                errors.append(f"{label} 中 npc id 重复：{npc_id}")
            npc_ids.add(npc_id)

        facts = npc["facts"]
        fact_ids: set[str] = set()
        if not isinstance(facts, list) or not facts:
            errors.append(f"{npc_label}.facts 必须是非空数组")
            facts = []
        for fact_index, fact in enumerate(facts):
            fact_label = f"{npc_label}.facts[{fact_index}]"
            if not check_keys(fact, FACT_KEYS, fact_label, errors):
                continue
            check_string(fact["id"], f"{fact_label}.id", errors)
            check_string(fact["topic"], f"{fact_label}.topic", errors)
            check_string(fact["text"], f"{fact_label}.text", errors)
            check_string_list(fact["accepts"], f"{fact_label}.accepts", errors)
            check_string_list(fact["keywords"], f"{fact_label}.keywords", errors)
            check_int(fact["weight"], f"{fact_label}.weight", errors, minimum=1)
            if type(fact["weight"]) is int and fact["weight"] > 5:
                errors.append(f"{fact_label}.weight 必须在 1 到 5 之间")
            check_string(fact["reaction_if_missed"], f"{fact_label}.reaction_if_missed", errors)
            check_string(fact["source_fragment"], f"{fact_label}.source_fragment", errors, allow_empty=True)
            fact_id = fact.get("id")
            if isinstance(fact_id, str):
                if fact_id in fact_ids:
                    errors.append(f"{npc_label} 中 fact id 重复：{fact_id}")
                fact_ids.add(fact_id)
            source_fragment = fact.get("source_fragment")
            if isinstance(source_fragment, str) and source_fragment and source_fragment not in fragment_ids:
                errors.append(f"{fact_label}.source_fragment 指向不存在的 fragment：{source_fragment}")

        questions = npc["questions"]
        question_ids: set[str] = set()
        if not isinstance(questions, list) or not questions:
            errors.append(f"{npc_label}.questions 必须是非空数组")
            questions = []
        for question_index, question in enumerate(questions):
            question_label = f"{npc_label}.questions[{question_index}]"
            if not check_keys(question, QUESTION_KEYS, question_label, errors):
                continue
            check_string(question["id"], f"{question_label}.id", errors)
            check_string(question["content"], f"{question_label}.content", errors)
            check_string(question["topic"], f"{question_label}.topic", errors)
            check_string_list(question["targets"], f"{question_label}.targets", errors)
            question_id = question.get("id")
            if isinstance(question_id, str):
                if question_id in question_ids:
                    errors.append(f"{npc_label} 中 question id 重复：{question_id}")
                question_ids.add(question_id)
            for target in question.get("targets", []):
                if isinstance(target, str) and target not in fact_ids:
                    errors.append(f"{question_label}.targets 指向本 NPC 不存在的 fact：{target}")

    for index, fragment in enumerate(fragments):
        if "requires" not in fragment:
            continue
        fragment_label = f"{label}.fragments[{index}]"
        requires = fragment["requires"]
        if not check_keys(requires, REQUIRES_KEYS, f"{fragment_label}.requires", errors):
            continue
        check_string(requires["npc"], f"{fragment_label}.requires.npc", errors)
        check_string(requires["mentions"], f"{fragment_label}.requires.mentions", errors)
        if isinstance(requires["npc"], str) and requires["npc"] not in npc_ids:
            errors.append(f"{fragment_label}.requires.npc 指向不存在的 NPC：{requires['npc']}")

    serialized = json.dumps(case, ensure_ascii=False, separators=(",", ":"))
    size = len(serialized.encode("utf-8"))
    if size > max_bytes:
        errors.append(f"{label} 压缩后为 {size} 字节，超过上限 {max_bytes} 字节")
    return errors


def minified(case: dict[str, Any]) -> str:
    return json.dumps(case, ensure_ascii=False, separators=(",", ":"))


def load_cases(cases_dir: Path, max_bytes: int) -> list[tuple[Path, dict[str, Any], str]]:
    if not cases_dir.is_dir():
        raise SeedError(f"案卷目录不存在：{cases_dir}")

    files = sorted(cases_dir.glob("*.json"))
    if not files:
        raise SeedError(f"案卷目录里没有 JSON 文件：{cases_dir}")

    loaded: list[tuple[Path, dict[str, Any], str]] = []
    errors: list[str] = []
    seen_pack_ids: dict[str, Path] = {}
    for path in files:
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path.name} 读取失败：{error}")
            continue
        case_errors = validate_case(case, path, max_bytes)
        errors.extend(case_errors)
        if case_errors:
            continue
        pack_id = case["pack_id"]
        if pack_id in seen_pack_ids:
            errors.append(f"pack_id 重复：{pack_id}（{seen_pack_ids[pack_id].name} 与 {path.name}）")
            continue
        seen_pack_ids[pack_id] = path
        loaded.append((path, case, minified(case)))

    if errors:
        raise SeedError("案卷校验失败：\n- " + "\n- ".join(errors))
    return loaded


def existing_cases(entries: Any) -> dict[str, str]:
    if not isinstance(entries, list):
        raise SeedError("entries/list 返回的 entries 不是数组")
    existing: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("kind") != CASE_KIND:
            continue
        text = entry.get("text")
        if not isinstance(text, str):
            continue
        try:
            case = json.loads(text)
        except json.JSONDecodeError:
            continue
        pack_id = case.get("pack_id") if isinstance(case, dict) else None
        if not isinstance(pack_id, str) or not pack_id:
            continue
        if pack_id in existing and existing[pack_id] != text:
            raise SeedError(f"案卷库中 pack_id={pack_id} 出现多个不同版本，请换新的 --scope-key")
        existing[pack_id] = text
    return existing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把 PlayAlong 案卷写入 PowerContext 案卷库")
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=DEFAULT_CASES_DIR,
        help=f"案卷 JSON 目录（默认：{DEFAULT_CASES_DIR}）",
    )
    parser.add_argument("--scope-key", default=DEFAULT_SCOPE_KEY, help="案卷库 scope 的幂等键")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="案卷库 scope 标题")
    parser.add_argument("--summary", default=DEFAULT_SUMMARY, help="案卷库 scope 摘要")
    parser.add_argument("--url", default=None, help="PowerContext 地址，默认读 PC_URL")
    parser.add_argument("--token", default=None, help="PowerContext token，默认读 PC_TOKEN")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="单条案卷正文字节上限")
    parser.add_argument("--dry-run", action="store_true", help="只校验，不连接 PowerContext")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(REPO_ROOT / ".env")

    cases_dir = args.cases_dir if args.cases_dir.is_absolute() else REPO_ROOT / args.cases_dir
    try:
        loaded = load_cases(cases_dir, args.max_bytes)
    except SeedError as error:
        return fail(error)

    if args.dry_run:
        print("PlayAlong")
        print()
        for path, case, text in loaded:
            size = len(text.encode("utf-8"))
            print(f"  {case['pack_id']:<8}通过    {size:,} 字节")
        print()
        print(f"{len(loaded)} 个案卷已就绪，未写入 PowerContext。")
        return 0

    url = args.url or read_env("PC_URL", "POWERCONTEXT_URL")
    token = args.token or read_env("PC_TOKEN", "POWERCONTEXT_TOKEN")
    if not url:
        return fail("缺少 PC_URL 或 POWERCONTEXT_URL。\n请在 .env 中设置，或使用 --url 传入。")
    if not token:
        return fail("缺少 PC_TOKEN 或 POWERCONTEXT_TOKEN。\n请在 .env 中设置，或使用 --token 传入。")

    try:
        scope = post_json(
            url,
            token,
            "/v1/scopes",
            {
                "title": args.title,
                "summary": args.summary,
                "idempotency_key": args.scope_key,
            },
        )
        scope_id = scope.get("scope_id")
        if not isinstance(scope_id, str) or not scope_id:
            raise SeedError("创建 scope 的响应里没有 scope_id")

        listing = post_json(url, token, "/v1/memory/entries/list", {"scope_id": scope_id})
        existing = existing_cases(listing.get("entries", []))

        seeded = 0
        skipped = 0
        statuses: list[tuple[str, str]] = []
        for _path, case, text in loaded:
            pack_id = case["pack_id"]
            if pack_id in existing:
                if existing[pack_id] != text:
                    raise SeedError(
                        f"案卷 {pack_id} 已存在但内容不同。"
                        "请把 --scope-key 换成新的版本号后重跑。"
                    )
                statuses.append((pack_id, "未变化"))
                skipped += 1
                continue

            response = post_json(
                url,
                token,
                "/v1/memory/remember",
                {
                    "scope_id": scope_id,
                    "kind": CASE_KIND,
                    "text": text,
                    "reason": f"Seed PlayAlong case {pack_id}",
                },
            )
            if response.get("changed") is False:
                statuses.append((pack_id, "未变化"))
                skipped += 1
            else:
                statuses.append((pack_id, "已写入"))
                seeded += 1

        env_updated = update_env_scope(REPO_ROOT / ".env", scope_id)

        print("PlayAlong")
        print()
        for pack_id, status in statuses:
            print(f"  {pack_id:<8}{status}")
        print()
        print(f"  案卷    {len(loaded)}")
        print(f"  写入    {seeded}")
        print(f"  跳过    {skipped}")
        print(f"  Scope   {scope_id}")
        print(f"  .env    {'已更新' if env_updated else '未更新'}")
        print()
        print(f"PC_CASE_SCOPE={scope_id}")
        if not env_updated:
            print("请手动把上面的 PC_CASE_SCOPE 写入 .env。", file=sys.stderr)
        return 0
    except SeedError as error:
        return fail(error)


if __name__ == "__main__":
    raise SystemExit(main())
