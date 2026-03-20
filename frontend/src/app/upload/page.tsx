"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import { uploadResume } from "@/lib/api";

interface ParsedData {
  skills: string[];
  experience: string;
  education: string[];
}

export default function UploadPage() {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{
    message: string;
    filename: string;
    parsed_data: ParsedData;
  } | null>(null);
  const [error, setError] = useState("");

  async function handleUpload(file: File) {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please log in first to upload your resume.");
      return;
    }

    setUploading(true);
    setError("");
    setResult(null);

    try {
      const data = await uploadResume(file, token);
      setResult(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    }
    setUploading(false);
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-10 animate-fade-in">
        <h1 className="text-3xl font-bold text-white mb-3">
          Upload Your{" "}
          <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Resume
          </span>
        </h1>
        <p className="text-gray-400">
          Our AI will parse your resume and match you with the best jobs
        </p>
      </div>

      {/* Upload Component */}
      <div className="mb-8 animate-fade-in">
        <FileUpload onFileSelect={handleUpload} uploading={uploading} />
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 mb-6 text-red-400 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="animate-fade-in space-y-6">
          {/* Success Banner */}
          <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4 text-emerald-400 text-sm">
            ✅ {result.message} — <span className="text-emerald-300 font-medium">{result.filename}</span>
          </div>

          {/* Parsed Data */}
          <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 space-y-6">
            <h2 className="text-xl font-semibold text-white">Parsed Resume Data</h2>

            {/* Skills */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
                <span>🛠️</span> Skills ({result.parsed_data.skills.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.parsed_data.skills.map((skill) => (
                  <span
                    key={skill}
                    className="px-3 py-1 bg-indigo-500/15 text-indigo-300 text-sm rounded-lg border border-indigo-500/20"
                  >
                    {skill}
                  </span>
                ))}
                {result.parsed_data.skills.length === 0 && (
                  <span className="text-gray-500 text-sm">No skills detected</span>
                )}
              </div>
            </div>

            {/* Experience */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                <span>💼</span> Experience
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed bg-gray-900/30 rounded-lg p-3 whitespace-pre-line">
                {result.parsed_data.experience || "No experience data detected"}
              </p>
            </div>

            {/* Education */}
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                <span>🎓</span> Education
              </h3>
              <ul className="space-y-1">
                {result.parsed_data.education.map((edu, i) => (
                  <li
                    key={i}
                    className="text-gray-300 text-sm bg-gray-900/30 rounded-lg px-3 py-2"
                  >
                    {edu}
                  </li>
                ))}
                {result.parsed_data.education.length === 0 && (
                  <li className="text-gray-500 text-sm">No education data detected</li>
                )}
              </ul>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <a
              href="/"
              className="inline-flex px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-indigo-500/25 transition-all"
            >
              View Your Matches →
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
