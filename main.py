# 실행 진입점
"""
-- 실행 조건
- Outlook 앱은 실행 상태여야 함.
- 콘솔에 메일 수 출력되면 연결 성공
"""

# import
import win32com.client

# OutLook 앱 실행 연결 및 접근
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
# 받은 편지함 (기본 폴더 ID : 6)
inbox = outlook.GetDefaultFolder(6)

print(f"총 메일 수: {inbox.Items.Coutn}")