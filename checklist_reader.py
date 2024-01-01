#!/usr/bin/env python3
from gtts import gTTS
import pygame, os, time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import thread
import speech_recognition as sr
import pickle
from pocketsphinx import LiveSpeech
from tkinter import HORIZONTAL
from PIL import Image, ImageTk
import sys

###### Initialize global Variables ####
# Path of where the main function is running. We need this to finde the rest of the data files
path = str(os.path.dirname(sys.modules['__main__'].__file__))

# Current active Checklist Line
lineindex = 0


# List containing the checklist
Lines = []

# Flag if the voicerecognition has detected a "check"
voicecheck = False

# List of ll Pygame game controllers
joysticks = []

# List of all Pygame game controller names
jname = []

# Check key on Keyboard ### INACTIVE
refkey = "c"

# List containing the last pressed button and the id of the device
lastbuttonpressed = [0, 0]

# ID ot the checkbutton and th4 device id
checkbutton = [0, 0]

# GUI Style
background = "#779198"
seconderycolor = "#919191"
font = ('Arial', 7)


# Flag if speech recognition is active
listen = False

# Set the tollerance for voice recognition
sensint = 20


# Load stored settings from "conf" file. So you dont have to set the checkbutton each time the app is started
def load():
    global refkey
    global checkbutton
    global sensint
    global toleranceslider
    global path

    filepath = str(path) + '\save.cfg'

    with open(filepath, 'rb') as file:
        # Deserialize and retrieve the variable from the file
        loaded_data = pickle.load(file)
    # Overwrite the global variables with the values from the "conf" file
    refkey = loaded_data[0]
    checkbutton = loaded_data[1]
    print("now")
    print(checkbutton)
    sensint = int(loaded_data[2])

    # initialize the checkbuttonlable, now that the checkbutton might have changed
    checkbuttondisplay()

    # set the tollerance slider to the value read from file
    toleranceslider.set(sensint)
    print("settings restored")



# If the app is closed using the quit button, a few key variables are stored on disk
def save():
    global refkey
    global checkbutton
    global sensitivity
    global path

    # Step 2: Saving Variables
    data = [refkey, checkbutton, str(sensint)]

    filepath = str(path) + '\save.cfg'

    # Open the file in binary mode
    with open(filepath, 'wb') as file:
        # Serialize and write the variable to the file
        pickle.dump(data, file)

    print("Settings saved")


# Open a dialoge to load a txt file
def getchecklist():
    global Lines
    global filename
    global lineindex
    # open dialoge to get filepath
    filename = askopenfilename()
    # open the file in read only mode
    file = open(filename, "r")
    # load the lines from text into a list
    Lines = file.readlines()

    # The for loop populates the listbox with all the list/ checklist entries
    index = 0
    for i in Lines:
        checklistbox.insert(index, i)
        index += 1

    # set the variable lineindex to 0 so the first entry is active first
    lineindex = 0
    print("checklist loadet")


# text to speech conversion and playback
def text_to_speech(text):
    global lineindex
    global filename
    global path

    # define a mp3 file for speech to be stored in
    speech_file = str(path) + "\speech.mp3"

    # pygame mixer loads an empty mp3 file in order to unload the speech file from the previous round.
    # without this step the mixer keeps the file open and prohibits the file from being overwritten.
    try:
        pygame.mixer.music.load(str(path) + "\empty.mp3")
    except:
        pass

    # converting the text passed to the function using "google text to speech"
    speech = gTTS(text, lang='en', tld='co.uk')

    # the speech file is written / overwritten with the converted text that was passed to the function
    try:
        speech.save(speech_file)
    except:
        print("Error")

    # Load the speechfile into pygame mixer and then play it
    pygame.mixer.music.load(speech_file)
    pygame.mixer.music.play()

    # Advance Checklist line by one
    checklistbox.selection_clear(lineindex - 1)
    lineindex += 1
    checklistbox.selection_set(lineindex - 1)



# Function that runs when ever a check is received
def check():
    global lineindex

    # Check on wish line in the checklistbox the curser currently stands. If the curser was moved by the user now the
    # lineindex pointer also points to selected line.
    for i in checklistbox.curselection():
        lineindex = i + 1

    if Lines != []:

        if lineindex <= len(Lines) - 1:
            print("Check")
            text_to_speech(Lines[lineindex])
            time.sleep(0.1)
        else:
            text_to_speech("All checklists complete!")
    else:
        text_to_speech("No checklist loaded!")


 # Resets the main Checklist. All configurations, like the checkbutton etc. stay. In order to reset everything. the conf file needs to be deleted
def reset():
    global lineindex
    global Lines
    lineindex = 0
    Lines = []
    startlistbutton()
    stopspeech()
    checklistbox.delete(0, "end")


