import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
from main import run_static_filter
from dynamic_filter import run_dynamic_filter

# ⏳ 로딩창
def show_loading_popup():
    loading = tk.Toplevel()
    loading.title("처리 중...")
    loading.geometry("300x80")
    loading.resizable(False, False)
    loading.grab_set()
    tk.Label(loading, text="메일을 처리 중입니다...\n잠시만 기다려주세요.").pack(pady=20)
    return loading

def set_ui_state(state):
    dynamic_btn.config(state=state)
    static_btn.config(state=state)

def update_keyword_display():
    subject_display.config(text=", ".join(subject_keywords))
    body_display.config(text=", ".join(body_keywords))

def add_subject_keyword():
    kw = subject_input.get().strip().lower()
    if kw and kw not in subject_keywords:
        subject_keywords.append(kw)
        update_keyword_display()
    subject_input.delete(0, tk.END)

def add_body_keyword():
    kw = body_input.get().strip().lower()
    if kw and kw not in body_keywords:
        body_keywords.append(kw)
        update_keyword_display()
    body_input.delete(0, tk.END)

def get_days_limit():
    try:
        return int(days_entry.get())
    except:
        return 7

# ▶️ 동적 필터 실행
def run_dynamic():
    if not subject_keywords and not body_keywords:
        messagebox.showwarning("입력 필요", "최소 하나의 키워드를 입력해주세요.")
        return

    set_ui_state("disabled")
    output_text.delete(1.0, tk.END)
    loading = show_loading_popup()
    root.update_idletasks()

    try:
        days = get_days_limit()
        count, log_lines = run_dynamic_filter(subject_keywords, body_keywords, days)
        output_text.insert(tk.END, f"✅ 이메일 {count}건 분류 완료!\n\n")
        output_text.insert(tk.END, "\n".join(log_lines))
        messagebox.showinfo("완료", f"이메일 {count}건이 분류되었습니다.")
    except Exception as e:
        output_text.insert(tk.END, f"❌ 오류 발생: {str(e)}\n")
        messagebox.showerror("오류", f"동적 필터링 중 오류 발생\n{str(e)}")

    loading.destroy()
    set_ui_state("normal")

# 📤 정적 필터 실행
def run_static():
    set_ui_state("disabled")
    output_text.delete(1.0, tk.END)
    loading = show_loading_popup()
    root.update_idletasks()

    try:
        count = run_static_filter()  # days_limit은 YAML에서 관리
        output_text.insert(tk.END, f"✅ 자동 필터로 {count}건 분류 완료!\n")
        messagebox.showinfo("완료", f"정적 필터링 완료!\n총 {count}건 분류됨.")
    except Exception as e:
        output_text.insert(tk.END, f"❌ 오류 발생: {str(e)}\n")
        messagebox.showerror("오류", f"정적 필터링 중 오류 발생\n{str(e)}")

    loading.destroy()
    set_ui_state("normal")

# ────────────────────────────────
subject_keywords = []
body_keywords = []

# 🖼️ GUI 구성
root = tk.Tk()
root.title("📬 선박중개 이메일 분류 프로그램")
root.geometry("800x580")
root.resizable(False, False)

style_font = ("맑은 고딕", 10)

# 📌 제목 키워드 입력 영역
frame_subject = tk.Frame(root)
frame_subject.pack(pady=5)
tk.Label(frame_subject, text="제목 키워드 추가:", font=style_font).grid(row=0, column=0, padx=5, sticky="e")
subject_input = tk.Entry(frame_subject, width=30)
subject_input.grid(row=0, column=1)
tk.Button(frame_subject, text="추가", command=add_subject_keyword).grid(row=0, column=2, padx=5)
tk.Label(frame_subject, text="현재 제목 키워드:", font=style_font).grid(row=1, column=0, sticky="e")
subject_display = tk.Label(frame_subject, text="", anchor="w", width=50)
subject_display.grid(row=1, column=1, columnspan=2, sticky="w")

# 📌 본문 키워드 입력 영역
frame_body = tk.Frame(root)
frame_body.pack(pady=5)
tk.Label(frame_body, text="본문 키워드 추가:", font=style_font).grid(row=0, column=0, padx=5, sticky="e")
body_input = tk.Entry(frame_body, width=30)
body_input.grid(row=0, column=1)
tk.Button(frame_body, text="추가", command=add_body_keyword).grid(row=0, column=2, padx=5)
tk.Label(frame_body, text="현재 본문 키워드:", font=style_font).grid(row=1, column=0, sticky="e")
body_display = tk.Label(frame_body, text="", anchor="w", width=50)
body_display.grid(row=1, column=1, columnspan=2, sticky="w")

# 📆 날짜 입력 (동적 필터만 사용)
frame_date = tk.Frame(root)
frame_date.pack(pady=10)
tk.Label(frame_date, text="며칠 이내 메일 검색할까요? (기본 7):", font=style_font).grid(row=0, column=0, padx=5, sticky="e")
days_entry = tk.Entry(frame_date, width=10)
days_entry.insert(0, "7")
days_entry.grid(row=0, column=1, sticky="w")

# ▶️ 동적 필터 실행 버튼 (날짜 아래)
dynamic_btn = tk.Button(root, text="▶️ 키워드로 이메일 분류", command=run_dynamic, width=30)
dynamic_btn.pack(pady=(0, 15))

# 📝 결과 출력창
output_text = scrolledtext.ScrolledText(root, width=95, height=18)
output_text.pack(padx=10, pady=10)

# ▶️ 정적 필터 실행 버튼 (로그 아래)
static_btn = tk.Button(root, text="📤 설정값 이메일 분류", command=run_static, width=30)
static_btn.pack(pady=(0, 20))

root.mainloop()
