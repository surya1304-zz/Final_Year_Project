import os
import face_recognition
import cv2
import numpy as np
import argparse
import pickle
import smtplib
import geocoder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import math

def getLocation():
    driver = webdriver.Safari()
    timeout = 3
    l = driver.session_id
    print(l)
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(10)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    driver.quit()
    print(latitude, longitude)
    return (float(latitude), float(longitude))

ap = argparse.ArgumentParser()
ap.add_argument("--mode", help=" train / display")
a = ap.parse_args()
mode = a.mode

if mode == 'train':

    k = '/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project/Training'
    original = '/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project'

    list = os.listdir(k)
    print(list)
    list_1 = os.listdir(original)
    if list_1.count("face_encodings.pckl") != 0 or list_1.count("face_names.pckl") != 0:
        os.remove('/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project/face_encodings.pckl')
        os.remove('/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project/face_names.pckl')
    known_face_encodings = []
    known_face_names = []

    os.chdir('/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project/Training')

    for i in list:
        j = i[:-4]
        k = face_recognition.load_image_file(i)
        face_encoding_name = "face_encoding_"+j
        globals()[face_encoding_name] = face_recognition.face_encodings(k, num_jitters=100)[0]
        face_encoding_name1 = globals()[face_encoding_name]
        known_face_encodings.append(face_encoding_name1)
        known_face_names.append(j.upper())
        print(known_face_encodings)
        print(known_face_names)

    os.chdir('/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project')

    f = open('face_encodings.pckl', 'wb')
    pickle.dump(known_face_encodings, f)
    f.close()

    f = open('face_names.pckl', 'wb')
    pickle.dump(known_face_names, f)
    f.close()

    print("Success")

if mode == 'display':

    g = geocoder.ip('me')

    location1 = " \nCity: " + str(g.city) + " \nState: " + str(g.state) + " \nCountry: " + str(g.country) + " \nPincode: " + str(g.postal)

    (lat, long) = getLocation()
    location = "Latitude: " + str(lat) + " Longitude: " + str(long) + location1

    lat_in_deg = math.floor(lat)
    lat_in_min1 = (lat - lat_in_deg)*60
    lat_in_min = math.floor(lat_in_min1)
    lat_in_sec = round((lat_in_min1 - lat_in_min)*60, 2)

    long_in_deg = math.floor(long)
    long_in_min1 = (long - long_in_deg)*60
    long_in_min = math.floor(long_in_min1)
    long_in_sec = round((long_in_min1 - long_in_min)*60, 2)

    sender="suryasai678@gmail.com"
    receiver="sindukuri@student.nitw.ac.in"
    cc = [ "suryasai6789@gmail.com" ]
    kcc = ""

    for k in cc:
        kcc = kcc + k

    receivers = cc + [receiver]
    password="Suryasai@67890"
    smtpserver=smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(sender,password)

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    os.chdir('/Users/indukurisuryasaiharischyandraprasad/Desktop/DATASET/Final_Year_Project/')
    f = open('face_encodings.pckl', 'rb')
    known_face_encodings = pickle.load(f)
    f.close()

    f = open('face_names.pckl', 'rb')
    known_face_names = pickle.load(f)
    f.close()

    names = []

    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame,
            model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if name != 'Unknown' and names.count(name) == 0:

                    if(abs(lat) == lat and abs(long) == long):
                        link = "https://www.google.com/maps/place/"+str(lat_in_deg)+"%C2%B0"+str(lat_in_min)+"'"+str(lat_in_sec)+"%22N+"+str(long_in_deg)+"%C2%B0"+str(long_in_min)+"'"+str(long_in_sec)+"%22E"

                    elif(abs(lat) != lat and abs(long) == long):
                        link = "https://www.google.com/maps/place/"+str(lat_in_deg)+"%C2%B0"+str(lat_in_min)+"'"+str(lat_in_sec)+"%22S+"+str(long_in_deg)+"%C2%B0"+str(long_in_min)+"'"+str(long_in_sec)+"%22E"

                    elif(abs(lat) == lat and abs(long) != long):
                        link = "https://www.google.com/maps/place/"+str(lat_in_deg)+"%C2%B0"+str(lat_in_min)+"'"+str(lat_in_sec)+"%22N+"+str(long_in_deg)+"%C2%B0"+str(long_in_min)+"'"+str(long_in_sec)+"%22W"

                    elif(abs(lat) != lat and abs(long) != long):
                        link = "https://www.google.com/maps/place/"+str(lat_in_deg)+"%C2%B0"+str(lat_in_min)+"'"+str(lat_in_sec)+"%22S+"+str(long_in_deg)+"%C2%B0"+str(long_in_min)+"'"+str(long_in_sec)+"%22W"

                    message = "Name of the criminal is " + name + " and His/Her Location is " + location + "\nThe Link to the location is " + link
                    print(message)

                    file_name = name+"_loc:"+str(lat)+"_"+str(long)+".txt"
                    f = open(file_name,"w+")
                    f.write(message)
                    f.close()

                    msg = MIMEMultipart()
                    msg['From'] = sender
                    msg['To'] = receiver
                    msg['Cc'] = kcc
                    msg['Subject'] = "Criminal Location Alert"
                    body = message
                    msg.attach(MIMEText(body, 'plain'))
                    filename = file_name
                    attachment = open(file_name, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    msg.attach(p)
                    text = msg.as_string()
                    smtpserver.sendmail(sender, receivers, text)
                    os.remove(file_name)

                face_names.append(name)
                names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    smtpserver.quit()
