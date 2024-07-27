import React from 'react'

export interface Movie {
  title: string;
  genre: string;
  thumbnail: string;
}

interface MovieListProps {
  movies: Movie[];
}

const MovieList: React.FC<MovieListProps> = ({
  movies
}) => {
  return (
    <div
      className="p-4"    
    >
    <div>MovieList</div>
    <div
    >
      <table className="table w-full">
        <thead>
          <tr>
            <th>Thumbnail</th>
            <th>Title</th>
            <th>Genre</th>
          </tr>
        </thead>
        <tbody>
          {movies.map((movie) => (
            <tr key={movie.title} onClick={() => console.log(movie.title)} className="hover cursor-pointer">
              <td><img src={"https://placehold.co/40x60"} alt={movie.title} /></td>
              <td>{movie.title}</td>
              <td>{movie.genre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </div>
  )
}

export default MovieList