import sys, os, re
import xml.etree.cElementTree as ET
import uuid
from xml.dom import minidom
import inspect

# os.startfile('D:\ProgramFiles\steamapps\common\Besiege\Besiege_Data\SavedMachines')

class requires(object):
    """ Requirement: if this is not met, it will not happen """

    def __init__(self, needs):
        self.req = needs

    def __call__(self, f):
        def wrapperFunc(*args):
            if self.req in globals().keys():
                return f(*args)
            else:
                print('%s requires %s' % (f.__qualName__, self.req))
                return False

        return wrapperFunc


"""
class driving:
    @safe(needs='seatbelt')
    def enjoy(self):
        return True

    def relax(self):
        return True
"""


# --------------- Attributable properties ------------- #


controllable = True  # -> can be affected by keypresses
customizable = True  # -> key mapping can be changed
# todo: are there blocks with data that can be controlled, but not customized? if so, split the attrs; if not, merge!

linkable = True
detach = True
dynamic = True  # can move / change
volume = []  # X, Y, Z -> width, height, depth
length = True # can be inferred from volume
rotation = True
friction = True
active = True
passive = True
static = True  # """ has no actions == cannot act """
variableLength = True  # -> start and end
faceAttached = True

class Block(ET.Element):
    """
    <Block id="28" guid="135edfe0-cc96-4216-adf1-a7ad2ea43e84">
        <Transform>
            <Position x="-0.5" y="0" z="0" />
            <Rotation x="-0.7071068" y="3.090862E-08" z="0.7071068" w="-3.090862E-08" />
            <Scale x="1" y="1" z="1" />
        </Transform>
        <Settings>
            <Skin Name="default" id="default" />
        </Settings>
        <Data>
            <StringArray key="bmt-left">UpArrow</StringArray>
            <StringArray key="bmt-right">DownArrow</StringArray>
            <Single key="bmt-rotation-speed">1</Single>
            <Boolean key="bmt-uselimits">True</Boolean>
            <SingleArray key="bmt-limits">
                <Single>40</Single>
                <Single>40</Single>
            </SingleArray>
            <Boolean key="flipped">False</Boolean>
        </Data>
    </Block>
    """

    ID = False
    guid = False
    transform = False
    settings = False
    data = False

    props = False


    def __init__(self, name='Block'):
        super().__init__(name)
        print('%s made',name)

        self.set('guid', uuid.uuid4())
        Global = ET.SubElement(self, 'Transform')
        ET.SubElement(Global, 'Position', attrib={'x': 0, 'y': 0, 'z': 0})
        ET.SubElement(Global, 'Rotation', attrib={'x': 0, 'y': 0, 'z': 0, 'w': 1})
        ET.SubElement(Global, 'Scale', attrib={'x': 1, 'y': 1, 'z': 1})

        Settings = ET.SubElement(self, 'Settings')
        ET.SubElement(Settings, 'Skin', attrib={'Name': 'default', 'id': 'default'})

        ET.SubElement(self, 'Data')


    # StringArray = ET.SubElement(Data, 'Skin', attrib={'Name': 'default', 'id': 'default'})

    def setBlockID(self,id):
        self.set('id', id)

    def setGuid(self):
        pass

    def setTransform(self):
        pass

    def setSettings(self):
        pass

    def setData(self):
        pass

    def setLength(self, length):
        self.length = length

    def printXML(self):
        tree = ET.ElementTree(self)
        for x in tree.iter():
            # print(type(x.attrib))
            for name, val in x.attrib.items():
                if type(val) != type(str):
                    x.attrib[name] = str(x.attrib[name])

        dom = minidom.parseString(ET.tostring(self))

        # version="1" bsgVersion="1.3" name="tester">
        pretty = dom.toprettyxml(indent='\t')
        print(pretty)


# --------------- Declaration of the different blocks ------------- #


class Base(Block):
    id = 0
    props = static,
    length = 1

    def __init__(self):
        super(Base, self).__init__()


class TwoBlock(Block):
    id = 1
    props = static,
    length = 2

    def __init__(self):
        # poles
        super().__init__()


class MotorWheel(Block):
    id = 2
    props = rotation, controllable
    '''
    it has a radius and a pivot
    
    '''

    def __init__(self):
        super().__init__()


