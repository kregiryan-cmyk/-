#!/bin/sh
# 비즈렌탈랩 오늘 할 일 — GitHub Pages 배포 스크립트
#
# 사용법 (저장소가 이미 만들어진 뒤에 실행):
#   sh deploy.sh                      # 기본값 kregiryan-cmyk/today
#   sh deploy.sh 다른계정/다른이름
#
# 하는 일: main 브랜치로 커밋 → 푸시 → GitHub Pages 켜기 → 빌드 완료까지 확인
set -e
cd "$(dirname "$0")"

REPO="${1:-kregiryan-cmyk/-}"
BRANCH=main

echo "== 0. 저장소 확인: $REPO"
if ! gh repo view "$REPO" >/dev/null 2>&1; then
  echo "!! 저장소가 없습니다. github.com/new 에서 public 저장소 '$REPO' 를 먼저 만들어 주세요."
  exit 1
fi

echo "== 1. 빌드 (tasks.json → index.html)"
python3 build.py

echo "== 2. 커밋"
if [ ! -d .git ]; then
  git init -b "$BRANCH" >/dev/null
fi
git add -A
if git diff --cached --quiet; then
  echo "   바뀐 내용 없음"
else
  git -c user.name="kregiryan-cmyk" -c user.email="kregiryan-cmyk@users.noreply.github.com" \
      commit -m "오늘 할 일 업데이트 $(date +%Y-%m-%d\ %H:%M)" >/dev/null
  echo "   커밋 완료"
fi

echo "== 3. 푸시"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "https://github.com/$REPO.git"
else
  git remote add origin "https://github.com/$REPO.git"
fi
git push -u origin "$BRANCH"

echo "== 4. GitHub Pages 켜기"
if gh api "repos/$REPO/pages" >/dev/null 2>&1; then
  echo "   이미 켜져 있음"
  gh api -X PUT "repos/$REPO/pages" -f 'build_type=legacy' -f 'source[branch]='"$BRANCH" -f 'source[path]=/' >/dev/null 2>&1 || true
else
  gh api -X POST "repos/$REPO/pages" -f 'build_type=legacy' -f 'source[branch]='"$BRANCH" -f 'source[path]=/' >/dev/null 2>&1 || \
    echo "   !! API로 못 켰습니다. 저장소 Settings → Pages → Source: Deploy from a branch → main / root 로 켜 주세요."
fi

echo "== 5. 빌드 상태 확인"
i=0
while [ "$i" -lt 20 ]; do
  STATUS=$(gh api "repos/$REPO/pages" --jq '.status' 2>/dev/null || echo "none")
  URL=$(gh api "repos/$REPO/pages" --jq '.html_url' 2>/dev/null || echo "")
  echo "   [$i] status=$STATUS"
  if [ "$STATUS" = "built" ]; then
    echo "완료: $URL"
    exit 0
  fi
  i=$((i + 1))
  sleep 15
done
echo "아직 빌드 중입니다. 1~2분 뒤 https://$REPO 를 확인하세요. (저장소 Settings → Pages 에서도 상태 확인 가능)"
