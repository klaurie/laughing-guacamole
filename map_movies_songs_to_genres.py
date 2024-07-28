import csv

def load_subgenre_mapping(csv_file_path):
    subgenre_to_genre = {}
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            genre, subgenre = row
            subgenre_to_genre[subgenre] = genre
    return subgenre_to_genre

def map_subgenres_to_genres(input_csv_path, output_csv_path, subgenre_mapping):
    with open(input_csv_path, mode='r', encoding='utf-8-sig') as infile, \
         open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)  # Read the header row
        header.append('song_genre')  # Add a new column for the main genre
        writer.writerow(header)
        
        for row in reader:
            song_subgenres = row[2]  # The subgenres are in the third column
            if song_subgenres:
                subgenres = song_subgenres.split(', ')
                genres = {subgenre_mapping.get(subgenre, '') for subgenre in subgenres}
                row.append(', '.join(genres))
            else:
                row.append('')
            writer.writerow(row)

def main():
    # Paths to the input CSV files
    subgenres_csv_path = 'csv_files/genres.csv'
    movies_songs_csv_path = 'csv_files/movies_songs_subgenres.csv'
    output_csv_path = 'csv_files/movies_songs_genres.csv'
    
    # Load the subgenre to genre mapping
    subgenre_mapping = load_subgenre_mapping(subgenres_csv_path)
    
    # Map subgenres to genres and write the output to a new CSV file
    map_subgenres_to_genres(movies_songs_csv_path, output_csv_path, subgenre_mapping)

# Call the main function
if __name__ == "__main__":
    main()
