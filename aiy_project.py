from ArticutAPI import Articut
import requests,json
import vlc
import youtube_dl
import base64
import hmac
import random
from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import date, datetime, time ,timedelta
from time import mktime



weatehr_api_key = "";# weather API KEY
key =""; # google map key

nounlist = [];
placelist = [];
timelist = [];
verblist = [];  


ydl_opts = {
    'default_search': 'ytsearch1:',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}
vlc_instance = vlc.get_default_instance();
vlc_player = vlc_instance.media_player_new();

def speech_recognition():
    while True:
        text = client.recognize(language_code='zh-TW',
                                    hint_phrases=hints)
        if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower();
            if(vlc_player.get_state() == vlc.State.Playing or vlc_player.get_state() == vlc.State.Paused):
                if(text.find('暫停')!=-1):
                    vlc_player.set_pause(True);
                    continue;
                elif(text.find('停止')!=-1):
                    vlc_player.stop();
                    continue;
                elif(text.find('繼續')!=-1 or text.find('播放')!=-1):
                    vlc_player.set_pause(False);
                    continue;
                    
            articut = Articut(username="", apikey="")
            result = articut.parse(text)
            noun = articut.getNounStemLIST(result,indexWithPOS=False);
            place = articut.getLocationStemLIST(result);
            time = articut.getTimeLIST(result);
            verb = articut.getVerbStemLIST(result);

            if noun:
                temp_str_noun = " ".join([str(x) for x in noun]);#將List轉回string方便處理
            if place:
                temp_str_place = " ".join([str(x) for x in place]);
            if time:
                temp_str_time = " ".join([str(x) for x in time]);
            if verb:
                temp_str_verb = " ".join([str(x) for x in verb]);
                nounlist.clear()
                placelist.clear();
                timelist.clear();
                verblist.clear();

                handle_result(temp_str_noun, temp_str_place, temp_str_time, temp_str_verb);
                judge(nounlist,placelist,timelist,text,verblist);
                
                #board.led.state = Led.ON
            elif '再見' in text:
                say('感謝您的使用，下次相見')
                break
def get_url(city): # 獲取該城市的URL
    return {    
    '宜蘭': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%AE%9C%E8%98%AD%E7%B8%A3",
    '花蓮': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%8A%B1%E8%93%AE%E7%B8%A3",
    '臺東': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E6%9D%B1%E7%B8%A3",
    '台東': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E6%9D%B1%E7%B8%A3",
    '澎湖': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E6%BE%8E%E6%B9%96%E7%B8%A3",
    '金門': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E9%87%91%E9%96%80%E7%B8%A3",
    '連江': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E9%80%A3%E6%B1%9F%E7%B8%A3",
    '臺北': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82",
    '台北': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E5%8C%97%E5%B8%82",
    '新北': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E6%96%B0%E5%8C%97%E5%B8%82",
    '桃園': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E6%A1%83%E5%9C%92%E5%B8%82",
    '臺中': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E4%B8%AD%E5%B8%82",
    '台中': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E4%B8%AD%E5%B8%82",
    '臺南': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E5%8D%97%E5%B8%82",
    '台南': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%87%BA%E5%8D%97%E5%B8%82",
    '高雄': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E9%AB%98%E9%9B%84%E5%B8%82",
    '基隆': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%9F%BA%E9%9A%86%E5%B8%82",
    '新竹': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E6%96%B0%E7%AB%B9%E5%B8%82",
    '苗栗': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E8%8B%97%E6%A0%97%E7%B8%A3",
    '彰化': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%BD%B0%E5%8C%96%E7%B8%A3",
    '南投': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%8D%97%E6%8A%95%E7%B8%A3",
    '雲林': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E9%9B%B2%E6%9E%97%E7%B8%A3",
    '嘉義': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%98%89%E7%BE%A9%E5%B8%82",
    '屏東': "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=weather_api_key&format=JSON&locationName=%E5%B1%8F%E6%9D%B1%E7%B8%A3",
    }.get(city,'error')

#-------抓資料---------------------------------------------
def get_today_weather_minT(city):#當日最低溫度
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]) 
    
def get_today_weather_maxT(city):#當日最高溫度
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]) 
   
def get_today_weather_wx(city):#天氣型態
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]) 
        
def get_today_weather_PoP(city):#降雨機率
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]) 

def get_tom_weather_minT(city):#明日最低溫度
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][2]["time"][2]["parameter"]["parameterName"]) 
    
