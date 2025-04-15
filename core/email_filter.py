# 메일 필터링 로직
from datetime import datetime

def filter_email(msg, rule, since: datetime) -> bool:
    """
    주어진 메일(msg)이 특정 필터 조건(rule)에 맞는지 확인하는 함수

    매칭 조건:
    - 받은 날짜가 since 이후인지
    - 제목에 subject_keywords 중 하나 이상 포함
    - 본문에 body_keywords 중 하나 이상 포함
    - 첨부파일 유무 조건
    - 안읽은 메일 조건

    파라미터:
        msg   : Outlook 메일 객체
        rule  : 필터 조건 딕셔너리
        since : 검사 대상이 될 최소 날짜 (ex. 최근 7일 등)

    반환:
        bool : 조건을 만족하면 True, 아니면 False
    """

    # 메일 수신 시간이 기준 날짜 이전이면 필터 제외
    if msg.ReceivedTime.replace(tzinfo=None) < since:
        return False

    # 메일 제목과 본문 추출 (소문자 변환)
    subject = msg.Subject.lower()
    body = ""
    try:
        body = msg.Body.lower()
    except:
        pass  # 일부 메일은 Body가 없거나 오류 발생 가능

    # 제목 키워드 검사
    if rule.get("subject_keywords"):
        if not any(kw.lower() in subject for kw in rule["subject_keywords"]):
            return False

    # 본문 키워드 검사
    if rule.get("body_keywords"):
        if not any(kw.lower() in body for kw in rule["body_keywords"]):
            return False

    # 첨부파일 조건 검사
    if rule.get("has_attachment") and msg.Attachments.Count == 0:
        return False

    # 안읽은 메일 조건 검사
    if rule.get("unread_only") and not msg.UnRead:
        return False

    # 모든 조건 통과 시 필터 매칭 성공
    return True
