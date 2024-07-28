import React from 'react';
import { Link } from 'react-router-dom';
import './NotFound.css';  // Assume you'll create this CSS file

const NotFound = () => {
  return (
    <div className="not-found">
      <h2>404 - Page Not Found</h2>
      <p>Sorry, the page you are looking for does not exist.</p>

    </div>
  );
};

export default NotFound;