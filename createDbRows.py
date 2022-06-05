
from util import columnListKbutton, columnListButton, columnListObutton


class KbuttonRow:
    def __init__(self, data: dict, columnListKbutton: list) -> object:
        for label in columnListKbutton:
            if label in data:
                setattr(self, label, data[label])
            else:
                setattr(self, label, ' ')

class ButtonRow:
    def __init__(self, data: dict, columnListButton: list) -> object:
        for label in columnListButton:
            if label in data:
                if columnListButton[1] == label:
                    try:
                        setattr(self, label, int(data[label]))
                    except:
                        setattr(self, label, 0)
                else:
                    setattr(self, label, data[label])
            elif columnListButton[1] == label:
                setattr(self, label, 0)
            else:
                setattr(self, label, ' ')

class ObuttonRow:
    def __init__(self, data: dict, columnListObutton: list) -> object:
        for label in columnListObutton:
            if label in data:
                setattr(self, label, data[label])
            else:
                setattr(self, label, ' ')


def createKbuttonRows(listOfsortInputData: list) -> list:

    listOfinserts: list = []
    for row in listOfsortInputData:
        returnKbuttonRow = KbuttonRow(
            data=row, 
            columnListKbutton=columnListKbutton
            )
        listOfinserts.append(returnKbuttonRow)

    return listOfinserts

def createButtonRows(listOfsortInputData: list) -> list:

    listOfinserts: list = []
    for row in listOfsortInputData:
        returnButtonRow = ButtonRow(
            data=row, 
            columnListButton=columnListButton
            )
        listOfinserts.append(returnButtonRow)

    return listOfinserts


def createObuttonRows(listOfsortInputData: list) -> list:
    """
    Also creates button_key for the later process if this was not given.
    """

    listOfinserts: list = []
    for row in listOfsortInputData:

        returnObuttonRoW = ObuttonRow(
            data=row, 
            columnListObutton=columnListObutton
            )
        if not returnObuttonRoW.button_key:
            setattr(returnObuttonRoW, columnListButton[0], row[columnListButton[0]])

        listOfinserts.append(returnObuttonRoW)

    return listOfinserts
