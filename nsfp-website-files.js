// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import TeamProfiles from './pages/TeamProfiles';
import Support from './pages/Support';
import Resources from './pages/Resources';
import Championship from './pages/Championship';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="container mx-auto px-4">
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/about" component={About} />
            <Route path="/team-profiles" component={TeamProfiles} />
            <Route path="/support" component={Support} />
            <Route path="/resources" component={Resources} />
            <Route path="/championship" component={Championship} />
          </Switch>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;

// src/components/Header.js
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

// src/pages/Home.js
import React from 'react';

function Home() {
  return (
    <div className="home">
      <h1 className="text-4xl font-bold mb-4">Welcome to the National Soccer Facilities Project</h1>
      <p className="mb-4">We're dedicated to improving soccer facilities across South Africa.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-green-100 p-4 rounded">
          <h2 className="text-2xl font-semibold mb-2">Our Mission</h2>
          <p>To provide quality training facilities for soccer teams nationwide.</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded">
          <h2 className="text-2xl font-semibold mb-2">Get Involved</h2>
          <p>Support a team or contribute to our resources. Every action counts!</p>
        </div>
      </div>
    </div>
  );
}

export default Home;

// src/pages/About.js
import React from 'react';

function About() {
  return (
    <div className="about">
      <h1 className="text-3xl font-bold mb-4">About NSFP</h1>
      <p className="mb-4">The National Soccer Facilities Project aims to address the facility needs of soccer teams nationwide.</p>
      <h2 className="text-2xl font-semibold mb-2">Our Objectives</h2>
      <ul className="list-disc list-inside mb-4">
        <li>Provide a centralized hub for teams to showcase their facility requirements</li>
        <li>Facilitate donations and sponsorships for facility improvement</li>
        <li>Promote collaboration and knowledge sharing among teams</li>
        <li>Foster a sense of community among soccer enthusiasts</li>
        <li>Organize the annual NSFP Championship</li>
      </ul>
    </div>
  );
}

export default About;

// src/pages/TeamProfiles.js
import React, { useState, useEffect } from 'react';

function TeamProfiles() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    // In a real application, this would be an API call
    setTeams([
      { id: 1, name: 'Soweto Stars', location: 'Soweto', needs: 'New goal posts' },
      { id: 2, name: 'Cape Town United', location: 'Cape Town', needs: 'Field maintenance equipment' },
      { id: 3, name: 'Durban Dynamos', location: 'Durban', needs: 'Training balls and cones' },
    ]);
  }, []);

  return (
    <div className="team-profiles">
      <h1 className="text-3xl font-bold mb-4">Team Profiles</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {teams.map(team => (
          <div key={team.id} className="bg-white shadow-md rounded p-4">
            <h2 className="text-xl font-semibold mb-2">{team.name}</h2>
            <p><strong>Location:</strong> {team.location}</p>
            <p><strong>Needs:</strong> {team.needs}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TeamProfiles;

// src/pages/Support.js
import React, { useState } from 'react';

function Support() {
  const [donationAmount, setDonationAmount] = useState('');

  const handleDonation = (e) => {
    e.preventDefault();
    // In a real application, this would connect to a payment processor
    alert(`Thank you for your donation of R${donationAmount}!`);
    setDonationAmount('');
  };

  return (
    <div className="support">
      <h1 className="text-3xl font-bold mb-4">Support a Team</h1>
      <p className="mb-4">Your donation can make a real difference in improving soccer facilities.</p>
      <form onSubmit={handleDonation} className="max-w-md">
        <div className="mb-4">
          <label htmlFor="amount" className="block mb-2">Donation Amount (R):</label>
          <input
            type="number"
            id="amount"
            value={donationAmount}
            onChange={(e) => setDonationAmount(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
          Donate
        </button>
      </form>
    </div>
  );
}

export default Support;

// src/pages/Resources.js
import React from 'react';

function Resources() {
  const resources = [
    { id: 1, title: 'Field Maintenance Guide', type: 'PDF' },
    { id: 2, title: 'Fundraising Strategies for Soccer Clubs', type: 'Video' },
    { id: 3, title: 'Effective Training Drills', type: 'Blog Post' },
  ];

  return (
    <div className="resources">
      <h1 className="text-3xl font-bold mb-4">Resources and Best Practices</h1>
      <ul className="space-y-4">
        {resources.map(resource => (
          <li key={resource.id} className="bg-white shadow-md rounded p-4">
            <h2 className="text-xl font-semibold">{resource.title}</h2>
            <p>Type: {resource.type}</p>
            <a href="#" className="text-blue-500 hover:underline">Download/View</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Resources;

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

// src/App.css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="National Soccer Facilities Project website" />
    <title>NSFP - National Soccer Facilities Project</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>

// package.json
{
  "name": "nsfp-website",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^5.3.0",
    "react-scripts": "4.0.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.5",
    "tailwindcss": "^3.0.7"
  }
}

// tailwind.config.js
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
