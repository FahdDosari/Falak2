import streamlit as st

st.set_page_config(
    page_title="المفردات الأكثر شيوعاً",
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
    </style>
""", unsafe_allow_html=True)

WORDS_LIST = ["جامعة", "وجود", "عضو", "ملك", "عامل", "جهة", "علاقة", "حال", "وصل", "أكبر", "مجموعة", "دراسة", "مال", "مباراة", "مستوى", "طالب", "ما", "مواطن", "نبي", "دكتور", "أمة", "لغة", "نتيجة", "أخير", "أمس", "عاد", "وجه", "مرة", "لاعب", "فعل", "اجتماعي", "مدير", "هم", "عمل", "بحث", "الآن", "فترة", "نادي", "دين", "أنا", "عندما", "مجال", "بلغ", "مليون", "شخص", "مكان", "وجب", "موقع", "ماء", "تعليم", "طفل", "اقتصادي", "باب", "قطاع", "مؤسسة", "هيئة", "آية", "نظر", "سلطة", "رغم", "حرب", "كلمة", "جنوب", "اتحاد", "أخذ", "مادة", "داخل", "نائب", "عين", "علم", "دعا", "ثالث", "المرأة", "أخ", "مرحلة", "نسبة", "بيان", "بيت", "صحيح", "جهاز", "نوع", "عسكري", "أمير", "اعتبر", "أب", "سوق", "بناء", "عالمي", "إذ", "مسؤول", "حالي", "مؤتمر", "نظر", "سيد", "زوج", "استطاع", "إجراء", "إنما", "سلام", "دعم", "لن", "رأي", "قلب", "مالي", "أدى", "أصل", "صلاة", "لقد", "شهد", "قيادة", "عرب", "تحت", "قيمة", "مشكلة"]

# زر الرجوع للصفحة الرئيسية
top_c1, top_c2, top_c3 = st.columns([1, 4, 1])
with top_c1:
    if st.button("⬅️ الرجوع للرئيسية", use_container_width=True):
        st.switch_page("app.py")

st.markdown("<h1 style='text-align: center; color: #0A192F; margin-top: 10px;'>📚 المفردات الأكثر شيوعاً</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0A192F; font-size: 16px; margin-bottom: 25px;'>مجمع الملك سلمان العالمي للغة العربية</p>", unsafe_allow_html=True)

num_cols = 5
for i in range(0, len(WORDS_LIST), num_cols):
    row_words = WORDS_LIST[i:i + num_cols]
    cols = st.columns(num_cols)
    for j, w in enumerate(row_words):
        col_idx = num_cols - 1 - j
        with cols[col_idx]:
            if st.button(f"{i + j + 1}. {w}", key=f"w_{i}_{j}", use_container_width=True):
                st.session_state.last_query = w
                st.switch_page("pages/search.py")