def get_tom_weather_maxT(city):#明日最高溫度 
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][4]["time"][2]["parameter"]["parameterName"]) 
       
def get_tom_weather_wx(city):#明日天氣型態
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][0]["time"][2]["parameter"]["parameterName"]) 
    
def get_tom_weather_PoP(city):#明日降雨機率
    url = get_url(city);
    if(url=='error'):
        return 'error'
    else:
        data = requests.get(url)
        data = json.loads(data.text);
        return (data["records"]["location"][0]["weatherElement"][1]["time"][2]["parameter"]["parameterName"]) 
    
#--------輸出------------------------------------------------
def weather_all(city):#天氣輸出
    if(get_today_weather_wx(city)!='error'):
        print(city ,"今天的氣候",get_today_weather_wx(city),"氣溫為",get_today_weather_minT(city),"到",get_today_weather_maxT(city),"度 降雨機率有",get_today_weather_PoP(city),"%");
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫")
    
def weather_wx(city):#氣候輸出
    if(get_today_weather_wx(city)!='error'):
        print(city ,"今天的氣候" , get_today_weather_wx(city));
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫")
        
def weather_PoP(city):#降雨機率輸出
    if(get_today_weather_PoP(city)!='error'):
        print(city ,"有",get_today_weather_PoP(city),"%的降雨機率");
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫");
        
def tomweather_all(city):#明日天氣輸出
    if(get_tom_weather_wx(city)!='error'):
        print(city ,"明天的氣候",get_tom_weather_wx(city),"氣溫為",get_tom_weather_minT(city),"到",get_tom_weather_maxT(city),"度 降雨機率有",get_tom_weather_PoP(city),"%");
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫");
        
def tomweather_wx(city):#明日氣候輸出
    if(get_tom_weather_wx(city)!='error'):
        print(city ,"明天的氣候" , get_tom_weather_wx(city));
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫");
        
def tomweather_PoP(city):#明日降雨機率輸出
    if(get_tom_weather_PoP(city)!='error'):
        print(city ,"明天有",get_tom_weather_PoP(city),"%的降雨機率");
    else:
        print("查無此地天氣，目前只能查詢各大縣市氣溫");
        
#---------------輸入判斷----------------------------------------------------
def judge(nounlist,placelist,timelist,verblist):
    fun_code=0;
    for i in nounlist:
        if(choice_motion(i)!=0): 
                fun_code = choice_motion(i);
                break;
        else :
            continue;
    if(fun_code == 0):
        for j in verblist:
            if(choice_motion(j)!=0):
                fun_code = choice_motion(j);
                break;
            else :
                continue;
#---------------天氣部分----------------------------------------------------
    if(fun_code<4 and fun_code>0):
        if(len(placelist)==0): #定位並查詢
            city = covert_to_city()
            if(get_url(city)!='error' and fun_code == 1): #天氣
                if(len(timelist)==0): #無時間
                    weather_all(city);
                elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日 
                    tomweather_all(city);
                else:
                    weather_all(city);
            elif(get_url(city)!='error' and fun_code == 2): #降雨機率
                if(len(timelist)==0): #無時間
                    weather_PoP(city)
                elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日
                    tomweather_PoP(city)
                else: 
                    weather_PoP(city)
            elif(get_url(city)!='error' and fun_code == 3): #天氣型態
                if(len(timelist)==0): #無時間
                    weather_wx(city)
                elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日
                    weather_wx(city)
                else: 
                    weather_wx(city)
        else:
            for j in placelist:
                if(get_url(j)!='error' and fun_code == 1): #天氣
                    if(len(timelist)==0): #無時間
                        weather_all(j);
                    elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日 
                        tomweather_all(j);
                    else:
                        weather_all(j);
                elif(get_url(j)!='error' and fun_code == 2): #降雨機率
                    if(len(timelist)==0): #無時間
                        weather_all(j);
                    elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日 
                        tomweather_all(j);
                    else:
                        weather_all(j);
                elif(get_url(j)!='error' and fun_code == 3): #天氣型態
                    if(len(timelist)==0): #無時間
                        weather_all(j);
                    elif(timelist[0].find('明天')!=-1 or timelist[0].find('明日')!=-1):#明日 
                        tomweather_all(j);
                    else:
                        weather_all(j);
#----------------------------------------------------------------------------   
    elif(fun_code == 4):#搜尋附近店家
        nearby_search();
