import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math as math
import numpy as np

st.set_page_config(layout="wide")
#セレクトボックスのリストを作成
pagelist = ["ヒストグラム","担当者","図番","工程","一日のデータ"]
st.title("生産データ分析")
#製造データの取り込み
st.title("製造データファイル")
uploaded_file=st.file_uploader("製造データの取り込み",type="xlsx")
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
#サイドバーのセレクトボックスを配置
selector=st.sidebar.selectbox( "ページ選択",pagelist)
#ヒストグラムの画面
if selector=="ヒストグラム":#===============================================================================================
    
    #標準時間の取り込み
    st.title("標準時間ファイル")
    uploaded_file=st.file_uploader("標準時間の取り込み",type="xlsx")
    if uploaded_file is not None:
        df_time=pd.read_excel(uploaded_file)
    base_time = pd.to_datetime('00:00:0', format='%M:%S:%f')
    df_time['標準時間']=pd.to_datetime(df_time['標準時間'], format='%M:%S:%f') - base_time
    df_time['標準時間']=df_time["標準時間"].dt.total_seconds()
    
    #図番の選択
    z_list = sorted(list(set(df["図番"])))
    z = st.selectbox(
         "図番",
         (z_list))
    x_num=df[(df["図番"]==z)]#dfからzで選んだ図番のデータ
    #工程の選択
    k_list = sorted(list(set(x_num["工程コード"])))
    k = st.selectbox(
         "工程コード",
         (k_list))
    x_num=df[(df["図番"]==z)&(df["工程コード"] == k)]#dfからz,kで選んだ図番,工程のデータ
    #担当の選択
    t_list = sorted(list(set(x_num["担当コード"])))
    t = st.multiselect(
         "担当コード",
         (t_list))

    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        #上限値、下限値のdata
        data_num=df[(df["図番"]==z)&(df["工程コード"]==k)]
        dosu_num=0
        
        for t_num in t_list:
            y_num=df[(df["図番"]==z)&(df["工程コード"]==k)&(df["担当コード"] == t_num)]
            y_num=y_num["処理時間"]
            #y軸の上限値
            x,y,_= plt.hist(y_num)
            if dosu_num<max(x):#tが2個以上の時に比較する
                dosu_num=max(x)
        
        #処理時間の抜き出し
        data_num=data_num.rename(columns={'処理時間': 'processing_time'}) 
        s_num=data_num['processing_time']
        
        # 描画領域を用意する
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.boxplot(s_num)#箱髭図作成
        # Matplotlib の Figure を指定して可視化する
        st.pyplot(fig)
        
        st.write(data_num['processing_time'].describe())#データの詳細データ
                
        q1=data_num['processing_time'].describe().loc['25%']#第一四分位範囲
        q3=data_num['processing_time'].describe().loc['75%']#第三四分位範囲
                
        iqr=q3-q1#四分位範囲
        upper_num=q3+(1.5*iqr)#上限
        lower_num=q1-(1.5*iqr)#下限
        upper_num2=round(upper_num) #きりあげ
        lower_num2=math.floor(lower_num)#きりおとし
        dif_num=upper_num2-lower_num2#差
                
        if dif_num%10!=0:#もし切り上げ切り落としした差が10で割れなかった
            dif_num2=math.ceil((dif_num/10))*10
        dif_num3=(dif_num2-dif_num)/2
        upper_num2=upper_num2+dif_num3
        lower_num2=lower_num2-dif_num3
                
        hazure=data_num[data_num["processing_time"]<=upper_num]
        hazure=hazure[hazure["processing_time"]>=lower_num]
        
        
        st.write('第一四分位数は%.1fです'%q1)
        st.write('第三四分位数は%.1fです'%q3)
        st.write('四分位範囲は%.1fです'%iqr)
        st.write('上限値は%.1fです'%upper_num)
        st.write('下限値は%.1fです'%lower_num)
        st.write('差は%.1fです'%dif_num)
        st.write('差は%.1fです'%dif_num2)
        st.write('外れてない数の割合は%d/%dです'%(len(hazure),len(data_num)))
        st.write('上限値は%.1fです'%upper_num2)
        st.write('下限値は%.1fです'%lower_num2)
        
        #ヒストグラムの作成
        for i in t:
            #データの整理
            scores=hazure[(hazure["図番"]==z)&(hazure["工程コード"]==k)&(hazure["担当コード"]==i)]#選択したデータ
            y_scores=df_time[(df_time["図番"]==z)&(df_time["工程コード"] ==k)]
            hyozyun=y_scores["標準時間"]
            #はずれちの除外
