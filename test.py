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
pagelist = ["(A-1)各人各日の実績ガントチャート","（A-2）各工程各日の実績ガントチャート","（B）同一人物の同一行程でのばらつきの把握_ヒストグラム","（C）同一行程内のばらつき把握_ヒストグラム","（D）一つの製品の総社内滞在時間の把握","（E）担当者別作業時間統計量","（E）作業時間統計量","（E）各人の工程量"]
st.title("生産データ分析")
#サイドバーのセレクトボックスを配置
selector=st.sidebar.selectbox( "ページ選択",pagelist)
#製造データの取り込み
st.title("製造データファイル")
uploaded_file=st.file_uploader("製造データの取り込み",type="xlsx")
if uploaded_file is not None:
    st.session_state.df=pd.read_excel(uploaded_file)

st.session_state.df["開始日時"]=0
st.session_state.df["完了日時"]=0
st.session_state.df=st.session_state.df[st.session_state.df["処理時間"]!=0]

for index,row in st.session_state.df.iterrows():
    
    time1=row["工程開始時間"]
    day1=row["工程開始日"]
    dateti1= datetime.datetime.combine(day1,time1)
    
    time2=row["工程完了時間"]
    day2=row["工程完了日"]
    
    dateti2= datetime.datetime.combine(day2,time2)
    
    
    st.session_state.df.at[index,'開始日時'] = pd.to_datetime(dateti1)
    st.session_state.df.at[index,'完了日時'] = pd.to_datetime(dateti2)
    
#標準時間の取り込み
st.title("標準時間ファイル")
uploaded_file1=st.file_uploader("標準時間の取り込み",type="xlsx")
if uploaded_file is not None:
    st.session_state.df_time=pd.read_excel(uploaded_file1)
base_time = pd.to_datetime('00:00:0', format='%M:%S:%f')
st.session_state.df_time['標準時間1']=pd.to_datetime(st.session_state.df_time['標準時間1'], format='%M:%S:%f') - base_time
st.session_state.df_time['標準時間1']=st.session_state.df_time["標準時間1"].dt.total_seconds()
st.session_state.df_time['標準時間2']=pd.to_datetime(st.session_state.df_time['標準時間2'], format='%M:%S:%f') - base_time
st.session_state.df_time['標準時間2']=st.session_state.df_time["標準時間2"].dt.total_seconds()
    
#================================================================================================================================
if selector=="(A-1)各人各日の実績ガントチャート":
    
    day_num = sorted(list(set(st.session_state.df["工程完了日"])))
    d = st.selectbox(
         "工程完了日",
         (day_num))
    
    d_num=st.session_state.df[(st.session_state.df["工程完了日"]==d)&(st.session_state.df["工程開始日"] == d)]
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
                    graph_num=pd.DataFrame()
                    t_list = sorted(list(set(d_num["担当者"])))
                    for t in t_list:
                        aki_time=0
                        t_num =d_num[d_num['担当者']==t]
                        t_num=t_num.sort_values("開始日時")
                        st.write(t_num)
                        #余裕率の計算、隙間時間
                        
                        sta_num=[]
                        end_num=[]
                        t_col=t_num.columns.values
                        for row in t_num.itertuples():
                            sta_num.append(row.開始日時)
                            end_num.append(row.完了日時)

                        for i in range(len(t_num)-1):
                            a=sta_num[i+1]-end_num[i]
                            st.write(a)
                            a=a.seconds
                            aki_time+=a
                            
                            df3 =pd.DataFrame(columns =t_col )
                            df2 = pd.DataFrame({"担当者":t,"工程名称":"隙間時間","開始日時":end_num[i], "完了日時":sta_num[i+1]},index=['time'])
                            
                            df3.loc[0,'担当者'] = t
                            df3.loc[0,'工程名称'] = "隙間時間"
                            df3.loc[0,'開始日時'] = end_num[i]+ datetime.timedelta(seconds=1)
                            df3.loc[0,'完了日時'] = sta_num[i+1]+ datetime.timedelta(seconds=-1)
                            t_num=pd.concat([t_num, df3], axis=0)
                        
                            
                        st.write("===")
                        st.write(aki_time)
                        st.write("===")
                        t_num=t_num.sort_values("開始日時")
                        graph_num=graph_num.append(t_num)
                      
                        
                    #描画領域を用意する
#                     fig = plt.subplots()
#                     fig = px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="製造番号",title="設備の稼働状況見える化")
#                     ax.update_traces(textposition='inside', orientation="h")
#                     st.show(fig)
                    
