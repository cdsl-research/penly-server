import socket,time

PORT = 8080
# server = (ip,PORT)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(server)
# # サーバに送信
# s.send(line.encode("UTF-8"))a
# s.close()
# espIdList = {
# "B" : "ESP_27B055",
# "A1" : "ESP_7B0B85",
# "A2" : "ESP_A97611",
# "A3" : "ESP_A974B5",
# "A4" : "ESP_A966F1",
# "A5" : "ESP_A9F0D9",
# "sA" : "ESP_5242C9",
# "sB" : "ESP_529B71",
# "sC" : "ESP_5267D1",
# "sD" : "ESP_51621D",
# "sE" : "ESP_60981D",
# "sF" : "ESP_530955"
# }
espIdList = {
"A" : "ESP_27B055",
"B" : "ESP_7B0B85",
"C" : "ESP_A97611",
"D" : "ESP_A974B5",
"E" : "ESP_A966F1",
"F" : "ESP_A9F0D9",
"G" : "ESP_5242C9",
"H" : "ESP_529B71",
"I" : "ESP_5267D1",
"J" : "ESP_51621D",
"K" : "ESP_60981D",
"L" : "ESP_530955"
}


# espIpDict = {
#     "B" : "192.168.100.158",
#     "A1" : "192.168.100.164",
#     "A2" : "192.168.100.177",
#     "A3" : "192.168.100.130",
#     "A4" : "192.168.100.92",
#     "A5" : "192.168.100.122",
#     "sA" : "192.168.100.138",
#     "sB" : "192.168.100.124",
#     "sC" : "192.168.100.173",
#     "sD" : "192.168.100.147",
#     "sE" : "192.168.100.46",
#     "sF" : "192.168.100.55"
# }

espIpDict = {
    "A" : "192.168.100.158",
    "B" : "192.168.100.164",
    "C" : "192.168.100.177",
    "D" : "192.168.100.130",
    "E" : "192.168.100.92",
    "F" : "192.168.100.122",
    "G" : "192.168.100.138",
    "H" : "192.168.100.124",
    "I" : "192.168.100.173",
    "J" : "192.168.100.147",
    "K" : "192.168.100.46",
    "L" : "192.168.100.55"
}

CONNECTION_CDSL = {
    "A" : "192.168.100.158",
    "B" : "192.168.100.164",
    "C" : "192.168.100.177",
    "D" : "192.168.100.130"
    }

def sendSocket(ipAdress,sendData):
    server = (ipAdress,PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    s.send(sendData.encode("UTF-8"))
    s.close()

def all_send_connect_CDSL(sendData):
    for k,v in CONNECTION_CDSL.items():
        print(f"""
            {k} ({v})へと {sendData}を送信します
            """)
        try:
            sendSocket(v,sendData)
        except:
            pass

def all_reboot_send(sendData):
    for k,v in espIpDict.items():
        print(f"""
            {k} ({v})へと {sendData}を送信します
            """)
        try:
            sendSocket(v,sendData)
        except:
            print("送信エラー")

def sendUdpSocket(sendData):
    # UDPソケットを作成する
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # ブロードキャストアドレスを指定する
    broadcast_addr = '192.168.100.255'
    sendData = bytes(sendData, 'utf-8')
    # ブロードキャストアドレスにデータを送信する
    sock.sendto(sendData, (broadcast_addr, 8888))
    sock.sendto(sendData, (broadcast_addr, 8888))
    sock.sendto(sendData, (broadcast_addr, 8888))

def choiceESP32ID():
    espID = input("送信先ID >>> ")
    
    return espID

def main():
    choiceText = """
    1. autowifi
    2. experiment start
    3. experiment stop
    4. reboot
    5. reset_battery
    6. startAP
    7. stopAP
    """

    print(choiceText)
    choiceNumber = int(input(">>> "))
    tx = "id=server"
    txDict = dict()
    if choiceNumber == 1:
        txDict = {
            "id_origin" : "server",
            "command_origin" : "autowifi"
        }
    elif choiceNumber == 2:
        txDict = {
            "id_origin" : "server",
            "command_origin" : "experiment_start"
        }
    elif choiceNumber == 3:
        txDict = {
            "id_origin" : "server",
            "command_origin" : "experiment_stop"
        }
    elif choiceNumber == 4:
        txDict = {
            "id_origin" : "server",
            "command_origin" : "reboot"
        }
    elif choiceNumber == 5:
        txDict = {
            "id_origin" : "server",
            "command_origin" : "reset_battery"
        }
    elif choiceNumber == 6:
        sendingEspId = choiceESP32ID()
        if sendingEspId == "all":
            for k,v in espIdList.items():
                tx = ""
                txDict = {
                "id_origin" : "server",
                "command_origin" : "startAP",
                "to" : k
                }
                
                for k ,v in txDict.items():
                    tx += f"&{k}={v}"
                all_send_connect_CDSL(tx)
                # sendUdpSocket(tx)
                time.sleep(1)
            return 0
        else:
            txDict = {
            "id_origin" : "server",
            "command_origin" : "startAP",
            "to" : sendingEspId
            }
    elif choiceNumber == 7:
        sendingEspId = choiceESP32ID()
        txDict = {
            "id_origin" : "server",
            "command_origin" : "stopAP",
            "to" :sendingEspId
        }

    for k ,v in txDict.items():
        tx += f"&{k}={v}"
        
    # sendSocket("192.168.100.158",tx)
    # sendSocket("192.168.100.164",tx)
    if choiceNumber != 4:
        all_send_connect_CDSL(tx)
        # sendUdpSocket(tx)
    else:
        choi = input("1 : all , 2 : not all >>> ")
        if int(choi) == 1:
            tx += "&option=force"
            all_reboot_send(tx)
            # sendUdpSocket(tx)
        else:
            all_send_connect_CDSL(tx)


if __name__ == "__main__":
    main()
