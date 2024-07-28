import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('csv_files/movies_songs_genres.csv', names=['name', 'song_name', 'song_subgenre', 'song_genre'], header=0)

# Drop rows where either 'song_subgenre' or 'song_genre' is empty
df = df.dropna(subset=['song_subgenre', 'song_genre'])
df = df[df['song_subgenre'].str.strip().astype(bool) & df['song_genre'].str.strip().astype(bool)]

# Clean up subgenres and genres by removing quotation marks and splitting into lists
df['song_subgenre'] = df['song_subgenre'].str.replace('"', '', regex=False).str.split(',').apply(lambda x: [s.strip() for s in x])
df['song_genre'] = df['song_genre'].str.replace('"', '', regex=False).str.split(',').apply(lambda x: [s.strip() for s in x])

# Function to get the first three subgenres, repeating the first one if necessary
def get_subgenres(series):
    subgenres = series.iloc[0]
    return (subgenres + subgenres[:3])[:3]

# Function to get the first genre
def get_first_genre(series):
    return series.iloc[0][0]

# Group by 'name' (movie) and aggregate subgenres and genre
grouped = df.groupby('name').agg({
    'song_subgenre': get_subgenres,
    'song_genre': get_first_genre
}).reset_index()

# Expand the subgenres into separate columns
grouped[['subgenre1', 'subgenre2', 'subgenre3']] = pd.DataFrame(grouped['song_subgenre'].tolist(), index=grouped.index)

# Drop the original 'song_subgenre' column
grouped = grouped.drop(columns=['song_subgenre'])

# Reorder columns to match the desired output format
grouped = grouped[['name', 'song_genre', 'subgenre1', 'subgenre2', 'subgenre3']]

# Save the results to a new CSV file
grouped.to_csv('categorized_movies.csv', index=False)

print("Categorization complete. Check 'categorized_movies.csv' for the results.")
