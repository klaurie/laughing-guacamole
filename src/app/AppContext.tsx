'use client'
import { createContext, useContext, useState } from 'react';
import { MusicGenre } from './components/MusicGenreList';

export interface MyContextProps {
  musicGenres: MusicGenre[];
  setMusicGenres: (musicGenres: MusicGenre[]) => void;
  selectedMusicGenre: string;
  setSelectedMusicGenre: (selectedMusicGenre: string) => void;
}

const MyContext = createContext<MyContextProps | undefined>(undefined);

export function MyProvider({ children }: { children: React.ReactNode }) {
  const [musicGenres, setMusicGenres] = useState<MusicGenre[]>([]);
  const [selectedMusicGenre, setSelectedMusicGenre] = useState("");

  return (
    <MyContext.Provider value={{ musicGenres, setMusicGenres, selectedMusicGenre, setSelectedMusicGenre }}>
      {children}
    </MyContext.Provider>
  );
}

export const useMyContext = () => {
  const context = useContext(MyContext);
  if (context === undefined) {
    throw new Error('useMyContext must be used within a MyProvider');
  }
  return context;
}