import { appendFile } from "fs";
import React, { useEffect, useState } from "react";

interface LoginProps {
  setMusicGenres: any;
  defaultMusicGenres: any;
  handleImportMusic: () => void;
}

const Login: React.FC<LoginProps> = ({
  setMusicGenres,
  defaultMusicGenres,
  handleImportMusic,
}) => {
  const APP_URL = process.env.NEXT_PUBLIC_APP_URL;
  const openModal = () => {
    const modal = document.getElementById(
      "my_modal_3"
    ) as HTMLDialogElement | null;
    modal?.showModal();
  };

  const closeModal = () => {
    const modal = document.getElementById(
      "my_modal_3"
    ) as HTMLDialogElement | null;
    modal?.close();
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [uid, setUid] = useState("");

  // retrieve user music info from Spotify
  const handleLogin = async () => {
    console.log(defaultMusicGenres);

    try {
      // // fetch auth token from backend 
      const response = await fetch(
        `${APP_URL}/login` ,
      );
      // const response = await fetch(`${APP_URL}/`)
      // top music genres 
      // console.log('response', response);
      const data = await response.json();
      console.log('data', data);
      
      // if (defaultMusicGenres.length > 0) {
      //   handleImportMusic();
      // }
      // setMusicGenres(defaultMusicGenres);
      closeModal();

    }
    catch (error) {
      console.error(error);
    }

  };
  const handleFakeLogin = async () => {
    console.log(defaultMusicGenres);

    try {
      // // fetch auth token from backend 
      const response = await fetch(`${APP_URL}/user/music/genres`);
      // top music genres 
      // console.log('response', response);
      const data = await response.json();
      console.log('data', data);
      
      
      if (defaultMusicGenres.length > 0) {
        handleImportMusic();
      }
      setMusicGenres(defaultMusicGenres);
      closeModal();

    }
    catch (error) {
      console.error(error);
    }

  };


  return (
    <>
      {/* You can open the modal using document.getElementById('ID').showModal() method */}
      <div
        className="flex gap-2 py-4 justify-center"
      >
        <button className="btn btn-primary" onClick={openModal}>
          Import Spotify Music
        </button>
      </div>
      <dialog id="my_modal_3" className="modal">
        <div className="modal-box">
          <form method="dialog">
            {/* if there is a button in form, it will close the modal */}
            <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
              ✕
            </button>
          </form>
          <h3 className="font-bold text-lg">Login</h3>

          <div className="modal-action">
            <button className="btn btn-primary" onClick={handleLogin}>Login</button>
            <button className="btn btn-primary" onClick={handleFakeLogin}>Fake Login</button>
          </div>
        </div>
      </dialog>
    </>
  );
};

export default Login;
