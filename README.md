# Flight Sim - Checklist Reader v 0.1

This is an attempt to create my very own checklist reader for MS Flightsimultor. 
It does however work with any kind of sim, or even for whatever purpos you want.
All it does, at its current state, is vocaly call out a checklist, or any txt file presented,
line by line on the press of a game controller button.
Alternatively the progression through the checklist can also be triggered by optional
voice recognition, on the predefined trigger word "check"

## Disclaimer:

  Please note, that I am not a programmer whatsoever. I just needed this tool to fly
  in VR and could not find anything that fit my needs. So I built something myself.
  Don't expect clean or beautiful code!

  **Also, the voice recognition is super early "alpha stage" 
  There are no guaranties that any of this works ;-)**

  Still, this was a lot work for me, so if like what I did please consider leaving a small donation
 
 [![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)]( https://www.paypal.com/donate/?hosted_button_id=MACUKZ7GTNKB4) 

## Installation:

  The Folder "Python code" contains the plain code version in case you want to run or
  pack this yourself or even want to make it better. If you just want to fly, you can just delete the folder.

  To use my pre packt app, there is no installation necessary. Just run the "checklist reader.exe" or if you like, run the python 
  code directly or pack it into a binary yourself. Note, that everything was built and tested 
  in Python 3.11
  For the casual user, just clicking on the "checklist reader.exe" file should work.

## Usage:

  Using the "open checklist" button, just load any .txt file into the application.
  The checklist needs to be in a simple line by line text form.

  The application permanently captures all game controller inputs and displays the
  captured button. By pressing the "set check button" button, you can set the last
  button captured to be your personal "checklist button"

  After clicking "start listening" the voice recognition is online.
  Voice recognition works using the pocketsphinx framework whish provides
  a threshold value for each keyword it is looking for. 
  This Value can be set by the "voice recognition tolerance" slider.
  I thought it might be easiest to expose this value to the user as recognition reliability
  is highly dependente on your mic setup as well as your voice.
  It is recommended to set the value as low as possible to avoid false positives.
  I am aware that the range of the slider is crazy powerful at the moment,
  this just to cover all kinds of voices and setups. Maybe in the future I can
  implement a cleaner way to do this.

## Future:
  Currently, I am working on an ingame-panel for MSFS to display the checklist or at least
  the next check to perform. When or if this is released I don't know.

  I would love to be able to pull checklists from the simulator with a "load checklist from sim"
  button. But at the moment I can not find a way to access this information. If anybody has an idea
  on how to get this, please contact me ;-)

## Notes:
  - Closing the app using the "quit" button will store your checkbutton and tolerance on disc

  - Deleting the "conf" file inside the "data" folder will reset all settings to stock

  - In the "Demo checklists" folder you can find a few examples of how checklists can look.
    those are just a few of the ones I use to fly with in VR

  - At the moment, having an **Internet connection is mandatory**, as text to speech is performed 
    by gTTS (Google text to speech) If an offline version is something of importance for users
    I could change that in the future



