import React, { useState } from 'react';

function TextFileReader() {
  const [file, setFile] = useState(null);
  const [fileContent, setFileContent] = useState('');

  const handleFileRead = (e) => {
    setFileContent(e.target.result);
  };

  const handleFileUpload = async () => {
    // Create form data object to send file
    const formData = new FormData();
    formData.append('file', file);
    console.log(formData);
    console.log("hi");
    // Send file to server
    const response = await fetch('api/upload/', {
      method: 'POST',
      body: formData
    });

    // Get response text
    const responseText = await response.text();
    setFileContent(responseText);
  };

  const handleFileChosen = (file) => {
    setFile(file);
  };

  return (
    <div>
      <input type="file" onChange={e => handleFileChosen(e.target.files[0])} />
      <button onClick={handleFileUpload}>Upload</button>
      <div>
        {fileContent}
      </div>
    </div>
  );
}

export default TextFileReader;