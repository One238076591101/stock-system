from os import name
from django.db import models

# Create your models here.
#資料庫模型
class StockDB(models.Model):
    name_code = models.CharField(max_length=4) #股票代碼
    date = models.IntegerField()               #日期
    capacity = models.IntegerField()           #總成交股數
    turnover = models.IntegerField()           #總成交金額
    open = models.FloatField()                 #開盤價
    high = models.FloatField()                 #盤中最高價
    low = models.FloatField()                  #盤中最低價
    close = models.FloatField()                #收盤價
    change = models.FloatField()               #漲跌價差
    transactions = models.IntegerField()       #成交筆數