from importlib.metadata import version
import sys

def get_metadata():
    pythonVersion = "{}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    pseutopyVersion = version('pseutopy')
    pseutopyTargetGrammar = "3.9"
    return (pythonVersion, pseutopyVersion, pseutopyTargetGrammar)