#----------------------------------------------------------------------------
    elif(fun_code == 5):
        name = input("請輸入歌曲名稱") #say('請說出歌曲名稱');
        #music_client = CloudSpeechClient();
        #name = music_client.recognize(language_code=zh-TW,hint_phrases=None)
        play_music(name);
#----------------------------------------------------------------------------
    elif(fun_code == 6):
        index = text.find("搜尋");
        ofs = 2;
        if(index==-1):
            index = text.find("查詢");
            ofs = 2;
        if(index==-1):
            index = text.find("找尋");
            ofs = 2;
        if(index==-1):
            index = text.find("找");
            ofs = 1;
        if(index==-1):
            index = text.find("吃");
            ofs = 1;
        if(index==-1):
            index = text.find("喝");
            ofs = 1;
        text_search(text[index+ofs:]);
#----------------------------------------------------------------------------
    elif(fun_code == 7):
        #speech_client = CloudSpeechClient();
        #say("請輸入起始站")
        #OStation = speech_client.recognize(language_code=zh-TW,hint_phrases=None);
        #say("請輸入目的站")
        #DStation = speech_client.recognize(language_code=zh-TW,hint_phrases=None);
        HSR_Search(OStation,DStation);
#---------------------------------------------------------------------------
    elif(fun_code == 8):
        time_ima();
#---------------------------------------------------------------------------
    elif(fun_code == 9):
        joke();
        
def get_lat_lng(): #定位 return 經緯度
    url="https://www.googleapis.com/geolocation/v1/geolocate?key="+key
    geo_res=requests.post(url)
    geo_res = json.loads(geo_res.text);
    lat = geo_res["location"]["lat"]; 
    lng = geo_res["location"]["lng"]; 
    lat_lng = str(lat)+","+str(lng);
    return lat_lng;

def covert_to_city():
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" +get_lat_lng()+"&key="+key+"&language=zh-TW";
    add = requests.get(url);
    add = add.text;
    formatadd = add[add.find("formatted_address"):add.find("geometry")-1];
    city = formatadd[formatadd.find("台灣")+2:formatadd.find("台灣")+4];
    return city;    
    
def nearby_search(): #搜尋附近餐廳
    url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?key="+key+"&location="+get_lat_lng()+"&language=zh-TW&radius=500&type=restaurant"
    nearby_res = requests.get(url)
    nearby_res = json.loads(nearby_res.text);
    restaurant_list = nearby_res["results"];
    output = "為您搜尋附近的餐廳:"
    index = 0;
    for i in restaurant_list:
        if(index >= 5):
            break;
        name = i["name"];
        output+=name;
        output+=","
        index++;
    print(output); # say(output);
    
def choice_motion(target): #1:查詢天氣 2:查詢降雨機率 3:查詢天氣型態 4:搜尋附近店家 5:播放音樂 6:搜尋店家 7:高鐵時刻
    return {
    '天氣':1,
    '下雨':2,
    '降雨':2,
    '氣候':3,
    '餐廳':4,
    '美食':4,
    '店家':4,
    '午餐':4,
    '晚餐':4,
    '早餐':4,
    '想聽':5,
    '聽':5,
    '播放':5,
    '唱歌':5,
    '音樂':5,
    '播音':5,
    '搜尋':6,
    '找':6,
    '找尋':6,
    '尋找':6,
    '查詢':6,
    '想吃':6,
    '想喝':6,
    '吃':6,
    '喝':6,
    '高鐵':7,
    '高鐵時刻':7,
    '時間':8,
    '笑話':9
    }.get(target,0)

def handle_result(temp_str_noun=" ",temp_str_place=" ",temp_str_time=" ",temp_str_verb=" ") :
    filtter = ", \'"; #切好的list只抓出需要部份
    filtter2 = "\')"
    index = 0;
    while index<len(temp_str_noun): #將字串篩掉多於的符號再丟入新的list(nounlist)
        index = temp_str_noun.find(filtter,index)
        if index == -1:
            break;
        index+=3;
        end = temp_str_noun.find(filtter2,index);
        temp_str = temp_str_noun[index:end];
        nounlist.append(temp_str)
    index = 0;
    while index<len(temp_str_place): #將字串篩掉多於的符號再丟入新的list(placelist)
        index = temp_str_place.find(filtter,index)
        if index == -1:
            break;
        index+=3;
        end = temp_str_place.find(filtter2,index);
        temp_str = temp_str_place[index:end];
        placelist.append(temp_str)
    index = 0;
    while index<len(temp_str_time): #將字串篩掉多於的符號再丟入新的list(timelist)
        index = temp_str_time.find(filtter,index)
        if index == -1:
            break;
        index+=3;
        end = temp_str_time.find(filtter2,index);
        temp_str = temp_str_time[index:end];
        timelist.append(temp_str)
    index = 0;
    while index<len(temp_str_verb): #將字串篩掉多於的符號再丟入新的list(verblist)
        index = temp_str_verb.find(filtter,index)
        if index == -1:
            break;
        index+=3;
        end = temp_str_verb.find(filtter2,index);
        temp_str = temp_str_verb[index:end];
        verblist.append(temp_str)

