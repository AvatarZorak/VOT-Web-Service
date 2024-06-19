import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from 'react';
import axios from 'axios';

import Keycloak from "keycloak-js";

let keycloak_options = {
  url: 'http://localhost:8080',
  realm: 'application',
  clientId: 'front-end-client'
}

console.log("1")

let keycloak = new Keycloak(keycloak_options)

await keycloak.init({
  onLoad: "login-required",
  checkLoginIframe: false,
  pkceMethod: "S256"
}).then((auth) => {
  if(!auth) {
    window.location.reload();
  } else {
    console.log("Access token: ", keycloak.token)
  }
}, () => {
  console.log("Authentication error")
  console.log(keycloak)
})
//
// const body = {
//   message: 'something'
// };
//
// const headers = {
//     'Content-Type': 'application/json',
//     'Authorization': `${keycloak.token}`
// };
//
// let responseBody;
//
// await axios.post("http://localhost:5000/", body, { headers }).then(response => {
//     responseBody = response.data;
// });

function App() {

  const [selectedImage, setSelectedImage] = useState(null)
  const [imageURL, setImageURL] = useState(null)

  const fileChange = (event) => {
    const image = event.target.files[0]
    const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg']

    if(image && allowedTypes.includes(image.type)) {
      setSelectedImage(image);
    } else {
      setSelectedImage(null);
      console.log('ERROR! INVALID IMAGE TYPE!');
    }

  };

  const fileUpload = async () => {
    console.log("sending")

    if(selectedImage) {
      console.log("in")
      const formData = new FormData();
      formData.append("image", selectedImage);

      await axios.post("http://localhost:5000/upload", formData, {
        responseType: "blob",
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `${keycloak.token}`
        }
      }).then(response => {
        const blobURL = window.URL.createObjectURL(new Blob([response.data]))
        console.log(blobURL);
        setImageURL(blobURL);
        setSelectedImage(null);
      }).catch(error => {
        console.log(error)
      });
    } else {
      console.log("out")
    }
  }


  return (
    <>
        <input type="file" onChange={fileChange} />
        <br/>
        <button onClick={fileUpload}>Upload</button>
        {imageURL ? (
          <img src={imageURL} alt="Fetched content" />
        ) : (
          <p>Loading...</p>
        )}
    </>
  );
}

export default App;
