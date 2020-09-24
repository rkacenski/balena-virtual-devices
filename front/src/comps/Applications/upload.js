import React, { useState } from 'react';
import { 
  Modal, 
  Button, 
  Box, 
  Select
} from 'rendition';

export default () => {
  const [selectedFiles, setSelectedFiles] = useState(undefined);

  const selectFile = (event) => {
    setSelectedFiles(event.target.files);
  };

  function uploadFile() {
    var formData = new FormData();
  
    formData.append(`file`, selectedFiles[0]);
    
    fetch('http://localhost:5000/apps/add', {
      // content-type header should not be specified!
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(success => {
        // Do something with the successful response
      })
      .catch(error => console.log(error)
    );
  }

  return (
    <div>
      <label className="btn btn-default">
        <input type="file" onChange={selectFile} />
      </label>

      <button
        className="btn btn-success"
        disabled={!selectedFiles}
        onClick={uploadFile}
      >
        Upload
      </button>
    </div>
  );
}