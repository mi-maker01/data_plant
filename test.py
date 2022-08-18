import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import math as math
import numpy as np

import plotly.express as px
import plotly.io as pio
import datetime

import plotly.graph_objects as go


st.set_page_config(layout="wide")
#セレクトボックスのリストを作成
pagelist = ["(A-1)各人各日の実績ガントチャート","（A-2）各工程各日の実績ガントチャート","（B）同一人物の同一行程でのばらつきの把握_ヒストグラム","（C）同一行程内のばらつき把握_ヒストグラム","（D）一つの製品の総社内滞在時間の把握_折れ線グラフ","（E）担当者別作業時間統計量","（E）図番別作業時間統計量","（E）工程別作業時間統計量","（E）各人の工程量"]
st.title("生産データ分析")
#製造データの取り込み
st.title("製造データファイル")
uploaded_file=st.file_uploader("製造データの取り込み",type="xlsx")
if uploaded_file is not None:
    df=pd.read_excel(uploaded_file)
#サイドバーのセレクトボックスを配置
selector=st.sidebar.selectbox( "ページ選択",pagelist)
#================================================================================================================================
if selector=="(A-1)各人各日の実績ガントチャート":
    t_list = sorted(list(set(df["担当コード"])))
    t = st.selectbox(
         "担当コード",
         (t_list))
    
    t_num=df[(df["担当コード"]==t)]
    day_num = sorted(list(set(t_num["工程完了日"])))
    d = st.selectbox(
         "工程完了日",
         (day_num))
    
    d_num=t_num[(t_num["工程完了日"]==d)]
    d_num=d_num.sort_values(["工程開始時間"])
    d_num=d_num.reset_index()
    
    d_num=d_num[(d_num["処理時間"] != 1)]
    st.dataframe(d_num)
    if len(d_num)!=0:
            if len(d_num)!=1:
                d_num["工程開始時間"] = pd.to_datetime(d_num["工程開始時間"], format="%H:%M:%S")
                d_num["工程完了時間"] = pd.to_datetime(d_num["工程完了時間"], format="%H:%M:%S")
                
                answer = st.button('分析開始')
                if answer == True:
                    
                    #描画領域を用意する
#                     fig = plt.subplots()
#                     fig = px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="製造番号",title="設備の稼働状況見える化")
#                     ax.update_traces(textposition='inside', orientation="h")
#                     st.show(fig)

                    fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="製造番号",color="工程コード",title="一日の稼働状況見える化"))
                    fig.update_traces(textposition='inside', orientation="h")
                    fig.update_yaxes(autorange='reversed')
                    st.plotly_chart(fig)
                    
                    fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="工程コード",color="工程コード",title="一日の稼働状況見える化"))
                    fig.update_traces(textposition='inside', orientation="h")
                    fig.update_yaxes(autorange='reversed')
                    st.plotly_chart(fig)
                    
                    fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="工程開始日",color="工程コード",title="一日の稼働状況見える化"))
                    fig.update_traces(textposition='inside', orientation="h")
                    fig.update_yaxes(autorange='reversed')
                    st.plotly_chart(fig)
                    #================================================================================================================================
elif selector=="（A-2）各工程各日の実績ガントチャート":
    day_num = sorted(list(set(df["工程完了日"])))
    d = st.selectbox(
         "工程完了日",
         (day_num))
    
    d_num=df[(df["工程完了日"]==d)]
    
    d_num["工程開始時間"] = pd.to_datetime(d_num["工程開始時間"], format="%H:%M:%S")
    d_num["工程完了時間"] = pd.to_datetime(d_num["工程完了時間"], format="%H:%M:%S")
    kikai_num = list(set(d_num["号機名称"]))
    
    answer = st.button('分析開始')
    if answer == True:
        fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="号機名称",color="号機名称",title="一日の稼働状況見える化"))
        fig.update_traces(textposition='inside', orientation="h")
        st.plotly_chart(fig)
        
        for k in kikai_num:
            k_num=d_num[d_num["号機名称"]==k]
            k_num=k_num.sort_values(["工程開始時間"])
            if len(k_num) >=1:
                st.write("================================================================================")
                st.write(k,":",len(k_num))

                fig = go.Figure(px.timeline(k_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="工程コード",color="担当コード", color_continuous_scale='Jet',title="稼働状況の詳細"))
                fig.update_traces(textposition='inside', orientation="h")
                fig.update_yaxes(autorange='reversed')
                st.plotly_chart(fig)
                 #================================================================================================================================

