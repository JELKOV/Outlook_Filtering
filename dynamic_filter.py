# dynamic_filter.py

"""
사용자 입력 기반 '동적 필터링' 실행 모듈
- 제목/본문 키워드 및 최근 날짜 기준을 입력받아
- 조건에 맞는 메일을 복사 및 분류
- GUI 또는 CLI에서 사용 가능
"""

from datetime import datetime, timedelta
from core.outlook_connector import get_inbox
from core.folder_manager import get_or_create_folder
from core.logger import log_message
from core.mail_mover import move_email
from core.email_filter import filter_email

def run_dynamic_filter(subject_keywords, body_keywords, days_limit):
    """
    동적 필터 실행 함수
    - 입력 키워드를 기준으로 필터링
    - 필터링된 메일을 temp/폴더명에 복사
    """
    since = datetime.now().astimezone() - timedelta(days=days_limit)
    folder_name = "temp/" + "_".join(subject_keywords + body_keywords) + "_" + datetime.now().strftime("%Y-%m-%d")

    inbox = get_inbox()
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    target_folder = get_or_create_folder(inbox, folder_name)

    log = []
    count = 0
    for msg in messages:
        # since보다 오래된 메일이면 반복 종료
        if msg.ReceivedTime < since:
            break

        rule = {
            "subject_keywords": subject_keywords,
            "body_keywords": body_keywords,
            "has_attachment": False,
            "unread_only": False
        }

        if filter_email(msg, rule, since):
            move_email(msg, target_folder)
            log_message(f"[DYNAMIC] {msg.Subject} → {folder_name}")
            log.append(f"{msg.Subject} → {folder_name}")
            count += 1

    return count, log

# CLI 테스트용 진입점
if __name__ == "__main__":
    print("\n📬 [동적 필터링 CLI 테스트]")
    subject = input("제목 키워드 (공백): ").split()
    body = input("본문 키워드 (공백): ").split()
    days = int(input("며칠 이내 메일만? (기본 7): ") or 7)
    count, log = run_dynamic_filter(subject, body, days)
    print(f"✅ 총 {count}건 필터링 완료!")
