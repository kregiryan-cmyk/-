#!/usr/bin/env python3
"""tasks.json 내용을 index.html 안의 fallback 블록에 그대로 넣는다.

받은 앱이 tasks.json 을 못 불러왔을 때(오프라인, 파일로 열었을 때)도
같은 목록이 보이도록 하는 빌드 단계. tasks.json 만 고치고 이 스크립트를
한 번 돌리면 index.html 도 함께 맞춰진다.

- 루트 앱      : tasks.json  -> index.html
- bohum/ 앱    : bohum/tasks.json -> bohum/index.html  (폴더가 있을 때만)
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MARK_OPEN = '<script id="fallback-tasks" type="application/json">'


def build(folder: pathlib.Path) -> None:
    tasks = json.loads((folder / "tasks.json").read_text(encoding="utf-8"))
    html = (folder / "index.html").read_text(encoding="utf-8")

    start = html.index(MARK_OPEN) + len(MARK_OPEN)
    end = html.index("</script>", start)

    payload = json.dumps(tasks, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = html[:start] + payload + html[end:]
    (folder / "index.html").write_text(out, encoding="utf-8")

    days = tasks.get("days", [])
    print("%-12s injected %d bytes · %d projects · %d days · %d tasks" % (
        folder.name + "/",
        len(payload),
        len(tasks.get("projects", [])),
        len(days),
        sum(len(d.get("tasks", [])) for d in days),
    ))


def main() -> int:
    build(ROOT)
    bohum = ROOT / "bohum"
    if (bohum / "tasks.json").exists() and (bohum / "index.html").exists():
        build(bohum)
    else:
        print("bohum/     skipped (tasks.json 또는 index.html 없음)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
