# 📬 OUTLOOK 이메일 분류 프로그램

업무에서 매일 수신되는 수많은 메일 중,  
**특정 키워드나 제원 정보에 맞는 메일만 골라 자동으로 분류**해주는  
Outlook 기반 **이메일 필터링 도구**입니다.

비개발자도 사용할 수 있도록 **GUI 기반으로 제작**되었으며,  
클릭 몇 번으로 메일을 자동 정리할 수 있습니다.

---

## ✅ 주요 기능

| 기능 | 설명 |
|------|------|
| 제목/본문 키워드 필터링 | 입력된 키워드를 포함한 메일만 분류 |
| 날짜 기준 필터링 | 최근 며칠 이내 수신된 메일만 대상 (예: 7일) |
| 자동 폴더 복사 | 조건에 맞는 메일을 복사하여 지정 폴더에 분류 |
| YAML 기반 정적 필터링 | 자주 쓰는 조건은 `filters.yaml`에 저장 후 자동 분류 |
| GUI 제공 | 누구나 클릭 한 번으로 분류 가능 |
| 실행 로그 저장 | `data/log.txt`에 결과 자동 기록 |
| `.exe` 실행 파일 제공 | Python 설치 없이 바로 실행 가능 |

---

## 🖥️ 실행 방법

### 🟩 일반 사용자  – `.exe` 실행

1. `OutlookFiltering.exe` 더블 클릭  
2. 화면에서 아래 항목 입력  
   - 제목 키워드 (예: `mv. open`)  
   - 본문 키워드 (예: `kendari bulk`)  
   - 날짜 입력 (예: `7`)
3. ▶️ `키워드로 이메일 분류` 버튼 클릭  
4. 로그창에서 결과 확인  
5. 완료 시 결과는 Outlook 내 `temp/` 하위 폴더에 복사됩니다.

또는

📤 `설정값 이메일 분류` 버튼을 누르면  
`config/filters.yaml` 파일 기준으로 자동 분류됩니다.

---

## ⚙️ 고급 사용자 – YAML 설정값 수정

### 경로:
```
config/filters.yaml
```

### 예시:

```yaml
global:
  days_limit: 7  # 최근 며칠치만 필터링할지

filters:
  - name: "bulk_asia"
    priority: 1
    subject_keywords: ["mv.", "open"]
    body_keywords: ["kendari", "supramax"]
    has_attachment: false
    unread_only: false
    folder: "vessels/bulk_asia"
```

- **subject_keywords**: 제목에 포함될 단어
- **body_keywords**: 본문에 포함될 단어
- **folder**: Outlook 내 복사할 폴더 경로

📌 우선순위는 `priority` 숫자가 작을수록 먼저 적용됩니다.  
📁 필터에 맞는 메일은 지정된 폴더에 **복사됩니다.**

---

## 📦 폴더 구조

```
OutlookFiltering/
├── gui_tk.py                🖥️ Tkinter GUI 실행 파일
├── main.py                 📤 YAML 기반 정적 필터 함수
├── dynamic_filter.py       ▶️ 키워드 기반 동적 필터 함수
├── config/
│   └── filters.yaml        ⚙️ 필터 조건 설정 파일
├── data/
│   └── log.txt             📋 실행 로그 자동 기록
├── dist/
│   └── gui_tk.exe          ✅ 실행파일 (PyInstaller로 생성됨)
```

---

## 🛠️ 개발자용 실행 방법

```bash
pip install -r requirements.txt
python gui_tk.py
```

> 실행 전: Outlook 앱은 반드시 열려 있어야 합니다!

---

## 🧊 실행 파일 `.exe` 배포 방식

`.exe`는 PyInstaller로 만들어졌으며 `gui_tk.exe` 단일 파일로 실행 가능합니다.  
Python 미설치 환경에서도 사용할 수 있습니다.

> **주의:** 실행파일 내 YAML 파일은 수정이 안되므로,  
> YAML을 유지하고 싶다면 `config/filters.yaml`도 함께 제공해야 합니다.

---

## ✅ 필터링 결과 예시

```
[2025-04-18 11:12:43] [DYNAMIC] MV. LOTUS 6 → temp/mv_open_kendari_2025-04-18
[2025-04-18 11:13:15] [STATIC] MV. SEA BIRD → vessels/spec_detail
```

---

## 🙋‍♀️ Q&A

**Q. 필터링 후 메일이 삭제되나요?**  
A. ❌ 아닙니다. **복사(Copy)** 후 지정된 폴더로 이동합니다. 원본은 남아있습니다.

**Q. 키워드 순서가 중요한가요?**  
A. 순서는 무관하며, 하나라도 포함되면 필터링됩니다.

**Q. 정적 필터는 어떻게 수정하나요?**  
A. `config/filters.yaml` 파일을 메모장으로 열어 직접 수정하면 됩니다.

---

## 👨‍💻 제작자 메모

- 이 프로그램은 `win32com`, `tkinter`, `yaml` 등을 기반으로 작동합니다.
- Outlook 데스크탑 앱(Microsoft 365 / Office)과 연동됩니다.
- 최초 실행 시 Outlook 보안 경고가 뜰 수 있습니다 (허용 필요).

---

> 최종 업데이트: 2025-04-18  
> 제작자: **안제호**
