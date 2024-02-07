from flask import Flask, request, jsonify
import requests
import os
import openai
import time
import codecs
import serial
import sys

web_port="5001"

app = Flask(__name__)

API_KEY = "YOUR API KEY"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "audio/mp3"
}
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files['audio']
    
    # 儲存語音檔案到伺服器
    filepath = os.path.join("sound", "voirec.mp3")
    audio_file.save(filepath)
    openai.api_key = "YOUR API KEY"
    with open(filepath, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    #print(type(transcript))
    print(transcript['text'])
    emotion=transcript['text']
    
    my_prompt=emotion+" 請你根據以上的心情，判斷是 positive or negative，並根據心情推薦以下三種飲料的其中一種：雪碧(代號1),紅茶(代號2),可樂(代號3)。請安撫這個人，簡約說明為甚麼推薦這種飲料，在80字以內，務必使用繁體中文。回覆的格式為：\{飲料代號\}@\{回覆\}@{ positive or negative }，一定要完整回覆"

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "你是一個心理諮商師"},
        {"role": "user", "content": my_prompt}
      ]
)
    #response = openai.Completion.create(
      #model="text-davinci-003",
      #prompt=my_prompt,
      #temperature=0.7,
      #max_tokens=1000,
      #top_p=1,
      #frequency_penalty=0.0,
      #presence_penalty=0.6,
    #)
    #print(emotion)
    #print(my_prompt)
    print(response.choices[0].message['content'])
    aa=response.choices[0].message['content'].split("@")
    print(aa)
    #if len(aa)<3:
    aa.append("positive") 
    drinking_num=aa[0]
    suggest=aa[1]
    try:
      emotion_status=aa[2]
    except:
      aa.append("positive") 
    #yoyo=response.choices[0].text
    #print(yoyo)
    print(drinking_num)
    #print(suggest)
    print(emotion_status)
    #Serial給Arduino
    #COM_PORT = 'COM47' 
    #BAUD_RATES = 9600
    #ser = serial.Serial(COM_PORT, BAUD_RATES)
    print("飲料代號:"+str(drinking_num))
    #print(type(drinking_num))
    #ser.write((bytes(drinking_num,encoding='utf-8')))
    #ser.write((bytes("2",encoding='utf-8')))
    #time.sleep(2)              # 暫停0.5秒，再執行底下接收回應訊息的迴圈
    try:
      SerialObj = serial.Serial('COM3') # COMxx   format on Windows
                                  # ttyUSBx format on Linux
      SerialObj.baudrate = 9600  # set Baud rate to 9600
      SerialObj.bytesize = 8     # Number of data bits = 8
      SerialObj.parity   ='N'    # No parity
      SerialObj.stopbits = 1     # Number of Stop bits = 1
      time.sleep(3)

      SerialObj.write((bytes(drinking_num,encoding='utf-8')))      #transmit 'A' (8bit) to micro/Arduino
      SerialObj.close()          # Close the port 
    except:
      pass
    #以下給前端
    movie_url_p_blacktea="http://127.0.0.1:"+web_port+"/static/blacktea_p.mp4"
    movie_url_n_blacktea="http://127.0.0.1:"+web_port+"/static/blacktea_n.mp4"
    movie_url_p_sprite="http://127.0.0.1:"+web_port+"/static/sprite_p.mp4"
    movie_url_n_sprite="http://127.0.0.1:"+web_port+"/sprite_n.mp4"
    movie_url_p_cola="http://127.0.0.1:"+web_port+"/static/cola_p.mp4"
    movie_url_n_cola="http://127.0.0.1:"+web_port+"/static/cola_n.mp4"
    movie_url=""
    if drinking_num=='1':
      if emotion_status=="positive":
        movie_url= movie_url_p_sprite
      else:
        movie_url=movie_url_n_sprite
    elif drinking_num=='2':
      if emotion_status=="positive":
        movie_url=movie_url_p_blacktea
      else:
        movie_url=movie_url_n_blacktea
    elif drinking_num=='3':
      if emotion_status=="positive":
        movie_url=movie_url_p_cola
      else:
        movie_url=movie_url_n_cola
    print(movie_url)
    #movie_url="https://talks-api-results.d-id.com/google-oauth2%7C117672023894599083572%2Ftlk_IOYlogSIeYFtHOCu1X-1x%2Fimage.mp4"
    return jsonify({"text": emotion+"@@"+suggest+"@@"+movie_url})
    #return "a"

if __name__ == '__main__':
    app.run(debug=True,port=int(web_port))
