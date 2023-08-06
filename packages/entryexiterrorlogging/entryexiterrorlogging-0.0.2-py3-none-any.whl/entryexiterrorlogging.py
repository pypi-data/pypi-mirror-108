import logging
import json

def entryEventLog(inputDict, loggingKey):
    """
        Input dictionary used for event logging
    """
    loggingDict = {loggingKey:"ENTRY", "status":"SUCCESS", "statusCode":"0000"}
    if inputDict is not None:
        loggingDict.update(inputDict)
    logging.info(json.dumps(loggingDict))

def exitEventLog(inputDict, loggingKey):
    """
        Input dictionary used for exit logging
    """
    loggingDict = {loggingKey:"EXIT", "status":"SUCCESS", "statusCode":"0000"}
    if inputDict is not None:
        loggingDict.update(inputDict)
    logging.info(json.dumps(loggingDict))

def errorEventLog(inputDict, loggingKey):
    """
        Input dictionary used for error logging
    """
    loggingDict = {loggingKey:"ERROR", "status":"FAILURE", "statusCode":"9999"}
    if inputDict is not None:
        loggingDict.update(inputDict)
    logging.info(json.dumps(loggingDict))