import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# لینک API SheetDB (همونی که دادی)
API_URL = "https://sheetdb.io/api/v1/51ra5pi0utm6x"

# رمز مربی
COACH_PASSWORD = "shatranj1404"

with st.form("form"):
    st.header("اطلاعات فردی")
    col1, col2 = st.columns(2)
    full_name = col1.text_input("نام و نام خانوادگی *")
    birth_date = col2.text_input("تاریخ تولد *", placeholder="مثال: ۱۳۹۸/۰۵/۲۰")

    col3, col4 = st.columns(2)
    national_code = col3.text_input("کد ملی *", max_chars=10)
    gender = col4.radio("جنسیت *", ["پسر", "دختر"], horizontal=True)

    st.header("اطلاعات تماس")
    col5, col6 = st.columns(2)
    parent_name = col5.text_input("نام ولی / سرپرست *")
    phone = col6.text_input("شماره تماس اضطراری *", placeholder="۰۹۱۲۳۴۵۶۷۸۹")

    address = st.text_area("آدرس محل سکونت *")

    st.header("اطلاعات آموزشی / ورزشی")
    col7, col8 = st.columns(2)
    grade = col7.selectbox("پایه تحصیلی *", [
        "پیش‌دبستانی", "اول", "دوم", "سوم", "چهارم", "پنجم", "ششم",
        "هفتم", "هشتم", "نهم", "دهم", "یازدهم", "دوازدهم"
    ])
    school_name = col8.text_input("نام مدرسه *")

    has_experience = st.radio("آیا قبلاً شطرنج کار کرده است؟ *", ["خیر", "بله"], horizontal=True)
    experience_duration = ""
    achievements = ""
    if has_experience == "بله":
        col9, col10 = st.columns(2)
        experience_duration = col9.text_input("مدت زمان تجربه *", placeholder="مثال: ۲ سال")
        achievements = col10.text_area("رتبه یا افتخارات")

    st.markdown("---")
    st.header("بخش استعدادیابی (توسط مربی تکمیل می‌شود)")
    password = st.text_input("رمز مربی", type="password")

    if password == COACH_PASSWORD:
        st.success("دسترسی مربی تأیید شد ✅")
        focus_level = st.radio("سطح تمرکز", ["عالی", "خوب", "متوسط", "نیازمند تقویت"], horizontal=True)
        problem_solving = st.radio("توانایی حل مسئله", ["عالی", "خوب", "متوسط", "نیازمند تقویت"], horizontal=True)
        learning_speed = st.radio("یادگیری قوانین اولیه", ["سریع", "معمولی", "کند"], horizontal=True)
        coach_suggestion = st.text_area("پیشنهاد مربی", placeholder="مثال: استعداد بالا - پیشنهاد کلاس پیشرفته")
    else:
        st.info("این بخش فقط توسط مربی و با رمز قابل تکمیل است.")
        focus_level = problem_solving = learning_speed = coach_suggestion = ""

    submitted = st.form_submit_button("ثبت نهایی فرم")

    if submitted:
        # چک فیلدهای اجباری
        required_fields = [full_name, birth_date, national_code, parent_name, phone, address, school_name]
        if has_experience == "بله":
            required_fields.append(experience_duration)
        if not all(required_fields):
            st.error("⚠️ لطفاً همه فیلدهای ستاره‌دار (*) را پر کنید!")
        elif len(national_code) != 10 or not national_code.isdigit():
            st.error("⚠️ کد ملی باید ۱۰ رقم باشد!")
        elif len(phone) != 11 or not phone.startswith("09"):
            st.error("⚠️ شماره موبایل باید ۱۱ رقمی و با ۰۹ شروع شود!")
        else:
            # داده‌ها رو آماده کن
            data = {
                "زمان_ثبت": datetime.now().strftime("%Y/%m/%d - %H:%M"),
                "نام_و_نام_خانوادگی": full_name,
                "تاریخ_تولد": birth_date,
                "کد_ملی": national_code,
                "جنسیت": gender,
                "نام_ولی_سرپرست": parent_name,
                "شماره_تماس_اضطراری": phone,
                "آدرس_محل_سکونت": address,
                "پایه_تحصیلی": grade,
                "نام_مدرسه": school_name,
                "تجربه_قبلی_شطرنج": has_experience,
                "مدت_زمان_تجربه": experience_duration if has_experience == "بله" else "",
                "رتبه_یا_افتخارات": achievements,
                "سطح_تمرکز": focus_level if password == COACH_PASSWORD else "",
                "توانایی_حل_مسئله": problem_solving if password == COACH_PASSWORD else "",
                "یادگیری_قوانین_اولیه": learning_speed if password == COACH_PASSWORD else "",
                "پیشنهاد_مربی": coach_suggestion if password == COACH_PASSWORD else ""
            }

            # ارسال به SheetDB
            try:
                response = requests.post(API_URL, json={"data": [data]})
                if response.status_code in [200, 201]:
                    st.success("✅ فرم با موفقیت ثبت شد! اطلاعات در گوگل شیت ذخیره شد.")
                    st.balloons()
                else:
                    st.error(f"⚠️ خطا در ذخیره: {response.status_code} - {response.text[:200]}...")
                    st.info("اگر SheetDB مشکل داره، API رو دوباره بسازید: https://sheetdb.io")
            except Exception as e:
                st.error(f"⚠️ مشکل اتصال به API: {str(e)}")
                st.info("راه‌حل: API رو در sheetdb.io بروز کنید یا شیت رو چک کنید.")

# بخش نمایش داده‌ها (برای مربی)
st.markdown("---")
if st.checkbox("نمایش تمام ثبت‌نام‌ها (مربی)"):
    try:
        get_response = requests.get(API_URL)
        if get_response.status_code == 200:
            data_list = get_response.json()
            if data_list:
                df = pd.DataFrame(data_list)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("هنوز ثبت‌نامی وجود ندارد.")
        else:
            st.warning(f"خطا در بارگیری: {get_response.status_code}")
    except Exception as e:
        st.error(f"مشکل در بارگیری داده‌ها: {str(e)}")
