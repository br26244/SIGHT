import cv2
import numpy as np
import pandas as pd
from colorblind import colorblind
import sys


print("---------------------------------SIGHT-------------------------------", '\n')
print("Welcome to SIGHT!")
print('\n','\n')


userChoice = 0
pictureName = "none"
typeProgram = 'z'

pictureName = input("Please input the image file name (Please exclude the .jpg extention):")

print('\n')
print('\n')

valueContinue = True

while valueContinue == True:


    while typeProgram not in ('a','b'):
        print("a. Color Detector",'\n')
        print("b. Daltonization (colorblind friendly filer)",'\n')
        print("c. Exit", '\n')
        typeProgram = input("Which are you interested in:")
        
        
    if typeProgram == 'b' :
        blindContinue = True
        while blindContinue == True:
            while userChoice not in (1, 2, 3, 4):
                print("1. Deuteranopia (red-green weakness, particularly green)", '\n')
                print("2. Protanopia (red-green weakness, particularly red)",'\n')
                print("3. Tritanopia (blue weakness)", '\n')
                print("4. Go Back", '\n')
                userChoice = int(input("Please choose from the following:"))
                print('\n')
                print('\n')
    
            if userChoice == 1 :
                colorFILE = pictureName + '.jpg'
                blindIMG = cv2.imread(colorFILE)
                simulated_img = colorblind.simulate_colorblindness(blindIMG, colorblind_type='deuteranopia')
                daltonized_img = colorblind.cbfs_correct(simulated_img, closeness=70)
                cv2.imshow('Deuteranopia', daltonized_img)
                cv2.waitKey()

            if userChoice == 2 :
                colorFILE = pictureName + '.jpg'
                blindIMG = cv2.imread(colorFILE)
                simulated_img = colorblind.simulate_colorblindness(blindIMG, colorblind_type='protanopia')
                daltonized_img = colorblind.daltonize_correct(simulated_img, colorblind_type='protanopia')
                cv2.imshow('protanopia', daltonized_img)
                cv2.waitKey()

            if userChoice == 3 :
                colorFILE = pictureName + '.jpg'
                blindIMG = cv2.imread(colorFILE)
                simulated_img = colorblind.simulate_colorblindness(blindIMG, colorblind_type='tritanopia')
                daltonized_img = colorblind.daltonize_correct(simulated_img, colorblind_type='tritanopia')
                cv2.imshow('tritanopia', daltonized_img)
                cv2.waitKey()

            if userChoice == 4:
                blindContinue = False
                
            
    if typeProgram == 'a' :
        File = pictureName + '.jpg'
        img = cv2.imread(File)
        index = ["color","color_name","hex","R","G","B"]
        csv = pd.read_csv('colors.csv',names = index)

        clicked = False

        def draw_function(event,x,y,flags,param):
            global clicked,r,g,b
            if event == cv2.EVENT_LBUTTONDBLCLK:
                clicked = True
                b,g,r = img[y,x]
                b,g,r = int(b),int(g), int(r)

        def getColor(R,G,B):
            min_distance = 1000
            for i in range (len(csv)):
                d = abs(R-int(csv.loc[i,"R"])) + abs(G-int(csv.loc[i,"G"])) + abs(B-int(csv.loc[i,"B"]))
                if(d<min_distance):
                    min_distance = d
                    cname = csv.loc[i,"color_name"]
            return cname
        cv2.namedWindow('Color detection')
        cv2.setMouseCallback('Color detection', draw_function)

        while True:
            cv2.imshow("Color detection", img)
            if clicked:
                cv2.rectangle(img,(10,20),(600,60),(b,g,r),-1)
                text = getColor(r,g,b) + '(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
                cv2.putText(img,text,(50,50), 3, 0.8,(255,255,255),2)
                if(r+g+b >= 500):
                    cv2.putText(img, text,(50,50),3,0.8,(0,0,0),2)
                clicked = False
            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()
        
    if typeProgram == 'c' :
        break



sys.exit()

