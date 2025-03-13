# 🚀 AI 코드 리뷰 자동화 레파지토리!

이 레포지토리는 GitHub Actions를 활용한 **PR 코드 리뷰를 자동화**합니다.
다른 프로젝트에서 이 워크플로우를 **Reusable Workflow**로 손쉽게 사용할 수 있도록 제공됩니다.

---

## **📌 1. 사용 방법**  
### ✅ **1.1 GitHub Actions 워크플로우 추가 (사용하는 레포지토리)**
🔹 **프로젝트의 `.github/workflows/code-review.yml` 파일을 생성하고 아래 내용을 추가하세요.**
(깃허브 Add file 로 만드시면 편합니다!)

```yaml
name: Code Review with Google Gemini

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.MY_GITHUB_PAT }}

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install google-generativeai requests

      - name: Download review_gemini.py from ai-code-review
        run: wget -O review_gemini.py https://raw.githubusercontent.com/tnvnfdla1214/ai-code-review/main/scripts/review_gemini.py

      - name: Run code review script
        run: python review_gemini.py
        env:
          GOOGLE_API_KEY: ${{ secrets.google_api_key }}
          GITHUB_TOKEN: ${{ secrets.MY_GITHUB_PAT }}
          GITHUB_EVENT_NUMBER: ${{ github.event.pull_request.number }}
```
### ✅ 1.2 GitHub Secrets 설정 방법
🔹 **사용하려면 Settings → Secrets and variables → Actions → New repository secret 에서 아래 두 개의 Secrets를 추가하세요.**
- [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key?hl=ko) 

|Secret Name|설명|
|------|---|
|GOOGLE_API_KEY|Google Gemini API Key (Google Cloud Console에서 발급)|
|MY_GITHUB_PAT|GitHub Personal Access Token (PR 댓글을 달기 위해 필요)|

📌 PAT(Token) 권한 설정:
- repo → 전체 레포지토리 읽기/쓰기 (read/write)
- pull_requests → PR 파일 조회 및 댓글 작성 가능 (write)

## **📌 2. 내부 동작 방식**
1. PR 생성 또는 변경 감지 → GitHub Actions가 실행됨
2. PR의 변경된 파일 조회 → GitHub API를 사용해 코드 가져옴
3. Google Gemini API에 코드 리뷰 요청
4. PR에 코드 리뷰 결과 자동 댓글 작성
