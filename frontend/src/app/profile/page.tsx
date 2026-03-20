"use client";

import { useState } from "react";
import { login, register } from "@/lib/api";

export default function ProfilePage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    if (typeof window !== "undefined") {
      return !!localStorage.getItem("token");
    }
    return false;
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      if (isLogin) {
        const data = await login(email, password);
        localStorage.setItem("token", data.access_token);
        setIsAuthenticated(true);
        setSuccess("Logged in successfully!");
      } else {
        await register(email, password, fullName);
        setSuccess("Account created! Please log in.");
        setIsLogin(true);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
    setLoading(false);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setSuccess("Logged out successfully.");
  }

  if (isAuthenticated) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12 animate-fade-in">
        <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-8 text-center">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mx-auto mb-6 text-3xl">
            👤
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Welcome Back!</h1>
          <p className="text-gray-400 mb-8">You are logged in and ready to explore opportunities.</p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            <a
              href="/"
              className="p-4 bg-gray-900/50 rounded-xl border border-white/5 hover:border-indigo-500/30 transition-all text-center"
            >
              <div className="text-2xl mb-2">🎯</div>
              <div className="text-white font-medium text-sm">View Matches</div>
            </a>
            <a
              href="/upload"
              className="p-4 bg-gray-900/50 rounded-xl border border-white/5 hover:border-indigo-500/30 transition-all text-center"
            >
              <div className="text-2xl mb-2">📄</div>
              <div className="text-white font-medium text-sm">Upload Resume</div>
            </a>
            <button
              onClick={handleLogout}
              className="p-4 bg-gray-900/50 rounded-xl border border-white/5 hover:border-red-500/30 transition-all text-center"
            >
              <div className="text-2xl mb-2">🚪</div>
              <div className="text-white font-medium text-sm">Logout</div>
            </button>
          </div>

          {success && (
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-400 text-sm">
              {success}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto px-4 py-12 animate-fade-in">
      <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
        {/* Tabs */}
        <div className="flex rounded-xl bg-gray-900/50 p-1 mb-8">
          <button
            onClick={() => { setIsLogin(true); setError(""); }}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
              isLogin ? "bg-indigo-500 text-white shadow-lg" : "text-gray-400 hover:text-white"
            }`}
          >
            Login
          </button>
          <button
            onClick={() => { setIsLogin(false); setError(""); }}
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
              !isLogin ? "bg-indigo-500 text-white shadow-lg" : "text-gray-400 hover:text-white"
            }`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="text-gray-400 text-sm mb-1 block">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="John Doe"
                required={!isLogin}
                className="w-full bg-gray-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20"
              />
            </div>
          )}

          <div>
            <label className="text-gray-400 text-sm mb-1 block">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="w-full bg-gray-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20"
            />
          </div>

          <div>
            <label className="text-gray-400 text-sm mb-1 block">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              minLength={8}
              className="w-full bg-gray-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20"
            />
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}
          {success && (
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-400 text-sm">
              ✅ {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-indigo-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : isLogin ? "Login" : "Create Account"}
          </button>
        </form>
      </div>
    </div>
  );
}
