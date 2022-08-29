#Before you can run this project you need the following: 
  1- python 3.8
  2- anaconda
# Then install rasa by following the steps in the video: 
 ## IMPORTANT NOTE: (DON'T use "rasa init" at the end, it will overwrite the project!!!)
 ## link to the video: https://www.youtube.com/watch?v=GlR60CvTh8A&t=2s
# Then start Anaconda Prompt
 ## cd to the folder containing this project
 ## run this command: rasa train
 ## Then run these two commands SIMULTANEOUSLY!! on two different shells WITH THE SAME ANACONDA ENVIROUMENT: 
  ### On the first shell run this:  rasa run -m models --enable-api --cors "*" 
  ### On the second shell run this: rasa run actions
# Now navigate to index.html file in this project folder and open it. then you will have the project running. 
