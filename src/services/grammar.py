import os
import json

dirname = os.path.dirname(__file__)
translation_path = "../translations/{}/grammar.json"

class MalformedJsonException(Exception):
    pass

def get_grammar(language):
    file_path = os.path.join(dirname, translation_path.format(language))

    if(os.path.exists(file_path)):
        file = open(file_path, 'r', encoding="utf8")
        file_txt = file.read()
        try:
            return json.loads(file_txt)
        except ValueError as err:
            raise MalformedJsonException(err)
        finally:
            file.close()
    else:
        raise FileNotFoundError("Unable to find grammar for language {} at location {}".format(language, file_path))