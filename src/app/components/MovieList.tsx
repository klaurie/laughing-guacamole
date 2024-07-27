import React from 'react'

export interface Movie {
  title: string;
  genre: string;
}

interface MovieListProps {
  movies: Movie[];
}

const MovieList: React.FC<MovieListProps> = ({
  movies
}) => {
  return (
    <>
    <div>MovieList</div>
    <div
    >
      <table className="table table-zebra w-full">
        <thead>
          <tr>
            <th>Title</th>
            <th>Genre</th>
          </tr>
        </thead>
        <tbody>
          {movies.map((movie) => (
            <tr key={movie.title} className="hover">
              <td>{movie.title}</td>
              <td>{movie.genre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </>
  )
}

export default MovieList