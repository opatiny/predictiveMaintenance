# append parent directory to path
import os
import sys

fileAbsPath = os.path.abspath(__file__)
fileDir = os.path.dirname(fileAbsPath)
parentDir = os.path.dirname(fileDir)

print("parentDir: ", parentDir)

sys.path.append(parentDir)

from parse.getCurrentSignals import getCurrentSignals


signalNames = getCurrentSignals()

print("Signal names: ", signalNames)
