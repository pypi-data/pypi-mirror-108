#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

packetTypes = {
    "auth_request": 0x0001, #запрос авторизации #нечётные клиента и чётные от сервера
    "auth_response":0x8001, #ответ авторизации, удаление, изменение, регистрацию, удаление пользователя

    "get_request": 0x0002, #запрос на чтение данных
    "get_response": 0x2001, #ответ на чтение данных

    "delete_request": 0x0003, #запрос на удаление данных
    "change_request": 0x0004, #запрос на изменение данных
    "registration_request": 0x0005, #запрос на регистрацию пользователей
    "delete_users": 0x0006, #запрос на удаление пользователя
}

def BuildProtoString(in_str, out_len):
    out_str = bytearray(out_len)
    in_str = bytearray(str(in_str), encoding = "utf-8")
    out_str[0:len(in_str)] = in_str
    return out_str

def BuildDecodeString(in_str, start_cut, end_cut):
    out_str = in_str[start_cut:end_cut].decode("utf-8")
    out_str = out_str.replace("\x00", "")
    return out_str

def GetDecodeСode(in_str):
    out_str = int.from_bytes(in_str[0:2],"big")
    out_str = hex(out_str)
    return out_str

def Decode(packetType, payloadBin):

    payload=''
    if packetType == "auth_request":
        
        code = GetDecodeСode(payloadBin)
        login = BuildDecodeString(payloadBin, 2, 32)
        password = BuildDecodeString(payloadBin, 32, 64)

        payload = {"code":code, "login": login, "password": password}

    if packetType == "auth_response":

        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        response = BuildDecodeString(payloadBin, 32, 62)

        payload={"code":code, "idSessions": idSessions, "response": response}

    if packetType == "get_request":
        
        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        key = BuildDecodeString(payloadBin, 32, 62)

        payload={"code":code, "idSessions": idSessions, "keys": key}

    if packetType == "get_response":

        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        response = BuildDecodeString(payloadBin, 32, 62)

        payload={"code":code, "idSessions": idSessions, "response": response}



    if packetType == "delete_request":
        
        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        key = BuildDecodeString(payloadBin, 32, 62)

        payload={"code":code, "idSessions": idSessions, "keys": key}

    if packetType == "change_request":
        
        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        key = BuildDecodeString(payloadBin, 32, 62)
        value = BuildDecodeString(payloadBin, 62, 92)

        payload={"code":code, "idSessions": idSessions, "value": value, "keys": key}

    if packetType == "registration_request":
        
        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        login = BuildDecodeString(payloadBin, 32, 62)
        password = BuildDecodeString(payloadBin, 62, 94)

        payload={"code":code, "idSessions": idSessions, "login": login, "password": password}

    if packetType == "delete_users":
        
        code = GetDecodeСode(payloadBin)
        idSessions = BuildDecodeString(payloadBin, 2, 32)
        login = BuildDecodeString(payloadBin, 32, 62)
        password = BuildDecodeString(payloadBin, 62, 94)

        payload={"code":code, "idSessions": idSessions, "login": login, "password": password}


    return payload

def Encode(packetType, payload):
    payloadBin = b''
    if packetType == "auth_request":
        login = payload["login"]
        password = payload["password"]
        payloadBin = BuildProtoString(login, 30) + BuildProtoString(password, 32)
    
    if packetType == "auth_response":
        idSessions = payload["idSessions"]
        message = payload["message"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(message, 30)

    if packetType == "get_request":
        
        idSessions = payload["idSessions"]

        keys = payload["keys"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(keys, 30)

    if packetType == "get_response":
        idSessions = payload["idSessions"]
        message = payload["message"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(message, 30)

    



    if packetType == "delete_request":
        
        idSessions = payload["idSessions"]
        keys = payload["keys"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(keys, 30)

    if packetType == "change_request":
        
        idSessions = payload["idSessions"]
        keys = payload["keys"]
        value = payload["value"]

        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(keys, 30) + BuildProtoString(value, 30)

    if packetType == "registration_request":
        
        idSessions = payload["idSessions"]
        login = payload["login"]
        password = payload["password"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(login, 30) + BuildProtoString(password, 32)

    if packetType == "delete_users":
        idSessions = payload["idSessions"]
        login = payload["login"]
        password = payload["password"]
        payloadBin = BuildProtoString(idSessions, 30) + BuildProtoString(login, 30) + BuildProtoString(password, 32)


    return packetTypes[packetType].to_bytes(2, "big") + payloadBin
    
