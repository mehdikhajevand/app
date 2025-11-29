import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="فرم استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# رمز مربی (هر وقت خواستی عوض کن)
COACH_PASSWORD = "shatranj1404"

@st.cache_resource
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1aVnTmh81lUe9gtHWtt3wdb6ZDU_XGL3bg3y88NoonyY").worksheet("ورودی‌ها")
    return sheet

sheet = get_sheet()

with st.form("main_form"):
    st.header("اطلاعات فردی")
    c1, c2 = st.columns(2)
    with c1: full_name = st.text_input("نام و نام خانوادگی *")
    with c2: birth_date = st.text_input("تاریخ تولد *", placeholder="مثال: ۱۳۹۸/۰۵/۲۰")

    c3, c4 = st.columns(2)
    with c3: national_code = st.text_input("کد ملی *", max_chars=10)
    with c4: gender = st.radio("جنسیت *", ["پسر", "دختر"], horizontal=True)

    st.header("اطلاعات تماس")
    c5, c6 = st.columns(2)
    with c5: parent_name = st.text_input("نام ولی / سرپرست *")
    with c6: phone = st.text_input("شماره تماس اضطراری *", placeholder="۰۹۱۲۳۴۵۶۷۸۹")

    address = st.text_area("آدرس محل سکونت *")

    st.header("اطلاعات آموزشی / ورزشی")
    c7, c8 = st.columns(2)
    with c7:
        grade = st.selectbox("پایه تحصیلی *", ["پیش‌دبستانی","اول","دوم","سوم","چهارم","پنجم","ششم","هفتم","هشتم","نهم","دهم","یازدهم","دوازدهم"])
    with c8: school = st.text_input("نام مدرسه *")

    experience = st.radio("آیا قبلاً شطرنج کار کرده است؟ *", ["خیر", "بله"], horizontal=True)
    exp_duration = achievements = ""
    if experience == "بله":
        c9, c10 = st.columns(2)
        with c9: exp_duration = st.text_input("مدت زمان تجربه *")
        with c10: achievements = st.text_input("رتبه یا افتخارات")

    st.markdown("---")
    st.header("بخش استعدادیابی (توسط مربی تکمیل می‌شود)")
    password = st.text_input("رمز مربی", type="password")

    if password == COACH_PASSWORD:
        st.success("دسترسی مربی تأیید شد")
        focus = st.radio("سطح تمرکز", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        problem = st.radio("توانایی حل مسئله", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        learning = st.radio("یادگیری قوانین اولیه", ["سریع","معمولی","کند"], horizontal=True)
        coach_note = st.text_area("پیشنهاد مربی")
    else:
        st.info("این بخش فقط با رمز مربی قابل پر کردن است")
        focus = problem = learning = coach_note = ""

    submitted = st.form_submit_button("ثبت نهایی فرم")

    if submitted:
        if not all([full_name, birth_date, national_code, parent_name, phone, address, school]):
            st.error("همه فیلدهای ستاره‌دار اجباری هستند!")
        elif len(national_code) != 10 or not national_code.isdigit():
            st.error("کد ملی باید ۱۰ رقم باشد")
        elif not phone.startswith("09") or len(phone) != 11:
            st.error("شماره موبایل نامعتبر")
        else:
            row = [datetime.now().strftime("%Y/%m/%d %H:%M"), full_name, birth_date, national_code, gender,
                   parent_name, phone, address, grade, school, experience, exp_duration, achievements,
                   focus if password == COACH_PASSWORD else "",
                   problem if password == COACH_PASSWORD else "",
                   learning if password == COACH_PASSWORD else "",
                   coach_note if password == COACH_PASSWORD else "",
                   datetime.now().strftime("%Y/%m/%d %H:%M") if password == COACH_PASSWORD else ""]
            sheet.append_row(row)
            st.success("اطلاعات با موفقیت ثبت شد!")
            st.balloons()
