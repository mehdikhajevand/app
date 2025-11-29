import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# رمز مربی
COACH_PASSWORD = "shatranj1404"

# فایل اکسل در حافظه (هر بار بروزرسانی می‌شه)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "زمان ثبت", "نام", "تولد", "کد ملی", "جنسیت", "ولی", "تلفن", "آدرس",
        "پایه", "مدرسه", "تجربه", "مدت تجربه", "افتخارات",
        "تمرکز", "حل مسئله", "یادگیری", "پیشنهاد مربی"
    ])

with st.form("form"):
    st.header("اطلاعات فردی")
    c1, c2 = st.columns(2)
    name = c1.text_input("نام و نام خانوادگی *")
    birth = c2.text_input("تاریخ تولد *", placeholder="۱۳۹۸/۰۵/۲۰")

    c3, c4 = st.columns(2)
    code = c3.text_input("کد ملی *", max_chars=10)
    gender = c4.radio("جنسیت *", ["پسر", "دختر"], horizontal=True)

    st.header("اطلاعات تماس")
    c5, c6 = st.columns(2)
    parent = c5.text_input("نام ولی / سرپرست *")
    phone = c6.text_input("شماره تماس اضطراری *", placeholder="۰۹۱۲۳۴۵۶۷۸۹")

    address = st.text_area("آدرس محل سکونت *")

    st.header("اطلاعات آموزشی / ورزشی")
    c7, c8 = st.columns(2)
    grade = c7.selectbox("پایه تحصیلی *", ["پیش‌دبستانی","اول","دوم","سوم","چهارم","پنجم","ششم","هفتم","هشتم","نهم","دهم","یازدهم","دوازدهم"])
    school = c8.text_input("نام مدرسه *")

    exp = st.radio("آیا قبلاً شطرنج کار کرده؟ *", ["خیر", "بله"], horizontal=True)
    exp_time = exp_rank = ""
    if exp == "بله":
        c9, c10 = st.columns(2)
        exp_time = c9.text_input("مدت تجربه *")
        exp_rank = c10.text_input("رتبه یا افتخارات")

    st.markdown("---")
    st.header("بخش استعدادیابی (فقط مربی)")
    pwd = st.text_input("رمز مربی", type="password")

    if pwd == COACH_PASSWORD:
        st.success("مربی تأیید شد")
        focus = st.radio("سطح تمرکز", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        solve = st.radio("حل مسئله", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        learn = st.radio("یادگیری قوانین", ["سریع","معمولی","کند"], horizontal=True)
        note = st.text_area("پیشنهاد مربی")
    else:
        st.info("این بخش فقط با رمز مربی باز می‌شه")
        focus = solve = learn = note = ""

    if st.form_submit_button("ثبت فرم"):
        if not all([name, birth, code, parent, phone, address, school]):
            st.error("فیلدهای * اجباری‌اند")
        elif len(code) != 10 or not code.isdigit():
            st.error("کد ملی ۱۰ رقم")
        elif not phone.startswith("09") or len(phone) != 11:
            st.error("شماره موبایل اشتباه")
        else:
            # اضافه کردن به دیتافریم
            new_row = {
                "زمان ثبت": datetime.now().strftime("%Y/%m/%d %H:%M"),
                "نام": name, "تولد": birth, "کد ملی": code, "جنسیت": gender,
                "ولی": parent, "تلفن": phone, "آدرس": address,
                "پایه": grade, "مدرسه": school, "تجربه": exp,
                "مدت تجربه": exp_time, "افتخارات": exp_rank,
                "تمرکز": focus if pwd == COACH_PASSWORD else "",
                "حل مسئله": solve if pwd == COACH_PASSWORD else "",
                "یادگیری": learn if pwd == COACH_PASSWORD else "",
                "پیشنهاد مربی": note if pwd == COACH_PASSWORD else ""
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
            
            # نمایش جدول بروزرسانی‌شده
            st.success("ثبت شد! اطلاعات زیر ذخیره شد:")
            st.dataframe(st.session_state.df.tail(1))  # فقط ردیف جدید رو نشون می‌ده
            
            # دکمه دانلود اکسل
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state.df.to_excel(writer, index=False, sheet_name='استعدادیابی')
            st.download_button(
                label="دانلود فایل اکسل کامل",
                data=output.getvalue(),
                file_name=f"استعدادیابی_شطرنج_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.balloons()

# نمایش کل جدول (برای مربی)
if st.checkbox("نمایش تمام ثبت‌نام‌ها (مربی)"):
    st.dataframe(st.session_state.df)
