import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- 設定 ----------
DATA_FILE = "homework_data.csv"

# 讀取或建立資料檔
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["subject", "title", "due_date", "status"])

# ---------- UI ----------
st.set_page_config(page_title="作業追蹤器", layout="wide")
st.title("📚 作業追蹤器 Homework Tracker")
st.info(
    "可以記錄作業、查看狀態統計，方便學生管理作業進度。"
)

# --- 新增作業 ---
with st.expander("✚ 新增作業"):
    with st.form("add_form"):
        subject = st.text_input("科目")
        title = st.text_input("作業標題")
        due_date = st.date_input("截止日期", value=datetime.now().date())
        status = st.selectbox("狀態", ["Pending", "In Progress", "Completed"])
        submitted = st.form_submit_button("新增作業")
        if submitted:
            new_row = pd.DataFrame({
                "subject": [subject],
                "title": [title],
                "due_date": [due_date.strftime("%Y-%m-%d")],
                "status": [status]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ 新增成功！")

# --- 顯示作業清單 ---
st.subheader("📋 作業清單")
if df.empty:
    st.info("目前沒有任何作業，請先新增一筆。")
else:
    df_display = df.copy()
    # 使用 errors='coerce' 避免無效日期造成錯誤
    df_display["due_date"] = pd.to_datetime(df_display["due_date"], errors='coerce').dt.strftime("%Y-%m-%d")
    st.dataframe(df_display[["subject", "title", "due_date", "status"]], use_container_width=True)

    st.markdown("---")
    st.subheader("📊 作業統計圖表")

    # 狀態統計
    st.write("### 作業狀態分佈")
    st.bar_chart(df["status"].value_counts())

    # 各科未完成數
    st.write("### 各科未完成作業數")
    unfinished = df[df["status"] != "Completed"]
    if not unfinished.empty:
        st.bar_chart(unfinished["subject"].value_counts())
    else:
        st.info("目前所有作業都已完成！👏")
