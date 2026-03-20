"use client";

import { useEffect, useState } from "react";
import JobCard from "@/components/JobCard";
import FilterBar from "@/components/FilterBar";
import { fetchJobs, fetchRecommendations } from "@/lib/api";

interface Job {
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

interface JobMatch {
  job: Job;
  match_score: number;
  skill_match_score: number;
  similarity_score: number;
  experience_match_score: number;
}

export default function Dashboard() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [recommendations, setRecommendations] = useState<JobMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"recommendations" | "all">("recommendations");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const jobData = await fetchJobs();
      setJobs(jobData);

      // Try to get recommendations (requires auth)
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const recData = await fetchRecommendations(token);
          setRecommendations(recData);
        } catch {
          // User not authenticated or no profile
        }
      }
    } catch (error) {
      console.error("Failed to load data:", error);
    }
    setLoading(false);
  }

  function handleFilter(filters: { location: string; role: string; experience_level: string; posted_within_hours?: number }) {
    setLoading(true);
    fetchJobs(filters)
      .then(setJobs)
      .finally(() => setLoading(false));
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
          Find Your{" "}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Perfect Match
          </span>
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          AI-powered job recommendations tailored to your skills, experience, and career goals.
        </p>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8 animate-fade-in">
        {[
          { label: "Total Jobs", value: jobs.length, icon: "💼" },
          { label: "Matches", value: recommendations.length, icon: "🎯" },
          { label: "High Match", value: recommendations.filter((r) => r.match_score >= 0.8).length, icon: "🔥" },
          { label: "New Today", value: Math.min(jobs.length, 5), icon: "✨" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-xl p-4 text-center"
          >
            <div className="text-2xl mb-1">{stat.icon}</div>
            <div className="text-2xl font-bold text-white">{stat.value}</div>
            <div className="text-gray-500 text-xs">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="mb-6">
        <FilterBar onFilter={handleFilter} />
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab("recommendations")}
          className={`px-5 py-2 rounded-xl text-sm font-medium transition-all ${
            activeTab === "recommendations"
              ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
              : "text-gray-500 hover:text-gray-300 border border-transparent"
          }`}
        >
          🎯 Recommendations
        </button>
        <button
          onClick={() => setActiveTab("all")}
          className={`px-5 py-2 rounded-xl text-sm font-medium transition-all ${
            activeTab === "all"
              ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
              : "text-gray-500 hover:text-gray-300 border border-transparent"
          }`}
        >
          💼 All Jobs
        </button>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-10 h-10 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
        </div>
      ) : activeTab === "recommendations" ? (
        recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((rec) => (
              <JobCard
                key={rec.job.id}
                id={rec.job.id}
                title={rec.job.title}
                company={rec.job.company}
                location={rec.job.location}
                description={rec.job.description}
                skills_required={rec.job.skills_required}
                experience_level={rec.job.experience_level}
                match_score={rec.match_score}
                skill_match_score={rec.skill_match_score}
                similarity_score={rec.similarity_score}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📄</div>
            <h3 className="text-white text-xl font-semibold mb-2">No recommendations yet</h3>
            <p className="text-gray-500 mb-6">Upload your resume to get personalized job matches</p>
            <a
              href="/upload"
              className="inline-flex px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-indigo-500/25 transition-all"
            >
              Upload Resume →
            </a>
          </div>
        )
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              id={job.id}
              title={job.title}
              company={job.company}
              location={job.location}
              description={job.description}
              skills_required={job.skills_required}
              experience_level={job.experience_level}
            />
          ))}
          {jobs.length === 0 && (
            <div className="col-span-full text-center py-20">
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-white text-xl font-semibold mb-2">No jobs found</h3>
              <p className="text-gray-500">Try adjusting your filters</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
