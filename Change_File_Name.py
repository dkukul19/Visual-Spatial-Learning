import os

def change_file_name(file_path, new_name):
    # Split the file path into its directory and file name parts
    head, tail = os.path.split(file_path)
    # Join the directory and the new file name to form the new file path
    new_file_path = os.path.join(head, new_name)
    # Rename the file
    os.rename(file_path, new_file_path)

#change_file_name(("/Users/doga/tdw_example_controller_output/send_images/a/id_0000.png"),("_segmentation"))