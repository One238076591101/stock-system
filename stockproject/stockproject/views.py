import os
import sqlite3
from django.shortcuts import render
from twstock import Stock,realtime
from twstock import BestFourPoint
import plotly.graph_objects as go

#首頁
def index(request):
    return render(request, 'index.html', locals())

#查詢資料庫：股票代號搜尋
def stock_form_db(request):
    return render(request, 'stock_form_db.html', locals())

#資料庫：選10支股票使用twstock API將五年之資訊存入sqlite3資料庫中，並且顯示於網頁
def stock_select_db(request):
    conn = sqlite3.connect('db.sqlite3') #連接資料庫
    c = conn.cursor()
    #建立資料庫內之資料，建立完成後註解掉
    '''stock_name=['2330','2317','2327','2409','2454','3481','0050','0056','2884','2002'] #選十支股票
        for i in stock_name:
            stock = Stock(i) #使用twstock API抓取股票代碼資訊放入變數stock中
            # for j in month:
            FiveYear = list(stock.fetch_from(2016,1)) #抓取從2016年至今之股票資料放入串列FiveYear中
            day = [int(datetime.strftime(FiveYear[l][0],'%Y%m%d')) for l in range(len(FiveYear))] #利用串列生成式將日期轉換成整數
            for row in range(len(FiveYear)):
                #對應欄位名稱一一將資料輸入資料庫
                R1 = StockDB(name_code=i, date=day[row], capacity=FiveYear[row][1], turnover=FiveYear[row][2], open=FiveYear[row][3], high=FiveYear[row][4], low=FiveYear[row][5], close=FiveYear[row][6], change=FiveYear[row][7], transactions=FiveYear[row][8])
                R1.save() #儲存'''
    c = c.execute("select * from stockproject_stockdb WHERE name_code={} ".format(request.GET['stock_name'])) #依據使用者輸入之股票代碼，從資料庫取出相關資料
    savedata=[]
    #串列生成式=>savedata巢狀迴圈=>按照資料庫內的資料順序一列列將股票資訊放入savedata中
    savedata=[[row[0].__str__(),row[1].__str__(),row[2].__str__(),row[3].__str__(),row[4].__str__(),row[5].__str__(),row[6].__str__(),row[7].__str__(),row[8].__str__(),row[9].__str__(),row[10].__str__()] for row in c]
    conn.commit()
    conn.close() #關閉資料庫連結
    return render(request, 'stock_select_db.html',{'savedata': savedata} ) #將資料傳至前端

#查詢即時股市程式：輸入股票代號搜尋
def stock_form_inquire(request):
    return render(request, 'StockInquire.html', locals())

#查詢即時股市程式：顯示股票之資訊
def stock_inquire(request):
    stock = realtime.get(str(request.GET['stock_name_inquire']))
    stock2 = Stock(request.GET['stock_name_inquire'])
    bfp = BestFourPoint(stock2)
    A = stock["info"].get("time")
    B = stock["info"].get("code")
    C = stock["info"].get("name")
    D = stock["info"].get("fullname")

    S1=[row for row in stock["realtime"].get("best_bid_price")]
    S2=[row for row in stock["realtime"].get("best_bid_volume")]
    S3=[row for row in stock["realtime"].get("best_ask_price")]
    S4= stock["realtime"].get("best_ask_volume")
    S5= stock["realtime"].get("open")
    S6= stock["realtime"].get("high")
    S7= stock["realtime"].get("low")

    tr1 = [S1[0],S2[0],S3[0],S4[0]]
    tr2 = [S1[1],S2[1],S3[1],S4[1]]
    tr3 = [S1[2],S2[2],S3[2],S4[2]]
    tr4 = [S1[3],S2[3],S3[3],S4[3]]
    tr5 = [S1[4],S2[4],S3[4],S4[4]]

    context = {
      "list_":[tr1, tr2, tr3, tr4,tr5],
      "list_5":S5,
      "list_6":S6,
      "list_7":S7,
      "list_8":A,
      "list_9":B,
      "list_10":C,
      "list_11":D,
    }     
          
    return render(request, 'StockInquire.html', context)

#查詢預測分析：輸入股票代號搜尋
def stock_form_predict(request):
    return render(request, 'StockPredict.html', locals())

#查詢預測分析：顯示股票之資訊
def stock_predict(request):
    stock2 = Stock(request.GET['stock_name_predict']) #取得輸入股票代碼，並利用其取的股票資訊
    bfp = BestFourPoint(stock2)
    E1=""
    E2=""
    E = bfp.best_four_point() 
    if(E[0]==True):
        E1=E[1]
    else:
        E2=E[1]

    context = {
      "list_12":E1,
      "list_13":E2,
    }     
          
    return render(request, 'StockPredict.html', context)

#輸入股票代碼、年份、月份來查詢走勢圖
def getGraphics(request):
    return render(request, 'StockGraphics.html', locals())

