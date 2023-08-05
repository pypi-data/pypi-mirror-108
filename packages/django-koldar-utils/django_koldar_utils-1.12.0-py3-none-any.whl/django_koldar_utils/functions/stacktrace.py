import os
import re
import traceback

def filter_django_stack():

    def filter_pycharm(line: traceback.FrameSummary) -> bool:
        return "JetBrains" not in os.path.split(line.filename)

    def filter_python(line: traceback.FrameSummary) -> bool:
        for s in os.path.split(line.filename):
            if s.startswith("Python"):
                return False
        else:
            return True

    def filter_venv(line: traceback.FrameSummary) -> bool:
        for s in os.path.split(line.filename):
            if s.startswith("site-packages"):
                return False
        else:
            return True

    return list(filter(filter_venv,
        filter(filter_python,
                  filter(filter_pycharm, list(traceback.extract_stack())[:-2]
    ))))