class Name3(Block):
    id = 3

    def __init__(self):
        super(Name3, self).__init__()


class Decoupler(Block):
    id = 4
    props = [detach]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
                <Data>
                    <StringArray key="bmt-explode">J</StringArray>
                </Data>

        """


class Hinge(Block):
    """ loose coupling; allows free rotation on its axis """
    id = 5
    props = [static, dynamic]

    def __init__(self):
        super().__init__()


class Name6(Block):
    id = 6

    def __init__(self):
        super().__init__()


class Brace(Block):
    id = 7
    props = [variableLength]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="7" guid="de4e590a-0c78-4619-a31c-909fdade0935">
            <Transform>
                <Position x="0" y="0.5" z="0" />
                <Rotation x="-0.7071068" y="0" z="0" w="0.7071068" />
                <Scale x="1" y="1" z="1" />
            </Transform>
            <Data>
                <Vector3 key="start-position">
                    <X>0</X>
                    <Y>0</Y>
                    <Z>0</Z>
                </Vector3>
                <Vector3 key="end-position">
                    <X>-3</X>
                    <Y>2.384187E-07</Y>
                    <Z>2.842171E-14</Z>
                </Vector3>
                <Vector3 key="start-rotation">
                    <X>270</X>
                    <Y>0</Y>
                    <Z>0</Z>
                </Vector3>
                <Vector3 key="end-rotation">
                    <X>270</X>
                    <Y>-6.830188E-06</Y>
                    <Z>0</Z>
                </Vector3>
            </Data>
        </Block>
        """


class Name8(Block):
    id = 8

    def __init__(self):
        super().__init__()


class Spring(Block):
    id = 9
    props = [variableLength]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="9" guid="85d39ce5-ccb4-475a-bf76-490e7c922098">
                <Transform>
                    <Position x="0" y="0.5" z="0" />
                    <Rotation x="-0.7071068" y="0" z="0" w="0.7071068" />
                    <Scale x="1" y="1" z="1" />
                </Transform>
                <Data>
                    <StringArray key="bmt-contract">L</StringArray>
                    <Boolean key="bmt-toggle">False</Boolean>
                    <Single key="bmt-slider">1</Single>
                    <Vector3 key="start-position">
                        <X>0</X>
                        <Y>0</Y>
                        <Z>0</Z>
                    </Vector3>
                    <Vector3 key="end-position">
                        <X>0</X>
                        <Y>-0.5000001</Y>
                        <Z>-0.5000001</Z>
                    </Vector3>
                    <Vector3 key="start-rotation">
                        <X>270</X>
                        <Y>0</Y>
                        <Z>0</Z>
                    </Vector3>
                    <Vector3 key="end-rotation">
                        <X>0</X>
                        <Y>0</Y>
                        <Z>0</Z>
                    </Vector3>
                </Data>
            </Block>
        """


class Woodenpanel(Block):
    id = 10
    props = [static, faceAttached]
    volume = [1, 2, 1]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
            <Block id="10" guid="45e0a114-efa8-4092-a8f5-13126f3d4d7c">
                <Transform>
                    <Position x="-0.5" y="0" z="0" />
                    <Rotation x="0" y="-0.7071068" z="0" w="0.7071068" />
                    <Scale x="1" y="1" z="1" />
                </Transform>
                <Data />
            </Block>
        """


class Name11(Block):
    id = 11

    def __init__(self):
        super().__init__()


class Name12(Block):
    id = 12

    def __init__(self):
        super().__init__()


