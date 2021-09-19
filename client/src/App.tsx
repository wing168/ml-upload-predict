import './App.css'
import Table from './components/Table/Table';

function App() {
  return (
    <div className="App">
      <header className="header-bar">
          <p className="header">ML Model Hosting and API</p>
        </header>
      <div className="container-fluid">
        <div className="row">
          <div className="col">
            <h3>Hosted models</h3>
            <Table />
          </div>
          <div className="col">
            <h1>Col 2</h1>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
