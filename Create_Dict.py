import random
dict = {}
with open("Object_names_dict.txt", "r") as f:
    for line in f:
        # Split the line on the space character
        line_split = line.strip().split(' ')
        #print(line_split)
        k = line_split[0]
        #print(k)
        last_comma_index = 0
        for word_index in range(len(line_split)):
            if ',' in line_split[word_index]: #find the last comma word
                last_comma_index = word_index

            if word_index == len(line_split)-1 and last_comma_index != 0: # for the ones which have comma in them
                values_list = line_split[last_comma_index+1:]
                val = ''
                for w in values_list:
                    if len(val)>1:
                        val += ' '+w
                    else:
                        val += w
                dict[k] = val
                #print(val)
            elif word_index == len(line_split)-1: #last word, no comma
                #print(line_split[1:])
                val = ''
                values_list = line_split[1:]
                for w in values_list:
                    if len(val)>1:
                        val += ' '+w
                    else:
                        val += w
                #print(val)
                dict[k] = val



print(len(dict.keys()))
object_name_label_dict = dict

one = 1
two = 2
three = 3
four = 4
five = 5
six = 6
seven = 7
eight = 8
nine = 9


positions = [one, two, three, four, five, six, seven, eight, nine]

next_to_possible_location_pairs = [(one, two), (two, one), (two, three), (three, two), (four, five), (five, four),
                                   (five, six), (six, five), (seven, eight), (eight, seven), (eight, nine),
                                   (nine, eight)]

next_to_wrong_location_pairs = [(i, j) for i in positions for j in positions if
                                (i != j) and ((i, j) not in next_to_possible_location_pairs)]
