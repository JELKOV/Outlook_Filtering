# 필터 설정 로더 - YAML 파일에서 필터 조건 및 설정 읽기

import yaml

def load_filters():
    """
    filters.yaml 파일을 불러와 필터 목록과 전역 설정을 반환

    구조 예시:
    - filters: 필터 조건 리스트
    - global: 전역 설정 (예: days_limit)

    반환:
        dict {
            "filters": [...],  # 필터 목록 리스트
            "global": {...}    # 전역 설정
        }
    """
    with open("config/filters.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 기본 키 유효성 검사 (선택 사항)
    if "filters" not in data:
        raise ValueError("filters.yaml에 'filters' 키가 없습니다.")

    return data