#             dd=scores[scores["処理時間"]<upper_num]
#             dd=dd[dd["処理時間"]>lower_num]
            dd=scores["processing_time"]#選択したデータの処理時間
            
            # 描画領域を用意する
            fig = plt.figure()
            ax = fig.add_subplot()
            
            plt.xlim([0,upper_num2])                        # X軸範囲
            plt.ylim([0,dosu_num+10])                      # Y軸範囲
            ax.set_title("chart")
            ax.set_xlabel("time")                # x軸ラベル
            plt.ylabel("count")               # y軸ラベル
            plt.grid(True)
            plt.axvline(x=int(hyozyun),color = "crimson")#標準時間の表記（赤軸）
            plt.xticks(np.arange(lower_num2, upper_num2,dif_num2/10))
            
            ax.hist(dd,bins=10,range=(lower_num2,upper_num2),rwidth=dif_num2/10)
            # Matplotlib の Figure を指定して可視化する
            st.write("---------------このグラフのデータ個数：",len(dd),"-------------担当コード：",i,"-----------------------")
            st.pyplot(fig)
        #===============================================================================================================================(ヒストグラムの設定)
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
        
        st.dataframe(pvit)
        st.table(pvit)
 
#工程の画面
elif selector=="一日のデータ":
    #標準時間の取り込み
    st.title("標準時間ファイル")
    uploaded_file=st.file_uploader("標準時間の取り込み",type="xlsx")
    if uploaded_file is not None:
        df_time=pd.read_excel(uploaded_file)
    base_time = pd.to_datetime('00:00:0', format='%M:%S:%f')
    df_time['標準時間']=pd.to_datetime(df_time['標準時間'], format='%M:%S:%f') - base_time
    df_time['標準時間']=df_time["標準時間"].dt.total_seconds()
    
    #担当の選択
    t_list = sorted(list(set(df["担当コード"])))
    t = st.selectbox(
         "担当コード",
         (t_list))
    k_list = sorted(list(set(df["工程コード"])))
    z_list = sorted(list(set(df["図番"])))
    
    
    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        
        for z in z_list:
            for k in k_list:
                data_num=df[(df["図番"]==z)&(df["工程コード"]==k)]
                dosu_num=0
                
                y_num=df[(df["図番"]==z)&(df["工程コード"]==k)&(df["担当コード"] == t)]
                y_num=y_num["処理時間"]
                #y軸の上限値
                x,y,_= plt.hist(y_num)
                if dosu_num<max(x):#tが2個以上の時に比較する
                    dosu_num=max(x)
                    
                data_num=data_num.rename(columns={'処理時間': 'processing_time'}) 
                s_num=data_num['processing_time']
                    
                q1=data_num['processing_time'].describe().loc['25%']#第一四分位範囲
                q3=data_num['processing_time'].describe().loc['75%']#第三四分位範囲
                
                iqr=q3-q1#四分位範囲
                upper_num=q3+(1.5*iqr)#上限
                lower_num=q1-(1.5*iqr)#下限
                upper_num2=round(upper_num) #きりあげ
                lower_num2=math.floor(lower_num)#きりおとし
                dif_num=upper_num2-lower_num2#差
                    
                if dif_num%10!=0:#もし切り上げ切り落としした差が10で割れなかった
                    dif_num2=math.ceil((dif_num/10))*10
                dif_num3=(dif_num2-dif_num)/2
                upper_num2=upper_num2+dif_num3
                lower_num2=lower_num2-dif_num3
                
                hazure=data_num[data_num["processing_time"]<=upper_num]
                hazure=hazure[hazure["processing_time"]>=lower_num]
        
                    #ヒストグラムの作成
                #データの整理
                scores=hazure[(hazure["図番"]==z)&(hazure["工程コード"]==k)&(hazure["担当コード"]==i)]#選択したデータ
                y_scores=df_time[(df_time["図番"]==z)&(df_time["工程コード"] ==k)]
                hyozyun=y_scores["標準時間"]
                dd=scores["processing_time"]#選択したデータの処理時間
            
                #描画領域を用意する
                fig = plt.figure()
                ax = fig.add_subplot()

                plt.xlim([0,upper_num2])                        # X軸範囲
                plt.ylim([0,dosu_num+10])                      # Y軸範囲
                ax.set_title("chart")
                ax.set_xlabel("time")                # x軸ラベル
                plt.ylabel("count")               # y軸ラベル
                plt.grid(True)
                plt.axvline(x=int(hyozyun),color = "crimson")#標準時間の表記（赤軸）
                plt.xticks(np.arange(lower_num2, upper_num2,dif_num2/10))

                ax.hist(dd,bins=10,range=(lower_num2,upper_num2),rwidth=dif_num2/10)
                # Matplotlib の Figure を指定して可視化する
                st.write("---------------工程コード:",k,"-------------図番:",z,"-----------------------")
                st.pyplot(fig)
          #===============================================================================================================================(ヒストグラムの設定)

