import gaf_construct as g
import importlib
from construct import *

def reimport():
    importlib.reload(g)


gaf_path = "CHANGE_ME"
gaf_contents = open(gaf_path, 'rb').read()

print("GAF File:")
print(g.gaf_file.parse(gaf_contents))
print("data_pos from test: 32")
