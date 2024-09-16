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