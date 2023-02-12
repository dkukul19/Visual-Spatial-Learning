import PIL
from PIL import ImageFilter, ImageChops
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import Util

# this code will run once segmentation_info is updated while main is running.
##################### TO DO ######################
#   save file_name to segmentation_info (DONE)
#   read file_name and save necessary information (bounding boxes image, bound values, corresponding id, etc.) to it
#
def extract_bounding_box_and_save():
    segmentation_info = Util.read_file_to_list('segmentation_info')


    table_red,table_green,table_blue,table_name,table_id = segmentation_info[0]
    o1_red,o1_green,o1_blue,o1_name,o1_id = segmentation_info[1]
    o2_red,o2_green,o2_blue,o2_name,o2_id = segmentation_info[2]
    filename = segmentation_info[3][0]
    table_color = (int(table_red),int(table_green),int(table_blue))
    o1_color = (int(o1_red),int(o1_green),int(o1_blue))
    o2_color = (int(o2_red),int(o2_green),int(o2_blue))
    color_to_name_dict = {(0,0,0):'background',table_color:table_name,o1_color:o1_name,o2_color:o2_name}
    color_to_id_dict = {(0,0,0):None,table_color:table_id,o1_color:o1_id,o2_color:o2_id}
    print(filename)
    DATA_PATH_NEW = '/Users/doga/tdw_example_controller_output/send_images/a/'+filename
    img1 = Image.open(DATA_PATH_NEW)
    pix = img1.load()
    width,height = img1.size
    colors_pixels_dictionary = {(0,0,0):[],table_color:[],o1_color:[],o2_color:[]}

    pixels = []
    for w in range(width):
        for h in range(height):
            coordinates = (w,h)
            pixel = img1.getpixel((w,h))
            colors_pixels_dictionary[pixel].append(coordinates)

            pixels.append(pixel)

    min_x, max_x, min_y, max_y = Util.extract_bounds(colors_pixels_dictionary[o1_color])
    Util.draw_bounds(pix,height,width,min_x, max_x, min_y, max_y,(255,255,255))
    min_x, max_x, min_y, max_y = Util.extract_bounds(colors_pixels_dictionary[o2_color])
    Util.draw_bounds(pix,height,width,min_x, max_x, min_y, max_y,(255,255,255))
    min_x, max_x, min_y, max_y = Util.extract_bounds(colors_pixels_dictionary[table_color])
    Util.draw_bounds(pix,height,width,min_x, max_x, min_y, max_y,(255,255,255))


    img1.save('/Users/doga/tdw_example_controller_output/send_images/BoundingBoxImages/'+'BB'+str(filename),'PNG')

