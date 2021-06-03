from pseutopy import pseutopy 
from enum import Enum

default_message = "An error occured: Unable to parse the input. Please check that your input is correct."

class ConversionStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

def convert(instructions, language):
    try:
        print(instructions)
        r = pseutopy.PseuToPy(language).convert_from_string(instructions).rstrip()
        if r == default_message:
            return "", ConversionStatus.ERROR, "{}".format(r)
        return r, ConversionStatus.SUCCESS, "Converted successfully!"
    except Exception as e:
        return "", ConversionStatus.ERROR, "{}".format(e)