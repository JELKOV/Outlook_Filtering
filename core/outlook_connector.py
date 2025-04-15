# Outlook 연결 및 받은편지함 접근 모듈

# 필요한 라이브러리 import
import win32com.client

def get_inbox():
    """
    Outlook 데스크탑 앱에 연결하고 받은편지함 객체를 반환

    실행 전 조건:
    - Outlook 데스크탑 앱이 실행 중이어야 함 (자동으로 실행되진 않음)

    반환:
    - outlook.Folder 객체 (기본 받은편지함)
    """
    # Outlook 애플리케이션 실행 객체 연결
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # 기본 폴더 6: 받은편지함 (Inbox)
    return outlook.GetDefaultFolder(6)
