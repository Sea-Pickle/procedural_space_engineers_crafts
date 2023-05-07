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

#==creating blueprint==#
definitions = et.Element("Definitions")
definitions.attrib = {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"}
tree = et.ElementTree(definitions)
ship_blueprints = et.SubElement(definitions,"ShipBlueprints")
blueprint = et.SubElement(ship_blueprints,"ShipBlueprint")
blueprint.attrib = {"xsi:type": "MyObjectBuilder_ShipBlueprintDefinition"}
et.SubElement(blueprint,"Id").attrib = {"Type": "MyObjectBuilder_ShipBlueprintDefinition", "Subtype": blueprint_name}
ship_cube_grids = et.SubElement(blueprint,"CubeGrids")
cube_grid = et.SubElement(ship_cube_grids,"CubeGrid")

#==setting blueprint position==#
ship_transform = et.SubElement(cube_grid,"PositionAndOrientation")
et.SubElement(ship_transform,"Position").attrib ={"x":"0","y":"0","z":"0"}
orientation = et.SubElement(ship_transform,"Orientation")
et.SubElement(orientation,"X").text = "0"
et.SubElement(orientation,"Y").text = "0"
et.SubElement(orientation,"Z").text = "0"
et.SubElement(orientation,"W").text = "1"

#==setting blueprint info==#
et.SubElement(cube_grid,"GridSizeEnum").text = grid_size
et.SubElement(cube_grid,"DisplayName").text = blueprint_owner_name
cube_blocks = et.SubElement(cube_grid,"CubeBlocks")

def create_block(pos,color,skin):
    block_type = grid_size+"BlockArmorBlock"
    new_block = et.SubElement(cube_blocks,"MyObjectBuilder_CubeBlock")
    new_block.attrib = {"xsi:type":"MyObjectBuilder_CubeBlock"}
    subtype = et.SubElement(new_block,"SubtypeName")
    subtype.text = block_type
    block_position = et.SubElement(new_block,"Min")
    block_position.attrib = {"x": str(pos[0]),"y": str(pos[1]),"z": str(pos[2])}
    block_color = et.SubElement(new_block,"ColorMaskHSV")
    color = [i/255 for i in color]
    color = colorsys.rgb_to_hsv(color[0],color[1],color[2])
    color = (color[0],color[1]-0.8,color[2]-0.5)
    color = [str(i) for i in color]
    block_color.attrib = {"x": color[0],"y": color[1],"z": color[2]}
    block_skin = et.SubElement(new_block,"SkinSubtypeId")
    block_skin.text = skin if skin in skin_types else "None"

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
                create_block((x,y,0),pixel_color,skin)
        else:
            create_block((x,y,0),pixel_color,skin)

et.indent(tree)
tree.write(output_file, encoding = "UTF-8", xml_declaration = True)
if os.path.isfile("bp.sbcB5") and remove_sbcb5:
    os.remove("bp.sbcB5")