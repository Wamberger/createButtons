
from pony.orm import db_session, select
from <pathToEntities> import Kbutton, Button, Obutton
from <pathToEntity> import Tables
from <pathToLog> import Log

log = Log(__name__)

errorMessages = [
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>',
    ]


def readAndInitKbuttonRow(data: object) -> object:
    """
    If the data is in DB then an update will happen. 
    The '' and 0 values of input data will be replaced 
    with the values from the DB.
    """
    with db_session:
        getButton = select(d for d in Kbutton 
            if d.button_key == data.button_key
            )[:]
        if getButton:
           for key, value in data.__dict__.items():
                if (isinstance(value, str) and value.isspace()) \
                or (isinstance(value, int) and not value):
                    for item in getButton:
                        dbValue = getattr(item, key)
                        setattr(data, key, dbValue)
                        break
        else:
            log(errorMessages[0].format(data.button_key))
    return data


def readAndInitButtonRow(data: object) -> object:
    """
    If the data is in DB then an update will happen. 
    The '' and 0 values of input data will be replaced 
    with the values from the DB.
    """
    with db_session:
        getButton = select(
            b for b in Button 
            if b.button_key == data.button_key
            )[:]
        if getButton:
           for key, value in data.__dict__.items():
                if (isinstance(value, str) and value.isspace()) \
                or (isinstance(value, int) and not value):
                    for item in getButton:
                        dbValue = getattr(item, key)
                        setattr(data, key, dbValue)
                        break
        else:
            log(errorMessages[1].format(data.button_key))
    return data


def readAndInitObuttonRow(data: object) -> object:
    """
    If the data is in DB then an update will happen. 
    The '' and 0 values of input data will be replaced 
    with the values from the DB.
    """
    with db_session:
        if data.user:
            getButton = select(
                b for b in Obutton
                if b.button_key == data.button_key
                and b.user == data.user
                )[:]
        if getButton:
           for key, value in data.__dict__.items():
                if (isinstance(value, str) and value.isspace()) \
                or (isinstance(value, int) and not value):
                    for item in getButton:
                        dbValue = getattr(item, key)
                        setattr(data, key, dbValue)
                        break
        else:
            log(errorMessages[1].format(data.button_key))
    return data


def checkType(validField: str, value: str or int) -> bool:
    """
    Check the datatype str or int.
    """
    if validField == 'S':
        if not isinstance(value, str):
            log(errorMessages[2].format(type(value)))
            return False
    elif validField == 'I':
        if not isinstance(value, int):
            log(errorMessages[3].format(type(value)))
            return False
    return True


def chechPrimaryKey(validField: str, value: str or int) -> bool:
    """
    If primary key in DB 
    first try string if not string check int
    """
    if validField == 'J':
        try:
            if not value:
                log(errorMessages[4])
                return False
            elif value.isspace():
                log(errorMessages[4])
                return False
        except:
            if value == 0:
                log(errorMessages[4])
                return False
    return True


def checkLength(validField: str, value: str or int) -> bool:
    """
    first try string if not string check int
    """
    try:
        if len(value) > validField:
            log(errorMessages[5].format(validField, len(value)))
            return False
    except:
        if len(str(value)) > len(str(validField)): #for digits
            log(errorMessages[5].format(validField, value))
            return False
    return True


def validateRow(data: object, table: str, ignorePrimeKey: list) -> bool:
    ''' Validate the data in object and return boolean.
        True: good,
        False: error
    '''

    with db_session:
        getValiData = select(
            v for v in Tables 
            if v.m_tab == table
            )[:]

    for validField in getValiData:
        for key, value in data.__dict__.items():
            if validField.field == key:
                resCheckType = checkType(
                    validField=validField.type,
                    value=value
                    )
                if not resCheckType:
                    if validField.none_value != value:
                        log(errorMessages[6].format(key, value))
                        return resCheckType
                
                resCheckPrimaryKey = chechPrimaryKey(
                    validField=validField.primarykey,
                    value=value
                    )
                if not resCheckPrimaryKey:
                    if key not in ignorePrimeKey:
                        log(errorMessages[7].format(key))
                        return resCheckPrimaryKey

                if value:
                    resCheckLength = checkLength(
                        validField=validField.length,
                        value=value
                        )
                    if not resCheckLength:
                        log(errorMessages[8].format(key, value))
                        return resCheckLength
    return True


def readAndValidateInput(tupleOfButtonInserts: tuple) -> tuple:

    """
    Three lists of object inputs in a tuple are delivered.
    For ever loop the objects from their lists will get updated - if the update happens.
    Then the objects from the list will be validated.
    returns a tuple with content of a bool and got tuples.
    """
    for row in tupleOfButtonInserts[0]:
        row = readAndInitKbuttonRow(row)
        resRow = validateRow(
            data=row, 
            table='kbutton',
            ignorePrimeKey=[]
            )
        if not resRow:
            return resRow, tupleOfButtonInserts

    listOfButtons: list = []
    for row in tupleOfButtonInserts[1]:
        row = readAndInitButtonRow(row)
        if row.button_key:
            keyData: dict = {}
            keyData['button_key'] = row.button_key
            keyData['location'] = row.location
            listOfButtons.append(keyData)
        resRow = validateRow(
            data=row, 
            table='button',
            ignorePrimeKey=['button_key']
            )
        if not resRow:
            return resRow, tupleOfButtonInserts
            
    for row in tupleOfButtonInserts[2]: 
        if listOfButtons:
            for keyDict in listOfButtons:
                if keyDict['button_key'] == getattr(row, 'button_key'):
                    setattr(row, 'location', keyDict['location'])
                    break
            row = readAndInitObuttonRow(row)
        resRow = validateRow(
            data=row, 
            table='obutton',
            ignorePrimeKey=[]
            )
        if not resRow:
            return resRow, tupleOfButtonInserts

    return True, tupleOfButtonInserts