#by gloop #5445
import xml.etree.ElementTree as et
import os,math,colorsys,sys,random

from PIL import Image,ImageOps #pip install pillow
#=====#
blueprint_name = "name"
blueprint_owner_name = "someone"
output_file = "bp.sbc"
image_file = "coco_transparent.png"
use_set_image_path = False
flip_image_vertical = False
flip_image_horizontal = False
use_transparency = True
transparency_threshold = 0.5
grid_size = "Small"
skin = "Weldless"
block_type = "DeadAstronaut"
remove_sbcb5 = True
#=====#
skin_types = [
    "None",
    "Battered_Armor",
    "Weldless",
    "Corrugated",
    "Clean_Armor",
    "CowMooFlage_Armor",
]
def add_tag(element,tag):
    name,attrib,text = tag
    tag = et.SubElement(element,name)
    if attrib:
        tag.attrib = attrib
    if text:
        tag.text = text
    return tag
#==creating blueprint==#
definitions = et.Element("Definitions")
definitions.attrib = {"xmlns:xsd":"http://www.w3.org/2001/XMLSchema", "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}
tree = et.ElementTree(definitions)
ship_blueprints = et.SubElement(definitions,"ShipBlueprints")
blueprint = add_tag(ship_blueprints,["ShipBlueprint",{"xsi:type": "MyObjectBuilder_ShipBlueprintDefinition"},""])
add_tag(blueprint,["Id",{"Type": "MyObjectBuilder_ShipBlueprintDefinition", "Subtype":blueprint_name},""])
ship_cube_grids = et.SubElement(blueprint,"CubeGrids")
cube_grid = et.SubElement(ship_cube_grids,"CubeGrid")

#==setting blueprint position==#
ship_transform = et.SubElement(cube_grid,"PositionAndOrientation")
et.SubElement(ship_transform,"Position").attrib ={"x":"0","y":"0","z":"0"}
et.SubElement(ship_transform,"Forward").attrib ={"x":"0","y":"0","z":"1"}
et.SubElement(ship_transform,"Up").attrib ={"x":"0","y":"1","z":"0"}
orientation = et.SubElement(ship_transform,"Orientation")
et.SubElement(orientation,"X").text = "0"
et.SubElement(orientation,"Y").text = "0"
et.SubElement(orientation,"Z").text = "0"
et.SubElement(orientation,"W").text = "1"

#==setting blueprint info==#
et.SubElement(cube_grid,"GridSizeEnum").text = grid_size
et.SubElement(cube_grid,"DisplayName").text = blueprint_owner_name
cube_blocks = et.SubElement(cube_grid,"CubeBlocks")

def create_block(pos,color,skin=None,type=None):
    if type is None:
        block_type = grid_size+"BlockArmorBlock"
    else:
        block_type = type
    new_block = add_tag(cube_blocks,["MyObjectBuilder_CubeBlock",{"xsi:type":"MyObjectBuilder_CubeBlock"},""])
    add_tag(new_block,["SubtypeName","",block_type])
    add_tag(new_block,["Min",{"x": str(pos[0]),"y": str(pos[1]),"z": str(pos[2])},""])
    color = [i/255 for i in color]
    color = colorsys.rgb_to_hsv(color[0],color[1],color[2])
    color = (color[0],color[1]-0.8,color[2]-0.5)
    color = [str(i) for i in color]
    add_tag(new_block,["ColorMaskHSV",{"x": color[0],"y": color[1],"z": color[2]},""])
    if skin in skin_types:
        add_tag(new_block,["SkinSubtypeId","",skin ])
    return new_block

def set_rotation(block,a,b):
    directions_horizontal = ["Forward","Right","Backward","Left"]
    directions_vertical = ["Up","Forward","Down","Backward"]
    dir = {
    "Forward": directions_horizontal[a%len(directions_horizontal)],
    "Up": directions_vertical[b%len(directions_vertical)]
    }
    add_tag(block,["BlockOrientation",dir,""])

if not use_set_image_path and len(sys.argv)>1:
    image_file = sys.argv[1]

with Image.open(image_file) as im:
    if flip_image_vertical:
        im = ImageOps.flip(im)
    if flip_image_horizontal:
        im = ImageOps.mirror(im)
    w,h = im.size
    px = im.load()

#saturation is offset by -0.8, value by -0.5
#color = (x/w)%1,(x/w)-0.8,(y/h)-0.5
import time
def progress_bar(length,n):
    amount_complete = int(n*length)
    return "#"*amount_complete+("."*(length-(amount_complete)))
for y in range(h):
    if int(y%(h/100))==0:
        print(f"{(y/h)*100:.0f}% Complete.. "+progress_bar(30,y/h),end="\r")
    for x in range(w):
        pixel_color = px[x,y]
        if im.mode == "RGBA":
            if pixel_color[3]>transparency_threshold:
                b =create_block((x,y,0),pixel_color,skin,block_type)
                set_rotation(b,0,0)
        else:
            b = create_block((x,y,0),pixel_color,skin,block_type)
            set_rotation(b,0,0)
et.indent(tree)
tree.write(output_file, encoding = "UTF-8", xml_declaration = True)
if os.path.isfile("bp.sbcB5") and remove_sbcb5:
    os.remove("bp.sbcB5")
