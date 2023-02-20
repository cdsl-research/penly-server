


#fileData = input("文字列を入力 >>> ")
fileData = "&id_origin=server&command_origin=startAP&to=sF?192.168.100.236"
fileDataSplit = fileData.split("?")
fileData = fileDataSplit[0]
addr = fileDataSplit[1]
print(f"処理データ : {fileData} ,受信IPアドレス[ = addr] :  {addr}\n")

fileDataProcessData = fileData.split("&")
recvEsp32Id = ""
command_origin = None
id_origin = ""
temporaryRoute = ""
print(fileDataProcessData)
for fspd in fileDataProcessData:
    if fspd == " " or fspd == "":
        pass
    else:
        print(f"fspd : {fspd} ({type(fspd)})")
        fspdSplit = fspd.split("=")
        proKey = fspdSplit[0]
        proValue = fspdSplit[1]
        print(f"処理データ KEY : {proKey}     VALUE : {proValue}")
        if proKey == "id":
            recvEsp32Id = proValue
            print(f"受信ESP32のID == {proValue}")
        if proKey == "command_origin":
            command_origin = proValue
        if proKey == "id_origin":
            id_origin = proValue
        if proKey == "route":
            temporaryRoute = proValue
            temporaryRoute += f">{AP_SSID}"
        if proKey == "battery":
            battery = proValue
        if proKey == "to":
            toSending = proValue
        if proKey == "weight":
            weight = proValue