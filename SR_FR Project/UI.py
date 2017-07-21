import time
import tkMessageBox
import tkinter
from PIL import ImageTk, Image
from Tkconstants import LEFT, RAISED, INSERT, W, HORIZONTAL, DISABLED, NORMAL
from Tkinter import StringVar, IntVar, Radiobutton
from tkinter import filedialog
import os
import recognize
from example.sr_image_example import LRImage_example
import ttk
import thread
import cv2

top = tkinter.Tk()
top.title("Super-Resolution Face Recognition Application, by Mohamad Hosein Danesh")
top.config(width = 1440, height = 600)


var1 = StringVar()
var1.set("")

urlLabel1 = tkinter.Label(top, textvariable = var1, bg = "#a4bfea")
urlLabel1.config(width = 50)
urlLabel1.place(x = 180, y = 85)

# get LR image url
var00 = IntVar()

def var00Sel():
    selection = "You selected the option " + str(var00.get())
    if var00.get() == 1:
        if button1.cget('state') == "disabled":
            button1.configure(state = NORMAL)
        print (button1.cget('state'))
    else:
        button1.configure(state = DISABLED)

        videoPreparation()
        print "video input"


def videoPreparation():
    # tkinter.Label(window, text="this is the window").pack()

    var1.set("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/webcam-input.jpg")
    urlLabel1 = tkinter.Label(top, textvariable=var1)

    cap = cv2.VideoCapture(0)

    window = tkinter.Toplevel()
    window.bind('<Escape>', lambda e: window.quit())
    lmain = tkinter.Label(window)
    lmain.pack()
    global counter
    counter = 0

    def show_frame():
        global counter
        _, frame = cap.read()
        cv2.imwrite("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/webcam-input.jpg", frame)
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        while counter != 100:
            counter += 1
            lmain.after(10, show_frame)

    show_frame()
    # cap.release()





R00 = Radiobutton(top, text="Single Image", variable=var00, value=1, command=var00Sel)
R00.invoke()
R00.place(x = 180, y = 15)

R01 = Radiobutton(top, text="Webcam", variable=var00, value=2, command=var00Sel)
R01.place(x = 350, y = 15)



label1 = tkinter.Label(top, text = "Low-Resolution Image", relief=RAISED)
label1.config(width = 50)
label1.place(x = 180, y = 50)



def click1():
    filename = filedialog.askopenfilename(initialdir='/Desktop')
    var1.set(filename)
    urlLabel1 = tkinter.Label(top, textvariable = var1)

button1 = tkinter.Button(top, text ="Browse", command = click1)
button1.place(x = 10, y = 85)
button1.config(width = 15)


# super-resolution process
label2 = tkinter.Label(top, text = "Super-Resolution Process", relief=RAISED)
label2.place(x = 180, y = 150)
label2.config(width = 50)

progressbar = ttk.Progressbar(top, orient=HORIZONTAL, length=450, mode='indeterminate')


def process_thread():
    print "SR Process bar"
    if not var1.get():
        print "1"
        tkMessageBox.showinfo("Alert!", "No image path specified!")
    else:
        print "2"
        progressbar.place(x=180, y=190)
        print "3"
        progressbar.start()
        print "4"
        thread.start_new_thread(sr_start, ())
        print "5"


def sr_start():
    print "6"
    print var1.get()
    LRImage_example(var1.get())
    print "7"
    progressbar.stop()
    changeImage("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/high-res.png")
    tkMessageBox.showinfo("Alert!", "Done! The SR image is saved here: /SR_FR Project/high-res.png")


button2 = tkinter.Button(top, text = "Start SR Process", command = process_thread)
button2.place(x = 10, y = 185)
button2.config(width = 15)


# recognition algorithm radio buttons
var3 = IntVar()
var4 = IntVar()

def var3Sel():
    selection = "You selected the option " + str(var3.get())
    print selection

def var4Sel():
    selection = "You selected the option " + str(var4.get())
    print selection

label5 = tkinter.Label(top, text = "Cascade for Detection", relief=RAISED)
label5.place(x = 180, y = 350)
label5.config(width = 25)

R1 = Radiobutton(top, text="HAAR Cascade", variable=var3, value=1, command=var3Sel)
R1.invoke()
R1.place(x = 180, y = 385)

R2 = Radiobutton(top, text="LBP Cascade", variable=var3, value=2, command=var3Sel)
R2.place(x = 380, y = 385)


label6 = tkinter.Label(top, text = "Feature Extraction Algorithms", relief=RAISED)
label6.place(x = 180, y = 430)
label6.config(width = 25)

R3 = Radiobutton(top, text="lbphFace Recognizer", variable=var4, value=1, command=var4Sel)
R3.invoke()
R3.place(x = 180, y = 465)

R4 = Radiobutton(top, text="fisherFace Recognizer", variable=var4, value=2, command=var4Sel)
R4.place(x = 380, y = 465)

R5 = Radiobutton(top, text="eigenFace Recognizer", variable=var4, value=3, command=var4Sel)
R5.place(x = 180, y = 495)

# face recognition process
label3 = tkinter.Label(top, text = "Face Recognition Process", relief=RAISED)
label3.place(x = 180, y = 250)
label3.config(width = 50)

var2 = StringVar()
var2.set("")

urlLabel2 = tkinter.Label(top, textvariable = var2, bg = "#a4bfea")
urlLabel2.config(width = 50)
urlLabel2.place(x = 180, y = 285)

def click2():
    filename = filedialog.askopenfilename(initialdir='/Desktop')
    var2.set(filename)
    urlLabel2 = tkinter.Label(top, textvariable = var2)

def click3():
    filename = var2.get()
    recognizedImage = recognize.prepareImage(filename, str(var4.get()), str(var3.get()))
    changeImage(recognizedImage)


button3 = tkinter.Button(top, text ="Browse", command = click2)
button3.place(x = 10, y = 285)
button3.config(width = 15)

button4 = tkinter.Button(top, text ="Start Face Recognition", command = click3)
button4.place(x = 10, y = 385)
button4.config(width = 15)



# result
label4 = tkinter.Label(top, text = "Result", relief = RAISED)
label4.config(width = 72)
label4.place(x=750, y=15)

image = Image.open("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/white-plain.png")
image = image.resize((650, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
panel = tkinter.Label(top, image = img)
panel.place(x=750, y=50)


def changeImage(recognizedPath):
    newImage = Image.open(recognizedPath)
    newImage = newImage.resize((650, 500), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(newImage)
    panel.configure(image = newImg)
    panel.image = newImg


top.mainloop()



