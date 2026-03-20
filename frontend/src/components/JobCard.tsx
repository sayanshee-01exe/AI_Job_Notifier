"use client";

import Link from "next/link";

interface JobCardProps {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  skills_required: string[];
  experience_level?: string;
  match_score?: number;
  skill_match_score?: number;
  similarity_score?: number;
}

export default function JobCard({
  id,
  title,
  company,
  location,
  description,
  skills_required,
  experience_level,
  match_score,
  skill_match_score,
  similarity_score,
}: JobCardProps) {
  const scorePercent = match_score ? Math.round(match_score * 100) : null;
  const scoreColor =
    scorePercent && scorePercent >= 80
      ? "from-emerald-400 to-green-500"
      : scorePercent && scorePercent >= 60
      ? "from-amber-400 to-yellow-500"
      : "from-rose-400 to-red-500";

  return (
    <Link href={`/jobs/${id}`}>
      <div className="group relative bg-gray-800/50 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:border-indigo-500/50 hover:bg-gray-800/70 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-500/5 cursor-pointer">
        {/* Match Score Badge */}
        {scorePercent !== null && (
          <div className="absolute -top-3 -right-3">
            <div
              className={`bg-gradient-to-r ${scoreColor} text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg`}
            >
              {scorePercent}% match
            </div>
          </div>
        )}

        {/* Header */}
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-white group-hover:text-indigo-300 transition-colors line-clamp-1">
            {title}
          </h3>
          <p className="text-indigo-400 font-medium text-sm">{company}</p>
          <p className="text-gray-500 text-xs mt-1 flex items-center gap-1">
            <span>📍</span> {location}
            {experience_level && (
              <>
                <span className="mx-1">•</span>
                <span>🎯 {experience_level}</span>
              </>
            )}
          </p>
        </div>

        {/* Description */}
        <p className="text-gray-400 text-sm leading-relaxed line-clamp-2 mb-4">
          {description}
        </p>

        {/* Skills */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {skills_required.slice(0, 5).map((skill) => (
            <span
              key={skill}
              className="px-2 py-0.5 bg-indigo-500/10 text-indigo-300 text-xs rounded-md border border-indigo-500/20"
            >
              {skill}
            </span>
          ))}
          {skills_required.length > 5 && (
            <span className="px-2 py-0.5 text-gray-500 text-xs">
              +{skills_required.length - 5} more
            </span>
          )}
        </div>

        {/* Score Breakdown */}
        {match_score !== undefined && (
          <div className="flex gap-4 pt-3 border-t border-white/5 text-xs text-gray-500">
            <span>Similarity: {Math.round((similarity_score || 0) * 100)}%</span>
            <span>Skills: {Math.round((skill_match_score || 0) * 100)}%</span>
          </div>
        )}
      </div>
    </Link>
  );
}
