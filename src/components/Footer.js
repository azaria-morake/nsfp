// src/components/Footer.js
import React from 'react';

function Footer() {
  return (
    <footer className="bg-green-800 text-white p-4 mt-8">
      <div className="container mx-auto text-center">
        <p>&copy; 2024 National Soccer Facilities Project. All rights reserved.</p>
        <div className="mt-2">
          <a href="#" className="mx-2 hover:text-yellow-300">Facebook</a>
          <a href="#" className="mx-2 hover:text-yellow-300">Twitter</a>
          <a href="#" className="mx-2 hover:text-yellow-300">Instagram</a>
          <a href="#" className="mx-2 hover:text-yellow-300">YouTube</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;