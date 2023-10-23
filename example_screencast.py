import pyautogui
import numpy as np
import cv2  # opencv-python
import threading
import sounddevice as sd
import queue
import soundfile as sf
from moviepy.editor import AudioFileClip, VideoFileClip
import tkinter as tk
from tkinter import messagebox
import time


class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()
        # Set up screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        # Set up the codec and create a VideoWriter object
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = None
        # Set up audio parameters
        self.sample_rate = 44100  # CD quality
        self.audio_buffer = queue.Queue()
        # Flag to indicate recording state
        self.recording = False
        self.recording_thread = None

    def start_recording(self):
        self.recording = True
        self.out = cv2.VideoWriter("output_screen_recording.avi", self.fourcc, 20.0,
                                   (self.screen_width, self.screen_height))
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        # Start recording video in a separate thread
        self.start_time = time.time()  # Record start time
        self.num_frames = 0  # Initialize frame counter
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()
        # Start recording audio
        with sd.InputStream(callback=self.record_audio, channels=2, samplerate=self.sample_rate):
            self.root.wait_window()  # Wait for the recording to finish

    def stop_recording(self):
        self.recording = False
        self.recording_thread.join()
        self.out.release()
        self.save_audio()
        self.combine_audio_video()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Recording Finished", "Recording has been saved.")

    def record_screen(self):
        while self.recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.out.write(frame)
            self.num_frames += 1  # Increment frame counter

    def record_audio(self, indata, frames, time, status):
        self.audio_buffer.put(indata.copy())

    def save_audio(self):
        audio_data = []
        while not self.audio_buffer.empty():
            audio_data.append(self.audio_buffer.get())
        audio_data = np.concatenate(audio_data, axis=0)
        sf.write("output_recorded_audio.wav", audio_data, self.sample_rate)

    def combine_audio_video(self):
        video_clip = VideoFileClip("output_screen_recording.avi")
        audio_clip = AudioFileClip("output_recorded_audio.wav")

        # Calculate the actual frame rate based on recorded frames and elapsed time
        actual_frame_rate = self.num_frames / (time.time() - self.start_time)

        final_clip = video_clip.set_audio(audio_clip)
        final_clip = final_clip.set_duration(audio_clip.duration)  # Adjust duration
        final_clip = final_clip.set_fps(actual_frame_rate)  # Set the calculated frame rate
        final_clip.write_videofile("output_video.mp4", codec="libx264")


root = tk.Tk()
app = ScreenRecorderApp(root)
root.mainloop()
