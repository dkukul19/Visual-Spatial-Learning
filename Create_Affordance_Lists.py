#other_behind_in_front_of_this = []
import random

affordance_dict = {}
with open("Augmentation.txt", "r") as f:
    for line in f:
        # Split the line on the space character
        line_split = line.strip().split('\t')
        #print(line_split)
        affordance_dict[line_split[0]] = (line_split[1],line_split[2],line_split[3],line_split[4],line_split[5])

def create_relation_list(dict_of_affordance,relation_position_index):
    pass


print(affordance_dict['banana_fix2'])
# has_face_direction is a list of tuples of (obj_name,facing_direction)
has_face_direction = []
has_face_direction_dict = {}
for key in affordance_dict:
    if int(affordance_dict[key][1]) != 0:
        has_face_direction.append((key,affordance_dict[key][1]))
        has_face_direction_dict[key] = affordance_dict[key][1]
#print(len(has_face_direction))



long_direction = []
long_direction_dict = {}
for key in affordance_dict:
    if int(affordance_dict[key][0]) != 0:
        long_direction.append((key,affordance_dict[key][0]))
        long_direction_dict[key] = affordance_dict[key][0]


under_objects_list = []
under_objects_dict = {}
on_objects_list = []
on_objects_dict = {}
for key in affordance_dict:
    if affordance_dict[key][2] == 'u':
        under_objects_list.append((key,affordance_dict[key][2]))
        under_objects_dict[key] = affordance_dict[key][2]
    elif affordance_dict[key][2] == 'o':
        on_objects_list.append((key,affordance_dict[key][2]))
        on_objects_dict[key] = affordance_dict[key][2]

print(under_objects_list[2][0])


# sets the rotation of an object to be vertical or horizontal
def set_rotation(obj_name,vertical = True):
    if obj_name not in affordance_dict:
        return
    if int(affordance_dict[obj_name][0]) < 3: # 1 or 2 -- both vertical
        if vertical:
            return 0
        else:
            return 90
    elif int(affordance_dict[obj_name][0]) < 5: # 3 or 4 -- both horizontal
        if vertical:
            return 90
        else:
            return 0
    else: # 5 means every direction
        return 0

scales_dict = {}
for key in affordance_dict:
    scales_dict[key] = affordance_dict[key][4]



in_front_of_objects_list = []
in_front_of_objects_dict = {}
for key in affordance_dict:
    if int(affordance_dict[key][3]) != 0:
        in_front_of_objects_list.append((key,affordance_dict[key][3]))
        in_front_of_objects_dict[key] = affordance_dict[key][3]

print(in_front_of_objects_list)