#                     fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="担当者",color="工程名称",title="一日の各人の稼働状況"))
#                     fig.update_traces(textposition='inside', orientation="h")
#                     st.plotly_chart(fig)
                    
#                     fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="号機名称",color="担当者",title="一日の号機の稼働状況"))
#                     fig.update_traces(textposition='inside', orientation="h")
#                     st.plotly_chart(fig)
                    
#                     fig = go.Figure(px.timeline(d_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="工程名称",color="担当者",title="一日の工程状況"))
#                     fig.update_traces(textposition='inside', orientation="h")
#                     st.plotly_chart(fig)
                    st.write(graph_num)
                    st.write("----------")
                    fig = go.Figure(px.timeline(graph_num, x_start="開始日時", x_end="完了日時",y="担当者",color="工程名称",title="一日の各人の稼働状況"))
                    fig.update_traces(textposition='inside', orientation="h")
                    st.plotly_chart(fig)
                    
                    
                    #================================================================================================================================
elif selector=="（A-2）各工程各日の実績ガントチャート":
    day_num = sorted(list(set(st.session_state.df["工程完了日"])))
    d = st.selectbox(
         "工程完了日",
         (day_num))
    
    d_num=st.session_state.df[(st.session_state.df["工程完了日"]==d)]
    
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

                fig = go.Figure(px.timeline(k_num, x_start="工程開始時間", x_end="工程完了時間",text="処理時間",y="工程名称",color="担当者", color_continuous_scale='Jet',title="稼働状況の詳細"))
                fig.update_traces(textposition='inside', orientation="h")
                fig.update_yaxes(autorange='reversed')
                st.plotly_chart(fig)
                 #================================================================================================================================

elif selector=="（B）同一人物の同一行程でのばらつきの把握_ヒストグラム":
    
    st.write(df_time)
    #曜日の設定
    
    
    #担当の選択
    t_list = sorted(list(set(st.session_state.df["担当者"])))
    t = st.selectbox(
         "担当者",
         (t_list))
    x_num=st.session_state.df[(st.session_state.df["担当者"]==t)]#dfからzで選んだ図番のデータ
    k_list = sorted(list(set(x_num["工程名称"])))
    z_list = sorted(list(set(x_num["図番"])))
    
