import pyaudio
import wave
from pydub import AudioSegment
import tkinter as tk
import threading

# 錄音參數
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
frames = []
is_recording = False

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

def record_audio():
    global frames, is_recording
    frames = []
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

def start_recording():
    global is_recording
    is_recording = True
    btn_start.config(state=tk.DISABLED)
    btn_stop.config(state=tk.NORMAL)
    print("錄音中...")
    threading.Thread(target=record_audio).start()

def stop_recording():
    global is_recording
    is_recording = False
    print("錄音結束")
    btn_start.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)
    
    # 將錄音數據保存為 WAV 文件
    with wave.open("temp.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    convert_to_mp3("temp.wav", "output.mp3")

def convert_to_mp3(wav_file, mp3_file):
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format="mp3")

root = tk.Tk()
root.title("錄音程式")

btn_start = tk.Button(root, text="開始錄音", command=start_recording)
btn_start.pack(pady=20)

btn_stop = tk.Button(root, text="結束錄音", command=stop_recording, state=tk.DISABLED)
btn_stop.pack(pady=20)

root.mainloop()

stream.stop_stream()
stream.close()
p.terminate()