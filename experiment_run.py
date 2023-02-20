import socket,time,sys
from collections import Counter

PORT = 8080

COMPLETING_ESP32 = [
    "ESP_27B055",
    "ESP_7B0B85",
    "ESP_A97611"
]

ESP32_NAME_LIST = [
    "ESP_27B055",
    "ESP_7B0B85",
    "ESP_A97611",
    "ESP_A974B5",
    "ESP_A966F1",
    "ESP_A9F0D9",
    "ESP_5242C9",
    "ESP_529B71",
    "ESP_5267D1",
    "ESP_51621D",
    "ESP_60981D",
    "ESP_530955"
]

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

espNameDict = {
    "ESP_27B055":"A",
    "ESP_7B0B85":"B",
    "ESP_A97611":"C",
    "ESP_A974B5":"D",
    "ESP_A966F1":"E",
    "ESP_A9F0D9":"F",
    "ESP_5242C9":"G",
    "ESP_529B71":"H",
    "ESP_5267D1":"I",
    "ESP_51621D":"J",
    "ESP_60981D":"K",
    "ESP_530955":"L"
}

CONNECTION_CDSL = {
    "A" : "192.168.100.158",
    "B" : "192.168.100.164",
    "C" : "192.168.100.177",
    "D" : "192.168.100.130"
}

GROUPS_1 = [
    ["B","A1"],
    ["B","A1"],
    ["A1","A2"],
    ["A1","A2"]
]
GROUPS_2 = [
    ["A3","A4"],
    ["A3","A4"],
    ["A3","A4","sA"],
    ["sA","sB"]
]
GROUPS_3 = [
    ["sC","sD"],
    ["sD","sC"]
]

GROUPS = [
    ["A","B"],
    ["A","B"],
    ["B","C","D"],
    ["B","C","D"],
    ["C","D"],
    ["E","F","G"],
    ["F","G","H"],
    ["G","H","I"],
    ["J","K"],
    ["K","L"]
]

HOP_DEVICE_NUM = [4,5,3]

ACTIVATED_ESP32 = []
DEACTIVATED_ESP32 = []

def checkGroup():
    pass

def getData():
    timeDict = {}
    dataDict = {}
    timeStampDict = {}
    for k, v in espIdList.items():
        fileName = f"battery_data/{v}.csv"
        timeList = list()
        dataList = list()
        timeStampList = list()
        #print(f"fileName : {fileName}")
        with open(fileName,"r") as f:
            for line in f:
                dataSplit = line.split(",")
                time = dataSplit[0]
                data = float(dataSplit[1])
                timeStamp = int(dataSplit[2])
                #print(f"{time} ({timeStamp}) >> {data}")
                timeList.append(time)
                dataList.append(data)
                timeStampList.append(timeStamp)
        timeDict[v] = timeList
        dataDict[v] = dataList
        timeStampDict[v] = timeStampList
    return timeDict,dataDict,timeStampDict

def activeAP(sendingEspId):
    tx = "id=server"
    txDict = {
            "id_origin" : "server",
            "command_origin" : "startAP",
            "to" : sendingEspId
        }
    for k ,v in txDict.items():
        tx += f"&{k}={v}"
    all_send_connect_CDSL(tx)
    time.sleep(1)

def deactiveAP(sendingEspId):
    tx = "id=server"
    txDict = {
            "id_origin" : "server",
            "command_origin" : "stopAP",
            "to" : sendingEspId
        }
    for k ,v in txDict.items():
        tx += f"&{k}={v}"
    all_send_connect_CDSL(tx)
    time.sleep(1)

def sD_sF_ap_deactive():
    # deactiveAP("sD")
    # deactiveAP("sF")
    # deactiveAP("A5")
    
    deactiveAP("sE+sF+A5")
    

def debugActive1():
    # deactiveAP("B")
    # deactiveAP("A2")
    # deactiveAP("A3")
    # deactiveAP("sA")
    # deactiveAP("sD")
    
    # deactiveAP("B+A2+A3+sA+sD+sE+sF+A5")
    
    
    # for i in range(60):
    #     sys.stdout.write("\rIteration: {}".format(i))
    #     sys.stdout.flush()
    #     time.sleep(1)
        
    
    while True:
        
        activeAP("B+A2+A3+sA+sD")
        time.sleep(3)
        deactiveAP("A1+sB+sC+A4")
        
        for i in range(300):
            sys.stdout.write("\rIteration: {}".format(i))
            sys.stdout.flush()
            time.sleep(1)
    
        activeAP("A1+sB+sC+A4")
        time.sleep(3)
        deactiveAP("B+A2+A3+sA+sD")
        
        for i in range(300):
            sys.stdout.write("\rIteration: {}".format(i))
            sys.stdout.flush()
            time.sleep(1)
            

