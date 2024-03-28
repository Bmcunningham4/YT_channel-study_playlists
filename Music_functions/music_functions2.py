
#! Functions to count filenames (songs) - to ensure songs aren't overused 
def string_to_list(input_string):
    elements = input_string.split(', ')
    return elements

def big_list(total_list, *args): # Slay that *args shit goat..
    for arg in args:
        for item in arg:
            total_list.append(item)
    return total_list

def list_to_dict(input_list):
    result_dict = {}
    for element in input_list:
        if element in result_dict:
            result_dict[element] += 1
        else:
            result_dict[element] = 1
    return result_dict

#! Simplified df - Based off vid count!!
def simplify_df(df, column_name, max_value):
    simplified_df = df[df[column_name] <= max_value].copy()
    return simplified_df


#! Function so the below function works (Creates mp3 filenames to transfer mp3 files on pc easily)
def mp3_names(stringy):
    list_1 = string_to_list(stringy)
    new_list = []
    for string in list_1:
        new_string = string + ".mp3"
        new_list.append(new_string)
    final_string = ' '.join(new_list)
    return final_string
