from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import threading 
from datetime import timedelta
import pyttsx3
from playsound import playsound
import googletrans
from googletrans import Translator


global contador, file_lesson_name, lesson, current_phrase, L_image_down_phrases_to_study,number_of_phrases_to_study
global hits
global misses 
global accuracy
file_lesson_name = ""
lesson = []
contador = 0
current_phrase = ""
number_of_phrases_to_study = 0
hits = 0
misses = 0
accuracy = 0.0

def play_audio_thread():
    global current_phrase
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 1.5)  # Volume 0-1
    # Voice IDs pulled from engine.getProperty('voices')
    # These will be system specific
    en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    gr_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
    # Use female German voice
    engine.setProperty('voice', gr_voice_id)        
    engine.say(current_phrase)
    
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()
        print("aleluya")

def play_audio():
    thread6 = threading.Thread(target = play_audio_thread)
    thread6.setDaemon(True)
    thread6.start()

def disable_buttons():
    global B_previous, B_play, B_next, B_check, B_help,Entry_image_left_input_entry
    B_previous["state"] = "disabled"
    B_play["state"] = "disabled"
    B_next["state"] = "disabled"
    B_check["state"] = "disabled"
    B_help["state"] = "disabled"
    Entry_image_left_input_entry["state"] = "disabled"

def enable_buttons():
    global B_previous, B_play, B_next, B_check, B_help,Entry_image_left_input_entry
    B_previous["state"] = "normal"
    B_play["state"] = "normal"
    B_next["state"] = "normal"
    B_check["state"] = "normal"
    B_help["state"] = "normal"
    Entry_image_left_input_entry["state"] = "normal"

def select_file_lesson_func():
    global file_lesson_name,lesson, current_phrase, contador,number_of_phrases_to_study
    contador = 0
    filename = filedialog.askopenfilename(initialdir = 'C:\\Users\\Dairon\\Documents\\202020\\python\\deutsch_app\\file_lessons')
    file_lesson_name = open(filename, "r")
    lesson = file_lesson_name.readlines()
    number_of_phrases_to_study = len(lesson)
    update_number_of_phrases_to_study(number_of_phrases_to_study)
    print(lesson)
    current_phrase = lesson[contador] #inizialize the current phrase
    print("Current phrase: "+current_phrase)
    enable_buttons()

def update_phrase_next():
    global contador,lesson, current_phrase, Entry_image_left_input_entry
    global L_image_left_output_message,L_image_left_output_notification
    global L_image_left_output_translation, img_end
    L_image_left_output_notification.configure(text = "")
    L_image_left_output_notification.update()
    L_image_left_output_message.configure(text = "")
    L_image_left_output_message.update()
    L_image_left_output_translation.configure(text = "")
    L_image_left_output_translation.update()
    
    Entry_image_left_input_entry.delete(0, END)
    Entry_image_left_input_entry.insert(0, "")
    if contador == len(lesson)-1:
        disable_buttons()
        def end_of_lesson():
            end_window = Tk()
            end_window.geometry("300x50+300+200")
            #algo = []
            #img_endd = ImageTk.PhotoImage(Image.open(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\end.JPG").resize((45,35), Image.ANTIALIAS))
            #algo.append(img_endd)
            L_end = Label(end_window,text = "LESSON FINISHED, CONGRATULATIONS!")
            L_end.pack(fill = "both", expand = "yes")
            end_window.after(2000,end_window.destroy)
            end_window.mainloop()
        thread7 = threading.Thread(target = end_of_lesson)
        thread7.setDaemon(True)
        thread7.start()
    if contador < len(lesson)-1:
        contador += 1
        current_phrase = lesson[contador] #update the current phrase
        play_audio()
        print(contador,current_phrase)
def update_phrase_next_bind(event):
    update_phrase_next()
def update_phrase_previous():
	global contador, lesson, current_phrase
	if contador > 0:
		contador -= 1
		current_phrase = lesson[contador] # update the current phrase
		play_audio()
		print(contador,current_phrase)

def update_number_of_phrases_to_study(number_of_phrases_to_study):
	global L_image_down_phrases_to_study_update
	L_image_down_phrases_to_study_update.configure(text = str(number_of_phrases_to_study))
	L_image_down_phrases_to_study_update.update()

def update_hits():
    global L_image_down_hits_update, hits
    L_image_down_hits_update.configure(text = str(hits))
    L_image_down_hits_update.update()

