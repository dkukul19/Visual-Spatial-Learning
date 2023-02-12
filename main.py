import os
import random
import time

import Util

batch_of_objects = ['s' for i in range(9)]
random.seed(441)
import Create_Dict
import Create_Affordance_Lists
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.object_manager import ObjectManager
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.output_data import OutputData, Bounds
from tdw.scene_data.scene_bounds import SceneBounds
from tdw.librarian import ModelLibrarian
from tdw.output_data import OutputData, Images,SegmentationColors, IdPassSegmentationColors
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH

object_names = []
object_label_dict = Create_Dict.object_name_label_dict  # (object_labe_dict['034_vray'] = 'camera')
object_file = open("After_Elimination_Object_names.txt", "r")
# labels_file = open("Data_Labels", "a")
RELATIONS = ['IN FRONT OF','BEHIND','ON','UNDER','NEXT TO']
RELATION = 'BEHIND'
list_of_objects = object_file.read().split("\n")
under_objects_list = Create_Affordance_Lists.under_objects_list
on_objects_list = Create_Affordance_Lists.on_objects_list
in_front_of_objects_list = Create_Affordance_Lists.in_front_of_objects_list # use this for behind as well


# create a sequence of elements to be visited on each list
random_iteration = [num for num in range(len(list_of_objects))]
random_iteration_under = [num for num in range(len(under_objects_list))]
random_iteration_on = [num for num in range(len(on_objects_list))]
random_iteration_in_front_of = [num for num in range(len(in_front_of_objects_list))]

print('length of list of objects', len(list_of_objects))
print('length of list of objects UNDER', len(under_objects_list))
print('length of list of objects ON', len(on_objects_list))
print('length of list of objects IN FRONT OF BEHIND', len(in_front_of_objects_list))





random.shuffle(random_iteration)
random.shuffle(random_iteration_under)
random.shuffle(random_iteration_on)
random.shuffle(random_iteration_in_front_of)

