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