def all_active():
    activeAP("B+A1+A2+A3+A4+A5+sA+sB+sC+sD+sE+sF")
    
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

def groups_counter():
    all_groups = GROUPS
    all_chars = [char for group in all_groups for char in group]

    char_counts = Counter(all_chars)
    char_counter = dict()
    for char, count in char_counts.items():
        char_counter[char] = count
        print(f"{char}: {count}")
    return  char_counter

def has_multiple_maximum(lst):
    return lst.count(max(lst)) > 1

def judge_multiple_maximum(weightDict):
    testList = []
    for k, v in weightDict.items():
        testList.append(v)
    result = has_multiple_maximum(testList)
    print(result)
    return result

def process_maxmum_send(weightDict,status):
    global ACTIVATED_ESP32
    global DEACTIVATED_ESP32
    max_weight = max(weightDict.values())
    max_weight_key = [k for k, v in weightDict.items() if v == max_weight][0]
    status[max_weight_key] = True
    espNameKey = espNameDict[max_weight_key]
    print(f"activate : {espNameKey}")
    if espNameKey not in ACTIVATED_ESP32:
        ACTIVATED_ESP32.append(espNameKey)
    # activeAP(espNameKey)
    
    deactivateEsp32NameText = ""
    for k, v in weightDict.items():
        if k != max_weight_key:
            status[k] = False
            espNameKey = espNameDict[k]
            if espNameKey not in DEACTIVATED_ESP32:
                DEACTIVATED_ESP32.append(espNameKey)
            deactivateEsp32NameText += f"{espNameKey}+"
    print(f"deactivate : {deactivateEsp32NameText}")
    # deactiveAP(deactivateEsp32NameText)
    return status

def process_multiple_maxmum_send(weightDict,currentBattery,status):
    global ACTIVATED_ESP32
    global DEACTIVATED_ESP32
    max_weight = max(weightDict.values())
    max_weight_keys = [k for k, v in weightDict.items() if v == max_weight]
    max_batterys = dict()
    for espN in max_weight_keys:
        max_batterys[espN] = currentBattery[espN]
    
    max_battery = max(max_batterys.values())
    max_battery_key = [k for k, v in max_batterys.items() if v == max_battery][0]
    status[max_battery_key] = True
    espNameKey = espNameDict[max_battery_key]
    # print(f"activate : {espNameKey}")
    if espNameKey not in ACTIVATED_ESP32:
        ACTIVATED_ESP32.append(espNameKey)
    # activeAP(espNameKey)
    deactivateEsp32NameText = ""
    for k, v in weightDict.items():
        if k != max_battery_key:
            status[k] = False
            espNameKey = espNameDict[k]
            if espNameKey not in DEACTIVATED_ESP32:
                DEACTIVATED_ESP32.append(espNameKey)
            deactivateEsp32NameText += f"{espNameKey}+"
    # print(f"deactivate : {deactivateEsp32NameText}")
    # deactiveAP(deactivateEsp32NameText)
    return status

def check_key(d, key):
    if key in d:
        return True
    else:
        return False

def check_not_true_device(weight,currentBattery,status,GROUP_NUM):
    for k, v in status.items():
        # if GROUP_NUM == 1:
        #     gggg = GROUPS_1
        # elif GROUP_NUM == 2:
        #     gggg = GROUPS_2
        # elif GROUP_NUM == 3:
        #     gggg = GROUPS_3
        gggg = GROUPS
        for li in gggg:
            if v == True:
                if espNameDict[k] not in li and k in weight:
                    # print(li)
                    weight_ddd = {}
                    for ll in li:
                        weight_ddd[espIdList[ll]] = weight[espIdList[ll]]
                    if not judge_multiple_maximum(weight_ddd):
                        status = process_maxmum_send(weight_ddd,status)
                    else:
                        status = process_multiple_maxmum_send(weight_ddd,currentBattery,status)
                    # print(status)

