
from <pathToEntities> import Kbutton, Button, Obutton
from pony.orm import db_session, rollback, select
from <pathToDBconnection> import getDB
from log import Log

log = Log(__name__)
errorMessages = [
    '<errorMessage>',
    '<errorMessage>',
    '<errorMessage>'
]

def insertKbutton(data: object):
    Kbutton( 
        button_key=data.button_key,
        button_text=data.button_text,
        sel=data.sel
        )

def insertButton(data: object):
    Button( 
            button_key=data.button_key,
            location=data.location,
            label=data.label
            )

def insertObutton(data: object):
    Obutton( 
            button_key=data.button_key,
            user=data.user,
            location=data.location
            )


def updateOrInsertKbutton(data: object) -> bool:
    """
    First try to update, if the data doesn't exist
    in the DB, then insert will happen otherwise
    it will make rollback, stop the program 
    and report the issue.
    """
    try:
        kbutton = Kbutton[data.button_key]
        kbutton.set(
            button_text=data.button_text,
            sel=data.sel
        )
    except:
        try:
            insertKbutton(data=data)
        except:
            log(errorMessages[0].format(
                data.button_key, 
                data.button_text
                )
            )
            rollback()
            return False
    return True


def updateOrInsertButton(data: object) -> bool:
    """
    First try to update, if the data doesn't exist
    in the DB, then insert will happen otherwise
    it will make rollback, stop the program 
    and report the issue.
    """
    try:
        button = Button[data.button_key]
        button.set(
            button_key=data.button_key,
            location=data.location,
            label=data.label
        )
    except:
        try:
            insertButton(data=data)
        except:
            log(errorMessages[1].format(
                data.button_key, 
                data.label
                )
            )
            rollback()
            return False
    return True


def updateOrInsertObutton(data: object) -> bool:
    """
    First try to update, if the data doesn't exist
    in the DB, then insert will happen otherwise
    it will make rollback, stop the program 
    and report the issue.
    """
    try:
        obutton = Obutton[data.button_key]
        obutton.set(
            button_key=data.button_key,
            user=data.user,
            location=data.location
        )
    except:
        try:
            insertObutton(data=data)
        except:
            log(errorMessages[2].format(
                data.button_key, 
                data.user
                )
            )
            rollback()
            return False
    return True


def updateOrInsertDB(tupleOfValidateButtonRows: tuple) -> list:

    outputListOfInsUpdData: list = []
    listOfButtons: list = []
    with db_session:
        for row in tupleOfValidateButtonRows[0]:
            resRow = updateOrInsertKbutton(data=row)
            if not resRow:
                return []
            else:
                outputListOfInsUpdData.append(row)
        for row in tupleOfValidateButtonRows[1]:
            resRow = updateOrInsertButton(data=row)
            if not row.id:
                getId = select(
                    k for k in Button 
                    if k.button_key == row.button_key
                    )[:]
                for but in getId:
                    keyData: dict = {}
                    keyData['button_key'] = but.button_key
                    keyData['location'] = but.location
                    listOfButtons.append(keyData)
            if not resRow:
                return []
            else:
                outputListOfInsUpdData.append(row)
    
    with db_session:
        for row in tupleOfValidateButtonRows[2]:
            if not row.button_key and listOfButtons:
                for keyDict in listOfButtons:
                    if keyDict['button_key'] == getattr(row, 'button_key'):
                        setattr(row, 'location', keyDict['location'])
                        break
            resRow = updateOrInsertObutton(data=row)
            if not resRow:
                return []
            else:
                outputListOfInsUpdData.append(row)

    return outputListOfInsUpdData