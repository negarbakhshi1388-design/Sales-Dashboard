
# Online Python - IDE, Editor, Compiler, Interpreter

import streamlit as st
import pandas as pd

# ---------- تنظیمات صفحه ----------
st.set_page_config(
    page_title="Sales Analysis Dashboard 🤖",
    page_icon="📊",
    layout="wide"
)

# ---------- عنوان و توضیح ----------
st.title("🤖 Sales Analysis Dashboard")
st.write("به داشبورد تحلیلی فروش خوش آمدید! در اینجا می‌توانید فایل CSV خود را بارگذاری کرده و تحلیل‌های خودکار انجام دهید.")

# ---------- آپلود فایل ----------
file = st.sidebar.file_uploader("📂 فایل CSV خود را آپلود کنید:")

if file is not None:
    # ---------- خواندن داده ----------
    df = pd.read_csv(file)
    df.dropna(inplace=True)

    # ---------- محاسبه قیمت کل ----------
    if "unit price" in df.columns and "Quantity" in df.columns:
        df["total price"] = df["unit price"] * df["Quantity"]
    else:
        st.error("ستون‌های 'unit price' و 'Quantity' در داده وجود ندارند.")
        st.stop()

    # ---------- تبدیل ستون تاریخ ----------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        st.warning("ستون 'Date' پیدا نشد — نمودار زمانی ممکن است نمایش داده نشود.")

    # ---------- محاسبه محصولات پرفروش ----------
    if "product" in df.columns:
        top_product = df.groupby("product")["total price"].sum().sort_values(ascending=False)
        products = df["product"].unique()
        selected_product = st.sidebar.selectbox("🛍️ انتخاب محصول:", products)
        filtered = df[df["product"] == selected_product]
    else:
        st.error("ستون 'product' در داده وجود ندارد.")
        st.stop()

    # ---------- محاسبه دسته‌بندی برتر ----------
    if "category" in df.columns:
        sales_by_category = df.groupby("category")["total price"].sum().idxmax()
    else:
        sales_by_category = "N/A"
        st.warning("ستون 'category' پیدا نشد.")

    # ---------- محاسبه رشد فروش ----------
    if "store" in df.columns and "sale" in df.columns:
        df["sale_pct_change"] = df.groupby("store")["sale"].pct_change() * 100
        grow_days = df[df["sale_pct_change"] > 10]
    else:
        grow_days = pd.DataFrame()
        st.warning("ستون‌های 'store' یا 'sale' وجود ندارند، رشد فروش محاسبه نشد.")

    # ---------- بخش خلاصه آمار ----------
    st.subheader("📈 خلاصه آمار فروش")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 درآمد کل", f"${df['total price'].sum():,.2f}")
    col2.metric("🏆 پرفروش‌ترین محصول", top_product.index[0])
    col3.metric("📅 تعداد روزهای رشد >10%", len(grow_days))

    # ---------- نمایش داده ----------
    st.subheader("📋 داده‌های بارگذاری شده")
    st.dataframe(df)

    # ---------- نمودار روند فروش ----------
    if "Date" in filtered.columns:
        st.subheader(f"📊 روند فروش محصول: {selected_product}")
        st.line_chart(filtered.set_index("Date")["total price"])

    # ---------- نمودار محصولات پرفروش ----------
    st.subheader("🔥 محصولات پرفروش")
    st.bar_chart(top_product.head(10))

    # ---------- نمایش دسته برتر ----------
    st.write(f"📦 بهترین دسته از نظر فروش: **{sales_by_category}**")

    # ---------- نمایش روزهای رشد فروش ----------
    if not grow_days.empty:
        st.subheader("🚀 روزهایی با رشد بیش از 10% فروش")
        st.dataframe(grow_days)

else:
    st.info("برای شروع، از نوار کناری فایل CSV خود را بارگذاری کنید.")
