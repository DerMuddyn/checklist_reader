Flight Sim - Checklist Reader v 0.1 - by Martin Ritter

This is an attempt to create my very own checklist reader for MS Flightsimultor. 
It does however work with any kind of sim, or even for whatever purpous you want.
All it does, at its current state, is vocaly call out a checklist, or any txt file presented,
line by line on the press of a game controller button.
Alternatively the progression throug the checklist can also be triggered by optional
voice recognition, on the predefined trigger word "check"

Disclaimer:
  Please note, that I am not a programmer what so ever. I just needet this tool to fly
  in VR and could not find anything that fit my needs. So I built something myself.
  Dont expect clean or beautiful code!
  Also the voice recognition is super early "alpha stage" 
  There are no guaranties that any of this works ;-)

  Still, this was a lot work for me, so if like what I did please consider leaving a small donation
  https://www.paypal.com/donate/?hosted_button_id=MACUKZ7GTNKB4

Installation:
  The Folder "Python code" contains the plain code version in case you want to run or
  pack this yourself or even want to make it better. If you just want to fly, you can just delete the folder.

  To use my pre packt app, there is no installation necessary. Just run the "checklist reader.exe" or if you like, run the python 
  code directly or pack it into a binary yourself. Note, that everything was built and tested 
  in Python 3.11
  For the casual user, just clicking on the "checklist reader.exe" file should work.

Usage:
  Using the "open checklist" button, just load any .txt file into the application.
  The checklist needs to be in a simple line by line text form.

  The application permanently captures all gamecontroller inputs and displays the
  captured button. By pressing the "set check button" button, you can set the last
  button captured to be your personal "checklist button"

  After clicking "start listening" the voice recognition is online.
  Voice recognition works using the pocketsphinx framework whish provides
  a threashold value for each keyword it is looking for. 
  This Value can be set by the "voice recognition tolerance" slider.
  I thought it might be easiest to expose this value to the user as recognition reliabilty
  is highy dependant on your mic setup as well as your voice.
  It is recomendet to set the value as low as possible to avoide false positives.
  I am aware that the range of the slider is crazy powerfull at the moment,
  this just to cover all kinds of voices and setups. Maybe in the future I can
  implement a cleaner way to do this.

Notes:
  - Closing the app using the "quit" button will store you checkbutton an tolerance on disc

  - Deleting the "conf" file inside the "data" folder will reset all settings to stock

  - In the "Demo checklists" folder you can find a few examples of how checklists can look.
    those are just a few of the ones I use to fly with in VR