class Steering(Block):
    id = 13
    props = [customizable, controllable]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="13" guid="5c8e570e-72a4-481f-b76e-d70914d4ca73">
            <Transform>
                <Position x="0.5" y="0" z="0" />
                <Rotation x="0" y="0.7071068" z="0" w="0.7071068" />
                <Scale x="1" y="1" z="1" />
            </Transform>
            <Data>
                <StringArray key="bmt-left">LeftArrow</StringArray>
                <StringArray key="bmt-right">RightArrow</StringArray>
                <Boolean key="bmt-autoReturn">False</Boolean>
                <Single key="bmt-rotation-speed">1</Single>
                <Boolean key="flipped">False</Boolean>
            </Data>
        </Block>
        """

class Name14(Block):
    id = 14

    def __init__(self):
        super().__init__()


class OneBlock(Block):
    id = 15
    props = [length]
    length = 1
    def __init__(self):
        super().__init__()


class Suspension(Block):
    id = 16
    props = [dynamic, passive]
    def __init__(self):
        super().__init__()


class Name17(Block):
    id = 17

    def __init__(self):
        super().__init__()


class Piston(Block):
    id = 18
    props = [dynamic, controllable]
    def __init__(self):
        super().__init__()


class Swivel(Block):
    """ motorized Coupling """
    id = 19

    def __init__(self):
        super().__init__()


class Name20(Block):
    id = 20

    def __init__(self):
        super().__init__()


class Name21(Block):
    id = 21

    def __init__(self):
        super().__init__()


class Spinningblock(Block):
    id = 22

    def __init__(self):
        super().__init__()

    # def rotation(self): pass


class Name23(Block):
    id = 23

    def __init__(self):
        super().__init__()


class Name24(Block):
    id = 24

    def __init__(self):
        super().__init__()


class Name25(Block):
    id = 25

    def __init__(self):
        super().__init__()


class Name26(Block):
    id = 26

    def __init__(self):
        super().__init__()


class Grabber(Block):
    id = 27

    def __init__(self):
        super().__init__()

    """
     <Block id="27" guid="498b778b-e4b0-49d4-8eb5-45a0ddbd096c">
            <Transform>
                <Position x="0" y="0" z="0.5" />
                <Rotation x="0" y="0" z="0" w="1" />
                <Scale x="1" y="1" z="1" />
            </Transform>
            <Data>
                <StringArray key="bmt-detach">V</StringArray>
                <Boolean key="bmt-grab-static">False</Boolean>
                <Boolean key="bmt-grab-static-only">False</Boolean>
                <Boolean key="bmt-auto-grab">True</Boolean>
            </Data>
        </Block>
    """


class Steeringhinge(Block):
    id = 28

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="28" guid="498d4360-af3d-48ce-9cc1-0e386a3db719">
            <Transform>
                <Position x="-0.5" y="0" z="0" />
                <Rotation x="0" y="-0.7071068" z="0" w="0.7071068" />
                <Scale x="1" y="1" z="1" />
            </Transform>
            <Data>
                <StringArray key="bmt-left">LeftArrow</StringArray>
                <StringArray key="bmt-right">RightArrow</StringArray>
                <Boolean key="bmt-autoReturn">False</Boolean>
                <Single key="bmt-rotation-speed">1</Single>
                <Boolean key="bmt-uselimits">True</Boolean>
                <SingleArray key="bmt-limits">
                    <Single>40</Single>
                    <Single>40</Single>
                </SingleArray>
                <Boolean key="flipped">False</Boolean>
            </Data>
        </Block>

        """


class Name29(Block):
    id = 29

    def __init__(self):
        super().__init__()


class Name30(Block):
    id = 30

    def __init__(self):
        super().__init__()


class Name31(Block):
    id = 31

    def __init__(self):
        super().__init__()


class Name32(Block):
    id = 32

    def __init__(self):
        super().__init__()


class Name33(Block):
    id = 33

    def __init__(self):
        super().__init__()


class Name34(Block):
    id = 34

    def __init__(self):
        super().__init__()


class Name35(Block):
    id = 35

    def __init__(self):
        super().__init__()


class Name36(Block):
    id = 36

    def __init__(self):
        super().__init__()


class Name37(Block):
    id = 37

    def __init__(self):
        super().__init__()


class Unpoweredmediumcog(Block):
    id = 38
    props = [passive, dynamic]
    volume = [1, 2, 2]


    def __init__(self):
        super().__init__()


