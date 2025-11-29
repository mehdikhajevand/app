import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# رمز مربی رو اینجا عوض کن (هر چی دوست داری بذار)
COACH_PASSWORD = "shatranj1404"   # ← عوضش کن!
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

# دیتابیس داخل حافظه
if "records" not in st.session_state:
    st.session_state.records = []

# فرم عمومی (همه می‌تونن پر کنن)
with st.form("public_form"):
    st.header("اطلاعات فردی")
    c1, c2 = st.columns(2)
    name = c1.text_input("نام و نام خانوادگی *")
    birth = c2.text_input("تاریخ تولد *", placeholder="مثال: ۱۳۹۸/۰۵/۲۰")

    c3, c4 = st.columns(2)
    code = c3.text_input("کد ملی *", max_chars=10)
    gender = c4.radio("جنسیت *", ["پسر", "دختر"], horizontal=True)

    st.header("اطلاعات تماس")
    c5, c6 = st.columns(2)
    parent = c5.text_input("نام ولی / سرپرست *")
    phone = c6.text_input("شماره تماس اضطراری *")

    address = st.text_area("آدرس محل سکونت *")

    st.header("اطلاعات آموزشی")
    c7, c8 = st.columns(2)
    grade = c7.selectbox("پایه تحصیلی *", ["پیش‌دبستانی","اول","دوم","سوم","چهارم","پنجم","ششم","هفتم","هشتم","نهم","دهم","یازدهم","دوازدهم"])
    school = c8.text_input("نام مدرسه *")

    exp = st.radio("تجربه قبلی شطرنج؟ *", ["خیر", "بله"], horizontal=True)
    exp_detail = achievements = ""
    if exp == "بله":
        c9, c10 = st.columns(2)
        exp_detail = c9.text_input("مدت تجربه")
        achievements = c10.text_input("افتخارات")

    submitted = st.form_submit_button("ثبت نهایی")

    if submitted:
        if not all([name, birth, code, parent, phone, address, school]):
            st.error("همه فیلدهای ستاره‌دار اجباری است!")
        elif len(code) != 10 or not code.isdigit():
            st.error("کد ملی باید ۱۰ رقم باشد")
        elif not phone.startswith("09") or len(phone) != 11:
            st.error("شماره موبایل اشتباه است")
        else:
            new = {
                "زمان": datetime.now().strftime("%Y/%m/%d - %H:%M"),
                "نام": name, "تولد": birth, "کد ملی": code, "جنسیت": gender,
                "ولی": parent, "تلفن": phone, "آدرس": address,
                "پایه": grade, "مدرسه": school, "تجربه": exp,
                "جزئیات تجربه": exp_detail, "افتخارات": achievements
            }
            st.session_state.records.append(new)
            st.success("ثبت شد! ممنون از شما")
            st.balloons()

# ————————————————————————————————
# بخش مربی — فقط با رمز باز می‌شه
st.markdown("---")
st.header("فقط برای مربی")

password_input = st.text_input("رمز عبور مربی", type="password")

if password_input == COACH_PASSWORD:
    st.success("دسترسی تأیید شد")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        # دکمه دانلود اکسل
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="دانلود تمام اطلاعات (اکسل CSV)",
            data=csv,
            file_name=f"شطرنج_استعدادیابی_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("هنوز هیچ ثبت‌نامی انجام نشده.")

    # دکمه پاک کردن همه داده‌ها (اختیاری)
    if st.button("پاک کردن همه داده‌ها"):
        st.session_state.records = []
        st.success("همه داده‌ها پاک شد!")
        st.rerun()

else:
    if password_input:  # یعنی چیزی وارد کرده ولی اشتباه بوده
        st.error("رمز اشتباه است!")
    else:
        st.info("برای دیدن داده‌ها و دانلود اکسل، رمز مربی را وارد کنید.")

st.caption("این فرم ۲۴ ساعته فعال است — نیازی به روشن بودن لپ‌تاپ نیست")