elif selector=="（B）同一人物の同一行程でのばらつきの把握_ヒストグラム":
    #標準時間の取り込み
    st.title("標準時間ファイル")
    uploaded_file=st.file_uploader("標準時間の取り込み",type="xlsx")
    if uploaded_file is not None:
        df_time=pd.read_excel(uploaded_file)
    base_time = pd.to_datetime('00:00:0', format='%M:%S:%f')
    df_time['標準時間１']=pd.to_datetime(df_time['標準時間１'], format='%M:%S:%f') - base_time
    df_time['標準時間１']=df_time["標準時間１"].dt.total_seconds()
    df_time['標準時間２']=pd.to_datetime(df_time['標準時間２'], format='%M:%S:%f') - base_time
    df_time['標準時間２']=df_time["標準時間２"].dt.total_seconds()
    
    st.write(df_time)
    #曜日の設定
    
    
    #担当の選択
    t_list = sorted(list(set(df["担当コード"])))
    t = st.selectbox(
         "担当コード",
         (t_list))
    x_num=df[(df["担当コード"]==t)]#dfからzで選んだ図番のデータ
    k_list = sorted(list(set(x_num["工程コード"])))
    z_list = sorted(list(set(x_num["図番"])))
    
    #曜日の選択
    y_list = ["月","火","水","木","金","すべて"]
    y = st.selectbox(
         "曜日",
         (y_list))
    
    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        
        for z in z_list:
            for k in k_list:
                data_num=df[(df["図番"]==z)&(df["工程コード"]==k)]
                dosu_num=0
                
                y_num=df[(df["図番"]==z)&(df["工程コード"]==k)&(df["担当コード"] == t)]
                y_num=y_num["処理時間"]
                if len(y_num)==0:
                    break
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
                scores=hazure[(hazure["図番"]==z)&(hazure["工程コード"]==k)&(hazure["担当コード"]==t)]#選択したデータ
                y_scores=df_time[(df_time["図番"]==z)&(df_time["工程コード"] ==k)]
                hyozyun=y_scores["標準時間１"]
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
                st.write("---------------工程コード:",k,"-------------図番:",z,"------------データの数:",len(scores),"------------------")
                left_column, right_column = st.columns(2)
                right_column.plotly_chart(fig)
                left_column.pyplot(fig)
                
#=======================================================================================================================================================
elif selector=="（C）同一行程内のばらつき把握_ヒストグラム":
    
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
#         fig = plt.figure()
#         ax = fig.add_subplot()
#         ax.boxplot(s_num)#箱髭図作成
#         # Matplotlib の Figure を指定して可視化する
#         st.pyplot(fig)
        fig = go.Figure(px.box(s_num))
        st.plotly_chart(fig, use_container_width=True)
        
        syosai_num=data_num['processing_time'].describe()#データの詳細データ
        syosai_num = pd.DataFrame(syosai_num)
        st.write(syosai_num.T)
        
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
        
        
#         st.write('第一四分位数は%.1fです'%q1)
#         st.write('第三四分位数は%.1fです'%q3)
#         st.write('四分位範囲は%.1fです'%iqr)
#         st.write('上限値は%.1fです'%upper_num)
#         st.write('下限値は%.1fです'%lower_num)
#         st.write('差は%.1fです'%dif_num)
#         st.write('差は%.1fです'%dif_num2)
#         st.write('外れてない数の割合は%d/%dです'%(len(hazure),len(data_num)))
#         st.write('上限値は%.1fです'%upper_num2)
#         st.write('下限値は%.1fです'%lower_num2)
        
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
            left_column, right_column = st.columns(2)
            right_column.plotly_chart(fig)
            left_column.pyplot(fig)            
