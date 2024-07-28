"use client";

import { useEffect, useState } from "react";
import MovieGenreSelector from "./components/MovieGenreSelector";
import MovieList from "./components/MovieList";
import Login from "./components/Login";
import MusicGenreList from "./components/MusicGenreList";
import { Movie } from "./components/MovieList";
import { MusicGenre } from "./components/MusicGenreList";
import { useRouter } from "next/navigation";
import { useMyContext, MyContextProps } from "./AppContext";

const DEFAULT_MOVIE_GENRES = [
  "Action",
  "Adventure",
  "Animation",
  "Biography",
  "Comedy",
  "Crime",
  "Drama",
  "Family",
  "Fantasy",
  "Film-Noir",
  "History",
  "Horror",
  "Music",
  "Musical",
  "Mystery",
  "Romance",
  "Sci-Fi",
  "Sport",
  "Thriller",
  "War",
  "Western"
];

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

const DEFAULT_MUSIC_GENRES = [
  { genre: "Rock", subgenres: ["Alternative", "Classic Rock", "Hard Rock"] },
  { genre: "Pop", subgenres: ["Dance", "Synthpop", "Electropop"] },
  { genre: "Jazz", subgenres: ["Smooth", "Bebop", "Swing"] },
  { genre: "Classical", subgenres: ["Baroque", "Romantic", "Classical Era"] },
  { genre: "Electronic", subgenres: ["House", "Techno", "Trance"] },
  { genre: "Country", subgenres: ["Bluegrass", "Honky Tonk", "Country Rock"] },
  { genre: "Rap", subgenres: ["Trap", "Old School", "Gangsta Rap"] },
  { genre: "R&B", subgenres: ["Soul", "Contemporary R&B", "Funk"] },
  { genre: "Latin", subgenres: ["Reggaeton", "Salsa", "Bossa Nova"] },
];

export default function Home() {
  const [selectedMovieGenre, setSelectedMovieGenre] = useState("Action");
  const [movies, setMovies] = useState<Movie[]>([]); // recommended movies from model
  // const [musicGenres, setMusicGenres] = useState<MusicGenre[]>([]); // music genres from user obtained through Spotify
  // const [selectedMusicGenre, setSelectedMusicGenre] = useState("");

  const {musicGenres, setMusicGenres, selectedMusicGenre, setSelectedMusicGenre} = useMyContext();
  
  const router = useRouter();

  // fetch movie genres

  // get recommended movies from model
  const handleFindMovies = () => {
    setMovies(DEFAULT_MOVIES);
  };

  const handleImportMusic = () => {
    router.push("/musicGenres")
  }

  const handleReset = () => {
    setMusicGenres([]);
    setMovies([]);
  };
  return (
    <>
      <MovieGenreSelector
        genres={DEFAULT_MOVIE_GENRES}
        selectedMovieGenre={selectedMovieGenre}
        setSelectedMovieGenre={setSelectedMovieGenre}
      />
      <Login
        setMusicGenres={setMusicGenres}
        defaultMusicGenres={DEFAULT_MUSIC_GENRES}
        handleImportMusic={handleImportMusic}
      />
      {/* <MusicGenreList
        genres={musicGenres?.slice(0, 3)}
        setSelectedMusicGenre={setSelectedMusicGenre}
      /> */}
      
      {/* <button className="btn btn-primary" onClick={handleReset}>
        Reset
      </button> */}
      {/* <div
        className="flex flex-col w-20 gap-4 "
      >
        <button className="btn btn-primary" onClick={handleFindMovies}>
          Find Movies
        </button>
      </div>
      <MovieList movies={movies} /> */}
    </>
  );
}
