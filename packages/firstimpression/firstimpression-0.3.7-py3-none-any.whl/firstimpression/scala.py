import warnings
import win32com.client
import sys
import os
import inspect
import tempfile

current_python_version = None

PYTHON2 = "Python2"
PYTHON3 = "Python3"
PYTHON3_MAIN = "Python3_Main"

TEMPFOLDER = tempfile.gettempdir()

try:
    import scalalib
    import scalatools

    current_python_version = PYTHON2

    warnings.warn("Python 2 is deprecated", DeprecationWarning)

except ImportError:
    try:
        import scalascript

        current_python_version = PYTHON3

    except ImportError:

        current_python_version = PYTHON3_MAIN


def get_scala_frame():
    for frame in inspect.stack():
        if "Script Block" in frame[1]:
            raise Exception("Yes")
            return frame[0]
    return None


def variables():
    if current_python_version == PYTHON2:
        svars = get_scala_frame().f_globals
        fh = open(os.path.join(TEMPFOLDER, "test.txt"), "w")
        text = "{}".format(svars)
        fh.write(text)
        fh.close()

    elif current_python_version == PYTHON3:
        return scalascript.variables()
    elif current_python_version == PYTHON3_MAIN:
        warnings.warn(
            "Cannot grab variables from scala when running in Python 3 from main", RuntimeWarning)
        return None
    else:
        raise RuntimeError("Wrong Python version used")


def install_content(abspath, subfolder=None, autostart=True):
    if current_python_version == PYTHON2:
        if not subfolder:
            subfolder = ''
        scalalib.install_content(abspath, subfolder, autostart)
    elif current_python_version == PYTHON3:
        scalascript.install_content(abspath, subfolder)
    elif current_python_version == PYTHON3_MAIN:
        warnings.warn(
            "Cannot install content in Python 3 when running from main", RuntimeWarning)
    else:
        raise RuntimeError("Wrong Python version used")
