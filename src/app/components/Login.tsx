import { appendFile } from "fs";
import React, { useEffect, useState } from "react";

interface LoginProps {
  setMusicGenres: any;
  defaultMusicGenres: any;
}

type User = {
  id: number;
  name: string;
  username: string;
  email: string;
  website: string;
};

const Login: React.FC<LoginProps> = ({
  setMusicGenres,
  defaultMusicGenres
}) => {
  const APP_URL = process.env.NEXT_PUBLIC_APP_URL;
  const openModal = () => {
    const modal = document.getElementById(
      "my_modal_3"
    ) as HTMLDialogElement | null;
    modal?.showModal();
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [uid, setUid] = useState("");

  const handleLogin = async () => {
    setMusicGenres(defaultMusicGenres);
  };

  return (
    <>
      {/* You can open the modal using document.getElementById('ID').showModal() method */}
      <button className="btn btn-primary" onClick={openModal}>
        Import Spotify Music
      </button>
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
          </div>
        </div>
      </dialog>
    </>
  );
};

export default Login;
