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
