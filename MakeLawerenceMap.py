""" ***************************************************************************
# * File Description:                                                         *
# * Makes a street map of Lawrence, Kansas where the streets are colored by   *
# * their length.                                                             *
# *                                                                           *
# * The contents of this script are:                                          *
# * 1. Importing Libraries                                                    *
# * 2. Version Check                                                          *
# * 3. Get Data                                                               *
# * 4. Unpack Data                                                            *
# * 5. Assign Each Segment a Color Based on its Length                        *
# * 6. Assign Each Segment a Width Based on its type                          *
# * 7. Make Map                                                               *
# * 8. Helper Functions: Add Border to the Map                                *
# * 9. Adding Border to Map                                                   *
# * 10. Adding Text to Map                                                     *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Frank Ceballos <frank.ceballos89@gmail.com>                   *
# * --------------------------------------------------------------------------*
# * DATE CREATED: September 30, 2019                                          *
# * --------------------------------------------------------------------------*
# * NOTES: None                                                               *
# * ************************************************************************"""


###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D


# To add text and a border to the map
import PIL # You dont really need this import
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw

# Remove if you're working in a Jupyter Notebook
#matplotlib auto

# print ("1. Importing Libraries")
###############################################################################
#                             2. Version Check                                #
###############################################################################
# print(f"The NetworkX package is version {nx.__version__}")
# print(f"The OSMNX package is version {ox.__version__}")
# print(f"The Request package is version {requests.__version__}")
# print(f"The PIL package is version {PIL.__version__}")

# print ("2. Version Check")
###############################################################################
#                                3. Get Data                                  #
###############################################################################
# Define city/cities
clean_name = "Burlington, NC"
places = ["Burlington, North Carolina, USA"]
file_name = "Burlington"
# font_file = "PMINGLIU.ttf"
font_file = "./fonts/brandon-grotesque-cufonfonts/Brandon_reg.otf"

# Get data for places
###
# You can also specify several different network types:
#
#     ‘drive’ – get drivable public streets (but not service roads)
#     ‘drive_service’ – get drivable public streets, including service roads
#     ‘walk’ – get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
#     ‘bike’ – get all streets and paths that cyclists can use
#     ‘all’ – download all (non-private) OSM streets and paths
#     ‘all_private’ – download all OSM streets and paths, including private-access ones
###
# G = ox.graph_from_place(places, network_type="drive_service", simplify = True)
# ox.save_graphml(G, filename=file_name)

G = ox.load_graphml(filename=file_name)

print ("3. Get Data")
###############################################################################
#                               4. Unpack Data                                #
###############################################################################
u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)

# print(u)
# print(v)
# print(key)
# print(data)

print ("4. Unpack Data")
###############################################################################
#                5. Assign Each Segment a Color Based on its Length           #
###############################################################################
# List to store colors
roadColors = []

# The length is in meters
for item in data:
    # if "length" in item.keys():
    #
    #     if item["length"] <= 100:
    #         color = "#d40a47"
    #
    #     elif item["length"] > 100 and item["length"] <= 200:
    #         color = "#e78119"
    #
    #     elif item["length"] > 200 and item["length"] <= 400:
    #         color = "#30bab0"
    #
    #     elif item["length"] > 400 and item["length"] <= 800:
    #         color = "#bbbbbb"
    #
    #     else:
    #         color = "w"

    if "length" in item.keys():

        if item["length"] <= 100:
            color = "#d4af37"

        elif item["length"] > 100 and item["length"] <= 200:
            color = "#d4af37"

        elif item["length"] > 200 and item["length"] <= 400:
            color = "#d4af37"

        elif item["length"] > 400 and item["length"] <= 800:
            color = "#d4af37"

        else:
            color = "#d4af37"
    roadColors.append(color)

print ("5. Assign Each Segment a Color Based on its Length")
###############################################################################
#                6. Assign Each Segment a Width Based on its type             #
###############################################################################
# List to store linewidths
roadWidths = []

for item in data:
    if "footway" in item["highway"]:
        linewidth = 1

    else:
        linewidth = 1

    roadWidths.append(linewidth)

print ("6. Assign Each Segment a Width Based on its type")
###############################################################################
#                               7. Make Map                                   #
###############################################################################
# Center of map
latitude = 35.9105124
longitude =  -82.0811887

#charlotte
#35.2030728,-80.9799136
#Spruce Pine
#35.9105124,-82.0811887

