import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# دو تا رمز کاملاً مجزا – اینجا عوضشون کن
FORM_PASSWORD   = "1234"          # رمز برای پر کردن فرم (به والدین بده)
ADMIN_PASSWORD  = "SuperSecret1404"  # رمز خیلی مهم برای دیدن داده‌ها و دانلود (فقط خودت بدون!)
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

# دیتابیس داخل حافظه
if "records" not in st.session_state:
    st.session_state.records = []

# ————————————————————
# مرحله ۱: ورود به فرم (رمز عمومی)
if "form_access" not in st.session_state:
    st.session_state.form_access = False

if not st.session_state.form_access:
    st.header("برای ورود به فرم، رمز را وارد کنید")
    pwd = st.text_input("رمز ورود به فرم", type="password")
    if st.button("ورود به فرم"):
        if pwd == FORM_PASSWORD:
            st.session_state.form_access = True
            st.success("ورود موفق! حالا می‌تونی فرم رو پر کنی")
            st.rerun()
        else:
            st.error("رمز اشتباه است!")
    st.stop()  # تا وقتی رمز درست نزنه، بقیه صفحه نشون داده نمی‌شه

# ————————————————————
# مرحله ۲: فرم عمومی (همه با رمز اول می‌تونن پر کنن)
st.success("به فرم خوش آمدی! لطفاً اطلاعات را وارد کن")
with st.form("chess_form"):
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

    exp = st.radio("تجربه قبلی شطرنج؟", ["خیر", "بله"], horizontal=True)
    exp_detail = achievements = ""
    if exp == "بله":
        c9, c10 = st.columns(2)
        exp_detail = c9.text_input("مدت تجربه")
        achievements = c10.text_input("افتخارات")

    if st.form_submit_button("ثبت نهایی"):
        if not all([name, birth, code, parent, phone, address, school]):
            st.error("همه فیلدهای ستاره‌دار اجباری است!")
        elif len(code) != 10 or not code.isdigit():
            st.error("کد ملی باید ۱۰ رقم باشد")
        elif not phone.startswith("09") or len(phone) != 11:
            st.error("شماره موبایل اشتباه است")
        else:
            st.session_state.records.append({
                "زمان": datetime.now().strftime("%Y/%m/%d - %H:%M"),
                "نام": name, "تولد": birth, "کد ملی": code, "جنسیت": gender,
                "ولی": parent, "تلفن": phone, "آدرس": address,
                "پایه": grade, "مدرسه": school, "تجربه": exp,
                "جزئیات تجربه": exp_detail, "افتخارات": achievements
            })
            st.success("ثبت شد! ممنون از شما")
            st.balloons()

# ————————————————————
# مرحله ۳: بخش ادمین (فقط با رمز دوم)
st.markdown("---")
st.header("بخش مدیریت (فقط مربی اصلی)")

admin_pwd = st.text_input("رمز مدیریت (برای دیدن و دانلود داده‌ها)", type="password")

if admin_pwd == ADMIN_PASSWORD:
    st.success("دسترسی مدیریت تأیید شد")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="دانلود تمام اطلاعات (اکسل CSV)",
            data=csv,
            file_name=f"شطرنج_استعدادیابی_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="download_admin"
        )
        
        if st.button("پاک کردن همه داده‌ها"):
            st.session_state.records = []
            st.success("همه داده‌ها پاک شد!")
            st.rerun()
    else:
        st.info("هنوز هیچ ثبت‌نامی وجود ندارد.")

elif admin_pwd:
    st.error("رمز مدیریت اشتباه است!")

st.caption("فرم ۲۴ ساعته فعال • رمز فرم: 1234 • رمز مدیریت: فقط خودت می‌دونی")