#     #曜日の選択
#     y_list = ["月","火","水","木","金","すべて"]
#     y = st.selectbox(
#          "曜日",
#          (y_list))
    
    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        
        for z in z_list:#図番でfor文回す
            for k in k_list:#工程名称でfor文回す
                data_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"]==k)]#図番と工程名称でデータを絞る
                dosu_num=0#度数の空の変数
                
                y_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"]==k)&(st.session_state.df["担当者"] == t)]#図番、工程名称、担当者でデータを絞る
                y_num=y_num["処理時間"]#処理時間だけ抜出
                if len(y_num)==0:#y_numの中にデータが一つも入ってなかった場合終了
                    break
                #y軸の上限値
                x,y,_= plt.hist(y_num)#x軸、y軸、度数
                if dosu_num<max(x):#度数の比較（最大値）
                    dosu_num=max(x)#（最大値）
                    
                data_num=data_num.rename(columns={'処理時間': 'processing_time'})#名前の変更 
                s_num=data_num['processing_time']#図番と工程名称で絞ったデータの処理時間を抜き出し
                    
                q1=data_num['processing_time'].describe().loc['25%']#第一四分位範囲
                q3=data_num['processing_time'].describe().loc['75%']#第三四分位範囲
                
                iqr=q3-q1#四分位範囲
                upper_num=q3+(1.5*iqr)#上限
                lower_num=q1-(1.5*iqr)#下限
                
                upper_num2=round(upper_num) #きりあげ（上限）見やすくする用
                lower_num2=math.floor(lower_num)#きりおとし（下限）見やすくする用
                dif_num=upper_num2-lower_num2#差
                dif_num3=0
                
                if dif_num%10!=0:#もし切り上げ切り落としした差が10で割れなかった
                    dif_num2=math.ceil((dif_num/10))*10
                    dif_num3=(dif_num2-dif_num)/2
                upper_num2=upper_num2+dif_num3
                lower_num2=lower_num2-dif_num3
                dif_num=upper_num2-lower_num2#差
                
                hazure=data_num[data_num["processing_time"]<=upper_num]#外れ値の除外
                hazure=hazure[hazure["processing_time"]>=lower_num]
        
                #ヒストグラムの作成
                #データの整理
                scores=hazure[(hazure["図番"]==z)&(hazure["工程名称"]==k)&(hazure["担当者"]==t)]#選択したデータ（外れ値）
                y_scores=st.session_state.df_time[(st.session_state.df_time["図番"]==z)&(st.session_state.df_time["工程名称"]==k)]#標準時間のデータ
                
                hyozyun1=y_scores["標準時間1"]
                hyozyun2=y_scores["標準時間2"]
                
                dd=scores["processing_time"]#選択したデータの処理時間
                scores=scores.rename(columns={'processing_time':'処理時間' })#名前の変更 
            
                #描画領域を用意する
                fig = plt.figure()
                ax = fig.add_subplot()

                plt.xlim([0,upper_num2])                        # X軸範囲
                plt.ylim([0,dosu_num+10])                      # Y軸範囲
                ax.set_title("chart")
                ax.set_xlabel("time")                # x軸ラベル
                plt.ylabel("count")               # y軸ラベル
                plt.grid(True)
                plt.axvline(x=int(hyozyun1),color = "crimson")#標準時間の表記（赤軸）
                plt.axvline(x=int(hyozyun2),color = "Blue")#標準時間の表記（軸）
                plt.xticks(np.arange(lower_num2, upper_num2,dif_num/10))
                

                ax.hist(dd,bins=10,range=(lower_num2,upper_num2))
                # Matplotlib の Figure を指定して可視化する
                st.write("---------------工程コード:",k,"-------------図番:",z,"------------データの数:",len(scores),"------------------")
                left_column, right_column = st.columns(2)
                left_column.pyplot(fig)
                
                num=pd.DataFrame(scores.groupby(['担当者',"図番","工程名称"])['処理時間'].agg(["count","mean", "median", "min", "max"]))
                pvit=num.set_axis(['件数', '平均', '中央値', '最小', '最大'], axis=1)
                pvit.insert(0, '総件数', len(y_num))
                pvit["標準時間1"]=int(hyozyun1)
                pvit["標準時間2"]=int(hyozyun2)
                st.write(pvit)
#=======================================================================================================================================================
elif selector=="（C）同一行程内のばらつき把握_ヒストグラム":
    #図番の選択
    z_list = sorted(list(set(st.session_state.df["図番"])))
    z = st.selectbox(
         "図番",
         (z_list))
    x_num=st.session_state.df[(st.session_state.df["図番"]==z)]#dfからzで選んだ図番のデータ
    #工程の選択
    k_list = sorted(list(set(x_num["工程名称"])))
    k = st.selectbox(
         "工程名称",
         (k_list))
    x_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"] == k)]#dfからz,kで選んだ図番,工程のデータ
    #担当の選択
    t_list = sorted(list(set(x_num["担当者"])))
    t = st.multiselect(
         "担当者",
         (t_list))

    #データ分析開始
    answer = st.button('分析開始')
    if answer == True:
        #上限値、下限値のdata
        data_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"]==k)]
        dosu_num=0
        
        for t_num in t_list:
            y_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"]==k)&(st.session_state.df["担当者"] == t_num)]
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
            x_num=st.session_state.df[(st.session_state.df["図番"]==z)&(st.session_state.df["工程名称"]==k)&(st.session_state.df["担当者"] == i)]
            scores=hazure[(hazure["図番"]==z)&(hazure["工程名称"]==k)&(hazure["担当者"]==i)]#選択したデータ
            y_scores=st.session_state.df_time[(st.session_state.df_time["図番"]==z)&(st.session_state.df_time["工程名称"] ==k)]
            hyozyun1=y_scores["標準時間1"]
            hyozyun2=y_scores["標準時間2"]
            #はずれちの除外
