'use client'
import React, { useEffect, useState } from 'react'
import { useMyContext } from '../AppContext'
import { useRouter } from 'next/navigation'
import LoadingComponent from '../LoadingComponent'

const MusicGenres = () => {
  const { musicGenres, setMusicGenres, selectedMusicGenre, setSelectedMusicGenre } = useMyContext()
  const router = useRouter()
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchTopGenres = async (token: string) => {
    // const response = await fetch('http://127.0.0.1:5000')
    const response = await fetch(`http://127.0.0.1:5000/top_genres?access_token=${token}`)
    const data = await response.json()
    console.log('data', data)
    setMusicGenres(data)
    setLoading(false)
  }

  const fetchDummyData = async () => {
    try {
      const response = await fetch("https://http.cat/status/200")
      const data = await response.json()
      console.log(data)
    }
    catch (error) {
      console.log(error)
    }
  }

  useEffect(() => {
    const access_token = localStorage.getItem("access_token") || "";
    console.log('access_token: ' + access_token);
    if (access_token) {
      setAccessToken(access_token);
      // get top genres 
      fetchTopGenres(access_token);
      // and possibly recommend movies from http://127.0.0.1:5000/top_genres?access_token=YOUR_ACCESS_TOKEN
      
      
      
      // fetchDummyData();
    }
  }, [])

  const handleFindMovies = () => {
    router.push("/movies")
  }

  if (loading) {
    return <LoadingComponent />
  }
  
  return (
    <div>
      <h1
        className='text-3xl font-bold text-center my-10'
      >Top Music Genres Based on Your Spotify Music Library</h1>
      <div
        className='flex flex-wrap justify-center'
      >
        {musicGenres && musicGenres.length > 0 ? musicGenres.map((genre) => (
          <button
            key={genre.genre}
            onClick={() => setSelectedMusicGenre(genre.genre)}
            className='btn btn-secondary m-2'
          >
            {genre.genre}
          </button>
        )) : <div>No music genres found</div>}
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