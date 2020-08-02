# Air Guitar (updated spring 2018)

## I wrote the code for the HardwareCode/GuitarUI.py file, found in the Hardware Code folder. I collaborated on some of the other files (such as PISTON.cpp in the GUITARAMIB1 folder, and GUITAR.comm), but files other than HardwareCode/GuitarUI.py were primarily written by others on my team in the Dos Pueblos Engineering Academy.

General description of the Air Guitar: Pneumatic cylinders act as "fingers" and are attached to a moveable carriage controlled by a stepper motor to have the potential to reach many frets. The guitar fingers its own chords in time to a song of choice that plays in the background, and the user strums the guitar him/herself.

The UI (written in Python and using Python's Kivy library) displays the song's rhythmic beats scrolling as rectangles across the screen. When the beats hit a triangle at the botton center of the screen, the triangle changes color. This is when the user knows to strum the guitar. At the top left of the UI is a dynamic graphic of a guitar tab showing all six strings. If a string is being pressed down by a piston in the current chord, it will light up green as well as display the fret number above it. This will change for each chord. Since there are multiple songs to choose from, the UI includes a song selection scene that will take you to a separate scene based on which song you pick.



