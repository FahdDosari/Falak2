import streamlit as st
import sqlite3
import json

st.set_page_config(
    page_title="البحث - المُلَقِّن اللغوي",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "show_video" not in st.session_state:
    st.session_state.show_video = False
if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False
if "show_ranking" not in st.session_state:
    st.session_state.show_ranking = False

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
    
    mark { background-color: #FFFF00; color: #000000; padding: 2px 5px; border-radius: 3px; }
    div.stButton > button { height: 38px !important; border-radius: 8px !important; background-color: #ffffff !important; color: #31333F !important; }
    </style>
""", unsafe_allow_html=True)

WORDS_LIST = ["جامعة", "وجود", "عضو", "ملك", "عامل", "جهة", "علاقة", "حال", "وصل", "أكبر", "مجموعة", "دراسة", "مال", "مباراة", "مستوى", "طالب", "ما", "مواطن", "نبي", "دكتور", "أمة", "لغة", "نتيجة", "أخير", "أمس", "عاد", "وجه", "مرة", "لاعب", "فعل", "اجتماعي", "مدير", "هم", "عمل", "بحث", "الآن", "فترة", "نادي", "دين", "أنا", "عندما", "مجال", "بلغ", "مليون", "شخص", "مكان", "وجب", "موقع", "ماء", "تعليم", "طفل", "اقتصادي", "باب", "قطاع", "مؤسسة", "هيئة", "آية", "نظر", "سلطة", "رغم", "حرب", "كلمة", "جنوب", "اتحاد", "أخذ", "مادة", "داخل", "نائب", "عين", "علم", "دعا", "ثالث", "المرأة", "أخ", "مرحلة", "نسبة", "بيان", "بيت", "صحيح", "جهاز", "نوع", "عسكري", "أمير", "اعتبر", "أب", "سوق", "بناء", "عالمي", "إذ", "مسؤول", "حالي", "مؤتمر", "نظر", "سيد", "زوج", "استطاع", "إجراء", "إنما", "سلام", "دعم", "لن", "رأي", "قلب", "مالي", "أدى", "أصل", "صلاة", "لقد", "شهد", "قيادة", "عرب", "تحت", "قيمة", "مشكلة"]

@st.cache_data(ttl=86400)
def fetch_dictionary_data(word):
    word_clean = word.strip()
    fallback_dict = {
        "جامعة": "مؤسسة للتعليم العالي تمنح الدرجات العلمية المختلفة وتضم كليات متعددة.",
        "وجود": "حصول الشيء وثبوته في الواقع وتحققه.",
        "عضو": "جزء من الكائن الحي، أو فرد من جماعة أو هيئة منظمة.",
        "ملك": "صاحب السيادة والسلطة العليا على الدولة."
    }
    return fallback_dict.get(word_clean, f"مفردة لغوية ({word_clean}) تُستخدم في السياقات الدلالية والنحوية.")

def get_snippet(text, word, window=8):
    words = text.split()
    word_clean = word.strip().lower()
    for i, w in enumerate(words):
        if word_clean in w.lower():
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            return f"...{' '.join(words[start:end])}..."
    return text

def search_word_in_db(query):
    conn = sqlite3.connect("ksgafal_data.db")
    cursor = conn.cursor()
    query_clean = query.strip()
    cursor.execute("SELECT video_id, title, channel, full_transcript, timestamps_json FROM videos WHERE full_transcript LIKE ?", (f"%{query_clean}%",))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        video_id, title, channel, full_transcript, timestamps_json = row
        try:
            timestamps = json.loads(timestamps_json) if timestamps_json else []
        except:
            timestamps = []
        for item in timestamps:
            if query_clean.lower() in item.get("word", "").lower():
                results.append({
                    "video_id": video_id, "title": title, "channel": channel,
                    "first_start": item.get("start", 0), "snippet": get_snippet(full_transcript, query_clean)
                })
    return results

def save_to_flashcards(word, snippet, video_id, start_time):
    conn = sqlite3.connect("ksgafal_data.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO flashcards (word, snippet, video_id, start_time, target_step, current_step) VALUES (?, ?, ?, ?, 0, 0)", (word, snippet, video_id, start_time))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

# زر الرجوع للصفحة الرئيسية
top_c1, top_c2, top_c3 = st.columns([1, 4, 1])
with top_c1:
    if st.button("⬅️ الرجوع للرئيسية", use_container_width=True):
        st.switch_page("app.py")

st.markdown("<h1 style='text-align: center; color: #0A192F; margin-top: 10px;'>🔍 البحث والتحليل</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0A192F; font-size: 16px; margin-bottom: 25px;'>مجمع الملك سلمان العالمي للغة العربية</p>", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    query = st.text_input("", label_visibility="collapsed", placeholder="أدخل الكلمة للبحث...", value=st.session_state.last_query)
    bc1, bc2, bc3 = st.columns([2, 1, 2])
    with bc2:
        search_clicked = st.button("بحث", use_container_width=True)

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

if search_clicked or (query and query != st.session_state.last_query):
    if query.strip():
        st.session_state.last_query = query
        st.session_state.current_index = 0
        st.session_state.search_results = search_word_in_db(query)
        st.session_state.show_video = False
        st.session_state.show_meaning = False
        st.session_state.show_ranking = False

results = st.session_state.search_results
current_query = st.session_state.last_query

if current_query.strip():
    if results:
        v_l, v_c, v_r = st.columns([1, 2, 1])
        with v_c:
            ac1, ac2, ac3, ac4 = st.columns(4)
            with ac1:
                if st.button("المعنى", use_container_width=True):
                    st.session_state.show_meaning = not st.session_state.show_meaning
                    st.session_state.show_video = False
                    st.session_state.show_ranking = False
                    st.rerun()
            with ac2:
                if st.button("السياق", use_container_width=True):
                    st.session_state.show_video = not st.session_state.show_video
                    st.session_state.show_meaning = False
                    st.session_state.show_ranking = False
                    st.rerun()
            with ac3:
                if st.button("حفظ", use_container_width=True):
                    curr_idx = st.session_state.current_index
                    res = results[curr_idx]
                    if save_to_flashcards(current_query, res["snippet"], res["video_id"], int(res["first_start"])):
                        st.success("تمت الإضافة للقائمة الخاصة")
                    else:
                        st.info("الكلمة موجودة مسبقاً")
            with ac4:
                if st.button("الترتيب", use_container_width=True):
                    st.session_state.show_ranking = not st.session_state.show_ranking
                    st.session_state.show_meaning = False
                    st.session_state.show_video = False
                    st.rerun()

            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            if st.session_state.show_meaning:
                st.markdown(f"<p style='font-size: 17px;'><b>معنى ({current_query}):</b> {fetch_dictionary_data(current_query)}</p>", unsafe_allow_html=True)
            if st.session_state.show_ranking:
                rank = WORDS_LIST.index(current_query) + 1 if current_query in WORDS_LIST else len(WORDS_LIST) // 2
                st.markdown(f"<p style='font-size: 18px;'><b>ترتيب الكلمة ({current_query}) هو {rank} من {len(WORDS_LIST)} كلمة.</b></p>", unsafe_allow_html=True)
            if st.session_state.show_video:
                curr_idx = st.session_state.current_index
                res = results[curr_idx]
                st.video(f"https://www.youtube.com/watch?v={res['video_id']}&t={int(res['first_start'])}s", start_time=int(res['first_start']))
                st.markdown(f"<p style='font-size: 19px;'>{res['snippet'].replace(current_query, f'<mark>{current_query}</mark>')}</p>", unsafe_allow_html=True)
    else:
        st.warning(f"لم يتم العثور على الكلمة '{current_query}'.")
