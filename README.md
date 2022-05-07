# 智慧音箱設計
![海報](https://user-images.githubusercontent.com/56255361/167265411-7434a063-7406-4dbf-aa53-337238bca17b.jpg)

## 目錄

[基本語音輸入](#基本語音輸入)

[查詢天氣](#查詢天氣)

[定位](#定位)

[查詢附近餐廳](#查詢附近餐廳)

[播放音樂](#播放音樂)

[查詢特定餐廳](#查詢特定餐廳)

[其他功能](#其他功能)
## 實作功能
### 基本語音輸入
* 透過使用Google Cloud中的 *cloud speech API* 將語音輸入轉成文字。
* 使用Articut API切割語句成動詞、名詞等，並判斷是否有功能關鍵字，並執行該功能。
### 查詢天氣
* 此功能將會察看使用者是否有輸入地點，若無則定位。
* 將地點(各大縣市)傳入中央氣象局所提供的天氣API，獲得該地天氣資訊。
```python
def get_url(city): # 獲取該城市的URL need to change weather_api_key
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
```
### 定位
* 透過*Google Geolocation API*定位獲得經緯度，再透過*Google GeoCode API* 將經緯度轉成地址。
```python
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
```
### 查詢附近餐廳
* 定位使用者位置 並將位置傳入 Google Place Nearby Search ，獲得附近店家資料。
```python
def nearby_search():
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
```
### 播放音樂
* 請使用者輸入欲播放歌曲名稱。
* 使用youtube_dl 搜尋歌曲，並抓取搜尋結果第一個的網址。
* 使用Python vlc套件透過網址播放。
```python
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
```
### 查詢特定餐廳
* 當偵測到查詢、尋找、找等動詞時，將後面部分當作搜尋的詞彙丟入*Google Place Search API*
* 根據店家所提供的資料，執行不同的回覆。
```python
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
```
### 查詢高鐵時刻
* 請使用者輸入起始站與終點站 ex:南港、台北、新左營等。
* 透過PTX公共運輸平台獲取高鐵時刻表。
* 回覆接下來三班的車次、到站時間。
```python
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
```
### 其他功能
* 一般基礎對話。
* 講笑話。
* 按鈕控制播放音樂的暫停與繼續。
* 現在時刻。
## 專題影片 
=>  https://youtu.be/nSlT1MyS-qA







