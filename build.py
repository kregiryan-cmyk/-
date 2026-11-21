#!/usr/bin/env python3
"""tasks.json 내용을 index.html 안의 fallback 블록에 그대로 넣는다.

받은 앱이 tasks.json 을 못 불러왔을 때(오프라인, 파일로 열었을 때)도
같은 목록이 보이도록 하는 빌드 단계. tasks.json 만 고치고 이 스크립트를
한 번 돌리면 index.html 도 함께 맞춰진다.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MARK_OPEN = '<script id="fallback-tasks" type="application/json">'


def main() -> int:
    tasks = json.loads((ROOT / "tasks.json").read_text(encoding="utf-8"))
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    start = html.index(MARK_OPEN) + len(MARK_OPEN)
    end = html.index("</script>", start)

    payload = json.dumps(tasks, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = html[:start] + payload + html[end:]
    (ROOT / "index.html").write_text(out, encoding="utf-8")

    days = tasks.get("days", [])
    print("injected %d bytes · %d days · %d tasks" % (
        len(payload), len(days), sum(len(d.get("tasks", [])) for d in days)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
