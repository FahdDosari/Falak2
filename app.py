import streamlit as st

st.set_page_config(
    page_title="المُلَقِّن اللغوي - البداية",
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
    
    /* تصميم المربعات بلون رمادي أغمق قليلاً، مع ترتيب الأيقونة بجانب النص وتفاعلية عالية */
    .stButton > button {
        width: 100% !important;
        height: 160px !important;
        background-color: #4B5563 !important; /* لون رمادي أغمق وجميل */
        color: #FFFFFF !important; /* نص أبيض لضمان الوضوح التام */
        border-radius: 20px !important;
        border: 2px solid #374151 !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.3s ease-in-out !important;
        display: flex !important;
        flex-direction: row !important; /* جعل العناصر بجانب بعضها (أفقي) */
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        gap: 12px !important; /* مسافة متناسقة بين الإيموجي والنص */
    }
    
    .stButton > button:hover {
        background-color: #374151 !important; /* درجة رمادي أغمق عند التمرير */
        border-color: #01DFD7 !important;
        transform: translateY(-6px) !important;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.25) !important;
        color: #01DFD7 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #0A192F; margin-top: 50px;'>📚 المُلَقِّن اللغوي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #0A192F; font-size: 18px; margin-bottom: 50px;'>مجمع الملك سلمان العالمي للغة العربية</p>", unsafe_allow_html=True)

col_space1, c1, c2, c3, col_space2 = st.columns([1.5, 2, 2, 2, 1.5])

with c1:
    if st.button("📖 المفردات الأكثر شيوعاً", use_container_width=True):
        st.switch_page("pages/more.py")

with c2:
    if st.button("⭐ القائمة الخاصة", use_container_width=True):
        st.switch_page("pages/spcal.py")

with c3:
    if st.button("🔍 البحث والتحليل", use_container_width=True):
        st.switch_page("pages/search.py")