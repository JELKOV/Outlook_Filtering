from datetime import datetime, timedelta

from core.outlook_connector import get_inbox
from core.folder_manager import get_or_create_folder
from core.logger import log_message
from core.mail_mover import move_email
from core.email_filter import filter_email


def input_keywords(prompt):
    """
    키워드를 공백 기준으로 받아 리스트로 반환
    예: "mv. open" → ["mv.", "open"]
    """
    raw = input(prompt).strip()
    return [kw.strip().lower() for kw in raw.split()] if raw else []


def main():
    print("\n📬 [동적 필터링] 키워드를 입력해 주세요.")

    # 🔤 사용자 입력
    subject_keywords = input_keywords("제목 키워드 입력 (예: mv. open): ")
    body_keywords = input_keywords("본문 키워드 입력 (예: kendari bulk): ")

    # ⏱️ 날짜 제한
    days_str = input("며칠 이내 메일을 필터링할까요? (기본 7): ").strip()
    try:
        days = int(days_str)
    except:
        days = 7
    since = datetime.now() - timedelta(days=days)

    # 📁 복사할 폴더 이름 자동 생성
    folder_name = "temp/" + "_".join(subject_keywords + body_keywords) + "_" + datetime.now().strftime("%Y-%m-%d")

    # 📨 Outlook 연결 및 받은편지함 접근
    inbox = get_inbox()
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    # 📁 폴더 없으면 생성
    target_folder = get_or_create_folder(inbox, folder_name)

    print(f"\n📂 필터링 대상 폴더: {folder_name}")
    print("📦 필터링을 시작합니다...\n")

    # 🔍 메일 필터링 및 복사
    count = 0
    for msg in messages:
        rule = {
            "subject_keywords": subject_keywords,
            "body_keywords": body_keywords,
            "has_attachment": False,
            "unread_only": False
        }

        if filter_email(msg, rule, since):
            move_email(msg, target_folder)
            log_message(f"[DYNAMIC] {msg.Subject} → {folder_name}")
            count += 1

    print(f"\n✅ 필터링 완료! 총 이동된 메일 수: {count}")


if __name__ == "__main__":
    main()
