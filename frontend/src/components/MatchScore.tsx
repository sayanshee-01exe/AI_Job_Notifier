"use client";

interface MatchScoreProps {
  score: number; // 0-1
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
}

export default function MatchScore({
  score,
  size = "md",
  showLabel = true,
}: MatchScoreProps) {
  const percent = Math.round(score * 100);

  const sizeClasses = {
    sm: { ring: "w-16 h-16", text: "text-lg", label: "text-xs" },
    md: { ring: "w-24 h-24", text: "text-2xl", label: "text-sm" },
    lg: { ring: "w-32 h-32", text: "text-3xl", label: "text-base" },
  };

  const { ring, text, label } = sizeClasses[size];

  // SVG circle params
  const radius = size === "sm" ? 26 : size === "md" ? 40 : 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score * circumference);

  const color =
    percent >= 80
      ? "#10b981"
      : percent >= 60
      ? "#f59e0b"
      : "#ef4444";

  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`${ring} relative`}>
        <svg className="w-full h-full -rotate-90" viewBox={`0 0 ${(radius + 6) * 2} ${(radius + 6) * 2}`}>
          {/* Background circle */}
          <circle
            cx={radius + 6}
            cy={radius + 6}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="6"
          />
          {/* Score arc */}
          <circle
            cx={radius + 6}
            cy={radius + 6}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className={`absolute inset-0 flex items-center justify-center ${text} font-bold text-white`}>
          {percent}%
        </div>
      </div>
      {showLabel && (
        <span className={`${label} text-gray-400 font-medium`}>
          {percent >= 80 ? "Excellent Match" : percent >= 60 ? "Good Match" : "Fair Match"}
        </span>
      )}
    </div>
  );
}
