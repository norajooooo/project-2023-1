import opencv
import numpy 

f=open("/Desktop/Project-2023-1/color_recognition/text/word.txt","r")

corpus=[]

for line in f:
 for word in line:
  corpus.append(word)

g=opencv.open("/Desktop/Project-2023-1/color_recognition/img/img.jpg").warpaffine()

