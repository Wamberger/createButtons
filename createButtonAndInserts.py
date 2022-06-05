
from createDbRows import createButtonRows, createKbuttonRows, createObuttonRows
from <pathToFunction> import readAndSortDataWithModeTest

listOfMode = [
    'mode',
    'test'
    ]

listOfLocations = [
    'location',
    'appButons',
]

listOfSelects = [
    'sel',
    'sel1'
]

def readInputDataAndSort(createdListOfDict: list) -> list:
    """
    In the list of dictionary is giving the information and some values,
    how the elements should be sorted and edited. 
    Thus, firstly the loop determine the location of the new created buttons in the App. 
    Secondly, the second loop is determine the data from the DB and the editing 
    of the values from the list of dictionaries.

    At the moment, only one location and mode is avaliable, to create automatic buttons in the app.
    """

    returnData: list = []
    for data in createdListOfDict:
        for key, value in data.items():
            if key == listOfLocations[0] \
            and value[0] == listOfLocations[1]:   
                for key, value in data.items():
                    if key == listOfMode[0] \
                    and value[0] == listOfMode[1]:
                        resData = readAndSortDataWithModeTest(
                            data=data,
                            listOfMode=listOfMode,
                            listOfSelects=listOfSelects
                            )
                        returnData += resData
            # Can be more if statements with more options.
    return returnData


def createButtonAndInserts(createdListOfDict: list) -> tuple:
    """
    The input list of dictionaries with keys and values will be read
    and sorted according to the rule which is written in one of keys.
    Then kbutton, button and obutton objects will be created with the 
    values from the list of dictionaries as well as with empty 
    attributes, which are needed for the DB.
    """

    listOfsortInputData = readInputDataAndSort(createdListOfDict=createdListOfDict)
    if not listOfsortInputData:
        return listOfsortInputData
    
    listOfKbuttonRows = createKbuttonRows(listOfsortInputData)
    listOfButtonRows = createButtonRows(listOfsortInputData)
    listOfObuttonRows = createObuttonRows(listOfsortInputData)
    return listOfKbuttonRows, listOfButtonRows, listOfObuttonRows