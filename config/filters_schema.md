
# 📘 filters_schema.md – 필터 설정 스키마 문서

> 이 문서는 `config/filters.yaml` 파일에서 사용되는 필터 조건 항목들을 정의합니다.  
> 각 항목의 역할과 형식을 명확히 기록하여, 유지보수성과 협업 효율을 높이기 위한 목적입니다.

---

## 🗂️ 전체 구조 예시

```yaml
global:
  days_limit: 7

filters:
  - name: "open_position_asia"
    priority: 1
    subject_keywords: ["open", "position", "mv."]
    body_keywords: ["kendari", "jakarta"]
    has_attachment: false
    unread_only: false
    folder: "vessels/open_position_asia"
```

---

## 🧾 항목 정의

### 🔹 `global` (전역 설정)

| 키            | 타입  | 필수 | 설명                                       | 예시         |
|---------------|-------|------|--------------------------------------------|--------------|
| `days_limit`  | int   | ❌   | 필터링 대상이 될 메일의 수신일 기준 (N일) | `7` = 최근 7일 |

---

### 🔹 `filters` (필터 리스트)

각 필터는 `-` 로 시작하는 딕셔너리 항목입니다.

| 키                | 타입            | 필수 | 설명                                                                 | 예시                         |
|-------------------|-----------------|------|----------------------------------------------------------------------|------------------------------|
| `name`            | string          | ✅   | 필터의 고유 이름 (로그 및 식별용)                                    | `"open_position_asia"`       |
| `priority`        | int             | ✅   | 필터 적용 우선순위 (낮을수록 먼저 적용)                              | `1`, `10`, `99` 등           |
| `subject_keywords`| list of string  | ✅   | 제목에 포함되어야 할 키워드 목록 (하나라도 포함 시 통과)              | `["mv.", "open", "position"]`|
| `body_keywords`   | list of string  | ✅   | 본문에 포함되어야 할 키워드 목록 (하나라도 포함 시 통과)              | `["kendari", "ETA"]`         |
| `has_attachment`  | bool            | ❌   | 첨부파일이 반드시 있어야 하는지 여부                                 | `true` / `false`             |
| `unread_only`     | bool            | ❌   | 안 읽은 메일만 필터링할지 여부                                       | `true` / `false`             |
| `folder`          | string          | ✅   | 조건을 만족한 메일을 복사할 Outlook 폴더 경로                         | `"vessels/bulk_50000plus"`   |

---

## ✅ 작동 규칙 요약

- `subject_keywords`, `body_keywords`는 **OR 조건**으로 작동  
  예: `"open"` 또는 `"position"`만 있어도 통과
- 필터는 `priority` 값이 **낮은 순서부터 적용**됨
- **하나의 메일이 여러 필터에 매칭될 수 있음**  
  (복수 조건 만족 시 여러 폴더로 복사됨)
- `folder` 경로는 Outlook 폴더 구조 기준이며, 존재하지 않으면 자동 생성됨

---

## 🔧 향후 확장 항목 (예정 시 아래 표에 추가)

| 키               | 타입            | 설명                                                   | 예시                     |
|------------------|-----------------|--------------------------------------------------------|--------------------------|
| `categories`     | list of string  | Outlook 태그 자동 부착 (카테고리 색상표시 등)           | `["Auto-Filtered"]`      |
| `save_attachments`| bool           | 메일 첨부파일 자동 저장 여부                            | `true`                   |
| `log_level`      | string          | 특정 필터만 별도 로그 레벨로 기록                       | `"INFO"`, `"ALERT"`      |

---

## 📁 파일 위치

> 이 문서는 다음 경로에 함께 보관됩니다:

```
config/
├── filters.yaml
├── filters_schema.md  ✅ 현재 문서
```

---

## 🧠 유지 팁

- 새로운 항목이 추가되면 **`filters.yaml` 작성 시 반드시 이 문서도 함께 업데이트**
- 필터 수가 많아질 경우 `name`을 기준으로 정렬하거나 `priority` 기준으로 그룹화 추천
