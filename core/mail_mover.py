# 메일 복사 및 이동 유틸리티

def move_email(msg, folder):
    """
    주어진 Outlook 메일을 복사한 뒤, 지정된 폴더로 이동시킨다.

    파라미터:
        msg    : Outlook 메일 객체 (원본)
        folder : Outlook Folder 객체 (대상 폴더)

    반환:
        None
    """
    try:
        # 메일 복사 후 이동
        copy = msg.Copy()
        copy.Move(folder)
    except Exception as e:
        print(f"[ERROR] 메일 이동 실패: {e}")