# Bbox sides
#north = latitude + 0.035
#south = latitude - 0.035
#east = longitude + 0.035
#west = longitude - 0.035

# Make Map
fig, ax = ox.plot_graph(G, node_size=0, bbox = None, margin = 0.1,
                        # fig_height=24, fig_width=24,
                        dpi = 300,  bgcolor = "#000000",
                        save = True, edge_color=roadColors,
                        node_edgecolor="#d40a47",
                        edge_linewidth=roadWidths,
                        edge_alpha=1,
                        file_format="png",
                        filename=file_name,
                        show=False,
                        # equal_aspect=True,
                        use_geom=True)

# What needs to happen here is pulling the new image,

# Text and marker size
markersize = 16
fontsize = 16
print("Saved Image")
###################################
# # Add legend
# legend_elements = [Line2D([0], [0], marker='s', color="#061529", label= 'Length < 100 m',
#                           markerfacecolor="#d40a47", markersize=markersize),
#
#                   Line2D([0], [0], marker='s', color="#061529", label= 'Length between 100-200 m',
#                          markerfacecolor="#e78119", markersize=markersize),
#
#                   Line2D([0], [0], marker='s', color="#061529", label= 'Length between 200-400 m',
#                          markerfacecolor="#30bab0", markersize=markersize),
#
#                   Line2D([0], [0], marker='s', color="#061529", label= 'Length between 400-800 m',
#                          markerfacecolor="#bbbbbb", markersize=markersize),
#
#                   Line2D([0], [0], marker='s', color="#061529", label= 'Length > 800 m',
#                   markerfacecolor="w", markersize=markersize)]
#
# l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1,
#               facecolor = '#061529', framealpha = 0.9,
#               loc='lower left',  fontsize = fontsize, prop={'family':"Georgia", 'size':fontsize})
#
# # Legend font color
# for text in l.get_texts():
#     text.set_color("w")
####################################


#This controls Matplotlib not making a low resolution file
# fig.set_size_inches(40, 40)

# Save figure
# fig.savefig("Spruce_Pine.png", dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=True)

# print ("7. Make Map")
###############################################################################
#                    8. Helper Functions: Add Border to the Map               #
###############################################################################
# Get color
def _color(color, mode):
    color = ImageColor.getcolor(color, mode)
    return color

# Expand image
def expand(image, fill = '#e0474c', bottom = 50, left = None, right = None, top = None):
    """
    Expands image

    Parameters
    ----------

    image: The image to expand.
    bottom, left, right, top: Border width, in pixels.
    param fill: Pixel fill value (a color value).  Default is 0 (black).

    return: An image.
    """


    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0

    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out.paste(image, (left, top))
    return out

# Add border
def add_border(input_image, output_image, fill = '#e0474c', bottom = 50, left = None, right = None, top = None):
    """ Adds border to image and saves it.

    Parameters
    ----------


    input_image: str,
        String object for the image you want to load. This is the name of the file you want to read.

    output_image: str,
        String object for the output image name. This is the name of the file you want to export.

    fill: str,
        Hex code for border color. Default is set to reddish.

    bottom, left, right, top: int,
        Integer object specifying the border with in pixels.

    """


    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0

    img = Image.open(input_image)
    bimg = expand(img, bottom = bottom, left = left, right = right, top = top, fill= '#e0474c')
    bimg.save(output_image)

print ("8. Helper Functions: Add Border to the Map")
###############################################################################
#                           9. Adding Border to Map                           #
###############################################################################
# Input image
in_img = './images/' + file_name + ".png"
new_img1 = in_img.split(".pn")[0]+"_b"+".png"
new_img2 = in_img.split(".pn")[0]+"_c"+".png"
new_img3 = in_img.split(".pn")[0]+"_d"+".png"


# Output Image
add_border(in_img, output_image=new_img1, fill = '#c0c0c0', bottom = 400)


print ("9. Adding Border to Map")
###############################################################################
#                           10. Adding Text to Map                            #
###############################################################################
# Open Image
img = Image.open(new_img1)
draw = ImageDraw.Draw(img)

# Get font from working directory. Visit https://www.wfonts.com/search?kwd=pmingliu to download fonts
font = ImageFont.truetype(font_file, 150)

# Add font: position, text, color, font
draw.text((10,10),clean_name, (200,10,10), font=font)

# font = ImageFont.truetype(font_file, 150)
# draw.text((2500,9750),"35.2030728,-80.9799136", (255,255,255), font=font)

# Save image
img.save(new_img2)

print ("10. Adding Text to Map")
