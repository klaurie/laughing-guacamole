import React from 'react'

export interface MusicGenre {
  genre: string;
}

interface MusicGenreListProps {
  genres: MusicGenre[];
}

const MusicGenreList: React.FC<MusicGenreListProps > = ({
  genres,
}) => {
  return (
    <>
    <div>Music Genre List</div>
    <div
    >
      <table className="table table-zebra w-full">
        <thead>
          <tr>
            <th>Genre</th>
          </tr>
        </thead>
        <tbody>
          {genres.map((genre) => (
            <tr key={genre.genre} className="hover">
              <td>{genre.genre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </>
  )
}

export default MusicGenreList