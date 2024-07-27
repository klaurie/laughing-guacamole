'use client'

import React, { useState } from 'react'

interface GenreSelectorProps {
  genres: string[];
  selectedGenre: string;
  setSelectedGenre: (genre: string) => void;
}

const GenreSelector: React.FC<GenreSelectorProps>  = ({genres, selectedGenre, setSelectedGenre}) => {

  // const [selectedGenre, setSelectedGenre] = useState("Action");
  
  return (
    <div className="p-4">
        <h2 className="text-2xl font-bold mb-4">Select a Genre</h2>
        <div className="flex flex-wrap gap-2">
          {genres.map((genre) => (
            <button
              key={genre}
              className={`btn ${
                selectedGenre === genre
                  ? 'btn-primary'
                  : 'btn-outline btn-primary'
              }`}
              onClick={() => setSelectedGenre(genre)}
            >
              {genre}
            </button>
          ))}
        </div>
        {selectedGenre && (
          <p className="mt-4">You selected: {selectedGenre}</p>
        )}
      </div>
  )
}

export default GenreSelector