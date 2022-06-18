import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
#セレクトボックスのリストを作成
pagelist = ["ヒストグラム","担当者","図番","工程"]
st.title("生産データ分析")
#製造データの取り込み
st.title("製造データファイル")
uploaded_file=st.file_uploader("製造データの取り込み",type="xlsx")
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
#サイドバーのセレクトボックスを配置
selector=st.sidebar.selectbox( "ページ選択",pagelist)
#ヒストグラムの画面
if selector=="ヒストグラム":
    st.dataframe(df)
    #標準時間の取り込み
    st.title("標準時間ファイル")
    uploaded_file=st.file_uploader("標準時間の取り込み",type="xlsx")
    if uploaded_file is not None:
        df_time=pd.read_excel(uploaded_file)
    base_time = pd.to_datetime('00:00:0', format='%M:%S:%f')
    df_time['標準時間']=pd.to_datetime(df_time['標準時間'], format='%M:%S:%f') - base_time
    df_time['標準時間']=df_time["標準時間"].dt.total_seconds()
    df_time['標準時間']=df_time["標準時間"]
    st.dataframe(df_time)
    #図番の選択
    z_list = sorted(list(set(df["図番"])))
    z = st.selectbox(
         "図番",
         (z_list))
    x=df[(df["図番"]==z)]#dfからzで選んだ図番のデータ
    #工程の選択
    k_list = sorted(list(set(x["工程コード"])))
    k = st.selectbox(
         "工程コード",
         (k_list))
    x=df[(df["図番"]==z)&(df["工程コード"] == k)]#dfからz,kで選んだ図番,工程のデータ
    #担当の選択
    t_list = sorted(list(set(x["担当コード"])))
    t = st.multiselect(
         "担当コード",
         (t_list))
    #データの整理
#     scores=df[(df["図番"]==z)&(df["工程コード"]==k)&(df["担当コード"]==t)]#選択したデータ
#     dd=scores["処理時間"]#選択したデータの処理時間
    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        for i in range(len(t)):
            st.write(t[i])
#         st.dataframe(scores)
        
#         # 描画領域を用意する
#         fig = plt.figure()
#         ax = fig.add_subplot()
#         ax.hist(dd, bins=10)
#         # Matplotlib の Figure を指定して可視化する
#         st.pyplot(fig)
        
#担当者の画面
elif selector=="担当者":
    t_list = sorted(list(set(df["担当コード"])))
    t = st.selectbox(
         "担当コード",
         (t_list))
    t_num=df[(df["担当コード"]==t)]
    num=pd.DataFrame(t_num.groupby(['担当コード',"図番","工程コード"])['処理時間'].agg(["count","mean", "std", "min", "max"]))
    pvit=num.set_axis(['件数', '平均', '標準偏差', '最小', '最大'], axis=1)
    pvit=pvit.round(1)   # 小数第1位まで．2位を切り捨て
    answer = st.button('分析開始')
    if answer == True:
        st.dataframe(t_num)
        st.dataframe(pvit)
        st.table(pvit)
        
#図番の画面
elif selector=="図番":
    z_list = sorted(list(set(df["図番"])))
    z = st.selectbox(
         "図番",
         (z_list))
    z_num=df[(df["図番"]==z)]
    num=pd.DataFrame(z_num.groupby(["図番","工程コード",'担当コード'])['処理時間'].agg(["count","mean", "std", "min", "max"]))
    pvit=num.set_axis(['件数', '平均', '標準偏差', '最小', '最大'], axis=1)
    pvit=pvit.round(1)   # 小数第1位まで．2位を切り捨て
    answer = st.button('分析開始')
    if answer == True:
        st.dataframe(z_num)
        st.dataframe(pvit)
        st.table(pvit)
        
#工程の画面
elif selector=="工程":
    k_list = sorted(list(set(df["工程コード"])))
    k = st.selectbox(
         "工程コード",
         (k_list))
    k_num=df[(df["工程コード"]==k)]
    num=pd.DataFrame(k_num.groupby(["工程コード","図番",'担当コード'])['処理時間'].agg(["count","mean", "std", "min", "max"]))
    pvit=num.set_axis(['件数', '平均', '標準偏差', '最小', '最大'], axis=1)
    pvit=pvit.round(1)   # 小数第1位まで．2位を切り捨て
    answer = st.button('分析開始')
    if answer == True:
        st.dataframe(k_num)
        st.dataframe(pvit)
        st.table(pvit)
        # 描画領域を用意する
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.hist(pvit)
        # Matplotlib の Figure を指定して可視化する
        st.pyplot(fig)
