import React from "react";

export interface MusicGenre {
  genre: string;
  subgenres: string[];
}

interface MusicGenreListProps {
  genres: MusicGenre[];
  setSelectedMusicGenre: (genre: string) => void;
}

const MusicGenreList: React.FC<MusicGenreListProps> = ({ genres, setSelectedMusicGenre }) => {
  return (
    <div
      className="p-4"
    >
      <div>Music Genre List</div>
      <div>
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th>Genre</th>
              <th>Action</th>
              <th>SubGenres</th>
            </tr>
          </thead>
          <tbody>
            {genres.map((genre) => (
              <>
              <tr key={genre.genre} >
                <td>{genre.genre}</td>
                <td>
                  <button
                    className="btn btn-primary"
                    onClick={() => setSelectedMusicGenre(genre.genre)}
                  >
                    Select
                  </button>
                </td>
                <td>
                  <ul>
                    {genre.subgenres.map((subgenre) => (
                      <li key={subgenre}>{subgenre}</li>
                    ))}
                  </ul>
                </td>
              </tr>
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MusicGenreList;
