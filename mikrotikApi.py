from librouteros import connect


def getInfo(username, password, host):

    api = connect(username=username, password=password, host=host)

    resource_info = api(cmd='/system/resource/print')
    identity_info = api(cmd='/system/identity/print')
    routerboard_info = api(cmd='/system/routerboard/print')

    rbIdentity = identity_info[0]['name']
    uptime = resource_info[0]['uptime']
    routerOsVersion = resource_info[0]['version']
    boardName = resource_info[0]['board-name']
    architectureName = resource_info[0]['architecture-name']
    currentFirmware = routerboard_info[0]['current-firmware']
    model = routerboard_info[0]['model']
    serialNumber = routerboard_info[0]['serial-number']

    rbDetails = {
        "rbIdentity" : rbIdentity,
        "uptime" : uptime,
        "routerOsVersion" : routerOsVersion,
        "boardName" : boardName,
        "architectureName" : architectureName,
        "currentFirmware" : currentFirmware,
        "model" : model,
        "serialNumber" : serialNumber
    }

    return rbDetails
