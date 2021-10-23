import { useState } from 'react';
import axios, { AxiosResponse } from 'axios';

import HostedTable from './components/Table/hosted-model/HostedTable';
import UploadTable from './components/Table/upload/UploadTable';
import Dropzone from './components/Dropzone/Dropzone';

import './App.css'

function App() {

  interface FileInfoInterface {
    name: string,
    size: number,
    type: string,
  }

  const [fileInfo, setFileInfo] = useState<FileInfoInterface>({ name: '', size: 0, type: '' });
  const [fileData, setFileData] = useState<object | null>(null);

  const clearFileInfo = () => {
    setFileInfo({
      name: '',
      size: 0,
      type: '',
    })
  }

  const uploadToS3 = async () => {

    try {
      // Get signed URL
      const { data }: AxiosResponse<object | any> = await axios({
        url: '/signed',
        method: 'POST',
        data: {
          id: fileInfo.name,
        }
      });

      const signedUrl: string = data.url;

      // Use signed URL and upload to S3

      const resUpload = await axios({
        url: signedUrl,
        method: 'PUT',
        data: fileData,
      });

      console.log(resUpload);

    } catch (err) {
        console.log(err);
    }
  }

  return (
    <div className="App">
      <header className="header-bar">
          <p className="header">ML Model Hosting and API</p>
        </header>
      <div className="container-fluid">
        <div className="row">
          <div className="col">
            <h4>Hosted models</h4>
            <HostedTable />
          </div>
          <div className="col">
            <h4>Model Upload</h4>
            {fileInfo.name && (
              <>
                <UploadTable 
                  fileInfo={fileInfo}
                />
                <button className="btn btn-primary btn-sm" onClick={uploadToS3}>Upload</button>
                <button className="btn btn-primary btn-sm" onClick={clearFileInfo}>Select different file</button>
              </>
            )}
            {!fileInfo.name &&
              <Dropzone 
                setFileInfo={setFileInfo}
                setFileData={setFileData}
              />
            }
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
