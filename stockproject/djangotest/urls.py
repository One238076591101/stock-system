"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stockproject.views import stock_select_db, stock_form_inquire, stock_inquire, stock_form_predict, stock_predict, index, getGraphics, StockMonthGraphics,StockYearGraphics,stock_form_db

urlpatterns = [
    path('admin/', admin.site.urls),                             
    path('stock_form_db/', stock_form_db),                       #查詢資料庫：股票代號搜尋
    path('stock_form_db/stock_select_db/', stock_select_db),     #於網頁顯示資料庫內之股票資料
    path('stockInquire/', stock_form_inquire),                   #查詢即時股市：輸入股票代號搜尋
    path('stockInquire/stock_inquire/', stock_inquire),          #查詢即時股市：顯示股票資訊
    path('StockPredict/', stock_form_predict),                   #查詢預測分析：輸入股票代號搜尋
    path('StockPredict/stock_predict/', stock_predict),          #查詢預測分析：顯示股票之資訊
    path('', index),                                             #首頁
    path('getGraphics/', getGraphics),                           #走勢圖查詢
    path('getGraphics/StockMonthGraphics/', StockMonthGraphics), #顯示月開盤/收盤價走勢圖
    path('getGraphics/StockYearGraphics/', StockYearGraphics),   #顯示年開盤/收盤價走勢圖
]
