#!/usr/bin/env python
# -*- coding: utf-8 -*-

import selectors
import socket
import random
from modules import ProtoHelper
from storage import Conf
from modules import Cheksum
from modules import Base
import json

packetTypes = {
    "0x1": "auth_request", #запрос авторизации #нечётные клиента и чётные от сервера
    "0x8001": "auth_response", #ответ авторизации, удаление, изменение, регистрацию, удаление пользователя
    "0x2": "get_request", #запрос на чтение данных
    "0x2001": "get_response", #ответ на чтение данных

    "0x3": "delete_request", #запрос на удаление данных
    "0x4": "change_request", #запрос на изменение данных
    "0x5": "registration_request", #запрос на регистрацию пользователей
    "0x6": "delete_users" #запрос на удаление пользователя
}

def Accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('\nAccepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, ServerRecvLoop)

def BuildData(code, payloadClient, idSessions): 

    payload = b""
    data = b""

    if code == "0x0":

        payloadDict = {"idSessions": idSessions, "message": "Damaged package"}
        payload = ProtoHelper.Encode("get_response", payloadDict)

    if code == "0x1":

        autor = False

        bd = Base.load("storage/users.json", False)
        allKey = bd.dgetall("users")


        for i in range(len(allKey)):
            if allKey[i]["login"] == payloadClient["login"]:
                if allKey[i]["password"] == payloadClient["password"]:
                    autor = True
                    
        if autor:
            idSessions = random.random()
            payloadDict = {"idSessions": idSessions, "message": "All right auth"}

        else:
            payloadDict = {"idSessions": idSessions, "message": "You are not authorized"}

        payload = ProtoHelper.Encode("auth_response", payloadDict)

    if code == "0x2":
        
        if payloadClient["idSessions"] == str(idSessions):
            selection = {}

            bd = Base.load("storage/data.json", False)


            keys = payloadClient["keys"]
            keys = keys.split(" ")

            for key in keys:
                try:
                    selectionKey = bd.get(key)
                except: continue
                selection.update({key: selectionKey})    

            payloadDict = {"idSessions": idSessions, "message": selection}

        else: 
            payloadDict = {"idSessions": idSessions, "message": "You cannot send requests"}
        payload = ProtoHelper.Encode("get_response", payloadDict)
    
    if code == "0x3":
        if payloadClient["idSessions"] == str(idSessions):
            selection = {}

            bd = Base.load("storage/data.json", False)

            keys = payloadClient["keys"]
            keys = keys.split(" ")

            for key in keys:
                try:
                    bd.rem(key)
                except: continue 

            bd.dump()
            payloadDict = {"idSessions": idSessions, "message": "You deleted data"}

        else: 
            payloadDict = {"idSessions": idSessions, "message": "You cannot send requests"}


        payload = ProtoHelper.Encode("get_response", payloadDict)

    if code == "0x4":

        if payloadClient["idSessions"] == str(idSessions):
            selection = {}

            bd = Base.load("storage/data.json", False)

            keys = payloadClient["keys"]
            value = payloadClient["value"]

            keys = keys.split(" ")
            value = value.split(" ")
            for i in range(len(keys)):      
                try:
                    bd.set(keys[i], value[i])
                except: continue 
            bd.dump()
            payloadDict = {"idSessions": idSessions, "message": "You have changed the data"}

        else: 
            payloadDict = {"idSessions": idSessions, "message": "You cannot send requests"}


        payload = ProtoHelper.Encode("get_response", payloadDict)

    if code == "0x5":
        if payloadClient["idSessions"] == str(idSessions):
            exists = False

            bd = Base.load("storage/users.json", False)

            allKey = bd.dgetall("users")


            for i in range(len(allKey)):
                if allKey[i]["login"] == payloadClient["login"]:
                    if allKey[i]["password"] == payloadClient["password"]:
                        exists = True

            if exists: 
                payloadDict = {"idSessions": idSessions, "message": "Such a user exists"}
            else:
                payloadDict = {"idSessions": idSessions, "message": "You have added a new user"}
                allKey.append({"login":payloadClient["login"], "password":payloadClient["password"]})
                bd.dump()



        else: 
            payloadDict = {"idSessions": idSessions, "message": "You cannot send requests"}


        payload = ProtoHelper.Encode("get_response", payloadDict)
    
    if code == "0x6":
        if payloadClient["idSessions"] == str(idSessions):
            selection = {}

            bd = Base.load("storage/users.json", False)
            allUsers = bd.dgetall("users")

            for i in range(len(allUsers)):
                if allUsers[i]["login"] == payloadClient["login"] and allUsers[i]["password"] == payloadClient["password"]:
                    allUsers.pop(i)
                    break
            bd.dump()

            payloadDict = {"idSessions": idSessions, "message": "You have deleted this user"}

        else: 
            payloadDict = {"idSessions": idSessions, "message": "You cannot send requests"}


        payload = ProtoHelper.Encode("get_response", payloadDict)

    cheksum=Cheksum.Cheksum(payload)
    data = 0x7f.to_bytes(1, "big") + payload + cheksum.to_bytes(2, "big") + 0x7f.to_bytes(1, "big")

    return data, idSessions

def ServerRecvLoop(conn, mask):

    bd = Base.load("storage/settingsBD.json", False)
    idSessions = bd["idSessions"]
    isRecvPacketProgess = False
    packetData = b''
    recvData = conn.recv(8) 
    if recvData:
        while True:
            # recvData = conn.recv(8) 
            
            identyPosL = recvData.find(b'\x7f')
            if isRecvPacketProgess :
                packetData += recvData
                print(packetData)

            if not isRecvPacketProgess and identyPosL >= 0:
                isRecvPacketProgess = True
                packetData += recvData[identyPosL:len(recvData)]      
            
            identyPosR = packetData.rfind(b'\x7f')
            if identyPosR > 0 and identyPosL != identyPosR:
                
                packetData=packetData[1:identyPosR] #identyPosL без -6 при запросе данных

                cheksum = Cheksum.CheksumTransportPackech(packetData)
                if not cheksum:

                    print("Damaged package")
                    data, idSessions = BuildData("0x0", 0, idSessions)
                    bd.set("idSessions", str(idSessions))
                    bd.dump()
                    sel.unregister(conn)
                    conn.send(data)
                    break
                    # return data

                else: 
                    payloadBin = packetData[0:len(packetData)-2]
                    packet = packetTypes[ProtoHelper.GetDecodeСode(payloadBin[0:2])]
                    payloadClient = ProtoHelper.Decode(packet, payloadBin)


                    data, idSessions = BuildData(payloadClient["code"], payloadClient, idSessions)  

                    bd.set("idSessions",str(idSessions))
                    bd.dump()
                    
                    sel.unregister(conn)
                    conn.send(data)
                    break
                    # return data, idSessions

            recvData = conn.recv(8) 
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind((Conf.HOST, Conf.PORT))
sock.listen(100)

sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, Accept)

while True: 
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
        print("\n", key)
        print("\n", mask)

    # conn, addr = sock.accept()
    # print ("\nПодключился клиент: ", addr)
    # data, idSessions = ServerRecvLoop(conn, idSessions)

    # conn.send(data)

conn.close()
    