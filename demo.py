import requests
import json
import parsel   # 数据解析模块
import re
import pprint #格式化输出
def change_title(title):
    mode = re.compile(r'[\\\/\:\*\?\"\<\>\|]')
    new_title = re.sub(mode,'_',title)
    return new_title

'''
    爬取酷狗音乐
    1.对于‘https://www.kugou.com/yy/html/rank.html’发送请求
    2.获取网页文本数据（网页源代码）提取每个榜单得分url地址（获取数据/解析数据）
    3.对于 每个榜单的url地址 发送请求 获取每首歌hashid
    4.把hash id参数传入数据包 获取歌曲播放url地址 以及 歌名 歌手
    5.对 歌曲播放url地址 发送请求 获取二进制数据
    6.保存音乐
'''
url = 'https://www.kugou.com/yy/html/rank.html'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
reponse = requests.get(url, headers=headers).text
# print(reponse)
# 解析数据 css选择器 根据标签属性内容提取数据
# 需要把获取到的网页文本数据(html字符串数据)转换成selector
selector = parsel.Selector(reponse)
href = selector.css('.pc_rank_sidebar li a::attr(href)').getall()# 获取所有a标签里所有href属性 attr:获取属性 返回列表
# print(href)
for link in href:
    reponse_1 = requests.get(link,headers=headers).text
    # 正则.*？  \d+
    Hash_list = re.findall('"Hash":"(.*?)"', reponse_1)
    Id_list = re.findall('"album_id":(.*?),', reponse_1)
    for index in zip(Hash_list,Id_list): # zip()返回一个元组
        hash = index[0]
        music_id = index[1]
        index_url = 'https://wwwapi.kugou.com/yy/index.php'
        params = {'r': 'play/getdata',
                  # 'callback': 'jQuery19109570377193664703_1635577187019',
                  'hash': hash,
                  'dfid': '0jIhin3BquV04QNkLX32IbAU',
                  'appid': '1014',
                  'mid': '5e9d8f657538ba7c06799446bb38a9c6',
                  'platid': '4',
                  'album_id': music_id,
                  '_': '1635577187021'}
        reponse_2 = requests.get(index_url,params=params,headers=headers).text
        json_data = json.loads(reponse_2)
        title = json_data['data']['audio_name']
        play_url = json_data['data']['play_url']
        # 对音乐地址发送请求 获取二进制数据
        music_content = requests.get(play_url,headers=headers).content
        new_title = change_title(title)
        with open('music\\' + title + '.mp3',mode='wb') as f:
            f.write(music_content) # 写入二进制数
        print(title,play_url)
        # pprint.pprint(title,play_url)
    # print(reponse_1)
    # print(Hash_list)
    # print(Id_list)
        break