def play_music(name):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(name, download=False)
    except Exception:
        print ('抱歉，無法找到此首歌曲'); # say('抱歉，無法找到此首歌曲');
        return

    if meta:
        info = meta['entries'][0]
        vlc_player.set_media(vlc_instance.media_new(info['url']))
        vlc_player.play();
        print ('為您播放' + re.sub(r'[^\s\w]', '', info['title'])); #say('為您播放' + re.sub(r'[^\s\w]', '', info['title']))
        
def check_statue_btn():
    if(vlc_player.get_state() == vlc.State.Playing):
        vlc_player.set_pause(True);
    elif(vlc_player.get_state() == vlc.State.Paused):
        vlc_player.set_pause(False);
    else:
        time_ima();
        
def time_ima():
    output = "現在時間為";
        AM_PM = datetime.now().strftime("%p");
        if(AM_PM == "AM"):
            result = datetime.now().strftime("早上%I點%M分");
        elif(AM_PM == "PM"):
            result = datetime.now().strftime("下午%I點%M分");
        output += result;
        say(output);
    
def text_search(query): #搜尋特定店家營業資訊
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+ query +"&language=zh-TW&key="+ key;
    data = requests.post(url)
    data = json.loads(data.text);
    try:
        place_id = data["results"][0]["place_id"];
    except IndexError:
        return 0;
    detail_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+ place_id +"&fields=name,rating,formatted_phone_number,opening_hours,formatted_address&language=zh-TW&key="+ key;
    detail_result = requests.get(detail_url);
    detail_result = json.loads(detail_result.text);
    today_weekday = datetime.today().isoweekday();
    open_now = False;
    #if(today_weekday==7):
        #today_weekday = 0;
    address = detail_result["result"]["formatted_address"];
    name = detail_result["result"]["name"];
    try:
        phone = detail_result["result"]["formatted_phone_number"];
    except KeyError:
        phone = "error";
    try:
        open_now = detail_result["result"]["opening_hours"]["open_now"];
        weekly_text = detail_result["result"]["opening_hours"]["weekday_text"][today_weekday-1];
        #close = detail_result["result"]["opening_hours"]["periods"][today_weekday]["close"]["time"];
        #close_time = close[:2] + ':' + close[2:];
        #opend = detail_result["result"]["opening_hours"]["periods"][today_weekday]["open"]["time"];
        #open_time = opend[:2] + ':' + opend[2:];
    except KeyError:
        weekly_text = "error";
    #period = detail_result["result"]["opening_hours"]["periods"][today_weekday];
    if(weekly_text.find("-")!=-1): #-1 = 24小時營業
        close_time = weekly_text[weekly_text.find("-")+2:];
    else:
        weekly_text = weekly_text[3:]
    if(open_now):
        if(phone=="error"):
            output = "為您搜尋" + name + "," + address + "目前營業中 ，營業時間為" + weekly_text + "該店家未提供聯絡電話"; 
        else:
            output = "為您搜尋" + name + "," + address + ",電話為" + phone + "目前營業中 ，營業時間為" + weekly_text; 
    elif(phone=="error" and weekly_text=="error"):
        output = "為您搜尋" + name + "," + address + ",該店家未提供連絡電話與營業時間";
    elif(weekly_text=="error"):
        output = "為您搜尋" + name + "," + address + ",電話為" + phone + "店家未提供營業時間"
    elif(phone=="error"):
        output = "為您搜尋" + name + "," + address + "目前未營業,今日營業時間為" + weekly_text + "該店家未提供聯絡電話"; 
    else:
        output = "為您搜尋" + name + "," + address + ",電話為" + phone + "目前未營業,今日營業時間為" + weekly_text; 
    
    print(output); #say(output);
        
