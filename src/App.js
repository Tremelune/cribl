import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import SearchForm from './SearchForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <strong>Benedict Cribl GOAT Log Reader</strong>
        <img src="goat-logger.jpg"/>
        <SearchForm />
      </header>
    </div>
  );
}

export default App;
