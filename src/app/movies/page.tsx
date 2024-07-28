'use client'

import React, { Suspense, useEffect } from 'react'
import MovieList, { Movie } from '../components/MovieList'
import LoadingComponent from '../LoadingComponent'
import { join } from 'path';

const DEFAULT_MOVIES = [
  // Action movies
  { title: "The Matrix", genre: "Action", thumbnail: "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg" },
  { title: "Die Hard", genre: "Action", thumbnail: "https://upload.wikimedia.org/wikipedia/en/6/69/Die_Hard.jpg" },
  { title: "Mad Max: Fury Road", genre: "Action", thumbnail: "https://upload.wikimedia.org/wikipedia/en/6/6e/Mad_Max_Fury_Road_poster.jpg" },
  { title: "John Wick", genre: "Action", thumbnail: "https://upload.wikimedia.org/wikipedia/en/1/14/John_Wick_Poster.jpg" },

  // Comedy movies
  { title: "Forrest Gump", genre: "Comedy", thumbnail: "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg" },
  { title: "The Hangover", genre: "Comedy", thumbnail: "https://upload.wikimedia.org/wikipedia/en/6/63/The_Hangover_Poster.jpg" },
  { title: "Bridesmaids", genre: "Comedy", thumbnail: "https://upload.wikimedia.org/wikipedia/en/1/12/Bridesmaids_Poster.jpg" },
  { title: "Anchorman: The Legend of Ron Burgundy", genre: "Comedy", thumbnail: "https://upload.wikimedia.org/wikipedia/en/6/6e/Anchorman_%E2%80%93_The_Legend_of_Ron_Burgundy.jpg" },

  // Romance movies
  { title: "The Notebook", genre: "Romance", thumbnail: "https://upload.wikimedia.org/wikipedia/en/8/8c/The_Notebook_Poster.jpg" },
  { title: "Pride and Prejudice", genre: "Romance", thumbnail: "https://upload.wikimedia.org/wikipedia/en/1/13/Pride_and_Prejudice.jpg" },
  { title: "Titanic", genre: "Romance", thumbnail: "https://upload.wikimedia.org/wikipedia/en/1/19/Titanic_Poster.jpg" },
  { title: "La La Land", genre: "Romance", thumbnail: "https://upload.wikimedia.org/wikipedia/en/0/0c/La_La_Land_Poster.jpg" },

  // Mystery movies
  { title: "Gone Girl", genre: "Mystery", thumbnail: "https://upload.wikimedia.org/wikipedia/en/4/47/Gone_Girl_Poster.jpg" },
  { title: "Shutter Island", genre: "Mystery", thumbnail: "https://upload.wikimedia.org/wikipedia/en/0/0b/Shutter_Island_Poster.jpg" },
  { title: "The Girl with the Dragon Tattoo", genre: "Mystery", thumbnail: "https://upload.wikimedia.org/wikipedia/en/9/9d/The_Girl_with_the_Dragon_Tattoo_Poster.jpg" },
  { title: "Memento", genre: "Mystery", thumbnail: "https://upload.wikimedia.org/wikipedia/en/c/c4/Memento_Poster.jpg" },

  // Horror movies
  { title: "The Shining", genre: "Horror", thumbnail: "https://upload.wikimedia.org/wikipedia/en/e/e1/The_Shining_%282006_film%29.jpg" },
  { title: "Get Out", genre: "Horror", thumbnail: "https://upload.wikimedia.org/wikipedia/en/8/8c/Get_Out_Poster.jpg" },
  { title: "A Quiet Place", genre: "Horror", thumbnail: "https://upload.wikimedia.org/wikipedia/en/8/83/A_Quiet_Place_Poster.jpg" },
  { title: "The Conjuring", genre: "Horror", thumbnail: "https://upload.wikimedia.org/wikipedia/en/9/9d/The_Conjuring_Poster.jpg" },
];

const MoviesPage = () => {
  const [movies, setMovies] = React.useState<Movie[]>([])
  const [loading, setLoading] = React.useState<boolean>(true)
  
  useEffect(() => {
    try {
      // get recommended movies from model 

      setTimeout(() => {
        setMovies(DEFAULT_MOVIES)
        setLoading(false);
      }, 2000);
    }
    catch (error) {
      console.log(error)
    }
  }, [])

  if (loading) return <LoadingComponent />
  // if(loading) return <p>Loading...</p>
  
  return (
    <Suspense fallback={<LoadingComponent />}>
      <MovieList movies={movies} />
    </Suspense>
  )
}

export default MoviesPage