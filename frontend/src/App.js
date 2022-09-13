import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [picture,setPicture] =useState({})
 

  // const getRequest= async() => {
  //   try {
  //     const response = await axios.get("http://localhost:5000/flask/hello");
  //     console.log("SUCCESS",response)
  //     setMessage(response)
  //   } catch (error) {
  //     setMessage(error);
  //   }
  // }

  // const UploadImage =async (event) => {
  //   const formData = new FormData();
  //   formData.append(
  //       "file",
  //       this.state.pictureAsFile
  //   );

  //   console.log(picture.pictureAsFile);

  //   for (var key of formData.entries()) {
  //     console.log(key[0] + ", " + key[1]);
  //   }
  // // }

  // function handleUploadImage(ev) {
  //   ev.preventDefault();



  //   axios.post('http://localhost:5000//SVM_api', {
  //     body: data,
  //   }).then(function (response) {
  //     console.log(response);
  //     setMessage(response.message)
      
  //   })
  //   .catch(function (error) {
  //     console.log(error);
  //   });
  // }


  return (
    <div className="App">
      <header className="App-header">
        {message && message}
        
        <form  action='/SVM_api' method="post">
          <label>Enter your image to predict which number :</label>
          <input type="file" name='image' onChange={Image}/>
          <button type="submit" name="upload">Upload</button>
        </form>
      </header>
    </div>
  );
}

export default App;
