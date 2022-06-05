
from createButtonAndInserts import createButtonAndInserts
from readAndValidateInput import readAndValidateInput
from dbProcess import updateOrInsertDB

errorMessages = [
    'Wrong params: {}.',
    'Validation error. For more information look into log file.',
    'Database insert or update error. For more information look into the log file.'
    ]

def createListOfDictWithInputData(structure: str) -> tuple: 
    """
    The function cut and edit input string into a list of dictionaries.
    The input string will firstly cut string into the list by char &.
    Then it will be cut ($) and created list in lists. 
    Finally, the key and values are sorted into a dictionary 
    and add into the list for the output. 
    """

    try:
        firstSplit = [l for l in structure.split('&')]
        structureSplitList: list = []
        for eachSplit in firstSplit:
            secondSplit = [l.split('=') for l in eachSplit.split('$')]
            dictRules: dict = {}
            for elem in secondSplit:
                dictRules[elem[0]] = [x for x in elem[1].split(',')]
            structureSplitList.append(dictRules)

        return True, structureSplitList
    except:
        return False, errorMessages[0].format(structure)


def generateButton(prop: object) -> tuple:
    """"
    The inserted data creates buttons on defined location in the app.
    Function read the input params from user or task script 
    and creates as well as inserts rows into DB.
    """

    createdListOfDict = createListOfDictWithInputData(structure=prop.structureButton)
    if not createdListOfDict[0]:
        return [], createdListOfDict[1]
    
    tupleOfButtonInserts = createButtonAndInserts(createdListOfDict[1])

    tupleOfValidateButtonRows = readAndValidateInput(tupleOfButtonInserts=tupleOfButtonInserts)
    if not tupleOfValidateButtonRows[0]:
        return [], errorMessages[1]
    
    if not prop.test and tupleOfValidateButtonRows[0]:
        getData = updateOrInsertDB(tupleOfValidateButtonRows=tupleOfValidateButtonRows[1])
        if not getData:
            return [], errorMessages[2]
        return getData, None
    else:
        testOutputList: str = []   
        for itemToReportList in tupleOfValidateButtonRows[1]:
            for item in itemToReportList:
                testOutputList.append(item)
        return testOutputList, None