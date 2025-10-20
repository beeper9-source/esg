# GitHub Pages 배포 가이드

## 1. GitHub 저장소 설정

1. GitHub에서 새 저장소 생성 (예: `esg`)
2. 로컬 프로젝트를 GitHub에 푸시

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/esg.git
git push -u origin main
```

## 2. package.json 수정

`package.json`의 `homepage` 필드를 실제 GitHub 사용자명과 저장소명으로 수정:

```json
"homepage": "https://yourusername.github.io/esg"
```

## 3. gh-pages 패키지 설치

```bash
npm install --save-dev gh-pages
```

## 4. GitHub Pages 배포

```bash
npm run deploy
```

## 5. GitHub Pages 설정 활성화

1. GitHub 저장소 → Settings → Pages
2. Source를 "Deploy from a branch"로 설정
3. Branch를 "gh-pages"로 선택
4. Save 클릭

## 6. 접속 확인

몇 분 후 다음 URL로 접속:
`https://yourusername.github.io/esg`

## 주의사항

- 첫 배포 후에는 몇 분 정도 시간이 걸릴 수 있습니다
- `npm run deploy` 명령어는 `build` 폴더의 내용을 `gh-pages` 브랜치에 푸시합니다
- 이후 코드 변경 시 `npm run deploy`만 실행하면 됩니다
