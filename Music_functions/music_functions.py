import csv
import pandas as pd
from Music_functions.music_functions2 import mp3_names

#! Convert unstructured tracklists to pandas dataframe
def lofi_convert(data1, letter):
    lines = data1.split('\n')
    nicer_data = []
    letter_count = 1
    
    for i in range(len(lines) - 1):
        current_line = lines[i]
        next_line = lines[i + 1]
        
        time_end_index = current_line.find(']')
        time = current_line[1:time_end_index]
        next_time_end_index = next_line.find(']')
        next_time = next_line[1:next_time_end_index]
        
        try:
            time_seconds = int(time[:2]) * 60 + int(time[3:])
            next_time_seconds = int(next_time[:2]) * 60 + int(next_time[3:])
        except ValueError:
            print("BEN!! Make sure this in correct format", '\n')
            return ""
        
        if current_line.lower().startswith("intro"):
            continue
        
        artists_end_index = current_line.find('- ')
        artists = current_line[time_end_index+2:artists_end_index - 1].split(' x ')
        song_name = current_line[artists_end_index + 2:]
        
        duration_seconds = next_time_seconds - time_seconds
        
        if len(artists) == 1:
            nicer_data.append([duration_seconds, artists[0], "", "", song_name])
        elif len(artists) == 2:
            nicer_data.append([duration_seconds, artists[0], artists[1], "", song_name])
        elif len(artists) == 3:  # Handling three artists
            nicer_data.append([duration_seconds, artists[0], artists[1], artists[2], song_name])
        
        nicer_data = [song for song in nicer_data if song[4] != 'Intro']  # Removing 'Intro' songs
    
    # Adding entries with the specified letter and a number in ascending order
    for idx, song in enumerate(nicer_data):
        song.append(f"{letter}{idx + 1}")
    
    return nicer_data

#? Private repository contains different functions like this for 3 other youtube channels (containing tracklists in different format)

#! Write to CSV file function
def write_to_csv(nicer_data, filename):
    headers = ['song_length', 'artist_1', 'artist_2', 'artist_3', 'song_name', 'file_name']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(nicer_data)

#! Append to CSV file function
def append_to_csv(some_data, filename2):
    with open(filename2, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(some_data)    

#! Creating a new simplified diff ready with a unique Tracklist    
def playlist_maker(dataframe, num_songs):
    if dataframe.empty or num_songs > len(dataframe):
        print("DataFrame is empty or has fewer songs than requested")
        return None
    
    playlist_df = dataframe.sample(n=num_songs)    
    playlist_df['vid_time_seconds'] = playlist_df['song_length'].cumsum()
    playlist_df['vid_time_seconds'] = playlist_df['vid_time_seconds'].shift(fill_value=0)
    
    def format_time(seconds):
        if seconds >= 3600:  # If video is longer than 1 hour
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            return '[{:02d}:{:02d}:{:02d}]'.format(hours, minutes, seconds)
        else:  # For videos less than 1 hour
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return '[{:02d}:{:02d}]'.format(minutes, seconds)
    
    playlist_df['vid_time'] = playlist_df['vid_time_seconds'].apply(format_time)
    playlist_df = playlist_df.drop(columns='vid_time_seconds')
    
    return playlist_df

#! Writing unique df in Tracklist form as a string
def dataframe_to_string(df):
    lines = ["Tracklist 🎶"]
    file_names_list = []
    for index, row in df.iterrows():
        vid_time = row['vid_time']
        artist_1 = row['artist_1']
        artist_2 = row['artist_2']
        artist_3 = row['artist_3']
        song_name = row['song_name']
        file_name_id = row['file_name']

        file_names_list.append(file_name_id)

        
        if pd.isnull(artist_2) and pd.isnull(artist_3):
            track_line = f"{vid_time} {artist_1} - {song_name}"
        elif pd.isnull(artist_3):
            track_line = f"{vid_time} {artist_1} x {artist_2} - {song_name}"
        else:
            track_line = f"{vid_time} {artist_1} x {artist_2} x {artist_3} - {song_name}"
        
        lines.append(track_line)
    
    track_string = "\n".join(lines)
    file_names_line = ", ".join(file_names_list)
    mp3_string = mp3_names(file_names_line)

    
    # Add a blank line before the file names line
    track_string += "\n\n" + file_names_line + '\n\n' + mp3_string
    
    return track_string

#! Write new vid to text file function
def write_to_text(epic_string, filename2):
    with open(filename2, 'w') as file:
        file.write(epic_string)

#! Remove duplicates in CSV file function
def remove_duplicates(dataframe, column_name):
    unique_df = dataframe.drop_duplicates(subset = column_name)
    return unique_df