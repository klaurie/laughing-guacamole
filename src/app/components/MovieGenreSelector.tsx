'use client'

import React, { useState } from 'react'

interface MovieGenreSelectorProps {
  genres: string[];
  selectedMovieGenre: string;
  setSelectedMovieGenre: (genre: string) => void;
}

const MovieGenreSelector: React.FC<MovieGenreSelectorProps>  = ({genres, selectedMovieGenre, setSelectedMovieGenre}) => {

  return (
    <div className="p-4 text-center justify-center">
        <h2 className="text-2xl font-bold mb-4">Select a Movie Genre</h2>
        <div className="flex flex-wrap gap-2 justify-center">
          {genres.map((genre) => (
            <button
              key={genre}
              className={`btn ${
                selectedMovieGenre === genre
                  ? 'btn-primary'
                  : 'btn-outline btn-primary'
              }`}
              onClick={() => setSelectedMovieGenre(genre)}
            >
              {genre}
            </button>
          ))}
        </div>
        {selectedMovieGenre && (
          <p className="mt-4">You selected: {selectedMovieGenre}</p>
        )}
      </div>
  )
}

export default MovieGenreSelector