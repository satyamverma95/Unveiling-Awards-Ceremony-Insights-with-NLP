# NLP_Project_2

_Satyam Verma, Syed Nizamuddin, Arpit Tiwari, Anishka Sharma_

### To Set Up:
In the command line: pip3 install -r requirements.txt on Mac or device running Python 2.7 by default or pip install -r requirements.txt on device running Python 3 by default Instructions below have paths specifically for Macs (change command and path to python3.6 and /Python 3.6/ instead of python3 and /Python 3/ if your computer requires that to run python 3.

sudo python3 -m nltk.downloader -d /usr/local/share/nltk_data all

If this gives you an SSL error, run

bash /Applications/Python\ 3/Install\ Certificates.command

For Non-Mac running Python 3 by default Perform inside a python3 shell:

$: Python3 # open a python3 shell

\>> nltk.download() # this will open open interactive installer

Select all-nltk and download

Flask
Installation:
$ pip install Flask

Pytorch
Installation:
1. pip –version
2. pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
3. pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
4. pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
5. pip3 show torch

Pytorch - Flask dependecy - 
To render the program, we have made use of flask to host the webapp, while it is convenient to host ,there are some technical dependecy with pytorch that creates a glitch.
Path variables need to be set. Please follow below link to set path variables correct:

https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#enable-long-paths-in-windows-10-version-1607-and-later

### References
We looked for various material, resources, youtubve videos, documentation. We looked for help from mentioned resources - 

-1. https://www.youtube.com/watch?v=GHvj1ivQ7ms
-2. https://flask.palletsprojects.com/en/2.2.x/
-3. https://pytorch.org/docs/stable/index.html


### Running the code
We were asked to create an interactive cookbook which will parse recipe given to it. The main idea is that::
-1. the steps of a recipe will be broken out into specific entries.
-2. Users can read or listen to the contents of the current step; navigate between steps (go forward or backwards);
-3. ask questions about, e.g., the cooking action(s) specified in the step; the ingredients used; the utensil or tool used; other parameters of the action (usually, time or temperature).
Note - We have kept screenshots of the same in the snapshots folder.

The user gets a choice to select a cuisines and from it a recipe. Fetch , will return the recipe insteructions in which you can go forward or backward using the next and prev button respectively. If the user is confused about any step, he can stop and ask questions about the recipe. There is a search box where user can write questions and get respective answers.

The same is available in speech mode also.


### Results

The whole project was divided mainly into two parts as directed by the problem statement - 

#### Part I
Parsing the sentences at each step/instruction of the cooking recipe for various elements in the instruction like ::
 -- cooking actions : boil, heat, fry, cook, bake etc
 -- utensils/tools : spoon, glass, bowl etc
 -- ingredients : lemon ginger, salt, sugar, spices etc
 -- time and temperature
#### Output 
User can ask questions like 'Hom much salt?', 'How many ginger lemons?' and the web app returns the user with an answer *in context of the question asked*.

#### Part II
Building a system that, in the very simplest form, allows you to navigate by command (“chatbot” style, or voice) between steps of the recipe such as - 
ability to query about the ingredients mentioned in a step, specifically, how much of the ingredient do you need
You should add in the ability to query about an action,
#### Output - 
Web app that provides with functions as - 
-- querying for actions, ingredients, steps(backward and forward).
-- speech to ask questions (if both of your hands are busy in dough ir maybe preparing the mix!! ;p) and answers that are spoken back at you.


### Note
In the zip, there is walkthrough video available which you can refer to as a ready reference. Use the video as an explainer for the readme.md included with the project.



