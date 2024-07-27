'use client'

import { useEffect, useState } from "react";
import GenreSelector from "./components/GenreSelector";
import MovieList from "./components/MovieList";
import Login from "./components/Login";
import MusicGenreList from "./components/MusicGenreList";
import { Movie } from "./components/MovieList";
import { MusicGenre } from "./components/MusicGenreList";

const DEFAULT_GENRES = ["Action", "Comedy", "Horror", "Romance", "Mystery"];

const DEFAULT_MOVIES = [
  // Action movies
  { title: "The Matrix", genre: "Action" },
  { title: "Die Hard", genre: "Action" },
  { title: "Mad Max: Fury Road", genre: "Action" },
  { title: "John Wick", genre: "Action" },

  // Comedy movies
  { title: "Forrest Gump", genre: "Comedy" },
  { title: "The Hangover", genre: "Comedy" },
  { title: "Bridesmaids", genre: "Comedy" },
  { title: "Anchorman: The Legend of Ron Burgundy", genre: "Comedy" },

  // Romance movies
  { title: "The Notebook", genre: "Romance" },
  { title: "Pride and Prejudice", genre: "Romance" },
  { title: "Titanic", genre: "Romance" },
  { title: "La La Land", genre: "Romance" },

  // Mystery movies
  { title: "Gone Girl", genre: "Mystery" },
  { title: "Shutter Island", genre: "Mystery" },
  { title: "The Girl with the Dragon Tattoo", genre: "Mystery" },
  { title: "Memento", genre: "Mystery" },

  // Horror movies
  { title: "The Shining", genre: "Horror" },
  { title: "Get Out", genre: "Horror" },
  { title: "A Quiet Place", genre: "Horror" },
  { title: "The Conjuring", genre: "Horror" }
];

const DEFAULT_MUSIC_GENRES = [
  { genre: "Rock" },
  { genre: "Pop" },
  { genre: "Jazz" },
  { genre: "Classical" },
  { genre: "Electronic" },
  { genre: "Country" },
  { genre: "Rap" },
  { genre: "R&B" },
  { genre: "Latin" },
];

export default function Home() {
  const [selectedGenre, setSelectedGenre] = useState("Action");
  const [movies, setMovies] = useState<Movie[]>([]);
  const [musicGenres, setMusicGenres] = useState<MusicGenre[]>([]);
  
  const handleFindMovies = () => {
    setMovies(DEFAULT_MOVIES);
  }
  
  return (
    <>
      <GenreSelector genres={DEFAULT_GENRES} selectedGenre={selectedGenre} setSelectedGenre={setSelectedGenre} />
      <Login setMusicGenres={setMusicGenres} defaultMusicGenres={DEFAULT_MUSIC_GENRES} />
      <MusicGenreList genres={musicGenres?.slice(0, 3)} />
      <button 
        className="btn btn-primary"
        onClick={handleFindMovies}
      >
        Find Movies
      </button>
      <MovieList movies={movies} />
    </>
  );
}