# Setup the pygame controllers
def controllersetup():
    global joysticks
    for i in range(pygame.joystick.get_count()):
        # Append all found joysticks to the joysticks list
        joysticks.append(pygame.joystick.Joystick(i))

        # Append all the names  of the joysticks to list jname
        jname.append(joysticks[i].get_name())


# Initializing a label on call, to display the last captured joystick button
def buttondisplay(button, joy):
    # deleting the old label if one exists. Its set in "try" statement so that there is no error when this runs
    # for the first time and there is no label

    try:
        global lastbuttonlable
        lastbuttonlable.after(1, lastbuttonlable.destroy())
    except:
        pass

    # initializing the new button
    lastbuttonlable = tk.Label(root, text="Button: " + str(button), font=font, bg=seconderycolor)
    lastbuttonlable.place(relx=0.988, rely=0.195, anchor='e', width=93, height=20)


# Taking the last pressed joystick button and set them as Checkbutton
def buttonselect():
    global checkbutton
    global lastbuttonpressed

    # Just sets the last pressed button as the checkbutton. The next function is called, so that the label gets refreshed
    checkbutton = lastbuttonpressed
    checkbuttondisplay()


# Creating two labels. One, that tells the button-number of the set "checkbutton". And one with the name of the controller
def checkbuttondisplay():
    global checkbutton

    # Same as before. We try to destroy the lable, and afterwards we create a new one
    try:
        global checkbuttonlable
        global checkbuttonlable2
        checkbuttonlable.after(1, checkbuttonlable.destroy())
        checkbuttonlable2.after(1, checkbuttonlable2.destroy())
    except:
        pass

    # initializing a lable, telling the user the set checkbutton. The first
    checkbuttonlable = tk.Label(root, text="Check Button: " + str(checkbutton[0]), font=font,
                                bg=seconderycolor)
    checkbuttonlable.place(relx=0.988, rely=0.298, anchor='e', width=93, height=20)


    # initializing a lable telling the name of the joystick that holds the checkbutton
    checkbuttonlable2 = tk.Label(root, text=str(jname[checkbutton[1]]), font=font, bg=seconderycolor)
    checkbuttonlable2.place(relx=0.988, rely=0.33, anchor='e', width=93, height=20)


### Funkctions for Speech recognition ####

# Delete the existing button and initializes the Start listen button
def startlistbutton():
    try:
        global startlintenbutton
        startlintenbutton.after(1, startlintenbutton.destroy())
    except:
        pass
    startlintenbutton = tk.Button(root, text="Start listening!", command=startspeech, width=12, height=3)
    startlintenbutton.place(relx=0.99, rely=0.63, anchor='e')


# Delete the existing button and initializes the Stop listen button
def stoplistbutton():
    try:
        global startlintenbutton
        startlintenbutton.after(1, startlintenbutton.destroy())
    except:
        pass
    startlintenbutton = tk.Button(root, text="Stop listening!", command=stopspeech, width=12, height=3)
    startlintenbutton.place(relx=0.99, rely=0.63, anchor='e')


# This function is called to start the voice recognition. listen is set to ture and a new thread is started that runs the
# voice recognition stuff
def startspeech():
    global listen
    listen = True

    # Starting the new thread
    thread.Thread(target=speechrec).start()

    # Changing the button for one, that says "stop listening"
    stoplistbutton()


def stopspeech():
    global listen

    # Changing this flag stops the voice recognition thread
    listen = False

    # Changing the button for one, that says "start listening"
    startlistbutton()


# This is the actual voice recognition function. This will allways run in a separate thread as it is blocking
def speechrec():
    global listen
    global voicecheck
    global sensint

    # setting up voice recognition
    r = sr.Recognizer()

    # sensint contains the value from the tolerance slider. Here it is used as an exponent in a float
    # Pocketshpinx takes a float as threshold value for keyword recognition
    sensitivity = float(1 * pow(10, int(sensint)))
    print("Starting speech recognition with tolerance: " + str(sensitivity))

    # Starting the (blocking) speechrecognition loop.
    while listen == True:
        # before processing the results, we check if the listen flag is still True. If not, we want the function
        # to run to the end, so that the thread can end and voice recognition stop
        if listen == False:
            break
        # Looking for keyword "check" with set sensitivity
        speech = LiveSpeech(keyphrase='check', kws_threshold=sensitivity)

        # the result is handed as list.
        for phrase in speech:
            # This is only going to give you an entry in the list if the word "check" was found. So we set the global
            # variable voicecheck to True. This communicates the check event out of the seperate thread and via the
            # globals to the mainthread
            voicecheck = True

            # Check for listen again as the thread was not closing down correctly all the time
            if listen == False:
                break

            print("Voce activated Check: " + str(phrase.segments(detailed=True)))


