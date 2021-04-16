from os.path import join, exists, dirname, normpath
import json

parent_path = dirname(__file__)
translation_path = "../translations/{}/grammar.json"

class MalformedJsonException(Exception):
    pass

def get_grammar(language):
    file_path = normpath(join(parent_path, translation_path.format(language)))
    if(exists(file_path)):
        file = open(file_path, 'r', encoding="utf8")
        file_txt = file.read()
        try:
            return json.loads(file_txt)
        except ValueError as err:
            raise MalformedJsonException("JSON file {} is malformed: {}".format(file_path, err))
        finally:
            file.close()
    else:
        raise FileNotFoundError("Unable to find grammar for language {} at location {}".format(language, file_path))