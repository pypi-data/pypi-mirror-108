import sys
del sys.modules["%s"%(__name__)]
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
print(os.path.abspath(os.path.dirname(__file__)))
sys.modules["%s"%(__name__)] = __import__('samna')
