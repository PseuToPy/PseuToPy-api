from pseutopy.pseutopy import PseuToPy
import astor
from enum import Enum

pseutopy = PseuToPy()

class ConversionStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

def convert(instructions, language):
    try:
        python_ast = pseutopy.convert_from_string("\n".join(instructions))
        python_instructions = astor.to_source(python_ast).rstrip('\n').split("\n")
        return python_instructions, ConversionStatus.SUCCESS, "Converted successfully!"
    except Exception as e:
        return [], ConversionStatus.ERROR, "{}".format(e)