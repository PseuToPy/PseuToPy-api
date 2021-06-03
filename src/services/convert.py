from pseutopy import pseutopy 
from enum import Enum

class ConversionStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

def convert(instructions, language):
    try:
        print(instructions)
        r = pseutopy.PseuToPy(language).convert_from_string(instructions)
        if r == "An error occured: Unable to parse the input. Please check that your input is correct.":
            return "", ConversionStatus.ERROR, "{}".format(e)
        return r, ConversionStatus.SUCCESS, "Converted successfully!"
    except Exception as e:
        return "", ConversionStatus.ERROR, "{}".format(e)