#             dd=scores[scores["処理時間"]<upper_num]
#             dd=dd[dd["処理時間"]>lower_num]
            dd=scores["processing_time"]#選択したデータの処理時間
            scores=scores.rename(columns={'processing_time':'処理時間' })#名前の変更 
            # 描画領域を用意する
            fig = plt.figure()
            ax = fig.add_subplot()
            
            plt.xlim([0,upper_num2])                        # X軸範囲
            plt.ylim([0,dosu_num+10])                      # Y軸範囲
            ax.set_title("chart")
            ax.set_xlabel("time")                # x軸ラベル
            plt.ylabel("count")               # y軸ラベル
            plt.grid(True)
            plt.axvline(x=int(hyozyun1),color = "crimson")#標準時間の表記（赤軸）
            plt.axvline(x=int(hyozyun2),color = "Blue")#標準時間の表記（軸）
            plt.xticks(np.arange(lower_num2, upper_num2,dif_num2/10))
            
            ax.hist(dd,bins=10,range=(lower_num2,upper_num2),rwidth=dif_num2/10)
            
            
            # Matplotlib の Figure を指定して可視化する
            st.write("---------------このグラフのデータ個数：",len(dd),"-------------担当コード：",i,"-----------------------")
            left_column, right_column = st.columns(2)
            left_column.pyplot(fig)
            num=pd.DataFrame(scores.groupby(['担当者',"図番","工程名称"])['処理時間'].agg(["count","mean", "median", "min", "max"]))
            pvit=num.set_axis(['件数', '平均', '中央値', '最小', '最大'], axis=1)
            pvit.insert(0, '総件数', len(x_num))
            pvit["標準時間1"]=int(hyozyun1)
            pvit["標準時間2"]=int(hyozyun2)
            st.write(pvit)
#================================================================================================================================
elif selector=="（D）一つの製品の総社内滞在時間の把握":
    day_num = sorted(list(set(st.session_state.df["工程完了日"])))#日付の抜出
    d_start = st.selectbox(#開始日の選択
         "開始日",
         (day_num))
    d_end = st.selectbox(#終了日の選択
         "終了日",
         (day_num))
    dt = d_end-d_start#開始日と終了日の差の計算
    dt= dt.days#int
    
    answer = st.button('分析開始')
    if answer == True:       
        k_list = sorted(list(set(st.session_state.df["工程名称"])))#全体データ（加工なし）から工程名称の抜出
        date_num = pd.DataFrame(columns=k_list)#列名だけ入れた表データ
        date_koutei_num=pd.DataFrame()#表データに入れる空データ
        d_num=st.session_state.df[(st.session_state.df["工程完了日"]==d_start)]#
        s_list = sorted(list(set(d_num["製造番号"])))
        for s in s_list:
            s_num=d_num[(d_num["製造番号"]==s)]
            s_num=s_num.sort_values(["完了日時"])
            date_koutei_num=date_koutei_num.append(s_num.tail(1))

        for d in range(dt+1):#日のデータの追加文
            kari_num=st.session_state.df[(st.session_state.df["工程完了日"]==d_start)]
            d_num=d_num.append(kari_num)
            d_start = d_start + datetime.timedelta(days=1)
        
    
        st.write(d_num)
        st.write(date_koutei_num)
#         k_date_list = sorted(list(set(date_koutei_num["工程名称"])))
#         for k in k_date_list:
#             st.write(k)
#             st.write(len(date_koutei_num[(date_koutei_num["工程名称"]==ｋ)]))
        
        st.write("-----------------------------------------------------------------------------------")
        fig = go.Figure(px.timeline(d_num, x_start="開始日時", x_end="完了日時",text="処理時間",y="製造番号",color="工程名称",title="総社内滞在時間"))
        fig.update_traces(textposition='inside', orientation="h")
        fig.update_yaxes(autorange='reversed')
        st.plotly_chart(fig)

#=======================================================================================================================================
#担当者の画面
elif selector=="（E）担当者別作業時間統計量":
    answer = st.button('分析開始')
    if answer == True:
        t_list = sorted(list(set(st.session_state.df["担当者"])))

        for t in t_list:
            t_num=st.session_state.df[(st.session_state.df["担当者"]==t)]
            k_list=sorted(list(set(t_num["工程名称"])))
            graph_num=pd.DataFrame()
           
            
            for k in k_list:
                k_num=t_num[(t_num["工程名称"]==k)]

                q1=k_num["処理時間"].describe().loc['25%']#第一四分位範囲
                q3=k_num['処理時間'].describe().loc['75%']#第三四分位範囲
                iqr=q3-q1#四分位範囲
                upper_num=q3+(1.5*iqr)#上限
                lower_num=q1-(1.5*iqr)#下限

                hazure=k_num[k_num["処理時間"]<=upper_num]#外れ値の除外
                hazure=hazure[hazure["処理時間"]>=lower_num]

                Nohazure_num=len(hazure)
                zentai_num=len(k_num)
                Yeshazure_num=(zentai_num-Nohazure_num)

                num=pd.DataFrame(hazure.groupby(['担当者',"図番","工程名称"])['処理時間'].agg(["count","mean", "median", "min", "max"]))
                pvit=num.set_axis(['件数', '平均', '中央値', '最小', '最大'], axis=1)
                pvit["標準時間"]=0
                pvit.insert(0, '総件数', zentai_num)
                
                graph_num=pd.concat([graph_num, pvit], axis=0)
            
            st.dataframe(graph_num)
            st.write("----------------------")
            
 #================================================================================================================================        
