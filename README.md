# Drumzy
6.835 Final Project

#### Collaborators: Sanchit Bhattacharjee and Cesar Guerrero

## Instructions:
### Wrapping the LeapSDK for Python 3.6
We tested our project using Python 3.6, and know it will not work with Python 2 or Python 3.7 due to package issues. We cannot speak to other versions but recommend Python 3.6 usage. However, as the LeapSDK is built for Python 2, we had to wrap it for our respective OS’s to get the application to work. Instructions for how to do this are below:

1. Download and install the LeapMotion V2 Software from https://www.leapmotion.com/setup/desktop/.
2. Download the LeapSDK, specifically the version found on the class Stellar website. From here we have to wrap this SDK for Python3.6, so instructions diverge by OS.

#### For OSX:
1. Because this does not work straight out of the box, you must do some modification. This can be done by following the instructions in the following link: 
https://github.com/Carotti/LeapPythonMac

Thanks must be given to Thomas Carotti for posting this on Piazza, and making the install process much easier.

#### For Windows:

So we are roughly going to follow the instructions at https://support.leapmotion.com/hc/en-us/articles/223784048-Generating-a-Python-3-3-0-Wrapper-with-SWIG-2-0-9, but they have some ambiguities that I will clarify below. Also make sure to heed the note unintuitively at the bottom of those instructions for using the x64 configuration if your system calls for it.

Hopefully this works, but these steps were ambiguous enough that it took me 2 weeks to get fully right. I hope I cleared any ambiguities with my writeup above, but am unsure how this could cause other issues on other systems. Also if you are using Windows 10 and these fail the first time, try the fix outlined here: https://forums.leapmotion.com/t/resolved-windows-10-fall-creators-update-bugfix/6585

1. Download SWIG for Windows at http://www.swig.org/Doc1.3/Windows.html and add it to the PATH so you can call SWIG from the command line
2. Download Visual Studio with the basic C++ compiler (Step 1 in linked guide)
3. Create an empty project called ‘LeapPython’ in VisualStudio. (Step 2 in linked guide)
4. From the LeapSDK folder downloaded from Stellar, copy the files mentioned in Step 2 of the linked guide to the subfolder LeapPython/LeapPython created by the empty project.
5. Complete Steps 3-6 from the guide above, replacing Python33 with your path to your local Python36 installation as appropriate.
6. Complete Steps 7 and 8 in the guide above.


Now, using both methods, you should have a folder that successfully built a ton of files. Make sure this folder is named LeapPython and has its own subfolder named LeapPython as well. Copy this folder into the root of the drumzy directory. Now it should be smoother sailing to get setup. If you run the code and get a ‘delete_SwigPyIterator’ error, the steps above were not performed properly

### Python Packages
Once you are done wrapping the SDK, congratulations, you are done with the hardest part of getting this working! Beyond this, we have some Python Packages we need to install, documented below:

First install Pygame 1.9.5. This can be easily installed using pip
 > pip install pygame 
 
Further Documentation on how to install this is at https://www.pygame.org/wiki/GettingStarted

After this, you must install SpeechRecognition 3.8.1. This can be done by following the instructions in the following link:
https://pypi.org/project/SpeechRecognition/

In order to be able to use microphone inputs with this program, you must install PyAudio V0.2.11. Instructions for doing so can be found here:
https://people.csail.mit.edu/hubert/pyaudio/

Lastly, you must install pydub v0.23.1. This can be done by following the instructions here:
https://github.com/jiaaro/pydub#installation

## Running the Application:

Once everything is installed, you’re ready to drum! To start the program, open a command line or terminal window, and navigate to the drumzy folder. Then run:
	> python drumzy.py NumDrums
NumDrums specifies how many drums are displayed and can be used while running the program. This number can be 1, 2, 4, 6, or 8.

Note: Don’t worry if the screen is black to begin with! The drum part of the visuals initialize on the first time that the LeapMotion detects your hands.

## File descriptions:

### Key Files:
- drumzy.py - The main file. It initializes the GUI, creates Drum objects, lists the available sound files, and initializes the LeapAPI and Speech listeners, which are in charge of getting and processing data from the Leap Motion and Microphone. This is also where voice commands are registered and call their respective functions.

- leap_parser.py - Defines SampleListener, which extends Leap.Listener. This class is what takes in Leap data, registers and plays drum hits, and updates the frames of the GUI, including highlighting triggered drums, cursor movement, and the metronome. Additionally, it defines functions that are triggered by voice commands.

- wav_processor.py - This is the AudioProcessor Component. It first defines Note objects, which store which drum is played and at what time in the recording. Then, it uses these Note objects to define a NoteList object, which is the internal representation of a final recorded measure. This object stores a list of notes and handles turning this into a WAV object, writing it to a file, and most importantly beat synchronization when merging two NoteLists.

### Other Files:

- drum.py - contains the Drum class implementation. This class is used to represent a drum. Each drum keeps track of its area in the GUI, as well as it’s area in the virtual Leap Motion plane. It also contains its corresponding sound, and whether or not it is triggered. There are object methods to trigger and untrigger the drum, as well as some observers to tell whether or not a point is in its triggering area, as well as its note value.

- load_sound.py - defines a function for loading sounds using the pygame API

- textbox.py - A file to render multiline textboxes in the GUI (for the application instructions) adapted from https://www.pygame.org/pcr/text_rect/index.php

- images/ - a folder containing images used to represent different kinds of drums

- sound_clips/ - a folder containing sound files, which are played when their corresponding drum is played. There are multiple different sound files for each drum, which can be switched out in the code.
