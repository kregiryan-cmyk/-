# 비즈렌탈랩 오늘 할 일 (웹앱)

휴대폰에서 열어 쓰는 하루 체크리스트. `kregiryan-cmyk/-` 저장소(GitHub Pages)에 그대로 올리면
`https://kregiryan-cmyk.github.io/-/` 에서 열립니다.

## 파일

| 파일 | 역할 |
|---|---|
| `index.html` | 앱 전체(화면·스타일·동작). 오프라인 대비용 목록 사본이 안에 들어 있음 |
| `tasks.json` | **할 일 원본.** 날짜별 할 일·단계·복사 문구·링크 |
| `manifest.json` | 홈 화면에 앱처럼 추가할 때 쓰는 설정 |
| `icon.svg` | 앱 아이콘(체크리스트) |
| `build.py` | `tasks.json` → `index.html` 안의 사본에 넣기 |
| `deploy.sh` | 커밋 → 푸시 → GitHub Pages 켜기 → 빌드 확인 |

## 할 일 고치는 법

1. `tasks.json` 을 고친다.
   한 날짜 항목은 `date`(YYYY-MM-DD), `label`(화면에 보이는 날짜), `tasks` 배열.
   할 일 하나는 `id`, `time`, `duration`, `badge`, `title`, `why`, `steps`, `links`, `copies`,
   그리고 피클이 미리 끝낸 일이면 `"preCompleted": true`.
2. `python3 build.py` — 오프라인 사본을 다시 넣는다.
3. `git add -A && git commit -m "..." && git push`
4. 휴대폰에서 새로고침만 하면 새 목록이 보인다 (`tasks.json` 을 매번 새로 받아옴).

## 배포

```sh
sh deploy.sh                 # 기본: kregiryan-cmyk/-
sh deploy.sh 계정/저장소      # 다른 이름
```

GitHub Pages 는 **public 저장소**에서만 무료로 열립니다.

## 넣으면 안 되는 것

공개 저장소라 누구나 볼 수 있습니다. 고객 실명·개인 휴대폰 번호·구글 독스/시트 링크·
내부 관리 코드는 넣지 않습니다. 업체 전화번호는 인터넷에 공개된 사업장 대표번호만 씁니다.
