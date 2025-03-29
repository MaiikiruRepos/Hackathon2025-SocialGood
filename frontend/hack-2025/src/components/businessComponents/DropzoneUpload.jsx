import React, { useCallback, useRef } from 'react';
import { useDropzone } from 'react-dropzone';

const API_BASE = 'http://localhost:8000'

const DropzoneUpload = () => {
  const inputRef = useRef();

  const onDrop = useCallback(async (acceptedFiles) => {
    const zipFile = acceptedFiles[0];
    const formData = new FormData();

    if (!zipFile) return;

    formData.append('file', zipFile);
    formData.append('googleID', '000001');

    console.log("hello");
    console.log([...formData]);
    console.log(zipFile.name, zipFile.type);

    try {
      const response = await fetch('http://localhost:8000/upload_zip/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Success:', data);
        // navigate('/dashboard') if needed
      } else {
        console.error('Upload failed');
      }
    } catch (err) {
      console.error('Error uploading file:', err);
    }
  }, []);

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
    accept: { 'application/zip': ['.zip'] },
  });

  return (
    <div>
      <input {...getInputProps()} className="hidden" />
      <button
        type="button"
        className='bg-amber-950 w-[200px] rounded-md font-medium my-6 mx-auto md:mx-0 py-3 text-white hover:scale-105 transition-all duration-300 ease-in-out'
        onClick={open}
      >
        Upload Your BOM/File
      </button>
    </div>
  );
};

export default DropzoneUpload;
