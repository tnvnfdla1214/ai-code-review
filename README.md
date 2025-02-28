# 🚀 AI 코드 리뷰 자동화 레파지토리!

이 레포지토리는 GitHub Actions를 활용한 **PR 코드 리뷰를 자동화**합니다.
다른 프로젝트에서 이 워크플로우를 **Reusable Workflow**로 손쉽게 사용할 수 있도록 제공됩니다.

---

## **📌 1. 사용 방법**  
### ✅ **1.1 GitHub Actions 워크플로우 추가 (사용하는 레포지토리)**
🔹 **프로젝트의 `.github/workflows/code-review.yml` 파일을 생성하고 아래 내용을 추가하세요.**  

```yaml
name: Code Review with AI  

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    uses: tnvnfdla1214/ai-code-review/.github/workflows/code-review.yml@main  # ✅ ai-code-review 워크플로우 사용
    secrets:
      google_api_key: ${{ secrets.GOOGLE_API_KEY }}  # ✅ Google API Key
      gh_pat: ${{ secrets.MY_GITHUB_PAT }}  # ✅ GitHub Personal Access Token