#図番の画面
elif selector=="（E）図番別作業時間統計量":
    z_list = sorted(list(set(st.session_state.df["図番"])))
    z = st.selectbox(
         "図番",
         (z_list))
    z_num=st.session_state.df[(st.session_state.df["図番"]==z)]
    num=pd.DataFrame(z_num.groupby(["図番","工程コード",'担当コード'])['処理時間'].agg(["count","mean", "std", "min", "max"]))
    pvit=num.set_axis(['件数', '平均', '標準偏差', '最小', '最大'], axis=1)
    pvit=pvit.round(1)   # 小数第1位まで．2位を切り捨て
    answer = st.button('分析開始')
    if answer == True:
        
        st.dataframe(pvit)
        st.table(pvit)
 #================================================================================================================================      
#工程の画面
elif selector=="（E）作業時間統計量":
    num_list = ["工程名称","担当者","図番",]
    num_1 = st.selectbox(
         "1つ目",
         (num_list))
    num_2 = st.selectbox(
         "2つ目",
         (num_list))
    num_3= st.selectbox(
         "3つ目",
         (num_list))
    
    answer = st.button('分析開始')
    if answer == True:
        
        graph_num=pd.DataFrame()
        list_1=sorted(list(set(st.session_state.df[num_1])))
        for hazure_num1 in list_1:
            x_num=st.session_state.df[(st.session_state.df[num_1]==hazure_num1)]
            list_2=sorted(list(set(x_num[num_2])))
            for hazure_num2 in list_2:
                y_num=x_num[(x_num[num_2]==hazure_num2)]
                list_3 = sorted(list(set(y_num[num_3])))
                for hazure_num3 in list_3:
                    z_num=y_num[(y_num[num_3]==hazure_num3)]

                    q1=z_num["処理時間"].describe().loc['25%']#第一四分位範囲
                    q3=z_num['処理時間'].describe().loc['75%']#第三四分位範囲
                    iqr=q3-q1#四分位範囲
                    upper_num=q3+(1.5*iqr)#上限
                    lower_num=q1-(1.5*iqr)#下限

                    hazure=z_num[z_num["処理時間"]<=upper_num]#外れ値の除外
                    hazure=hazure[hazure["処理時間"]>=lower_num]

                    Nohazure_num=len(hazure)
                    zentai_num=len(z_num)
                    Yeshazure_num=(zentai_num-Nohazure_num)

                    num=pd.DataFrame(hazure.groupby([num_1,num_2,num_3])['処理時間'].agg(["count","mean", "median", "min", "max"]))
                    pvit=num.set_axis(['件数', '平均', '中央値', '最小', '最大'], axis=1)
                    pvit.insert(0, '総件数', zentai_num)
                    graph_num=pd.concat([graph_num, pvit], axis=0)        
           
        
        st.dataframe(graph_num)
 
 #===============================================================================================================================================
elif selector=="（E）各人の工程量":
    num=st.session_state.df[["図番","製造番号","工程コード","担当コード","工程開始時間","工程開始日","工程完了日","工程完了時間"]]
    
    n_list = sorted(list(set(st.session_state.df["工程開始日"])))
    n = st.selectbox(
         "工程日",
         (n_list))
    n_num=st.session_state.df[(st.session_state.df["工程開始日"]==n)]
    
    t_list = sorted(list(set(n_num["担当コード"])))
    
    hito_list = sorted(list(set(st.session_state.df["担当者"])))
    ko_list = sorted(list(set(st.session_state.df["工程名称"])))
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
    answer = st.button('分析開始')
    if answer == True:
        
        #描画領域を用意する
        left_column, right_column = st.columns(2)
        fig = go.Figure(px.bar(n_num,x="担当者",y="作成数",color="工程名称"))
        left_column.plotly_chart(fig, use_container_width=True)
        right_column.dataframe(bar_num1)
        
        fig = go.Figure(px.bar(bar_num1,x="担当者",y="%",text="%",color="工程名称"))
        st.plotly_chart(fig, use_container_width=True)
        