def update_misses():
	global L_image_down_misses_update, misses
	L_image_down_misses_update.configure(text = str(misses))
	L_image_down_misses_update.update()

def update_accuracy():
	global accuracy, lesson, hits, L_image_down_accuracy_update
	accuracy = hits/len(lesson)*100
	L_image_down_accuracy_update.configure(text = str(accuracy)[0:3]+"%")
	L_image_down_accuracy_update.update()
def check_function():
    global contador, L_image_left_output_message,Entry_image_left_input_entry,current_phrase,L_image_left_output_notification
    global L_image_left_output_translation
    global hits, misses
    L_image_left_output_message.configure(text = "")
    acerto = "false"
    frase_01 = Entry_image_left_input_entry.get()
    print(current_phrase[0:(len(current_phrase)-1)],frase_01)
    print(len(current_phrase),len(frase_01))
    
    if current_phrase[0:(len(current_phrase)-1)].lower() == frase_01.lower():
        acerto = "true"
        frase_02 = current_phrase
        L_image_left_output_message.configure(text = frase_02)
        L_image_left_output_message.update()
    if acerto == "true":
        hits += 1
        update_hits()
        update_accuracy()
        L_image_left_output_notification.configure(text = "You did it :)",font = ("Courier",20),foreground = "green")
        L_image_left_output_notification.update()
        translator = Translator()
        t = translator.translate(current_phrase,src='de',dest='es')
        L_image_left_output_translation.configure(text = t.text)
        L_image_left_output_translation.update()
        playsound(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\sound_effects\right_answer.MP3")
    else:
        misses += 1
        update_misses()
        L_image_left_output_notification.configure(text = "Try it again :(",font = ("Courier",20),foreground = "red")
        L_image_left_output_notification.update()
        playsound(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\sound_effects\wrong_answer.MP3")
    print("You hit return.")
def check_thread():
    thread8 = threading.Thread(target = check_function)
    thread8.setDaemon(True)
    thread8.start()	
def enter_check_function(event):
	check_function()
def show_help_thread():
    global current_phrase
    ventana = Tk()
    ventana.geometry("500x100+150+200")
    L_help = Label(ventana,text = current_phrase)
    L_help.pack(fill = "both", expand = "yes")
    ventana.mainloop()


def help_function():
    thread2 = threading.Thread(target=show_help_thread)
    thread2.setDaemon(True)
    thread2.start()
def new_file_thread():
    master = Tk()
    master.geometry("200x100+300+200")
    label = Label( master, text = "Inserte el nombre del archivo")
    label.pack()
    e = Entry(master)
    e.pack()
    e.focus_set()
    def callback():
        filename = e.get()
        print(filename) # This is the text you may want to use later
        f = open("C:\\Users\\Dairon\\Documents\\202020\\python\\deutsch_app\\file_lessons\\"+filename+".txt","w+")
        
        master.destroy()
    def f_cancelar():
        master.destroy()
    b = Button(master, text = "OK", width = 10, command = callback)
    b_cancelar = Button(master, text = "Cancelar", width = 10, command = f_cancelar)
    b.pack()
    b_cancelar.pack()
    master.mainloop()
def create_new_file():
    thread3 = threading.Thread(target=new_file_thread)
    thread3.setDaemon(True)
    thread3.start()


def append_data_into_file_thread():
    #root = Tk() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename(initialdir = 'C:\\Users\\Dairon\\Documents\\202020\\python\\deutsch_app\\file_lessons') # show an "Open" dialog box and return the path to the selected file
    print(filename)
    if filename != "":
        print(filename)
        window_append = Tk()
        window_append.geometry("350x100+225+250")

        def ok_func():
            f = open(filename,"a")
            frase_to_append = entry.get()
            f.write("\n"+frase_to_append)
            f.close()
            entry.delete(0,END)
        def ok_func_bind(event):
            ok_func()
        def cancel_func():
            window_append.destroy()
        info_label = Label(window_append,text = "Inserte una nueva frase")
        info_label.grid(row = 0, column = 0, columnspan = 2,rowspan = 1,sticky = W+E+N+S,padx=100, pady=5)

        entry_phrase = StringVar()
        entry = Entry(window_append,textvariable = entry_phrase,width = 45)
        entry.bind('<Return>',ok_func_bind)
        entry.grid(row = 1, column = 0, columnspan = 2,rowspan = 1, sticky = N, padx = 2)

        ok_button = Button(window_append, text = "OK",height = 2, width = 15, command = ok_func)
        ok_button.grid(row = 2,column = 0, sticky = N)

        cancel_button = Button(window_append, text = "Cancelar",height = 2, width = 15, command = cancel_func)
        cancel_button.grid(row = 2, column = 1, sticky = N)

        window_append.mainloop()
    #root.destroy()
def append_data_into_file():
    thread4 = threading.Thread(target=append_data_into_file_thread)
    thread4.setDaemon(True)
    thread4.start()

################################################################################################################
################################################# INTERFACE ####################################################
################################################################################################################
root = Tk()
root.geometry("650x450+100+100")
root.title("Learn German with Dairon")
root.resizable(width = FALSE, height = FALSE)

# imagen 
LF_image = LabelFrame(root,text = "",labelanchor = "n",height=120, width=450)
LF_image.pack(fill = "both")
#PI_object = PhotoImage(file = "/german_flag.jpeg")
img = ImageTk.PhotoImage(Image.open("german_flag.jpeg").resize((645,120), Image.ANTIALIAS))
L_image = Label(LF_image,image = img)
L_image.pack()

#global img_end 
#img_end = ImageTk.PhotoImage(Image.open("end.JPG"))

LF_display_info = Frame(root,height = 240,width = 450)
LF_display_info.pack(fill = "both", expand = "yes")
LF_image_left = LabelFrame(LF_display_info,text = "Dictation zone",labelanchor = "n",height=240, width=240)
LF_image_left.pack(fill = "both", expand = "yes",side = LEFT)
LF_image_left_input = LabelFrame(LF_image_left,text = "  In",labelanchor = "w",height=125,width=240)
LF_image_left_input.pack(fill = "both",expand = "yes")
F_image_left_input_buttons = Frame(LF_image_left_input,height= 62,width=120)
F_image_left_input_buttons.pack(fill = "both", expand = "yes")
img_previous = ImageTk.PhotoImage(Image.open(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\previous.JPG").resize((45,35), Image.ANTIALIAS))
global B_previous
B_previous = Button(F_image_left_input_buttons,width = 3,image = img_previous, command = update_phrase_previous)
B_previous.pack(fill = "x", expand = "yes",side = LEFT,ipady=4)
img_play = ImageTk.PhotoImage(Image.open(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\play.JPG").resize((45,35), Image.ANTIALIAS))
global B_play
B_play = Button(F_image_left_input_buttons,width = 3, image = img_play,command = play_audio)
B_play.pack(fill = "x", expand = "yes",side = LEFT,ipady=4)
img_next = ImageTk.PhotoImage(Image.open(r"C:\Users\Dairon\Documents\202020\python\deutsch_app\next.JPG").resize((45,35), Image.ANTIALIAS))
global B_next
B_next = Button(F_image_left_input_buttons,width = 3,image = img_next,command = update_phrase_next)
B_next.pack(fill = "x", expand = "yes",side = LEFT,ipady=4)
e1_value = StringVar()
F_image_left_input_entry = Frame(LF_image_left_input,height= 62,width=130)
F_image_left_input_entry.pack(fill = "both", expand = "yes")
global Entry_image_left_input_entry
Entry_image_left_input_entry = Entry(F_image_left_input_entry,textvariable = e1_value,width = 50)
Entry_image_left_input_entry.pack(fill = "both",expand = "yes",ipady=5)
Entry_image_left_input_entry.bind('<Return>', enter_check_function)
Entry_image_left_input_entry.bind('<Right>', update_phrase_next_bind)
F_image_left_input_entry_options = Frame(F_image_left_input_entry,height= 62,width=130)
F_image_left_input_entry_options.pack(fill = "both", expand = "yes")
global B_check
B_check = Button(F_image_left_input_entry_options,text = "Check",command = check_function)
global B_help
B_help = Button(F_image_left_input_entry_options,text = "Help",command = help_function)
B_check.pack(fill = "both",expand = "yes",side=LEFT)
B_help.pack(fill = "both",expand = "yes",side = LEFT)

LF_image_left_output = LabelFrame(LF_image_left,text = "Out",labelanchor = "w",height=135,width=240)
LF_image_left_output.pack(fill = "both", expand = "yes")
global L_image_left_output_notification
L_image_left_output_notification = Label(LF_image_left_output,text = "",font = ("Courier",20),foreground = "green")
L_image_left_output_notification.pack(fill = "both", expand = "yes")
global L_image_left_output_message
L_image_left_output_message = Label(LF_image_left_output, text = "")
L_image_left_output_message.pack(fill = "both", expand = "yes")
global L_image_left_output_translation
L_image_left_output_translation = Label(LF_image_left_output,text = "Translation")
L_image_left_output_translation.pack(fill = "both", expand = "yes")

LF_image_right = Frame(LF_display_info,height=250, width=200)
LF_image_right.pack(fill = "both", expand = "yes",side = LEFT)
LF_image_up = LabelFrame(LF_image_right,text = "Elapsed time",labelanchor = "n",height=125, width=200)
LF_image_up.pack(fill = "both", expand = "yes")
global L_time
L_time = Label(LF_image_up, text = "alelluya")
L_time.pack(fill = "both",expand = "yes")
LF_image_down = LabelFrame(LF_image_right,text = "Statistics",labelanchor = "n",height=125, width=200)
LF_image_down.pack(fill = "both", expand = "yes")
LF_image_down_left = Frame(LF_image_down,width=200)
LF_image_down_left.pack(fill = "both",expand = "yes",side = LEFT)
LF_image_down_right = Frame(LF_image_down,width=200)
LF_image_down_right.pack(fill = "both",expand = "yes",side = LEFT)
#LF_image_down.columnconfigure(0, weight=2)
#LF_image_down.rowconfigure(0, weight=2)
L_image_down_hits = Label(LF_image_down_left,text="Hits:")
L_image_down_hits.pack(fill = "both",expand = "yes")
L_image_down_misses = Label(LF_image_down_left,text="Misses:")
L_image_down_misses.pack(fill = "both",expand = "yes")
L_image_down_accuracy = Label(LF_image_down_left, text = "Accuracy:")
L_image_down_accuracy.pack(fill = "both", expand = "yes")
L_image_down_phrases_to_study = Label(LF_image_down_left, text = "phrases to study:")
L_image_down_phrases_to_study.pack(fill = "both",expand = "yes")
global L_image_down_hits_update
L_image_down_hits_update = Label(LF_image_down_right,text="0",font=("Courier",25),foreground="green")
L_image_down_hits_update.pack(fill = "both",expand = "yes")
L_image_down_misses_update = Label(LF_image_down_right,text="0",font=("Courier",25),foreground="red")
L_image_down_misses_update.pack(fill = "both",expand = "yes")
global L_image_down_accuracy_update
L_image_down_accuracy_update = Label(LF_image_down_right,text = "0",font = ("Courier",25),foreground = "blue")
L_image_down_accuracy_update.pack(fill = "both", expand = "yes")
L_image_down_phrases_to_study_update = Label(LF_image_down_right,text = "0",font = ("Courier",25),foreground = "black")
L_image_down_phrases_to_study_update.pack(fill = "both",expand = "yes")

LF_options = LabelFrame(root,text = "Options",labelanchor = "n",height = 40,width = 450)
LF_options.pack(fill = "both", expand = "yes")
B_options_start = Button(LF_options,text = "Start",width = 5,state = "disabled")
B_options_start.pack(fill = "x",expand = "yes",side = LEFT)
B_options_stop = Button(LF_options, text = "Stop",width = 5,state = "disabled")
B_options_stop.pack(fill = "x", expand = "yes", side = LEFT)
B_options_restart = Button(LF_options,text = "Restart",width = 5,state = "disabled")
B_options_restart.pack(fill = "x",expand = "yes",side = LEFT)
B_options_option1 = Button(LF_options,text = "Load lesson",width = 5,command = select_file_lesson_func)
B_options_option1.pack(fill = "x",expand = "yes",side = LEFT)
B_options_option2 = Button(LF_options,text = "Create lesson",command = create_new_file,width = 5)
B_options_option2.pack(fill = "x",expand = "yes",side = LEFT)
B_options_append = Button(LF_options,text = "Append data",command = append_data_into_file,width = 5)
B_options_append.pack(fill = "x",expand = "yes",side = LEFT)

#########################################################################################################################
#################################################### END OF INTERFACE ###################################################
#########################################################################################################################

def show_time_thread():
	global L_time
	total_time = 0
	initial_time = time.perf_counter()
	while TRUE:
		current_time = time.perf_counter()-initial_time
		t = str(timedelta(seconds=current_time))
		L_time.configure(text = t,font=("Courier",12))
		L_time.update()

thread1 = threading.Thread(target=show_time_thread)
thread1.setDaemon(True)
thread1.start()
disable_buttons()
root.mainloop()