# Settolerance is called when the tollerance slider is moved. Its ment to change the sensitivity val (sensiint) and stop
# and restart voicerecognition with the new value
def settollerance(val):
    global sensint
    sensint = val

    # Stop and restart speech rec. if it was running
    if listen == True:
        stopspeech()
        startspeech()



# Kill the app
def exitapp():
    global running
    global listen
    save()
    root.destroy()
    listen = False
    running = False
    quit()



## Pygame initialisieren und Controller abfragen
pygame.init()
controllersetup()

###### GUI #############################################################################################################

# Setup of the main application window
root = tk.Tk()
root.title('Checklist reader - v0.1')
root.resizable(False, False)
root.geometry('450x600+100+100')
root["bg"] = background



### Head Label #####################
# Load the image for the menu bar logo from disk.
icon = tk.PhotoImage(file= str(path) + "\logo.png")
# Set it as the window icon.
root.iconphoto(True, icon)


# Create a photoimage object of the image for the application header
image1 = Image.open( str(path) + "\hd.png")
head = ImageTk.PhotoImage(image1)
Label = tk.Label(image=head, bg=background)
Label.image = head
# Position image
Label.pack()




### Main Checklist ###
checklistbox = tk.Listbox(root, selectmode='browse', width=55, height=30)
checklistbox.place(relx=0.02, rely=0.18)



### Set checkbutton button ###
buttonbutton = tk.Button(root, text="Set button", command=buttonselect, width=12, height=2)
buttonbutton.place(relx=0.99, rely=0.245, anchor='e')

### Speech rec tolerance label ###
tolerancelable = tk.Label(root, text="""Speech recognition 
tolerance""", font=font, bg=seconderycolor)
tolerancelable.place(relx=0.988, rely=0.385, anchor='e', width=93, height=30)

### Speech rec tolerance slider ###
toleranceslider = tk.Scale(root, from_=40, to=-40, width=15, length=88, orient=HORIZONTAL, bg=seconderycolor,
                           command=settollerance, showvalue=False)
# Set its value
toleranceslider.set(sensint)
toleranceslider.place(relx=0.99, rely=0.43, anchor='e')


### Open Checklist button ###
openbutton = tk.Button(root, text="Open checklist", command=getchecklist, width=12, height=3)
openbutton.place(relx=0.99, rely=0.53, anchor='e')

### Listen button ###
# The start listen button is set by a function, because it is exchanged by a stop listen button when pressed
# and might need to be reinitialized if pressed again
startlistbutton()

### Check button ###
guicheckbutton = tk.Button(root, text="CHECK", command=check, width=12, height=3)
guicheckbutton.place(relx=0.99, rely=0.73, anchor='e')

### Reset button ###
resetbutton = tk.Button(root, text="Reset", command=reset, width=12, height=3)
resetbutton.place(relx=0.99, rely=0.83, anchor='e')

### Quit button ###
exit_button = tk.Button(root, text="Quit", command=exitapp, width=12, height=3)
exit_button.place(relx=0.99, rely=0.94, anchor='e')











# main function including game loop etc
def main():
    global root
    global voicecheck

    ## Load Checkbuttonsettings from last session
    try:
        load()
    except:
        print("Settings restore failed")


    # Starting the main pygame loop. This one is blocking!
    running = True
    print("running")
    while running:

        try:
            # I use root.update() in order to update the GUI in a pygame loop. Otherwise Tkinter main loop would be blocking in and
            # of itself. I might change this to have the tk main loop running in a separate thread in the future
            rootstate = root.state()
            root.update()

            # I let the game loop sleep for 0.02 seconds because otherwise pygame eats up a lot of CPU overhead. Having it
            # run, slowed down like this, is still responsive enough. This app is supposed to run alongside a flight sim
            # and without this, it generates 10% CPU usage on my system
            time.sleep(0.02)

            # Check if the voice recognition function found a check event
            if voicecheck == True:
                # If that is the case run check()
                check()
                # And set voicecheck back to False again after a short while.
                # The system waits a second to avoid double positives.
                time.sleep(1)
                voicecheck = False

            # Get the pygame evnet
            for event in pygame.event.get():


                # As a button press event happend?
                if event.type == pygame.JOYBUTTONDOWN:
                    # Call buttondisplay function to get lable, telling the user the last pressed button an any controller
                    buttondisplay(event.button, event.joy)

                    # Set the lastbuttonpressed variable. This is used to set the checkbutton
                    lastbuttonpressed = [event.button, event.joy]

                    # Is the pressed button = the defindes checkbutton. Then call the check function
                    if event.button == checkbutton[0] and event.joy == checkbutton[1]:
                        check()




        # If any ot this produces an error set running and listening to False, and the app just closes
        except:
            running = False
            listen = False

    listen = False


if __name__ == "__main__":
    main()