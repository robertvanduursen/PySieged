import sys,os,re
import xml.etree.cElementTree as ET
from xml.dom import minidom

import blocks as BL
import fileFormat as FF


class siegeEngine(ET.Element):
	"""
	<?xml version="1.0" encoding="utf-8"?>
	<!--Besiege machine save file.-->
	<Machine version="1" bsgVersion="1.3" name="7_part">
	    <!--The machine's position and rotation.-->
	    <Global>
	        <Position x="0" y="6" z="0" />
	        <Rotation x="0" y="0" z="0" w="1" />
	    </Global>
	    <!--The machine's additional data or modded data.-->
	    <Data />
	    <!--The machine's blocks.-->
	    <Blocks>
	        <Block id="0" guid="069de941-7538-4b92-9157-a9c6540203ee">
	            <Transform>
	                <Position x="0" y="0" z="0" />
	                <Rotation x="0" y="0" z="0" w="1" />
	                <Scale x="1" y="1" z="1" />
	            </Transform>
	            <Settings>
	                <Skin name="default" id="default" />
	            </Settings>
	            <Data />
	        </Block>
	     </Blocks>
	</Machine>
	"""

	ID = False
	transform = False
	settings = False
	data = False

	def __init__(self,name):
		print('%s engine made' % name)
		super().__init__('Machine')
		self.name = name
		self.attrib = {'version': "1", 'bsgVersion': "1.3", 'name': name}

		Machine = self
		Machine.append(ET.Comment("Besiege machine save file"))

		Machine.append(ET.Comment("The machine's position and rotation."))
		Global = ET.SubElement(Machine, 'Global')
		pos = ET.SubElement(Global, 'Position', attrib={'x': 0, 'y': 0, 'z': 0})
		rot = ET.SubElement(Global, 'Rotation', attrib={'x': 0, 'y': 0, 'z': 0, 'w': 1})

		Machine.append(ET.Comment("The machine's additional data or modded data."))
		Data = ET.SubElement(Machine, 'Data')

		Machine.append(ET.Comment("The machine's blocks."))
		Blocks = ET.Element('Blocks')
		Machine.append(Blocks)

		block = BL.Block()
		block.set('id', 0)
		Blocks.append(block)

		self.Blocks = Blocks

	def add(self, block, loc):
		pos = block.find('Transform').find('Position')
		for idx,attr in enumerate(['x', 'y', 'z']): pos.attrib[attr] = loc[idx]

		self.Blocks.append(block)


	def setBlockID(self):
		pass

	def setTransform(self):
		pass

	def setSettings(self):
		pass

	def setData(self):
		pass

	def save(self, location=False):
		tree = ET.ElementTree(self)
		for x in tree.iter():
			# print(type(x.attrib))
			for name, val in x.attrib.items():
				if type(val) != type(str):
					# print(val)
					x.attrib[name] = str(x.attrib[name])
				# print(val)

		# tree.write('test.bsg',xml_declaration=1)
		dom = minidom.parseString(ET.tostring(self))
		# "utf-8"

		# version="1" bsgVersion="1.3" name="tester">
		pretty = dom.toprettyxml(indent='\t')
		with open(os.path.join(location, self.name + '.bsg'), 'w') as FH:
			FH.write(pretty)
		print(pretty)
# dom.saveXML()

baseBlock = BL.Block()
