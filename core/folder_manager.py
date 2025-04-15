# Outlook 폴더 탐색 및 생성 유틸리티

def get_or_create_folder(parent, path: str):
    """
    Outlook에서 주어진 경로(path)의 폴더를 찾아 반환하고,
    폴더가 없으면 생성하여 반환한다.

    예시 경로: "vessels/bulk_50000plus"

    파라미터:
        parent : 시작 폴더 (보통 받은편지함 inbox)
        path   : "/"로 구분된 폴더 경로 문자열

    반환:
        Folder : 최종 탐색된 또는 생성된 Outlook Folder 객체
    """

    # 폴더 경로를 '/' 기준으로 분할 → 각 단계 탐색
    parts = path.split("/")
    current = parent

    for part in parts:
        try:
            # 폴더가 존재하면 접근
            current = current.Folders[part]
        except:
            # 없으면 생성 후 접근
            current = current.Folders.Add(part)

    return current
