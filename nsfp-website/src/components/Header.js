import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-green-600 text-white p-4">
      <nav>
        <ul className="flex justify-around">
          <li><Link to="/" className="hover:text-yellow-300">Home</Link></li>
          <li><Link to="/about" className="hover:text-yellow-300">About</Link></li>
          <li><Link to="/team-profiles" className="hover:text-yellow-300">Team Profiles</Link></li>
          <li><Link to="/support" className="hover:text-yellow-300">Support a Team</Link></li>
          <li><Link to="/resources" className="hover:text-yellow-300">Resources</Link></li>
          <li><Link to="/championship" className="hover:text-yellow-300">NSFP Championship</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;