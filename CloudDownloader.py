#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:04:26 2022

@author: aru
"""

import socket
import base64
from time import sleep
import sys
indexFile = sys.argv[1] #Gets the Index Dile
authentication  = sys.argv[2] #Gets the Authentication

hostName = indexFile[:indexFile.find("/")].strip() #Slice the indexFile to obtain host name and address
address = indexFile[indexFile.find("/"):indexFile.find("txt") + 3].strip()
password = authentication
serverList = [] # doesnt only contain server urls conatin all the data from the indext file
text = ""

try:#If there is a unknown error, program doesn't crash and prints Unknown Error Occurred
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM) #creates the socket
    s.connect((socket.gethostbyname(hostName), 80))

    authin = base64.b64encode(password.encode()).decode() # server understands the password as Base64 so the password encoded
    request="GET " + address + " HTTP/1.1\r\nHost:" + hostName + "\r\n"+"Authorization: Basic "+authin+"\r\n\r\n" #connection request in http
    s.send(request.encode()) #Send host to connection request in http

    response = s.recv(4096) #receve responce and adjusting the buffer size
    s.close() #closing the tcp connection

    responseText = response.decode()  #decodes responce to string
    lookError = responseText[responseText.find("HTTP/1.1") + 8: responseText.find("Date")].strip() #looks for the server static code
    
    if (lookError != "200 OK"): # if error findins in while finding indext file prints "Error: the index file is not found"
        print("Error: the index file is not found")
        
    else: #if recived 200 ok message continues the system
        responseText = responseText[responseText.find("text/plain") + 14 : ] #gets the data of the  
        serverList = responseText.splitlines() # converts responseText text to list
        
        textName = serverList[0].strip()
        serverList.pop(0)


        totalBytle = int( serverList[0].strip()) #Finds total byte
        serverList.pop(0) #Deletes the total byte

        lastHightByte = 0 

        serverNumber = responseText.count("txt") - 1 # usinf count() the total number of the url's are found but the first url is the inital servers so I decrease the value by 1

        print("URL of the index file: " +hostName +  address) #prints the URL of the index file
        print("File size is " + str(totalBytle) + " Bytes") #prints the total byte
        print("Index file is downloaded")
        print("There are " + str(serverNumber) + " servers in the index") # prints the number of the server

        while (len(serverList) > 0):
            url = serverList[0].strip() # takes the first url
            print("Connected to " + url)

            hostName = url[:url.find("/")].strip() #gets the host name from the url
            serverList.pop(0) #Deletes url

            address =  url[url.find("/"):url.find("txt") + 3].strip() # gets the address from the url

            password = serverList[0].strip() #gets the password
            serverList.pop(0) #Deletes password

            byteRange = serverList[0].strip() #gets the byte range
            lowByte = int(byteRange[0:byteRange.find("-")]) -1 # gets the lower range of the index
            highByte = int(byteRange[byteRange.find("-") + 1: ]) # gets the higher range of the index

            if (int(lastHightByte) > int(lowByte)): #if the low indext lower than the last high indext, takes the last high indext as the low indext
                print("Downloaded bytes " + str(int(lastHightByte) + 1) + " to " + str(highByte) + " (size = " + str(highByte - (int(lastHightByte))) + ")")
                lowByte = lastHightByte - lowByte + 1
        
                
            highByte = highByte - lowByte
            
            if (int(lastHightByte) <= int(lowByte)):# if the low byte is not higher than changes low byte as 1
                print("Downloaded bytes " + str(lowByte + 1) + " to " + str(highByte)+ " (size = " + str(highByte - lowByte) + ")")
                lowByte = 0
                
            highByte = str(highByte)
            lowByte = str(lowByte)
            lastHightByte = int(byteRange[byteRange.find("-") + 1: ])

            serverList.pop(0) #Deletes byte range

            s = socket.socket (socket.AF_INET, socket.SOCK_STREAM) #creates the socket
            s.connect((socket.gethostbyname(hostName), 80)) 

            authin = base64.b64encode(password.encode()).decode() # server understands the password as Base64 so the password encoded
            request="GET " + address + " HTTP/1.1\r\nHost:" + hostName + "\r\n" + "Range: bytes=" + lowByte + "-" + highByte + "\r\n"+"Authorization: Basic "+authin+"\r\n\r\n"  #connection request in http
            s.send(request.encode())  #Send host to connection request in http
            sleep(1) # wait to get all datas
            response = s.recv(1000000) #receve responce and adjusting the buffer size

            responceData = response.decode()  #decodes responce to string
            responceData = responceData[responceData.find("text/plain") + 14 :] #gets the data
            text = text + responceData # adds to the final text file
            
            s.close() #closing the tcp connection

        print("Download of the file is complete (size = " + str(totalBytle) +")")

        f = open(textName, "w") #create a file with name provided in the text file
        f.write(text) #writes the obtain text to the file
        f.close() #closes the file
        
except:
    print("Unknown Error Occurred")