#顯示月開盤/收盤價走勢圖
def StockMonthGraphics(request):
    MonthDict = ['NONE','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    filename = 'static/img/stock/month/['+request.GET['stock_name_graphics'] + '] ' + request.GET['year']+ '-' + MonthDict[int(request.GET['month'])] + '.png'
    if os.path.exists('stockproject/'+filename): #檢查檔案是否存在
        return render(request, 'StockGraphics.html', {'message': filename}) #回傳檔案名稱

    conn = sqlite3.connect('db.sqlite3') #連接資料庫
    c = conn.cursor()
    Y=int(request.GET['year']) #取的輸入年分
    M=int(request.GET['month']) #取得輸入月份
    start=Y*10000+M*100+1 
    end=Y*10000+M*100+30
    target = request.GET['stock_name_graphics'] #取得輸入股票代碼

    #執行SQL語法
    c = c.execute("SELECT date FROM stockproject_stockdb WHERE (name_code={} AND (date>{} AND date<{}))".format(target,start,end)) 
    # chooseDate = [int(str(row[0]))%100 for row in c]
    chooseDate = [str(row[0]) for row in c]
    c = c.execute("SELECT open FROM stockproject_stockdb WHERE (name_code={} AND (date>{} AND date<{}))".format(target,start,end))
    OpenPrice = [row[0] for row in c] #取的開盤價
    c = c.execute("SELECT close FROM stockproject_stockdb WHERE (name_code={} AND (date>{} AND date<{}))".format(target,start,end))
    ClosePrice = [row[0] for row in c] #取的收盤價

    #關閉資料庫連結
    conn.commit()
    conn.close() 
   
    #開始繪製折線圖
    fig = go.Figure()
    #繪製折線圖:x軸為當月日期，y軸為開盤價; 標籤: 4px紅線 開盤價
    fig.add_trace(go.Scatter(x=chooseDate, y=OpenPrice, name='當月開盤價', line=dict(color='firebrick', width=4)))
    #繪製折線圖:x軸為當月日期，y軸為收盤價; 標籤: 4px藍線 收盤價
    fig.add_trace(go.Scatter(x=chooseDate, y=ClosePrice, name = '當月收盤價', line=dict(color='royalblue', width=4)))
    #標示折線圖標題
    fig.update_layout(title = request.GET['stock_name_graphics']+'股票'+request.GET['year']+'年'+request.GET['month']+'月走勢圖',xaxis_title='Month',yaxis_title='Price')
    #匯出圖檔
    fig.write_image('stockproject/'+filename)
    
    #回傳檔案名稱
    return render(request, 'StockGraphics.html', {'message': filename}) #回傳檔案名稱

#顯示年開盤/收盤價走勢圖
def StockYearGraphics(request):
    filename = 'static/img/stock/year/'+request.GET['stock_name_graphics'] + '-' + request.GET['year'] + '.png'
    if os.path.exists('stockproject/'+filename): #檢查是否已經查詢過
        return render(request, 'StockGraphics.html', {'message': filename}) #回傳檔案名稱

    #資料庫連接
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    month=[1,2,3,4,5,6,7,8,9,10,11,12]
    Y=int(request.GET['year']) #取得輸入年分
    a=[]
    b=[]
    #取得當年每月開盤價
    for M in range(1,13):
        count=0 
        openPrice=0
        start=Y*10000+M*100+1
        end=Y*10000+M*100+30
        c = c.execute("SELECT open FROM stockproject_stockdb WHERE (name_code={} AND (date>{} AND date<={}))".format(request.GET['stock_name_graphics'],start,end))
        for row in c:
            openPrice+=int(row[0])
            count+=1 
        
        if count != 0:
            openPrice=openPrice/count 
            a.append(openPrice)

    #取得當年每月開盤價
    for M in range(1,13):
        count=0
        closePrice=0
        start=Y*10000+M*100+1
        end=Y*10000+M*100+30
        c = c.execute("SELECT close FROM stockproject_stockdb WHERE (name_code={} AND (date>{} AND date<={}))".format(request.GET['stock_name_graphics'],start,end))
        for row in c:
            closePrice+=row[0] 
            count+=1 
        closePrice=closePrice/count 
        b.append(closePrice)

    #關閉資料庫連結
    conn.commit()
    conn.close() 
    
    fig = go.Figure()
    #繪製折線圖:x軸為當月日期，y軸為開盤價; 標籤: 4px紅線 開盤價
    fig.add_trace(go.Scatter(x=month, y=a, name='開盤價', line=dict(color='firebrick', width=4)))
    #繪製折線圖:x軸為當月日期，y軸為收盤價; 標籤: 4px藍線 收盤價
    fig.add_trace(go.Scatter(x=month, y=b, name = '收盤價', line=dict(color='royalblue', width=4))) 
    #標示折線圖標題
    fig.update_layout(title = request.GET['stock_name_graphics']+'股票'+request.GET['year']+'年走勢圖',xaxis_title='Month',yaxis_title='Price') #顯示標題, X/Y軸說明
    #匯出圖檔
    fig.write_image('stockproject/'+filename)
    
    #回傳檔案名稱
    return render(request, 'StockGraphics.html', {'message': filename}) #回傳檔案名稱