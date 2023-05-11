#by gloop #5445
import xml.etree.ElementTree as et
import os,math,colorsys,sys,random
import vox_file_reader

#=====#
blueprint_name = "name"
blueprint_owner_name = "someone"
output_file = "bp.sbc"
use_set_file_path = False

grid_size = "Small"
skin = "Weldless"
remove_sbcb5 = True
use_set_file_path = False
source_file = "chr_knight.vox"
#=====#
if not use_set_file_path:
    if len(sys.argv)>1:
        source_file = sys.argv[1]
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
et.SubElement(blueprint,"Id").attrib = {"Type": "MyObjectBuilder_ShipBlueprintDefinition", "Subtype": blueprint_name}
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

def color_from_trig(h,offset=(math.pi/4)):
    n = h * math.pi
    r = int(255*abs(math.sin(n-offset)))
    g = int(255*abs(math.sin(n)))
    b = int(255*abs(math.sin(n+offset)))
    return (r,g,b)

def progress_bar(length,n):
    amount_complete = int(n*length)
    return "#"*amount_complete+("."*(length-(amount_complete)))
vox_data = vox_file_reader.voxels_from_file(source_file)
voxels = vox_data[0]
palette = vox_data[1]
r_x,r_y,r_z = vox_data[2]
for idx,v in enumerate(voxels):
    if int(idx%(len(voxels)/100))==0:
        print(f"{(idx/(len(voxels)/100)):.0f}% Complete",progress_bar(10,idx/len(voxels)),end="\r")
    x,y,z,palette_index = v
    r,g,b,a = palette[(palette_index-1)%(len(palette))]
    block_color = (r,g,b)
    create_block((x,y,z),block_color,skin)

et.indent(tree)
tree.write(output_file, encoding = "UTF-8", xml_declaration = True)
if os.path.isfile("bp.sbcB5") and remove_sbcb5:
    os.remove("bp.sbcB5")