class PoweredMediumcog(Block):
    id = 39
    props = [active, dynamic]
    volume = [1, 2, 2]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="39" guid="7857b14d-caf9-4d55-9099-83dfa6a5ed71">
            <Data>
                <Boolean key="bmt-automatic">False</Boolean>
                <Boolean key="bmt-toggle-mode">False</Boolean>
                <Boolean key="bmt-auto-brake">True</Boolean>
                <StringArray key="bmt-forward">UpArrow</StringArray>
                <StringArray key="bmt-backward">DownArrow</StringArray>
                <Single key="bmt-speed">1</Single>
                <Single key="bmt-acceleration">Infinity</Single>
                <Boolean key="flipped">True</Boolean>
            </Data>
        </Block>
        """


class Unpoweredwheelsmall(Block):
    id = 40
    props = [rotation, dynamic, passive]
    volume = [1, 1, 1]
    radius = 10.0  # ?


    def __init__(self):
        super().__init__()


class Stick(Block):
    id = 41

    def __init__(self):
        super().__init__()


class Slider(Block):
    """ passive suspension - chaos like """
    id = 42

    def __init__(self):
        super().__init__()


class Name43(Block):
    id = 43

    def __init__(self):
        super().__init__()


class Balljoint(Block):
    """ 3 DOF hinge """
    id = 44

    def __init__(self):
        super().__init__()


class Ropeandwinch(Block):
    id = 45
    props = [active, dynamic]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
        <Block id="45" guid="c982bb0b-4214-4eac-98af-e6c17f82d248">
                <Transform>
                    <Position x="0" y="0.5" z="0" />
                    <Rotation x="-0.7071068" y="0" z="0" w="0.7071068" />
                    <Scale x="1" y="1" z="1" />
                </Transform>
                <Data>
                    <StringArray key="bmt-contract">N</StringArray>
                    <StringArray key="bmt-unwind">M</StringArray>
                    <Boolean key="bmt-start-unwound">False</Boolean>
                    <Single key="bmt-slider">1</Single>
                    <Vector3 key="start-position">
                        <X>0</X>
                        <Y>0</Y>
                        <Z>0</Z>
                    </Vector3>
                    <Vector3 key="end-position">
                        <X>0</X>
                        <Y>0.5000002</Y>
                        <Z>-0.5</Z>
                    </Vector3>
                    <Vector3 key="start-rotation">
                        <X>270</X>
                        <Y>0</Y>
                        <Z>0</Z>
                    </Vector3>
                    <Vector3 key="end-rotation">
                        <X>0</X>
                        <Y>180</Y>
                        <Z>0</Z>
                    </Vector3>
                </Data>
            </Block>
        """


class LargePoweredWheel(Block):
    id = 46
    props = [rotation]
    volume = [1, 3, 3]


    def __init__(self):
        super().__init__()

    """
            <Block id="46" guid="f1753ad0-fdf8-4100-a7a0-4c81dc9921fd">
            <Transform>
                <Position x="0.5" y="0" z="0" />
                <Rotation x="0" y="0.7071068" z="0" w="0.7071068" />
                <Scale x="1" y="1" z="1" />
            </Transform>
            <Data>
                <Boolean key="bmt-automatic">False</Boolean>
                <Boolean key="bmt-toggle-mode">False</Boolean>
                <Boolean key="bmt-auto-brake">True</Boolean>
                <StringArray key="bmt-forward">UpArrow</StringArray>
                <StringArray key="bmt-backward">DownArrow</StringArray>
                <Single key="bmt-speed">1</Single>
                <Single key="bmt-acceleration">Infinity</Single>
                <Boolean key="flipped">False</Boolean>
            </Data>
        </Block>
    """


class Name47(Block):
    id = 47

    def __init__(self):
        super().__init__()


class Name48(Block):
    id = 48

    def __init__(self):
        super().__init__()


class Grippad(Block):
    id = 49
    props = [friction, faceAttached]

    def __init__(self):
        super().__init__()

    def setData(self):
        """
               <Block id="49" guid="bef82663-00b8-46e0-8560-00b2774e3c7b">
                <Transform>
                    <Position x="0" y="0" z="-0.5" />
                    <Rotation x="0" y="1" z="0" w="0" />
                    <Scale x="1" y="1" z="1" />
                </Transform>
                <Data />
            </Block>
        """


class Smallwheel(Block):
    props = [rotation, passive]
    volume = [1, 1, 1]

    id = 50

    def __init__(self):
        super().__init__()


class LargeUnpoweredCog(Block):
    id = 51
    props = [rotation, passive, linkable]
    volume = [1, 4, 4]

    def __init__(self):
        super().__init__()


class Name52(Block):
    id = 52

    def __init__(self):
        super().__init__()


class Name53(Block):
    id = 53

    def __init__(self):
        super().__init__()


