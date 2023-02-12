import os

def change_file_name(file_path, new_name):
    # Split the file path into its directory and file name parts
    head, tail = os.path.split(file_path)
    # Join the directory and the new file name to form the new file path
    new_file_path = os.path.join(head, new_name)
    # Rename the file
    os.rename(file_path, new_file_path)


def write_to_file(strings, file_name):
    with open(file_name, 'w') as file:
        for string in strings:
            file.write(string + '\n')

def read_file_to_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip().split() for line in file]

def extract_bounds(list_of_coordinates):

    x_values = [x for x, y in list_of_coordinates]
    y_values = [y for x, y in list_of_coordinates]

    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    return min_x, max_x, min_y, max_y

def draw_bounds(pix,height,width,min_x, max_x, min_y, max_y,color=(0,255,0)):
    for y in range(height):
        for x in range(width):
            if x >= min_x and x <= max_x and (y == min_y or y == max_y):
                pix[x, y] = color
            if y >= min_y and y <= max_y and (x == min_x or x == max_x):
                pix[x, y] = color