#================================================================================================================================
elif selector=="（D）一つの製品の総社内滞在時間の把握_折れ線グラフ":
    day_num = sorted(list(set(df["工程完了日"])))
    d = st.selectbox(
         "工程完了日",
         (day_num))
    d_num=df[(df["工程完了日"]==d)]
    d_num=d_num.sort_values(["工程開始時間"])
    s_num = sorted(list(set(d_num["製造番号"])))
    
    answer = st.button('分析開始')
    if answer == True:
        for s in s_num:        
            sei_num=d_num[d_num["製造番号"]==s]
            sei_num=sei_num.sort_values(["工程開始時間"])
            sei_num["工程開始時間"] = pd.to_datetime(sei_num["工程開始時間"], format="%H:%M:%S")
            sei_num["工程完了時間"] = pd.to_datetime(sei_num["工程完了時間"], format="%H:%M:%S")
            sei_num=sei_num.reset_index()
            
            gura_num = pd.DataFrame()
            s_num = pd.DataFrame()
            for i in range(len(sei_num)):
                sei_num['工程時間'] = sei_num["工程開始時間"]
                s_num = sei_num.iloc[i]
                gura_num=gura_num.append(s_num)
                sei_num['工程時間'] = sei_num["工程完了時間"]
                s_num = sei_num.iloc[i]
                gura_num=gura_num.append(s_num)
           
            gura_num=gura_num.sort_values(["工程時間"])
            st.write("-----------------------------------------------------------------------------------")
            st.dataframe(gura_num)
            fig = go.Figure(px.line(gura_num, x="工程時間", y="工程コード", markers=True))
            fig.update_yaxes(autorange='reversed')
            st.plotly_chart(fig)

#=======================================================================================================================================
#担当者の画面
elif selector=="（E）担当者別作業時間統計量":
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
 #================================================================================================================================        
#図番の画面
elif selector=="（E）図番別作業時間統計量":
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
 #================================================================================================================================      
#工程の画面
elif selector=="（E）工程別作業時間統計量":
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
 
 #===============================================================================================================================================
elif selector=="（E）各人の工程量":
    num=df[["図番","製造番号","工程コード","担当コード","工程開始時間","工程開始日","工程完了日","工程完了時間"]]
    
    n_list = sorted(list(set(df["工程開始日"])))
    n = st.selectbox(
         "工程日",
         (n_list))
    n_num=df[(df["工程開始日"]==n)]
    
    t_list = sorted(list(set(n_num["担当コード"])))
    
    hito_list = sorted(list(set(df["担当者"])))
    ko_list = sorted(list(set(df["工程名称"])))
    bar_num1=pd.DataFrame(columns=["担当者","工程名称","%"] )
    
    for t in hito_list:
        t_num=n_num[(n_num["担当者"]==t)]
        k_list = sorted(list(set(t_num["工程名称"])))
        for k in k_list:
            k_num=t_num[(t_num["工程名称"]==k)]
            r=round(100 * len(k_num) / len(t_num), 1)
            fruit_list = [ (t, k, r )]
            app_num = pd.DataFrame(fruit_list, columns = ["担当者","工程名称","%"])
            
            bar_num1=bar_num1.append(app_num,ignore_index=True)
            
    bar_num1=bar_num1.sort_values('担当者')
    
    n_num=n_num.sort_values('担当者')
    
    st.dataframe(bar_num1)
    st.dataframe(n_num)
    answer = st.button('分析開始')
    if answer == True:
        
        #描画領域を用意する
        left_column, right_column = st.columns(2)
        fig = go.Figure(px.bar(n_num,x="担当者",y="作成数",color="工程名称"))
        st.plotly_chart(fig, use_container_width=True)
        
        fig = go.Figure(px.bar(bar_num1,x="担当者",y="%",color="工程名称"))
        st.plotly_chart(fig, use_container_width=True)
        