class Name54(Block):
    id = 54

    def __init__(self):
        super().__init__()


class Name55(Block):
    id = 55

    def __init__(self):
        super().__init__()


class Name56(Block):
    id = 56

    def __init__(self):
        super().__init__()


class Pin(Block):
    id = 57

    def __init__(self):
        super().__init__()


class Camera(Block):
    id = 58

    def __init__(self):
        super().__init__()


class Name59(Block):
    id = 59

    def __init__(self):
        super().__init__()


class LargeUnpoweredWheel(Block):
    id = 60
    props = [rotation, passive]
    volume = [3, 3, 3]

    def __init__(self):
        super().__init__()


class Name61(Block):
    id = 61

    def __init__(self):
        super().__init__()


class Name62(Block):
    id = 62

    def __init__(self):
        super().__init__()


class ThreeBlock(Block):
    id = 63
    props = [static]
    volume = [1, 3, 1]

    def __init__(self):
        # poles
        super().__init__(self.__class__.__name__)
        self.setBlockID(self.id)
        self.setData()

    def setData(self):
        """
        <Data>
            <Integer key="length">2</Integer>
        </Data>

        """
        data = self.find('Data')
        lol = ET.SubElement(data, 'Integer', attrib={'key': 'length'})
        lol.text = str(2)



def printBlockList():
    print('blockIDs = {')
    for k, v in list(globals().items()):
        # print('%s : %s,' % (v, k))
        if hasattr(v, '__mro__'):
            if Block == inspect.getmro(v)[1]:
                print('%s : %s,' % (v.id, k))
    print('}')


def aggregateBlockProperties():
    allProperties = []
    for k, v in list(globals().items()):
        if hasattr(v, '__mro__'):
            if Block == inspect.getmro(v)[1]:
                properties = list(filter(lambda x:not x.startswith('_'), v.__dict__.keys()))
                #print('%s : %s,' % (k, properties))
                allProperties += properties

    for prop in sorted(set(allProperties) - {'id'}):
        print(prop)


aggregateBlockProperties()


class Goal:
    """ none """
    _name = False
    _implication = []

    def __repr__(self):
        if self._name:
            return '%s as Goal' % self._name
        else:
            return '%s as Goal' % self.name

    def __init__(self):
        pass

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            for k, v in globals().items():
                if v == self: return k

    @property
    def implication(self):
        return self._implication

    @implication.setter
    def implication(self, input):
        print(input)
        self._implication = input


def compute_goalsmatch():
    """ trying to match Goals with Means (things = blocks) """

    goals = {}
    for k, v in list(globals().items()):
        if isinstance(v, Goal):
            goals[str(k).lower()] = []

    for goal in goals:
        for k, v in list(globals().items()):
            if 'class' in str(v):
                # print(v,v.__dict__)
                options = [(option, v.__dict__[option]) for option in v.__dict__.keys() if option == goal]
                if any(options):
                    test = v()
                    realityCheck = [opt for opt, checksOut in options if checksOut and checksOut(test)]
                    print(v.__Name__, '= an option for having', realityCheck)
                    goals[goal].append(v.__Name__)

    print()
    for goal in goals:
        if not goals[goal]:
            print('cant', goal, ': nothing provides it')
        else:
            print('%s allows to %s' % (', '.join(goals[goal]), goal))


"""

I need a machine that can do X, Y & Z

"""

GettingOverThere = Goal()
GettingOverThere.implication = ['movement', 'starting']
ControllingMovement = Goal()
ControllingMovement.implication = ['input', 'keys', 'direction']

#compute_goalsmatch()


'''
27 / 07 / 19
we are now at the point of being able to express:
    a block with unique properties -> set by adjective
    the set of 63 blocks currently in-game
    simple goals 
    demands from the implications of those goals
    the ability to write out an Engine to test with
    
todo
    the building of an Engine that will achieve the goals
    the test loop


'''


def makeTheDamnMachine():
    def whatMustItDo(): # ?
        pass


    def whatAreTheConstants():
        # what must it do in all situations?
        pass

def testIt():
    def whatAreItsAxis(): # ?
        pass

def rateIt():
    def howDoesItCompare():
        pass

    def whatShouldBeChanged():
        pass

    def shouldWeTryAnotherApproach():
        pass