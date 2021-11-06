import requests
import json
print("欢迎来到天气查询系统")
print("-"*20)
name = input("请输入查询省份：")
name_city = input("请输入查询城市：")
city_file = open("city_id1.txt", encoding="utf-8")
open_file = city_file.read()
dic = json.loads(open_file)


d1=dic["城市代码"]
j = int(0)
v = int(0)


for i in d1:
    if d1[j]["省"] == name:

        for k in d1[j]["市"]:

           if k["市名"] == name_city:

            city_id = dic["城市代码"][j]["市"][v]["编码"]
            print(f"城市编码:{city_id}")
            break
    j+=1


url = "http://wthrcdn.etouch.cn/weather_mini?citykey=" + city_id
res = requests.get(url)
tq_text = res.text
tq_josn = json.loads(tq_text)
# print(tq_josn)
date = tq_josn["data"]["yesterday"]["date"]
high = tq_josn["data"]["yesterday"]["high"]
print(f"{date}")
print(f"{high}")








