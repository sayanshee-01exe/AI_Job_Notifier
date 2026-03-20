"use client";

import { useCallback, useState } from "react";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  uploading?: boolean;
}

export default function FileUpload({
  onFileSelect,
  accept = ".pdf,.docx",
  uploading = false,
}: FileUploadProps) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    },
    [onFileSelect]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    },
    [onFileSelect]
  );

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
        dragOver
          ? "border-indigo-400 bg-indigo-500/10 scale-[1.01]"
          : "border-white/10 bg-gray-800/30 hover:border-white/20 hover:bg-gray-800/50"
      }`}
    >
      {uploading ? (
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
          <p className="text-indigo-300 font-medium">Parsing your resume...</p>
        </div>
      ) : (
        <>
          <div className="text-5xl mb-4">📄</div>
          <p className="text-white font-semibold text-lg mb-1">
            {selectedFile ? selectedFile.name : "Drop your resume here"}
          </p>
          <p className="text-gray-500 text-sm mb-6">
            {selectedFile
              ? `${(selectedFile.size / 1024).toFixed(1)} KB`
              : "Supports PDF and DOCX files"}
          </p>
          <label className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-xl cursor-pointer hover:shadow-lg hover:shadow-indigo-500/25 transition-all duration-300 hover:scale-105">
            <span>Browse Files</span>
            <input
              type="file"
              accept={accept}
              onChange={handleFileInput}
              className="hidden"
            />
          </label>
        </>
      )}
    </div>
  );
}
