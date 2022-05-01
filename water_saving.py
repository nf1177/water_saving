import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import time

# データの読みこみ
data = pd.read_csv("water_saving_chart.csv")

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="エコアクア：節水測定",
                   page_icon=":potable_water:", layout="wide")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- スライドバー ----
st.sidebar.write("""## 以下の情報を入力してください""")
industry = st.sidebar.selectbox('業種を選択してください。：', data["industry"].unique())
types = st.sidebar.selectbox('蛇口／シャワーどちらを利用していますか？：', data["types"].unique())
momentum = st.sidebar.selectbox(
    '水の流量の強さはどれくらいでしょうか？：', data["momentum"].unique())
num_faucet = st.sidebar.number_input('何箇所に設置していますか？', 0, 100, 10)
water_charges = st.sidebar.number_input(
    '月の水道の使用料金はいくらでしょうか？', 0, 1000000, 100000)

# ---- 節水効果 ----
df_selection = data.query(
    "industry == @industry & types ==@types & momentum == @momentum")


# TOP KPI's
print(df_selection["saving_rate"].sum()*100)
average_rating = df_selection["saving_rate"].sum()
str_average_rating = str(round(df_selection["saving_rate"].sum()*100, 0))


tree = ":deciduous_tree:" * int(round(average_rating, 0))
price = "{:,}".format(round(water_charges * average_rating))

st.header("エコアクア：ATOM節水効果試算")

st.write("""記入いただいた箇所以外にお手洗い、洗濯機等を利用いただいている場合、
その使用量によって、節水金額は異なります。詳細な節水効果の測定をご希望の場合は株式会社エコアクアまでご連絡ください。""")

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'節水率計算中：{i+1}%')
    bar.progress(i+1)
    time.sleep(0.01)

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("節水率：")
        st.subheader(f"{str_average_rating}%")
    with right_column:
        st.subheader("節水金額：")
        st.subheader(f"{price} 円")