def main():
    # activeAP("B+A2+A3+sA+sD")
    # time.sleep(3)
    # deactiveAP("A1+sB+sC+A4")
    
    # time.sleep(10)
    
    global DEACTIVATED_ESP32
    global ACTIVATED_ESP32
    # B,A1,A2
    hop1 = {}
    status1 = {}
    weight1 = {}
    # A3,A4,sA,sB
    hop2 = {}
    status2 = {}
    weight2 = {}
    # sC, sD
    hop3 = {}
    status3 = {}
    weight3 = {}
    
    beforeActivated = []
    beforeDeactivated = []
    weightCountDict = groups_counter()
    
    deathDevice = []
    
    enableProcess = True
    
    activeEnable = False
    deactiveEnable = False
    
    #sD_sF_ap_deactive()
    
    time.sleep(5)
    while True:
        timeDict,dataDict,timeStampDict = getData()
        
        # print(timeDict,dataDict,timeStampDict)
        
        # Key : espName , value : 現在の電池残量
        currentBattery = {}
        
        for espName , dataList in timeStampDict.items():
            max_value = max(dataList)
            max_index = dataList.index(max_value)
            text = f"""{espName} : {max_value} ({max_index}) | {dataDict[espName][max_index]}  < ({max_index-1}) {int(dataDict[espName][max_index] - dataDict[espName][max_index-1])}"""
            print(text)
            battery = float(dataDict[espName][max_index])
            currentBattery[espName] = battery
            if battery <= 0.0 and espName not in deathDevice:
                deathDevice.append(espName)
                enableProcess = True
            if espNameDict[espName] in ["A","B","C","D"] and battery > 0.0:
                hop1[espName] = battery
                weight1[espName] = weightCountDict[espNameDict[espName]]
            elif espNameDict[espName] in ["E","F","G","H","I"] and battery > 0.0:
                hop2[espName] = battery
                weight2[espName] = weightCountDict[espNameDict[espName]]
            elif espNameDict[espName] in ["J","K","L"] and battery > 0.0:
                hop3[espName] = battery
                weight3[espName] = weightCountDict[espNameDict[espName]]
            
            
            
            
            
            
        # #  print(currentBattery)
        # print(weight1)
        # print(weight2)
        # print(weight3)
        # print("----------------------------------")
        
    
        # if not judge_multiple_maximum(weight1):
        #     status1 = process_maxmum_send(weight1,status1)
        # else:
        #     status1 = process_multiple_maxmum_send(weight1,currentBattery,status1)
        # #print(status1)
        
        # check_not_true_device(weight1,currentBattery,status1,1)
        
        
        # if not judge_multiple_maximum(weight2):
        #     status2 = process_maxmum_send(weight2,status2)
        # else:
        #     status2 = process_multiple_maxmum_send(weight2,currentBattery,status2)
        # #print(status2)
        
        # check_not_true_device(weight2,currentBattery,status2,2)
        
        # if not judge_multiple_maximum(weight3):
        #     status3 = process_maxmum_send(weight3,status3)
        # else:
        #     status3 = process_multiple_maxmum_send(weight3,currentBattery,status3)
        # #print(status3)
        
        # check_not_true_device(weight3,currentBattery,status3,3)
        
        # if enableProcess:
        #     enableProcess = False
        #     print(ACTIVATED_ESP32)
        #     print(DEACTIVATED_ESP32)
            
        #     print(f"""
        #         ------ CURRENT STATUS ------
        #     ACTIVATED   : {ACTIVATED_ESP32}
        #     DEACTIVATED : {DEACTIVATED_ESP32}
        #         """)
            
        #     common = set(ACTIVATED_ESP32) & set(DEACTIVATED_ESP32)
        #     DEACTIVATED_ESP32 = [item for item in DEACTIVATED_ESP32 if item not in common]
            
        #     uniqueToActivated = set(ACTIVATED_ESP32) - set(beforeActivated)
        #     if uniqueToActivated:
        #         print(f"起動デバイスに変化あり : {uniqueToActivated}")
        #         text = ""
        #         for uta in uniqueToActivated:
        #             text += f"{uta}+"
        #         # if activeEnable == False:
        #         #     activeEnable = True
        #         # else:
                
        #         #activeAP(text)
                
        #     else:
        #         print("起動デバイス：変化なし")
        #     print("----------")
            
        #     time.sleep(5)
            
        #     uniqueToDeactivated = set(DEACTIVATED_ESP32) - set(beforeDeactivated)
        #     if uniqueToDeactivated:
        #         print(f"停止デバイスに変化あり : {uniqueToDeactivated}")
        #         text = ""
        #         for uta in uniqueToDeactivated:
        #             text += f"{uta}+"
        #         if deactiveEnable == False:
        #             deactiveEnable = True
                    
        #             #deactiveAP(text)
                    
        #     else:
        #         print("停止デバイス：変化なし")
            
        #     beforeActivated = ACTIVATED_ESP32
        #     beforeDeactivated = DEACTIVATED_ESP32
        
        
        # for i in range(10):
        #     print(f"\r time : {i}",end="")
        #     time.sleep(1)
        # print("\n")
        
        

if __name__ == '__main__':
    main()