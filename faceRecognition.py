import os
import cv2
import sys

faceDetector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
camera=cv2.VideoCapture(0)

#set a dictionary to store id(key) :name (value) of a face
Id2Name={}

#font = cv2.FONT_HERSHEY_SIMPLEX
font = cv2.FONT_HERSHEY_DUPLEX
print("begin...\n")
while True:

    #get picture from internal camera
    success,img=camera.read()
    if success == True:
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        print("FAILED TO GET PICTURE\n")
        break
    print("get picture\n")
    #get all faces which were detected and then do recognize for each face
    faces = faceDetector.detectMultiScale(grayImg, 1.3, 5)
    print(len(faces))

    name=""
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(155,175,131))
        cv2.rectangle(img,(x,y-30),(x+w,y),(155,175,131))

        #get all patterns in the model folder and then use each pattern to recognize all faces
        patterns = [os.path.join('./staticResource/model', f) for f in os.listdir('./staticResource/model')]
        if len(patterns) != 0:
            #set the flag to judge if face was detected in the picture
            #set the confidences to collect faces which have the similar confidence
            #and the select the smallest as the final result of prediction
            flag=False
            confidences = []

            for pattern in patterns:
                name=pattern.split('.')[2]
                id=pattern.split('.')[3]
                Id2Name[id]=name

                #the function to create a recognization and recognize face by setted model
                #and return the face id and confidence
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(pattern)
                idnum, confidence = recognizer.predict(grayImg[y:y + h, x:x + w])

                # if the confidence less than 70 ,
                # It is considered was the persons face who we want
                print(confidence)
                if confidence<70:
                    confidences.append([idnum,confidence])
                    flag=True

            if flag == True:
                confidences.sort(key=lambda x:x[1])
                name=Id2Name[str(confidences[0][0])]
                print(name)
                cv2.putText(img, name, (x + 5, y - 5), font,0.55, (154, 157,252 ),1)
                cv2.imwrite("./staticResource/data/"+name+".jpg",img)
            else:
                cv2.putText(img, "unknow", (x + 5, y - 5), font, 0.55, (101, 67, 254), 1)
                name=""
        else:
            print("NO MODEL AVAILABLE")

    #cv2.imshow("me",img)
    cv2.imwrite("./staticResource/data/current.jpg",img)
camera.release()
#cv2.destroyAllWindows()
print(Id2Name)
