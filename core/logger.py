# 콘솔 출력 및 로그 파일 기록 유틸리티

from datetime import datetime

def log_message(text: str):
    """
    메시지를 콘솔에 출력하고, log.txt 파일에도 타임스탬프와 함께 기록한다.

    로그 저장 위치:
    - ./data/log.txt

    로그 포맷 예시:
    [2025-04-17 14:30:10.123456] [COPIED] MV. LOTUS 6 → vessels/bulk

    파라미터:
        text (str): 로그로 남길 메시지 문자열
    """

    # 콘솔에 출력
    print(text)

    # 로그 파일에 타임스탬프와 함께 기록
    with open("data/log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {text}\n")
