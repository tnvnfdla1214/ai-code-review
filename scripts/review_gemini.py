import os
import json
import google.generativeai as genai
import requests

# 환경 변수에서 API 키 가져오기
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_EVENT_NUMBER")
GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

# Google Gemini API 설정
genai.configure(api_key=GOOGLE_API_KEY)

# GitHub에서 PR의 변경된 코드 가져오기
def get_pr_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching PR files: {response.json()}")
        return []

# Google Gemini API를 사용해 코드 리뷰 생성
def request_code_review(code):
    model = genai.GenerativeModel("gemini-2.0-flash")  # gemini-2.0-flash 사용
    response = model.generate_content(
        f"다음 코드를 리뷰하고, 한국어로 피드백을 제공해주세요:\n\n{code}"
    )
    return response.text if response else "코드 리뷰를 받을 수 없습니다."

# GitHub PR에 리뷰 댓글 추가
def comment_on_pr(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {"body": comment}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Successfully commented on PR.")
    else:
        print(f"Error commenting on PR: {response.json()}")

# 실행 로직
if __name__ == "__main__":
    pr_files = get_pr_files()
    for file in pr_files:
        filename = file["filename"]
        patch = file.get("patch", "")
        if patch:
            review_comment = request_code_review(f"File: {filename}\n\n{patch}")
            comment_on_pr(f"### Code Review for `{filename}`\n\n{review_comment}")
