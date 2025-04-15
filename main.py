# 실행 진입점
"""
[실행 조건]
- Outlook 앱은 실행 상태여야 함.
- 콘솔에 메일 수 출력되면 연결 성공
"""

from datetime import datetime, timedelta

# 설정 파일에서 필터 조건 및 전역 설정 불러오기
from config.filters import load_filters
from core.mail_mover import move_email
from core.outlook_connector import get_inbox
from core.email_filter import filter_email
from core.folder_manager import get_or_create_folder
from core.logger import log_message

# YAML 설정에서 필터 목록과 날짜 제한 값 가져오기
config = load_filters()  # filters.yaml에는 "filters"와 "global" 모두 포함
filters = config["filters"]

# 최근 며칠까지 메일을 필터링할지 설정 (기본값 7일)
days_limit = config.get("global", {}).get("days_limit", 7)
since = datetime.now() - timedelta(days=days_limit)

def main():
    # Outlook 받은편지함 연결
    inbox = get_inbox()

    # 받은편지함의 모든 메일 목록 정렬 (최신순)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    print("\n 메일 필터링 시작...\n")
    moved_count = 0

    # 받은 메일 1개씩 순회
    for msg in messages:
        # filters.yaml에서 우선순위 순으로 순회
        for rule in sorted(filters, key=lambda x: x["priority"]):
            # 필터 조건 만족 여부 확인
            if filter_email(msg, rule, since):
                # 조건에 맞는 폴더가 없다면 생성
                folder = get_or_create_folder(inbox, rule["folder"])

                # 해당 메일 복사 후 폴더로 이동 (복수 필터 적용 허용)
                move_email(msg, folder)

                # 로그 기록
                log_message(f"[COPIED] {msg.Subject} → {rule['folder']}")
                moved_count += 1

    print(f"\n필터링 완료! 총 이동된 메일 수: {moved_count}")

if __name__ == "__main__":
    main()
