# main.py

"""
YAML 기반 '정적 필터링' 실행 모듈
- filters.yaml 파일 내 정의된 조건을 기반으로
- 메일을 자동 분류/복사하여 지정된 폴더에 저장
- GUI 및 CLI에서 모두 호출 가능
"""

from datetime import datetime, timedelta
from config.filters import load_filters
from core.mail_mover import move_email
from core.outlook_connector import get_inbox
from core.email_filter import filter_email
from core.folder_manager import get_or_create_folder
from core.logger import log_message

def run_static_filter():
    """
    정적 필터 실행 함수
    - filters.yaml에서 필터 조건과 기간 제한을 읽음
    - 조건에 맞는 메일을 복사하여 폴더 분류
    """
    config = load_filters()
    filters = config["filters"]
    days_limit = config.get("global", {}).get("days_limit", 7)
    since = datetime.now() - timedelta(days=days_limit)

    inbox = get_inbox()
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    print("\n📦 정적 필터링 시작...\n")
    moved_count = 0

    for msg in messages:
        if msg.ReceivedTime < since:
            break

        for rule in sorted(filters, key=lambda x: x["priority"]):
            if filter_email(msg, rule, since):
                folder = get_or_create_folder(inbox, rule["folder"])
                move_email(msg, folder)
                log_message(f"[COPIED] {msg.Subject} → {rule['folder']}")
                moved_count += 1

    print(f"\n✅ 필터링 완료! 총 이동된 메일 수: {moved_count}")
    return moved_count

# CLI 테스트용 진입점
if __name__ == "__main__":
    run_static_filter()
