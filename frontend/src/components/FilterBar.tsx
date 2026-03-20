"use client";

import { useState } from "react";

interface FilterBarProps {
  onFilter: (filters: {
    location: string;
    role: string;
    experience_level: string;
    posted_within_hours?: number;
  }) => void;
}

export default function FilterBar({ onFilter }: FilterBarProps) {
  const [location, setLocation] = useState("");
  const [role, setRole] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("");
  const [postedWithin, setPostedWithin] = useState("");

  const handleApply = () => {
    onFilter({ 
      location, 
      role, 
      experience_level: experienceLevel,
      posted_within_hours: postedWithin ? parseInt(postedWithin) : undefined
    });
  };

  const handleReset = () => {
    setLocation("");
    setRole("");
    setExperienceLevel("");
    setPostedWithin("");
    onFilter({ location: "", role: "", experience_level: "", posted_within_hours: undefined });
  };

  return (
    <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-5">
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="📍 Location"
          className="flex-1 bg-gray-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-500 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 transition-all"
        />
        <input
          type="text"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          placeholder="💼 Role / Title"
          className="flex-1 bg-gray-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-gray-500 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 transition-all"
        />
        <select
          value={experienceLevel}
          onChange={(e) => setExperienceLevel(e.target.value)}
          className="flex-1 bg-gray-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 transition-all appearance-none"
        >
          <option value="">🎯 Experience Level</option>
          <option value="Intern">Intern</option>
          <option value="Junior">Junior</option>
          <option value="Mid">Mid-Level</option>
          <option value="Senior">Senior</option>
          <option value="Lead">Lead</option>
        </select>
        <select
          value={postedWithin}
          onChange={(e) => setPostedWithin(e.target.value)}
          className="flex-1 bg-gray-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 transition-all appearance-none"
        >
          <option value="">🕒 Any Time</option>
          <option value="12">Past 12 hours</option>
          <option value="24">Past 24 hours</option>
          <option value="168">Past 7 days</option>
        </select>
        <div className="flex gap-2">
          <button
            onClick={handleApply}
            className="px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-medium rounded-xl hover:shadow-lg hover:shadow-indigo-500/25 transition-all duration-300"
          >
            Filter
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2.5 bg-gray-700/50 text-gray-300 text-sm rounded-xl hover:bg-gray-700 transition-all"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