random_index = random_iteration[0]  # to iterate over all objects (using list_of_objects)
random_index_under = random_iteration_under[0]
random_index_on = random_iteration_on[0]
random_index_in_front_of = random_iteration_in_front_of[0]
EPOCH_START = 13000
SCENE_AMOUNT = 15000-EPOCH_START
# (6000,6008)
# NOTE: 1000 NEXT TO IMAGES' NAMES SHOULD BE CHANGED (REMOVE THE IMG_ PART FROM THE BEGINNING)
# list_of_objects = list_of_objects[len(list_of_objects)//2:len(list_of_objects)]
#c = Controller(port=1071)
for epoch in range(EPOCH_START, EPOCH_START+SCENE_AMOUNT):


    port_no = 1071+ ((epoch%SCENE_AMOUNT)%2)
    c = Controller(port=port_no)
    print(port_no)


    iteration = epoch

    # Increment the index every 4 epochs
    if epoch % 4 == 0: # this statement is not necessary since there's an integer division below, but it increases readability
    # General Case
        if RELATION != 'IN FRONT OF' and RELATION != 'BEHIND':
            random_index = random_iteration[(epoch//4)%(len(random_iteration)-9)] # -9 is to avoid out of range index on batch of objects.
    # FOR ON/UNDER
        random_index_under = random_iteration_under[(epoch // 4) % len(random_iteration_under)]  # len = 14
    # FOR IN FRONT OF/BEHIND
        random_index_in_front_of = random_iteration_in_front_of[
            (epoch // 4) % len(random_iteration_in_front_of)]  # len = 7

    # For Under/On relationships, the object that is 'under' the other one changes while the object on top stays the same.
    # After all combinations of under objects are exhausted, the under object is changed here
    if epoch % (4 * len(random_iteration_under)) == 0: # aprx. once in 4*14=56 epochs
        random_index_on = random_iteration_on[(epoch // (4 * len(random_iteration_under))) % len(random_iteration_on)]

    # Same logic as above
    print(random_iteration_in_front_of)
    print(len(random_iteration_in_front_of))
    print(random_index)
    print(random_index_in_front_of)
    if (epoch % (4 * len(random_iteration_in_front_of)) == 0) and (RELATION == 'IN FRONT OF' or RELATION == 'BEHIND'): # aprx. once in 4*7=28 epochs
        print('ENTERED THIS LINE')
        random_index = random_iteration[(epoch // (4 * len(random_iteration_in_front_of))) % len(random_iteration)]

    #batch_of_objects = list_of_objects[(random_index):(random_index + 9)]  # [0:9], [1:10]
    # to only get objects that have a face direction
    #face_batch_of_objects = [i for (i, t) in
    #                         Create_Affordance_Lists.has_face_direction[(random_index):(random_index + 9)]]


    # get the name of the object (stored in [0]th index) at a random location of desired list
    under_object = under_objects_list[random_index_under][0]
    on_object = on_objects_list[random_index_on][0]

    looking_object = in_front_of_objects_list[random_index_in_front_of][0]
    looked_object = list_of_objects[random_index] # stopped storing tuples and started storing only the name

    lib = ModelLibrarian(library="models_core.json")


    below_object = "dining_room_table"
    # the scenes are created with the same structure in 'in front of' and 'behind', only the caption of the scene changes.
    if RELATION == 'IN FRONT OF' or RELATION == 'BEHIND':
        o1 = looking_object
        o2 = looked_object
    # the scenes are created with the same structure in 'on' and 'under', only the caption of the scene changes.
    elif RELATION == 'ON' or RELATION == 'UNDER':
        o1 = under_object
        o2 = on_object
    elif RELATION == 'NEXT TO':
        o1 = list_of_objects[random_index]
        o2 = list_of_objects[(random_index+441)%len(list_of_objects)] # maybe use a different but random index


    o1_label = Create_Dict.object_name_label_dict[o1]
    o2_label = Create_Dict.object_name_label_dict[o2]


    relation = RELATION.lower()
    if RELATION == 'IN FRONT OF':
        # looked object in front of looking object
        file_name = "img_" + str(epoch) + '_' + o2_label + '_' + relation + '_' + o1_label
    elif RELATION == 'BEHIND':
        # looked object behind looking object
        file_name = "img_" + str(epoch) + '_' + o2_label + '_' + relation + '_' + o1_label
    elif RELATION == 'ON':
        # on object on under object
        file_name = "img_" + str(epoch) + '_' + o2_label + '_' + relation + '_' + o1_label
    elif RELATION == 'UNDER':
        # under object under on object
        file_name = "img_" + str(epoch) + '_' + o1_label + '_' + relation + '_' + o2_label
    elif RELATION == 'NEXT TO':
        # object1 next to object2
        file_name = "img_" + str(epoch) + '_' + o1_label + '_' + relation + '_' + o2_label

    #file_name = "img_" + str(epoch) + '_' + o2_label + ' ' + relation + ' ' + o1_label

    # first 2 scenes are correct representations, last 2 are incorrect representations
    if epoch % 4 == 0:
        truth_label = '1'
    elif epoch % 4 == 1:
        truth_label = '1'
    elif epoch % 4 == 2:
        truth_label = '0'
    else:
        truth_label = '0'
    # write the label into the file
    with open("Data_Labels", "a") as f:
        if RELATION == 'UNDER' or RELATION == 'NEXT TO':
            f.write(
                "{\"image\":\"" + file_name + ".jpg\",\"image_link\":\"\",\"caption\":\"The " + o1_label + " is " + relation + " the " + o2_label + ".\",\"label\":" + truth_label + ",\"relation\":\"" + relation + "\",\"annotator_id\":0,\"vote_true_validator_id\":[],\"vote_false_validator_id\":[]}")
            f.write("\n")
        # under, in front of, behind
        else:
            f.write(
                "{\"image\":\"" + file_name + ".jpg\",\"image_link\":\"\",\"caption\":\"The " + o2_label + " is " + relation + " the " + o1_label + ".\",\"label\":" + truth_label + ",\"relation\":\"" + relation + "\",\"annotator_id\":0,\"vote_true_validator_id\":[],\"vote_false_validator_id\":[]}")
            f.write("\n")
    """
    Create a scene, add an object, and save the image. 
    """

    REFLECTIONS = True

    table_id = c.get_unique_id()
    print('table id',table_id)
    object_id = c.get_unique_id()
    print('object_id',object_id)
    object_id_1 = c.get_unique_id()
    print('object_id_1',object_id_1)
    object_id_2 = c.get_unique_id()
    object_id_3 = c.get_unique_id()
    object_id_4 = c.get_unique_id()
    object_id_5 = c.get_unique_id()
    object_id_6 = c.get_unique_id()
    object_id_7 = c.get_unique_id()
    object_id_8 = c.get_unique_id()

    object_names = {table_id: "table",
                    object_id: o1_label,
                    object_id_1: o2_label,
                    }

    c.communicate(TDWUtils.create_empty_room(12, 12))
    c.communicate({"$type": "set_screen_size", "width": 1024, "height": 1024})

    om = ObjectManager(transforms=False, bounds=True, rigidbodies=True)
    cam = ThirdPersonCamera(position={"x": 1, "y": 1.7, "z": 0},
                            # x = 2.65 y = 1.65 z = -0.3  x goes forward, z goes right
                            look_at={"x": 0, "y": 0.35, "z": 0},
                            )

    c.add_ons.extend([om, cam])

    c.communicate([c.get_add_object(model_name=below_object,
                                    position={"x": 0, "y": 0, "z": 0},
                                    object_id=table_id),
                   {"$type": "set_screen_space_reflections", "enabled": REFLECTIONS},
                   {"$type": "enable_reflection_probes", "enable": REFLECTIONS},
                   # {"$type": "set_color",
                   # "color": {"r": 0, "g": 0, "b": 0, "a": 0},
                   # "id": table_id}
                   ]
                  )
    print('tableid is it 10187973?', table_id)
    commands = []

    put_obj_1 = True
    put_obj_2 = True
    put_obj_3 = False
    put_obj_4 = False
    put_obj_5 = False
    put_obj_6 = False
    put_obj_7 = False
    put_obj_8 = False
    put_obj_9 = False

    topoftable = float(om.bounds[table_id].top[1])

    top_of_below_object = topoftable + 2  # float(om.bounds[object_id].top[1])

    one = {"x": -0.25, "y": topoftable, "z": -0.33}
    two = {"x": -0.25, "y": topoftable, "z": 0}
    three = {"x": -0.25, "y": topoftable, "z": 0.33}
    four = {"x": 0.1, "y": topoftable, "z": -0.33}
    five = {"x": 0.1, "y": topoftable, "z": 0}
    five_up = {"x": 0.1, "y": topoftable + 2, "z": 0}
    six = {"x": 0.1, "y": topoftable, "z": 0.33}
    seven = {"x": 0.35, "y": topoftable, "z": -0.33}
    seven_up = {"x": 0.35, "y": topoftable + 2, "z": -0.33}
    eight = {"x": 0.35, "y": topoftable, "z": 0}
    nine = {"x": 0.35, "y": topoftable, "z": 0.33}

    on_one = {"x": -0.25, "y": top_of_below_object, "z": -0.33}
    on_two = {"x": -0.25, "y": top_of_below_object, "z": 0}
    on_three = {"x": -0.25, "y": top_of_below_object, "z": 0.33}
    on_four = {"x": 0.1, "y": top_of_below_object, "z": -0.33}
    on_five = {"x": 0.1, "y": top_of_below_object, "z": 0}
    on_six = {"x": 0.1, "y": top_of_below_object, "z": 0.33}
    on_seven = {"x": 0.35, "y": top_of_below_object, "z": -0.33}
    on_eight = {"x": 0.35, "y": top_of_below_object, "z": 0}
    on_nine = {"x": 0.35, "y": top_of_below_object, "z": 0.33}

    positions = [one, two, three, four, five, six, seven, eight, nine]

    # NEXT TO
    next_to_possible_location_pairs = [(one, two), (two, one), (two, three), (three, two), (four, five), (five, four),
                                       (five, six), (six, five), (seven, eight), (eight, seven), (eight, nine),
                                       (nine, eight)]

    next_to_wrong_location_pairs = [(i, j) for i in positions for j in positions if
                                    (i != j) and ((i, j) not in next_to_possible_location_pairs)]
    ############
    # ON / UNDER
    on_under_possible_location_pairs = [(one, on_one), (two, on_two), (three, on_three), (four, on_four),
                                        (five, on_five),
                                        (six, on_six), (seven, on_seven), (eight, on_eight), (nine, on_nine)]

    on_under_wrong_location_pairs = [(i, j) for i in positions for j in positions if (i != j)]
    ##############
    # IN FRONT OF
    in_front_of_possible_location_pairs = [(one, two), (one, four), (two, one), (two, three), (two, five), (three, two),
                                           (three, six),
                                           (four, one), (four, five), (four, seven), (five, two), (five, four),
                                           (five, six), (five, eight),
                                           (six, three), (six, five), (six, nine), (seven, four), (seven, eight),
                                           (eight, five), (eight, seven),
                                           (eight, nine), (nine, six), (nine, eight)]

    in_front_of_wrong_location_pairs = [(i, j) for i in positions for j in positions if ((i != j) and ((i, j) not in in_front_of_possible_location_pairs))]

    if RELATION == 'NEXT TO':
        # select a pair of locations that represents the relationship
        location_pair1 = next_to_possible_location_pairs[random.randint(0, len(next_to_possible_location_pairs)-1)]  # len(list) = 11
        location_pair2 = next_to_possible_location_pairs[random.randint(0, len(next_to_possible_location_pairs)-1)]
        while location_pair2 == location_pair1:
            location_pair2 = next_to_possible_location_pairs[random.randint(0, len(next_to_possible_location_pairs)-1)]

        # select a pair of locations that does not represent the relationship
        wrong_location_pair1 = next_to_wrong_location_pairs[random.randint(0, len(next_to_wrong_location_pairs) - 1)]
        wrong_location_pair2 = next_to_wrong_location_pairs[random.randint(0, len(next_to_wrong_location_pairs) - 1)]
        while wrong_location_pair2 == wrong_location_pair1:
            wrong_location_pair2 = next_to_wrong_location_pairs[
                random.randint(0, len(next_to_wrong_location_pairs) - 1)]
    elif RELATION == 'ON' or RELATION == 'UNDER':
        # select a pair of locations that represents the relationship
        location_pair1 = on_under_possible_location_pairs[random.randint(0, len(on_under_possible_location_pairs) - 1)]
        location_pair2 = on_under_possible_location_pairs[random.randint(0, len(on_under_possible_location_pairs) - 1)]
        while location_pair2 == location_pair1:
            location_pair2 = on_under_possible_location_pairs[random.randint(0, len(on_under_possible_location_pairs) - 1)]

        # select a pair of locations that does not represent the relationship
        wrong_location_pair1 = on_under_wrong_location_pairs[random.randint(0, len(on_under_wrong_location_pairs) - 1)]
        wrong_location_pair2 = on_under_wrong_location_pairs[random.randint(0, len(on_under_wrong_location_pairs) - 1)]
        while wrong_location_pair2 == wrong_location_pair1:
            wrong_location_pair2 = on_under_wrong_location_pairs[random.randint(0, len(on_under_wrong_location_pairs) - 1)]
    elif RELATION == 'IN FRONT OF' or RELATION == 'BEHIND':
        # select a pair of locations that represents the relationship
        location_pair1 = in_front_of_possible_location_pairs[random.randint(0, len(in_front_of_possible_location_pairs) - 1)]  # len(list) = 9
        location_pair2 = in_front_of_possible_location_pairs[random.randint(0, len(in_front_of_possible_location_pairs) - 1)]
        while location_pair2 == location_pair1:
            location_pair2 = in_front_of_possible_location_pairs[random.randint(0, len(in_front_of_possible_location_pairs) - 1)]

        # select a pair of locations that does not represent the relationship
        wrong_location_pair1 = in_front_of_wrong_location_pairs[random.randint(0, len(in_front_of_wrong_location_pairs) - 1)]
        wrong_location_pair2 = in_front_of_wrong_location_pairs[random.randint(0, len(in_front_of_wrong_location_pairs) - 1)]
        while wrong_location_pair2 == wrong_location_pair1:
            wrong_location_pair2 = in_front_of_wrong_location_pairs[random.randint(0, len(in_front_of_wrong_location_pairs) - 1)]

    if epoch % 4 == 0:
        obj1_loc = location_pair1[0]
        obj2_loc = location_pair1[1]
    elif epoch % 4 == 1:
        obj1_loc = location_pair2[0]
        obj2_loc = location_pair2[1]
    elif epoch % 4 == 2:
        obj1_loc = wrong_location_pair1[0]
        obj2_loc = wrong_location_pair1[1]
    else:
        obj1_loc = wrong_location_pair2[0]
        obj2_loc = wrong_location_pair2[1]

    scale_1_int = Create_Affordance_Lists.scales_dict[o1]
    scale_2_int = Create_Affordance_Lists.scales_dict[o2]
    scale_3_int = 1
    scale_4_int = 1
    scale_5_int = 1
    scale_6_int = 1
    scale_7_int = 1
    scale_8_int = 1
    scale_9_int = 1

    scale_1 = {"x": scale_1_int, "y": scale_1_int, "z": scale_1_int}
    scale_2 = {"x": scale_2_int, "y": scale_2_int, "z": scale_2_int}
    scale_3 = {"x": scale_3_int, "y": scale_3_int, "z": scale_3_int}
    scale_4 = {"x": scale_4_int, "y": scale_4_int, "z": scale_4_int}
    scale_5 = {"x": scale_5_int, "y": scale_5_int, "z": scale_5_int}
    scale_6 = {"x": scale_6_int, "y": scale_6_int, "z": scale_6_int}
    scale_7 = {"x": scale_7_int, "y": scale_7_int, "z": scale_7_int}
    scale_8 = {"x": scale_8_int, "y": scale_8_int, "z": scale_8_int}
    scale_9 = {"x": scale_9_int, "y": scale_9_int, "z": scale_9_int}

    rotation_angle_1 = Create_Affordance_Lists.set_rotation(o1)
    rotation_angle_2 = Create_Affordance_Lists.set_rotation(o2)
    rotation_angle_3 = 0
    rotation_angle_4 = 0
    rotation_angle_5 = 0
    rotation_angle_6 = 0
    rotation_angle_7 = 0
    rotation_angle_8 = 0
    rotation_angle_9 = 0

    scales = [scale_1_int,
              scale_2_int,
              scale_3_int,
              scale_4_int,
              scale_5_int,
              scale_6_int,
              scale_7_int,
              scale_8_int,
              scale_9_int,
              ]

    rotations = [rotation_angle_1,
                 rotation_angle_2,
                 rotation_angle_3,
                 rotation_angle_4,
                 rotation_angle_5,
                 rotation_angle_6,
                 rotation_angle_7,
                 rotation_angle_8,
                 rotation_angle_9]
    """
    title1 = "Object Name"
    title2 = "Scale"
    title3 = "Rotation Angle"
    for x in range(40):
        print()
    print(f"          {title1:<40} {title2:<10} {title3:<10}")
    for i in range(len(batch_of_objects)):
        print(f"Object {i + 1}: {batch_of_objects[i]:<40} {scales[i]:<10} {rotations[i]:<10}")
    for x in range(15):
        print()
    """
    # 1

    if put_obj_1:
        c.communicate([
            c.get_add_object(model_name=o1,#batch_of_objects[0],
                             library="models_core.json",
                             position=obj1_loc,  # one,
                             object_id=object_id),
            {"$type": "rotate_object_by", "angle": rotation_angle_1, "id": object_id, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "enable_reflection_probes", "enable": REFLECTIONS},
            {"$type": "scale_object", "id": object_id, "scale_factor": scale_1}])

    c.communicate([{"$type": "send_bounds", "frequency": "always"}])
    #print(float(om.bounds[object_id].top[1]))

    if ((epoch % 4 == 0) or (epoch % 4 == 1)) and (RELATION == 'ON' or RELATION == 'UNDER'):
        obj2_loc['y'] = float(om.bounds[object_id].top[1])
    # 2
    if put_obj_2:
        c.communicate([
            c.get_add_object(model_name=o2,#batch_of_objects[1],
                             library="models_core.json",
                             position=obj2_loc,  # two,
                             object_id=object_id_1),
            {"$type": "rotate_object_by", "angle": rotation_angle_2, "id": object_id_1, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_1, "scale_factor": scale_2}])
    # 3
    if put_obj_3:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[2],
                             library="models_core.json",
                             position=three,
                             object_id=object_id_2),
            {"$type": "rotate_object_by", "angle": rotation_angle_3, "id": object_id_2, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_2, "scale_factor": scale_3}])
    # 4
    if put_obj_4:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[3],
                             library="models_core.json",
                             position=four,
                             object_id=object_id_3),
            {"$type": "rotate_object_by", "angle": rotation_angle_4, "id": object_id_3, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_3, "scale_factor": scale_4}])

    # 5
    if put_obj_5:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[4],
                             library="models_core.json",
                             position=five,
                             object_id=object_id_4),
            {"$type": "rotate_object_by", "angle": rotation_angle_5, "id": object_id_4, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_4, "scale_factor": scale_5},
            {"$type": "enable_reflection_probes", "enable": REFLECTIONS}])
    # 6

    if put_obj_6:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[5],
                             library="models_core.json",
                             position=six,
                             object_id=object_id_5),
            {"$type": "rotate_object_by", "angle": rotation_angle_6, "id": object_id_5, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_5, "scale_factor": scale_6}])
    # 7
    if put_obj_7:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[6],
                             library="models_core.json",
                             position=seven,
                             object_id=object_id_6),
            {"$type": "rotate_object_by", "angle": rotation_angle_7, "id": object_id_6, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_6, "scale_factor": scale_7}])
    # 8
    if put_obj_8:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[7],
                             library="models_core.json",
                             position=eight,
                             object_id=object_id_7),
            {"$type": "rotate_object_by", "angle": rotation_angle_8, "id": object_id_7, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_7, "scale_factor": scale_8}])
    # 9
    if put_obj_9:
        commands.extend([
            c.get_add_object(model_name=batch_of_objects[8],
                             library="models_core.json",
                             position=nine,
                             object_id=object_id_8),
            {"$type": "rotate_object_by", "angle": rotation_angle_9, "id": object_id_8, "axis": "yaw", "is_world": True,
             "use_centroid": False},
            {"$type": "scale_object", "id": object_id_8, "scale_factor": scale_9},
            {"$type": "send_bounds", "ids": [object_id_8], "frequency": "always"}
        ])

    # print(get_front(object_id_8))
    """
    resp = c.communicate(commands)
    
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "boun":
            bounds = Bounds(resp[i])
            for j in range(bounds.get_num()):
                if bounds.get_id(j) == object_id_8:
                    print(object_id, bounds.get_center(j))
                    print("front: ", bounds.get_front(j))
                    print("back: ", bounds.get_back(j))
                    print("left: ", bounds.get_left(j))
                    print("right: ", bounds.get_right(j))
                    print("top: ", bounds.get_top(j))
                    print("bottom: ", bounds.get_bottom(j))
    
    c.communicate({"$type": "terminate"})
    """

    commands.extend(TDWUtils.create_avatar(position={"x": 1, "y": 1.7, "z": 0},
                                           avatar_id="a",
                                           look_at={"x": 0, "y": 0.35, "z": 0}))
    commands.extend([{"$type": "set_pass_masks",
                      "pass_masks": ["_img"],
                      "avatar_id": "a"},
                     {"$type": "send_images",
                      "frequency": "always",
                      "ids": ["a"]},
                     {"$type": "set_img_pass_encoding",
                      "value": "False"}])


    resp = c.communicate(commands)


    if (RELATION == 'IN FRONT OF') and ((epoch % 4 == 0) or (epoch % 4 == 1)):
        c.communicate(
            {"$type": "object_look_at", "other_object_id": object_id_1, "id": object_id})  # ojb1 is looking at obj2

    elif (RELATION == 'IN FRONT OF') and ((epoch % 4 == 2) or (epoch % 4 == 3)):
        c.communicate(
            {"$type": "object_look_at", "other_object_id": object_id_1, "id": object_id})  # ojb1 is looking at obj2
        c.communicate({"$type": "rotate_object_by", "angle": 90*random.randint(1,3), "id": object_id, "axis": "yaw", "is_world": True,
            "use_centroid": False})
    elif (RELATION == 'BEHIND') and ((epoch % 4 == 0) or (epoch % 4 == 1)):
        c.communicate(
            {"$type": "object_look_at", "other_object_id": object_id_1, "id": object_id})  # ojb1 is looking at obj2
        c.communicate({"$type": "rotate_object_by", "angle": 180, "id": object_id, "axis": "yaw",
                       "is_world": True,
                       "use_centroid": False})
    elif (RELATION == 'BEHIND') and ((epoch % 4 == 2) or (epoch % 4 == 3)):
        c.communicate(
            {"$type": "object_look_at", "other_object_id": object_id_1, "id": object_id})  # ojb1 is looking at obj2
        c.communicate({"$type": "rotate_object_by", "angle": 90*random.randint(-1,1), "id": object_id, "axis": "yaw", "is_world": True,
            "use_centroid": False})
    """
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        if r_id == "boun":
            bounds = Bounds(resp[i])
            for j in range(bounds.get_num()):
                if bounds.get_id(j) == object_id_1 or True:
                    print(object_id, bounds.get_center(j))
                    print("front: ", bounds.get_front(j))
                    print("back: ", bounds.get_back(j))
                    print("left: ", bounds.get_left(j))
                    print("right: ", bounds.get_right(j))
                    print("top: ", bounds.get_top(j))
                    print("bottom: ", bounds.get_bottom(j))
    """
    time_steps = 2
    if RELATION == 'NEXT TO':
        time_steps = 100
    for i in range(time_steps):
        # bottom_objects_top_point = float(om.bounds[object_id].top[1])
        # top_objects_bottom_point = float(om.bounds[object_id_1].bottom[1])
        # if top_objects_bottom_point > bottom_objects_top_point:
        resp = c.communicate([])
    output_directory = str(EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("send_images").resolve())#"/Users/doga/PycharmProjects/ThreeDWorld/Saved_images/Scenes"
    print(f"Images will be saved to: {output_directory}")
    cap = ImageCapture(path=output_directory, avatar_ids=["a"], pass_masks=["_id"])
    c.add_ons.append(cap)
    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        # Get Images output data.
        if r_id == "imag":
            images = Images(resp[i])
            # Determine which avatar captured the image.
            if images.get_avatar_id() == "a":
                # Iterate through each capture pass.
                for j in range(images.get_num_passes()):
                    # This is the _img pass.
                    if images.get_pass_mask(j) == "_img":
                        image_arr = images.get_image(j)
                        # Get a PIL image.
                        pil_image = TDWUtils.get_pil_image(images=images, index=j)
                # Save the image.
                TDWUtils.save_images(images=images, filename=file_name[4:], output_directory=output_directory)


    commands.extend([{"$type": "set_pass_masks",
                      "avatar_id": "a",
                      "pass_masks": ["_id"]},
                     {"$type": "send_segmentation_colors",
                      "frequency": "once"},
                     {"$type": "send_id_pass_segmentation_colors",
                      "frequency": "always"}])


    resp = c.communicate(commands)
    # Get each segmentation color.
    segmentation_colors_per_object = dict()
    segmentation_colors_in_image = list()

    for i in range(len(resp) - 1):
        r_id = OutputData.get_data_type_id(resp[i])
        # Get segmentation color output data.
        if r_id == "segm":
            segm = SegmentationColors(resp[i])
            for j in range(segm.get_num()):
                object_id_temp = segm.get_object_id(j)
                object_name = object_names[object_id_temp]
                segmentation_color = segm.get_object_color(j)
                segmentation_colors_per_object[object_id_temp] = segmentation_color
        elif r_id == "ipsc":
            ipsc = IdPassSegmentationColors(resp[i])
            for j in range(ipsc.get_num_segmentation_colors()):
                segmentation_colors_in_image.append(ipsc.get_segmentation_color(j))


    c.communicate({"$type": "terminate"})

    Util.change_file_name((output_directory + "/a/id_0000.png"), (file_name[4:] + "_segmentation.png"))

    s = segmentation_colors_per_object
    print(segmentation_colors_per_object)
    print(segmentation_colors_per_object[table_id],object_names[table_id],table_id)
    print(segmentation_colors_per_object[object_id],object_names[object_id],object_id)
    print(segmentation_colors_per_object[object_id_1],object_names[object_id_1],object_id_1)# dict -> id: color [r,g,b]
    l1 = str(s[table_id][0]) +" " + str(s[table_id][1]) +" " + str(s[table_id][2]) +" " + str(object_names[table_id]) +" " + str(table_id)
    l2 = str(s[object_id][0]) +" " + str(s[object_id][1]) +" " + str(s[object_id][2]) +" " + str(object_names[object_id]) +" " + str(object_id)
    l3 = str(s[object_id_1][0]) +" " + str(s[object_id_1][1]) +" " + str(s[object_id_1][2]) +" " + str(object_names[object_id_1]) +" " + str(object_id_1)
    l4 = (file_name[4:] + "_segmentation.png")
    RGB_label_id = [l1,l2,l3,l4]
    Util.write_to_file(RGB_label_id,"segmentation_info")

    import ExtractBoundingBoxes
    ExtractBoundingBoxes.extract_bounding_box_and_save()



