# 필터 설정 로더 - YAML 파일에서 필터 조건 및 설정 읽기

import yaml
import os
import sys

def resource_path(relative_path):
    """
    실행 환경에 따라 리소스 파일 경로를 반환하는 함수
    - PyInstaller로 빌드된 .exe 파일이 실행될 경우: 임시 경로(sys._MEIPASS) 사용
    - 로컬에서 .py 파일로 실행할 경우: 현재 디렉토리 기준으로 경로 계산

    예시:
    resource_path("config/filters.yaml") → 실행 환경에 맞는 절대 경로 반환
    """
    try:
        # PyInstaller로 패키징된 .exe가 실행 중인 경우
        base_path = sys._MEIPASS  # PyInstaller가 설정하는 임시 폴더 경로
    except AttributeError:
        # 로컬에서 .py 파일로 실행 중인 경우
        base_path = os.path.abspath(".")  # 현재 경로 기준

    return os.path.join(base_path, relative_path)


def load_filters():
    """
    filters.yaml 설정 파일을 로드하여 파싱된 데이터를 반환하는 함수

    동작 방식:
    - config/filters.yaml 파일을 열어 읽고
    - YAML 내용을 dict로 변환
    - 반드시 'filters' 키가 존재해야 함

    반환값 예시:
    {
        "filters": [...],  # 필터 규칙 리스트
        "global": {...}    # days_limit 등의 전역 설정
    }

    오류 상황:
    - filters.yaml이 존재하지 않거나
    - "filters" 키가 없을 경우 예외 발생
    """
    # 필터 설정 파일 경로 계산
    path = resource_path(os.path.join("config", "filters.yaml"))

    # YAML 파일 열기 및 파싱
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 유효성 검사
    if "filters" not in data:
        raise ValueError("filters.yaml에 'filters' 키가 없습니다.")

    return data

