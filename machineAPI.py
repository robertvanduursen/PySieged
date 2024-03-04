import xml.etree.cElementTree as ET
from xml.dom import minidom

besiegedFolder = r"D:\ProgramFiles\steamapps\common\Besiege\Besiege_Data\SavedMachines"

import sys
sys.path.append(r'C:\Users\rober\Google Drive\Experiments\project_beseiged')
import blocks as BL
import engine as EN

engine = EN.siegeEngine('newMachine')


engine.add(BL.ThreeBlock(),loc=(10,0,1))
engine.add(BL.ThreeBlock(),loc=(10,5,1))


engine.save(location=besiegedFolder)