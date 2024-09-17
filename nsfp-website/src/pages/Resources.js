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