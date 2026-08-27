import streamlit as st
import sqlite3

st.set_page_config(
    page_title="القائمة الخاصة",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    html, body, .stApp { overflow-x: hidden !important; }
    html, body, [class*="css"], button, input, textarea, div, span, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Calibri', 'Segoe UI', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #01DFD7; }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu, header, footer, .stDeployButton { visibility: hidden !important; display: none !important; }
    
    div.stButton > button { height: 38px !important; border-radius: 8px !important; background-color: #ffffff !important; color: #31333F !important; }
    .anki-card { background-color: #ffffff; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

def get_due_flashcards():
    conn = sqlite3.connect("ksgafal_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, word, snippet, video_id, start_time, target_step, current_step FROM flashcards ORDER BY current_step DESC, id ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_flashcards_count():
    conn = sqlite3.connect("ksgafal_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM flashcards")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def update_flashcard_review(card_id, choice):
    conn = sqlite3.connect("ksgafal_data.db")
    cursor = conn.cursor()
    if choice == "never":
        cursor.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    else:
        step_delay = 5 if choice == "five" else 10
        cursor.execute("UPDATE flashcards SET current_step = current_step + 1 WHERE id != ?", (card_id,))
        cursor.execute("UPDATE flashcards SET target_step = ?, current_step = 0 WHERE id = ?", (step_delay, card_id))
    conn.commit()
    conn.close()

# زر الرجوع للصفحة الرئيسية
top_c1, top_c2, top_c3 = st.columns([1, 4, 1])
with top_c1:
    if st.button("⬅️ الرجوع للرئيسية", use_container_width=True):
        st.switch_page("app.py")

st.markdown("<h1 style='text-align: center; color: #0A192F; margin-top: 10px;'>⭐ القائمة الخاصة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0A192F; font-size: 16px; margin-bottom: 25px;'>مجمع الملك سلمان العالمي للغة العربية</p>", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    due_cards = get_due_flashcards()
    total_count = get_total_flashcards_count()

    if not due_cards or total_count == 0:
        st.info("🎉 لا توجد بطاقات محفوظة حالياً!")
    else:
        card_id, word, snippet, video_id, start_time, _, _ = due_cards[0]
        st.markdown(f"<h5 style='text-align: center; margin-bottom: 15px;'>يوجد {total_count} كلمات محفوظة، والكلمة الحالية هي:</h5>", unsafe_allow_html=True)
        st.markdown(f"<div class='anki-card'><h2>{word}</h2></div>", unsafe_allow_html=True)

        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("المعنى", use_container_width=True):
                st.session_state.show_m = not st.session_state.get("show_m", False)
                st.rerun()
        with bc2:
            if st.button("السياق", use_container_width=True):
                st.session_state.show_v = not st.session_state.get("show_v", False)
                st.rerun()

        if st.session_state.get("show_m", False):
            st.markdown(f"<p style='font-size: 17px;'><b>معنى الكلمة:</b> مفردة لغوية ({word}) دالة في سياقها.</p>", unsafe_allow_html=True)
        if st.session_state.get("show_v", False):
            st.video(f"https://www.youtube.com/watch?v={video_id}&t={start_time}s", start_time=start_time)
            st.markdown(f"<p style='font-size: 19px;'>{snippet.replace(word, f'<mark>{word}</mark>')}</p>", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            if st.button("سهل", use_container_width=True):
                update_flashcard_review(card_id, "never")
                st.rerun()
        with rc2:
            if st.button("متوسط", use_container_width=True):
                update_flashcard_review(card_id, "five")
                st.rerun()
        with rc3:
            if st.button("صعب", use_container_width=True):
                update_flashcard_review(card_id, "ten")
                st.rerun()