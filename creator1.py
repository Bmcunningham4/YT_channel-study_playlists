import pandas as pd
from music_functions import lofi_convert, write_to_csv, append_to_csv, remove_duplicates
from music_data import song1, song2, song3

#! Creating the CSV file
nicer_data1 = lofi_convert(song1, "ga")
write_to_csv(nicer_data1, "lofi.csv")

#! Appending 
nicer_data2 = lofi_convert(song2, "gb")
append_to_csv(nicer_data2, "lofi.csv")

nicer_data3 = lofi_convert(song3, "gc")
append_to_csv(nicer_data3, "lofi.csv")

#? Done for 12+ additional songs in each genre ...



#! Removing Duplicates and rewriting back to CSV
music_df = pd.read_csv("lofi.csv")
unique_df = remove_duplicates(music_df, "song_name")
unique_df.to_csv("lofi.csv", index=False)


#! Tweaking Song lengths (Post video making)
lofi_dict = {"ga1": 182, "gb12": 221, "gc7": -8, "gc11": -4} #* Change song length either alters length or submits new length
for name, change_value in lofi_dict.items():
    if change_value < 0:
        unique_df.loc[unique_df.file_name == name, 'song_length'] += change_value
    else:
        unique_df.loc[unique_df.file_name == name, 'song_length'] = change_value

remove_list = ["ga3", "gb1"] #* Remove if song has copyright warning on youtube 
unique_df = unique_df[~unique_df.file_name.isin(remove_list)]

unique_df.to_csv("lofi.csv", index=False)
