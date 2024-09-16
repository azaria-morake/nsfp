// src/pages/Championship.js
import React from 'react';

function Championship() {
  return (
    <div className="championship">
      <h1 className="text-3xl font-bold mb-4">NSFP Championship</h1>
      <p className="mb-4">Join us for the annual National Soccer Facilities Project Championship!</p>
      <div className="bg-yellow-100 p-4 rounded mb-4">
        <h2 className="text-2xl font-semibold mb-2">Next Event</h2>
        <p><strong>Date:</strong> December 15-17, 2024</p>
        <p><strong>Location:</strong> Johannesburg Stadium</p>
      </div>
      <a href="#" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
        Register Your Team
      </a>
    </div>
  );
}

export default Championship;