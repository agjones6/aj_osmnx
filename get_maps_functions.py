""" ***************************************************************************
# * File Description:                                                         *
# * Organizes the functions for making maps based on the original file of     *
# * 'MakeLawerenceMap.py'                                                     *
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
# * 10. Adding Text to Map                                                    *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Andy Jones     <andyjones4774@gmail.com>                      *
# *   ORIGINAL: Frank Ceballos <frank.ceballos89@gmail.com>                   *
# * --------------------------------------------------------------------------*
# * DATE CREATED: January 27, 2020                                            *
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
import os


# To add text and a border to the map
import PIL # You dont really need this import
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw

def check_folder(folder):
    # Checking if the folder is there, if it isn't, the folder is created
    check_val = os.path.isdir(folder)
    if not check_val:
        os.mkdir(folder)

    return check_val


###############################################################################
#                            Creating a Class                                 #
###############################################################################
class img:
    def __init__(self, location_name,**kwargs):

        # ---> Initializing the user inputs
        # The actual location to be pulled using OSMnx
            # NOTE: This should be "CITY, STATE, COUNTRY"
        self.loc_name = location_name

        # Getting the cleaner name to be written on the image
        loc_list = self.loc_name.split(",")
        try:
            self.city    = loc_list[0]
            self.state   = loc_list[1]
            self.country = loc_list[2]
            # Here there could be checks to ensure all of these are valid
        except Exception as e:
            print("The 'CITY, STATE, COUNTRY' format did not import correctly")
            self.city    = ""
            self.state   = ""
            self.country = ""
            return

        # ---> Initializing optional arguments
        # Font to be used
        self.font_file = kwargs.get("font_file",
                         "./fonts/brandon-grotesque-cufonfonts/Brandon_reg.otf")

        # File Name of the saved image
        self.obj_name = kwargs.get("obj_name",self.city)

        # Image location
        self.dest_folder = kwargs.get("dest_folder","./images")
        check_folder(self.dest_folder) # Makes a new folder if the destination isn't there

        # Image Extension
        self.img_ext = kwargs.get("img_ext","png")

        # General Folder of the source data
        self.source_data_loc = kwargs.get("src_data_loc","./data")

        # General Picture name to be used for the first bare image
        self.base_img_name = kwargs.get("base_img_name","base")

        # ---> Establishing final Variable Values
        # Full file path for the final image
        self.dest_fold_path = os.path.join(self.dest_folder,self.obj_name)
        check_folder(self.dest_fold_path)

        # Checking to see if the desired data has already been imported and is in
        #   the data source location ('source_data_loc')
        if self.check_file():
            # Pulling data from pre-existing data file
            self.raw_data = ox.load_graphml(filename=self.obj_name,
                                            folder=self.source_data_loc)
        else:
            try:
                # Pulling data from the server
                self.raw_data = ox.graph_from_place(self.loc_name,
                                                    network_type="drive_service",
                                                    simplify = True)
                # Saving the data as a file
                ox.save_graphml(self.raw_data,
                                filename=self.obj_name,
                                folder=self.source_data_loc)

            except Exception as e:
                print("Error with pulling and saving data on --> ", self.obj_name)
                print("\n", e, "\n")
                return

        ########################################################################
        #                           4. Unpack Data                             #
        ########################################################################
        self.u = []
        self.v = []
        self.key = []
        self.data = []
        for uu, vv, kkey, ddata in self.raw_data.edges(keys=True, data=True):
            self.u.append(uu)
            self.v.append(vv)
            self.key.append(kkey)
            self.data.append(ddata)

        #######################################################################
        #            5. Assign Each Segment a Color Based on its Length       #
        #######################################################################
        # List to store colors
        self.road_colors = []

        # The length is in meters
        for item in self.data:
            if "length" in item.keys():
                if item["length"] <= 100:
                    color = "#d40a47"
                    # color = "#d4af37"
                elif item["length"] > 100 and item["length"] <= 200:
                    color = "#e78119"
                    # color = "#d4af37"
                elif item["length"] > 200 and item["length"] <= 400:
                    color = "#30bab0"
                    # color = "#d4af37"
                elif item["length"] > 400 and item["length"] <= 800:
                    color = "#bbbbbb"
                    # color = "#d4af37"
                else:
                    color = "w"
                    # color = "#d4af37"

            self.road_colors.append(color)


        #######################################################################
        #            6. Assign Each Segment a Width Based on its type         #
        #######################################################################
        # List to store linewidths
        self.road_widths = []

        for item in self.data:
            if "footway" in item["highway"]:
                linewidth = 1

            else:
                linewidth = 1

            self.road_widths.append(linewidth)


        #######################################################################
        #                           7. Make Map                               #
        #######################################################################
        # Make Base Map
        self.base_img_fig, ax = ox.plot_graph(self.raw_data,
                                              node_size=0,
                                              bbox = None,
                                              margin = 0.1,
                                              # fig_height=24, fig_width=24,
                                              dpi = 300,
                                              bgcolor = "#000000",
                                              save = True,
                                              edge_color=self.road_colors,
                                              node_edgecolor="#d40a47",
                                              edge_linewidth=self.road_widths,
                                              edge_alpha=1,
                                              filename=os.path.join(self.obj_name,self.base_img_name),
                                              file_format=self.img_ext,
                                              show=False,
                                              # equal_aspect=True,
                                              use_geom=True)

    # ============================== FUNCTIONS =================================
    def check_file(self):
        self.data_file_path = os.path.join(self.source_data_loc,self.obj_name)
        check_val = os.path.isfile(self.data_file_path)

        return check_val


test = img("Burlington, North Carolina, NC")
