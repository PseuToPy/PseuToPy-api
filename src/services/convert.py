from pseutopy.pseutopy import PseuToPy
import astor

pseutopy = PseuToPy()

class PseutopyParsingException(Exception):
    pass

def convert(instructions, language):
    try:
        python_ast = pseutopy.convert_from_string("\n".join(instructions))
        python_instructions = astor.to_source(python_ast)
        return python_instructions.rstrip('\n').split("\n")
    except Exception as e:
        raise PseutopyParsingException(e)