import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="استعدادیابی شطرنج", layout="centered")
st.title("فرم ثبت‌نام و استعدادیابی شطرنج")
st.markdown("---")

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# دو تا رمز مجزا — اینجا عوض کن
COACH_PASSWORD   = "coach1404"        # رمز مربی‌ها برای پر کردن بخش ارزیابی
ADMIN_PASSWORD   = "SuperBoss2025"    # رمز فقط خودت برای دیدن همه چیز و دانلود
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

if "records" not in st.session_state:
    st.session_state.records = []

# ========================================
# فرم عمومی — بدون رمز — همه می‌بینن
# ========================================
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

    exp = st.radio("تجربه قبلی شطرنج؟", ["خیر", "بله"], horizontal=True)
    exp_detail = achievements = ""
    if exp == "بله":
        c9, c10 = st.columns(2)
        exp_detail = c9.text_input("مدت تجربه")
        achievements = c10.text_input("افتخارات")

    # بخش ارزیابی مربی — فقط با رمز اول باز می‌شه
    st.markdown("---")
    st.subheader("ارزیابی مربی (اختیاری)")
    coach_pwd = st.text_input("رمز مربی (برای پر کردن ارزیابی)", type="password", key="coach_input")

    if coach_pwd == COACH_PASSWORD:
        st.success("مربی تأیید شد — بخش ارزیابی فعال شد")
        focus = st.radio("سطح تمرکز", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        problem = st.radio("توانایی حل مسئله", ["عالی","خوب","متوسط","نیازمند تقویت"], horizontal=True)
        learn = st.radio("یادگیری قوانین اولیه", ["سریع","معمولی","کند"], horizontal=True)
        note = st.text_area("پیشنهاد و یادداشت مربی")
    elif coach_pwd:
        st.error("رمز مربی اشتباه است!")
        focus = problem = learn = note = ""
    else:
        st.info("برای پر کردن بخش ارزیابی، رمز مربی را وارد کنید")
        focus = problem = learn = note = ""

    if st.form_submit_button("ثبت نهایی فرم"):
        if not all([name, birth, code, parent, phone, address, school]):
            st.error("فیلدهای ستاره‌دار اجباری است!")
        elif len(code) != 10 or not code.isdigit():
            st.error("کد ملی باید ۱۰ رقم باشد")
        elif not phone.startswith("09") or len(phone) != 11:
            st.error("شماره موبایل اشتباه است")
        else:
            st.session_state.records.append({
                "زمان": datetime.now().strftime("%Y/%m/%d %H:%M"),
                "نام": name, "تولد": birth, "کد_ملی": code, "جنسیت": gender,
                "ولی": parent, "تلفن": phone, "آدرس": address,
                "پایه": grade, "مدرسه": school, "تجربه": exp,
                "مدت_تجربه": exp_detail, "افتخارات": achievements,
                "تمرکز": focus if coach_pwd == COACH_PASSWORD else "",
                "حل_مسئله": problem if coach_pwd == COACH_PASSWORD else "",
                "یادگیری": learn if coach_pwd == COACH_PASSWORD else "",
                "یادداشت_مربی": note if coach_pwd == COACH_PASSWORD else ""
            })
            st.success("ثبت شد! ممنون از همکاری")
            st.balloons()

# ========================================
# بخش مدیریت — فقط با رمز دوم
# ========================================
st.markdown("---")
st.header("مدیریت و دانلود داده‌ها (فقط ادمین)")

admin_pwd = st.text_input("رمز مدیریت (برای دیدن و دانلود همه داده‌ها)", type="password", key="admin_input")

if admin_pwd == ADMIN_PASSWORD:
    st.success("ادمین تأیید شد — دسترسی کامل")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="دانلود تمام اطلاعات به صورت اکسل",
            data=csv,
            file_name=f"استعدادیابی_شطرنج_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        if st.button("پاک کردن تمام داده‌ها"):
            st.session_state.records = []
            st.rerun()
    else:
        st.info("هنوز هیچ ثبت‌نامی وجود ندارد.")

elif admin_pwd:
    st.error("رمز مدیریت اشتباه است!")

st.caption("فرم ۲۴ ساعته فعال • بدون نیاز به روشن بودن لپ‌تاپ")
