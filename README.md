# Text-Adventure

A Short Text Adventure For CS 1400

Although I only really needed to make this a regular text adventure, I decided to integrate a personal project I had been working on at the time and add a few short "gameplay" segments. These take you into a console-based 2D "game engine" rendered using the print function (making it very slow). 

A known issue is with loading levels. The game state is stored in a list of lists, each describing a different game object. I needed a way to conveniently store a list in a file as a literal value, rather than as a string. This is because the output of "writing" a list to a file is not directly compatible with the list() function, and some serious, tedious string splitting was necessary to get it back as a usable value. The only way I could think to get around it was to store it as a python variable, and import it when needed. I have since learned more about JSON and how to integrate it with Python, so I may go back at a later date and flesh out that feature.

And yes, I know the code isn't very good. The good news is that, each time I finish a project, I look back and realize how much better I could have done things and use that knowledge going forward. My code since finishing this project has been significantly better, faster, and more optimized.