""" #This part is only for saving the image.

commands.extend(TDWUtils.create_avatar(position={"x": 1, "y": 1.7, "z": 0},
                                       avatar_id="a",
                                       look_at={"x": 0, "y": 0.35, "z": 0}))
commands.extend([{"$type": "set_pass_masks",
                  "pass_masks": ["_img"],
                  "avatar_id": "a"},
                 {"$type": "send_images",
                  "frequency": "always",
                  "ids": ["a"]}])

resp = c.communicate(commands)
output_directory = str(EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("send_images").resolve())
print(f"Images will be saved to: {output_directory}")

for i in range(len(resp) - 1):
    r_id = OutputData.get_data_type_id(resp[i])
    # Get Images output data.
    if r_id == "imag":
        images = Images(resp[i])
        # Determine which avatar captured the image.
        if images.get_avatar_id() == "a":
            # Iterate throught each capture pass.
            for j in range(images.get_num_passes()):
                # This is the _img pass.
                if images.get_pass_mask(j) == "_img":
                    image_arr = images.get_image(j)
                    # Get a PIL image.
                    pil_image = TDWUtils.get_pil_image(images=images, index=j)
            # Save the image.
            TDWUtils.save_images(images=images, filename="0", output_directory=output_directory)
c.communicate({"$type": "terminate"})
"""
