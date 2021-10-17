import { useState } from 'react';

import Table from './components/Table/Table';
import Dropzone from './components/Dropzone/Dropzone';

import './App.css'

function App() {

  const [fileInfo, setFileInfo] = useState({});
  const [fileData, setFileData] = useState();

  return (
    <div className="App">
      <header className="header-bar">
          <p className="header">ML Model Hosting and API</p>
        </header>
      <div className="container-fluid">
        <div className="row">
          <div className="col">
            <h4>Hosted models</h4>
            <Table />
          </div>
          <div className="col">
            <h4>Model Upload</h4>
            <Dropzone />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
