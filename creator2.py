import pandas as pd 
from music_functions import dataframe_to_string, write_to_text, playlist_maker, string_to_list, big_list, list_to_dict, simplify_df

#? Vid Tracklists
vid_g1 = "gb21, gb17, gc18, ga6, gb8, gc8, gc7, gc14, ga16, gc2, ga27, gb23, gc24, ga1, gc10, ga19, gb26, gb14, gb12, ga11" # Devil wears Prada - work vid
vid_g2 = "gb24, gc1, gb15, gb25, gb9, ga24, ga15, gc21, gb12, gc7, gb22, gb14, ga2, gb16, gb2, gc14, ga26, gb4, ga6, ga18"

#? String Conversions and Dictionary making
str_g1 = string_to_list(vid_g1)
str_g2 = string_to_list(vid_g2)

big_g1 = big_list(str_g1, str_g2) #* Keep appending here
dict_lofi = list_to_dict(big_g1) 

#? Updating df with new vid_count column
lofi_df = pd.read_csv("lofi.csv")
lofi_df['vid_count'] = pd.to_numeric(lofi_df['file_name'].map(dict_lofi), downcast='integer', errors='coerce').fillna(0)
lofi_df.to_csv("lofi.csv", index=False)

#!: Vid maker & Text file creator
special_df = simplify_df(lofi_df, "vid_count", max_value=3)
playlist_df = playlist_maker(special_df, 20) #todo: Select num songs here
new_vid = dataframe_to_string(playlist_df)
write_to_text(new_vid, "lofi.txt")