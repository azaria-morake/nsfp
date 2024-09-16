import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1 className="text-4xl font-bold mb-4">Welcome to the National Soccer Facilities Project</h1>
      <p className="mb-4">We're dedicated to improving soccer facilities across South Africa.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-green-100 p-4 rounded">
          <h2 className="text-2xl font-semibold mb-2">Our Mission</h2>
          <p>To provide quality training facilities for soccer teams nationwide.</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded">
          <h2 className="text-2xl font-semibold mb-2">Get Involved</h2>
          <p>Support a team or contribute to our resources. Every action counts!</p>
        </div>
      </div>
      <div className="flex justify-center space-x-4">
        <Link to="/signup" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Sign Up
        </Link>
        <Link to="/signin" className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
          Sign In
        </Link>
      </div>
    </div>
  );
}

export default Home;