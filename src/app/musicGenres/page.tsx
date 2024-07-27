'use client'
import React from 'react'
import { useMyContext } from '../AppContext'
import { useRouter } from 'next/navigation'

const MusicGenres = () => {
  const { musicGenres, setMusicGenres, selectedMusicGenre, setSelectedMusicGenre } = useMyContext()
  const router = useRouter()

  const handleFindMovies = () => {
    router.push("/movies")
  }
  
  return (
    <div>
      <h1
        className='text-3xl font-bold text-center my-10'
      >Top Music Genres Based on Your Spotify Music Library</h1>
      <div
        className='flex flex-wrap justify-center'
      >
        {musicGenres.map((genre) => (
          <button
            key={genre.genre}
            onClick={() => setSelectedMusicGenre(genre.genre)}
            className='btn btn-secondary m-2'
          >
            {genre.genre}
          </button>
        ))}
      </div>
      <div
        className='flex justify-center my-10 gap-4'
      >
        <button
          className='btn '
          onClick={() => {
            setMusicGenres([])
            router.back()
          }}
        >
          Back
        </button>
        <button className="btn btn-primary" onClick={handleFindMovies}>
          Find Movies
        </button>
      </div>
    </div>
  )
}

export default MusicGenres