# 콘솔 출력 및 로그 파일 기록 유틸리티

import os
import sys
from datetime import datetime

def resource_path(relative_path):
    try:
        # PyInstaller 배포 시: 임시 실행 폴더
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_log_path():
    """
    항상 실제 쓰기 가능한 log.txt 경로 반환
    배포 버전에서는 실행 파일이 있는 폴더 기준으로 생성
    """
    # 실행 파일이 있는 위치 (PyInstaller용)
    if getattr(sys, 'frozen', False):
        # exe 실행일 경우
        base_dir = os.path.dirname(sys.executable)
    else:
        # 로컬 실행일 경우
        base_dir = os.path.abspath(".")

    log_dir = os.path.join(base_dir, "data")
    os.makedirs(log_dir, exist_ok=True)

    return os.path.join(log_dir, "log.txt")

def log_message(text: str):
    print(text)

    log_path = get_log_path()

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {text}\n")
    except Exception as e:
        print(f"[로그 기록 실패] {e}")
