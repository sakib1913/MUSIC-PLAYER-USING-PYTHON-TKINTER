import os
from tkinter import *
from PIL import ImageTk,Image
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading

from tkinter import ttk
from ttkthemes import  themed_tk as tk
from tkinter import filedialog

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
#canvas = Canvas(root,width=200,height=40)
#image=ImageTk.PhotoImage(Image.open("sakib.jpg"))
#canvas.create_image(0,0,anchor=NW,image=image)
#canvas.pack()

statusbar =ttk.Label(root, text="Welcome to MS", relief=SUNKEN, anchor=W,font='Times 13 italic')
statusbar.pack(side=BOTTOM, fill=X)

# create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# create the submenubar
subMenu = Menu(menubar, tearoff=0)

playlist=[]

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename= os.path.basename(filename_path)
    index=0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index+=1



menubar.add_cascade(label='file', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Maverick Studio',
                                'This is a music player build using python tkinter by @sakib_1913')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)

mixer.init()  # initilize the mixer
# root.geometry('300x300')
root.title("Maverick Studio")
# root.iconbitmap(r'002-music.ico')
#filelabel = Label(root, text='Lets make some noise!')
#filelabel.pack()

leftframe =Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30 )

playlistbox=Listbox(leftframe)
playlistbox.pack()

btn1 = ttk.Button(leftframe, text="+ ADD",command=browse_file)
btn1.pack(side=LEFT)

def delete_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlistbox.pop(selected_song)


btn2 = ttk.Button(leftframe, text="- DELETE", command=delete_song)
btn2.pack()


rightframe=Frame(root)
rightframe.pack(pady=30)

topframe= Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length: --:--',font='Arial 10 bold')
lengthlabel.pack(pady=5)
currenttimelabel = ttk.Label(topframe, text='Current Time: --:--',relief=GROOVE)
currenttimelabel.pack()


def show_detail(play_song):
    #filelabel['text'] = "Playing" + " " + os.path.basename(filename)
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total length" + "-" + timeformat
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()
def start_count(t):
    global paused
    current_time=0
    while current_time<= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + "-" + timeformat
            time.sleep(1)
           # t -= 1
            current_time += 1



def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song =int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + " " + os.path.basename(play_it)
            show_detail(play_it)
        except:
            tkinter.messagebox.showerror('FIle not found', 'Maverick studio Could not find file please check again')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


def set_val(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)
playPhoto = PhotoImage(file='img/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music,)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='img/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='img/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file='img/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='img/mute.png')
volumePhoto = PhotoImage(file='img/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_val)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

def on_closing():
    stop_music()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
