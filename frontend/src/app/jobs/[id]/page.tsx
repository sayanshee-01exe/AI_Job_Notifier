"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import MatchScore from "@/components/MatchScore";
import { fetchJobById } from "@/lib/api";

interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  skills_required: string[];
  experience_level?: string;
  salary_range?: string;
  job_type: string;
  source_url?: string;
  created_at: string;
}

export default function JobDetailPage() {
  const params = useParams();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.id) {
      fetchJobById(Number(params.id))
        .then(setJob)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (!job) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <div className="text-5xl mb-4">🔍</div>
        <h2 className="text-2xl font-bold text-white mb-2">Job Not Found</h2>
        <p className="text-gray-500 mb-6">The job listing you&#39;re looking for doesn&#39;t exist.</p>
        <a href="/" className="text-indigo-400 hover:text-indigo-300">← Back to Dashboard</a>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
      {/* Back Link */}
      <a href="/" className="text-gray-500 hover:text-indigo-400 text-sm mb-6 inline-block transition-colors">
        ← Back to Jobs
      </a>

      {/* Header Card */}
      <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-8 mb-6">
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{job.title}</h1>
            <p className="text-indigo-400 text-lg font-semibold mb-3">{job.company}</p>
            <div className="flex flex-wrap gap-3 text-sm text-gray-400">
              <span className="flex items-center gap-1">📍 {job.location}</span>
              {job.experience_level && (
                <span className="flex items-center gap-1">🎯 {job.experience_level}</span>
              )}
              <span className="flex items-center gap-1">💼 {job.job_type}</span>
              {job.salary_range && (
                <span className="flex items-center gap-1">💰 {job.salary_range}</span>
              )}
            </div>
          </div>

          {/* Placeholder Match Score */}
          <div className="flex-shrink-0">
            <MatchScore score={0.75} size="lg" />
          </div>
        </div>
      </div>

      {/* Skills */}
      <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 mb-6">
        <h2 className="text-lg font-semibold text-white mb-4">Required Skills</h2>
        <div className="flex flex-wrap gap-2">
          {job.skills_required.map((skill) => (
            <span
              key={skill}
              className="px-3 py-1.5 bg-indigo-500/10 text-indigo-300 text-sm rounded-lg border border-indigo-500/20 hover:bg-indigo-500/20 transition-colors"
            >
              {skill}
            </span>
          ))}
          {job.skills_required.length === 0 && (
            <span className="text-gray-500">No specific skills listed</span>
          )}
        </div>
      </div>

      {/* Description */}
      <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 mb-6">
        <h2 className="text-lg font-semibold text-white mb-4">Job Description</h2>
        <div className="text-gray-300 leading-relaxed whitespace-pre-line text-sm">
          {job.description}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3">
        {job.source_url && (
          <a
            href={job.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 text-center px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-indigo-500/25 transition-all"
          >
            Apply Now →
          </a>
        )}
        <button className="flex-1 px-6 py-3 bg-gray-800 text-gray-300 font-medium rounded-xl border border-white/10 hover:bg-gray-700 transition-all">
          Save Job
        </button>
      </div>
    </div>
  );
}
