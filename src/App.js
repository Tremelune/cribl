import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import SearchForm from './SearchForm';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
      fetch('http://127.0.0.1:5000/', { mode: 'no-cors'})
          .then(response => response.status)
          .then(data => console.log(data))
          .then(body => setData(body))
          .catch(error => console.error(error));
  }, []);

  console.log('I was triggered during componentDidMount')
  return (
    <div className="App">
      <header className="App-header">
        <SearchForm />
      </header>
    </div>
  );
}

export default App;
