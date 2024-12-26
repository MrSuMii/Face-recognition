import tkinter as tk
import cv2
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class FaceDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.container = tk.Frame(window)
        self.container.pack(expand=True, fill="both")
    
        self.page1 = StartPage(self.container, self)
        self.page1.pack(expand=True, fill="both")
        
        self.page2 = WebcamPage(self.container, self)
    
    def show_webcam_page(self):
        self.page1.pack_forget()
        self.page2.pack(expand=True, fill="both")
        self.page2.start_webcam()
    
    def quit(self):
        self.page2.stop_webcam()
        self.window.destroy()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.start_button = tk.Button(self, text="Start", command=self.start_webcam)
        self.start_button.pack(pady=20)
    
    def start_webcam(self):
        self.controller.show_webcam_page()

class WebcamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.cap = cv2.VideoCapture(0)
        self.paused = False
        
        self.canvas = tk.Canvas(self, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)
        
        self.pause_button_text = tk.StringVar()
        self.pause_button_text.set("Pause")
        self.pause_button = tk.Button(self.button_frame, textvariable=self.pause_button_text, command=self.toggle_pause, width=10)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit, width=10)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
        
        self.delay = 10
        self.update()
    
    def update(self):
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = face_cascade.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.after(self.delay, self.update)
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button_text.set("Resume")
        else:
            self.pause_button_text.set("Pause")
    
    def start_webcam(self):
        self.controller.show_webcam_page()
    
    def stop_webcam(self):
        self.cap.release()
    
    def quit(self):
        self.cap.release()
        self.controller.quit()
4
root = tk.Tk()
app = FaceDetectionApp(root, "Face Detection App")
root.mainloop()
