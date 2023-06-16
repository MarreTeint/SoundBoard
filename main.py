import numpy
import threading
import tkinter
import customtkinter
import serial
import soundfile as sf
import sounddevice as sd
import os

ser = serial.Serial('COM3', 9600, timeout=0)
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
customtkinter.deactivate_automatic_dpi_awareness()

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1280x720")
app.title("SoundBoard")

sound1 = sf.read("sounds/sound1.mp3")
sound2 = sf.read("sounds/sound2.mp3")
def read_from_port(ser):
    while True:
        reading = ser.readline().decode()
        #clear reading of whitespace
        reading = reading.strip()
        if reading != "":
            print(reading)
            if(reading == "1"):
                playing_sound_threaded(sound1)
            elif(reading == "2"):
                playing_sound_threaded(sound2)

def play_sound(sound, device):
    sd.play(sound[0], sound[1], device=device)
    sd.wait()
    sd.stop()

def playing_sound_threaded(sound):
    threading.Thread(target=play_sound, args=(sound, 9)).start()
    threading.Thread(target=play_sound, args=(sound, 16)).start()

def button_play() :
    print("button pressed")
    playing_sound_threaded(sound1)
    #if sound == "sound1.mp3":
        #    playing_sound_threaded(sound1)
    #elif sound == "sound2.mp3":
    #    playing_sound_threaded(sound2)

# Start the thread
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

def switch_event():
    print("switch toggled, current value:", switch_var.get())

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(fill=tkinter.BOTH, expand=True,padx=20, pady=20)

tabview.add("Mes sons")  # add tab at the end
tabview.add("Ajouter un son")  # add tab at the end
tabview.add("Parametres")
tabview.set("Mes sons")  # set currently visible tab

# Mes sons
for file in os.listdir("sounds"):
    if file.endswith(".mp3"):
        button = customtkinter.CTkButton(master=tabview.tab("Mes sons"), text=file.split('.')[0], command=button_play)
        button.pack(padx=20, pady=20)

# Ajouter un son
# Parametres
switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(master=tabview.tab("Parametres"), text="Custom SoundBoard", command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off")
switch.pack(padx=20, pady=20)

app.mainloop()