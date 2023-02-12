import matplotlib.pyplot as plt
obj_dict = {}
def increment_object_count(obj, relation, dic = obj_dict):
    if (obj,relation) in dic:
        dic[(obj,relation)] += 1
    else:
        dic[(obj,relation)] = 1




hist = []


with open("Data_Labels", "r") as f:
    for line in f:
        # Split the line on the space character
        #line_split = line.strip().split(' ')
        relation_index = line.find('relation') + len('relation":"')
        relation_end_index = line.find('"',relation_index)
        relation = line[relation_index:relation_end_index]
        caption_index = line.find('caption')
        first_the_index = line.find('The',caption_index)
        is_index = line.find(' is',first_the_index)
        first_object = line[first_the_index+len('The '):is_index]
        second_the_index = line.find('the', is_index)
        period_index = line.find('.',second_the_index)
        second_object = line[second_the_index+len('the '):period_index]
        #increment_object_count(first_object,relation)
        increment_object_count(second_object,relation)
        #hist.append((first_object,relation))
        #hist.append((second_object,relation))
on_list = []
under_list = []
in_front_of_list = []
behind_list = []
next_to_list = []

for key in obj_dict:
    #print(key[0],key[1],obj_dict[key])
    if key[1] == 'on':
        on_list.append((key[0],obj_dict[key]))
    if key[1] == 'next to':
        next_to_list.append((key[0],obj_dict[key]))
    if key[1] == 'under':
        under_list.append((key[0],obj_dict[key]))
    if key[1] == 'in front of':
        in_front_of_list.append((key[0],obj_dict[key]))
    if key[1] == 'behind':
        behind_list.append((key[0],obj_dict[key]))

x = []
y = []
for item in next_to_list:
    x.append(item[0])
    y.append(item[1])


plt.rcParams.update({'font.size': 4})
plt.figure(dpi=400)
plt.barh(x,y)
plt.title('Object/Occurrence for Object B in A Next to B Relation')
plt.ylabel('Object Name')
plt.xlabel('Occurrence')
for i, v in enumerate(y):
    plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
plt.savefig('Object B in A Next to B Relation.png',dpi=400)

plt.show()

