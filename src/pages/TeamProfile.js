import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function TeamProfile() {
  const [activeTab, setActiveTab] = useState('gallery');

  // Placeholder data
  const team = {
    name: 'Example FC',
    icon: '/path/to/icon.png',
    funds: 10000,
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'gallery':
        return <div>Gallery Content</div>;
      case 'needs':
        return <div>Needs Content</div>;
      case 'squads':
        return <div>Squads Content</div>;
      case 'staff':
        return <div>Coaching Staff Content</div>;
      case 'achievements':
        return <div>Achievements Content</div>;
      default:
        return <div>Gallery Content</div>;
    }
  };

  return (
    <div className="container mx-auto p-4">
      <nav className="flex justify-between items-center mb-4">
        <div className="flex items-center">
          <img src={team.icon} alt={team.name} className="w-10 h-10 mr-2" />
          <h1 className="text-2xl font-bold">{team.name}</h1>
        </div>
        <div>Funds: R{team.funds}</div>
        <Link to="/settings" className="bg-gray-200 px-4 py-2 rounded">Settings</Link>
      </nav>

      <div className="mb-4">
        <button 
          onClick={() => setActiveTab('gallery')} 
          className={`mr-2 ${activeTab === 'gallery' ? 'bg-blue-500 text-white' : 'bg-gray-200'} px-4 py-2 rounded`}
        >
          Gallery
        </button>
        <button 
          onClick={() => setActiveTab('needs')} 
          className={`mr-2 ${activeTab === 'needs' ? 'bg-blue-500 text-white' : 'bg-gray-200'} px-4 py-2 rounded`}
        >
          Needs
        </button>
        <button 
          onClick={() => setActiveTab('squads')} 
          className={`mr-2 ${activeTab === 'squads' ? 'bg-blue-500 text-white' : 'bg-gray-200'} px-4 py-2 rounded`}
        >
          Squads
        </button>
        <button 
          onClick={() => setActiveTab('staff')} 
          className={`mr-2 ${activeTab === 'staff' ? 'bg-blue-500 text-white' : 'bg-gray-200'} px-4 py-2 rounded`}
        >
          Coaching Staff
        </button>
        <button 
          onClick={() => setActiveTab('achievements')} 
          className={`${activeTab === 'achievements' ? 'bg-blue-500 text-white' : 'bg-gray-200'} px-4 py-2 rounded`}
        >
          Achievements
        </button>
      </div>

      {renderContent()}
    </div>
  );
}

export default TeamProfile;