def get_auth_header():
        app_id = 'df8a7fea3a07476ba24ae1add84120e4'
        app_key = 'mpUylfv7NssdhHXcmyraGHWWaUQ'
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

def HSR_StationID(Station):
    return {
    '南港':"0990",
    '台北':"1000",
    '板橋':"1010",
    '桃園':"1020",
    '新竹':"1030",
    '苗栗':"1035",
    '台中':"1040",
    '彰化':"1043",
    '雲林':"1047",
    '嘉義':"1050",
    '台南':"1060",
    '左營':"1070",
    '高雄':"1070",
    '新左營':"1070"
    }.get(Station,'error')

def HSR_Search(OStation,DStation):
    OStationID = HSR_StationID(OStation); #獲取起始站ID
    DStationID = HSR_StationID(DStation); #獲取終點站ID
    output = OStation + "到" + DStation + "的下三班起站與目的站到站時間如下:\n";
    if(OStationID!="error" or DStationID !="error"):
        date_today = datetime.now().strftime('%Y-%m-%d');
        url = "https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/"+OStationID+"/to/"+DStationID+"/"+date_today+"?$select=DailyTrainInfo%2COriginStopTime%2CDestinationStopTime&$top=70&$format=JSON";    
        data = requests.get(url,headers = get_auth_header());
        data = json.loads(data.text);
        now = datetime.now().strftime('%H:%M');
        time_now=datetime.strptime(now,'%H:%M');
        index = 0;
        for i in data:
            arrival_time = datetime.strptime(i["OriginStopTime"]["ArrivalTime"],'%H:%M');
            delta = arrival_time - time_now;
            #print(type(delta.seconds));
            if (delta.seconds>0 and ((delta.seconds/60)/60)<3):
                if(index>=3):
                    break;
                try:
                    TrainNo = i["DailyTrainInfo"]["TrainNo"];
                    Oarrival = i["OriginStopTime"]["ArrivalTime"];
                    Darrival = i["DestinationStopTime"]["ArrivalTime"];
                    temp = "車次" + TrainNo + ", 到達起站時間為" + Oarrival + ", 到達目的時間為" + Darrival + "\n";
                except:
                    output="獲取車次資料出現錯誤";
                    break;
                output += temp;
                index+=1;
        print(output);
    else:
        print("所輸入的地點無高鐵站，請重新輸入"); # say("所輸入的地點無高鐵站，請重新輸入");
        
def joke():
    rnd = random.randint(1,5);
    output = joke_dictionary(str(rnd));
    priint(output); # say(output);

def joke_dictionary(index):
    return {
    '1':"冰塊最想做什麼事？ ，，，， 「退伍」因為他當冰當很久了",
    '2':"我昨天吃了一條鮭魚 ，，，， 牠今天在我胃食道逆流",
    '3':"為何電腦不快樂？ ，，，， 因為有D槽(低潮)。",
    '4':"為什麼科學園區裡面常常跌倒 ，，，， 因為那裡很多半導體",
    '5':"門鎖壞了要找誰 ，，，， 碩班學長（因為他們是研究所的）",
    }.get(index,'error')
    
#text = input("輸入 :");
#speech_recognition():


"""

def main():
    logging.basicConfig(level=logging.DEBUG)
    #say('Test')
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args();
    vlc_player.audio_set_volume(15);
    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language);
    with Board() as board:
        board.button.when_pressed = check_statue_btn;
        while True:
            speech_recognition();

if __name__ == '__main__':
    main()


"""

        elif '幾點' in text:
            time_ima();
        elif '陪我聊天' in text:
            say('你想聊甚麼呢?');
        elif '我好無聊' in text:
            say('我可以講笑話給你聽');
            joke();
        elif '我肚子餓了' in text:
            say('你可以說說看 查詢附近餐廳 讓我當您找尋附近餐廳哦');
        elif '早安' in text:
            say('早安 ˋ祝您有個美好的一天');
        elif '晚安' in text:
            say('晚安，祝你有個好夢');
        elif '你是男生還是女生' in texy:
            say('我都被叫做google小姐應該算是女生吧');
        elif '今天星期幾' in text:
            output = '今天星期'+ str(datetime.today().isoweekday());
            say(output);
        elif '今天幾號' or '今天日期' or '今天幾月幾號' in text:
            output = '今天是' + datetime.today().strftime("%m月%d號");
            say(output);
