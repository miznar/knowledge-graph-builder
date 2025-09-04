"use client";
import { useState } from "react";
import { motion } from "framer-motion";

export default function Home() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [graphAvailable, setGraphAvailable] = useState(false); // ✅ Track if graph is ready

  // 📂 Upload PDF
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/ingest", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      alert(data.message); // show success message

      if (data.knowledge_graph) {
        setGraphAvailable(true); // ✅ Show graph button
      }
    } catch (err) {
      console.error(err);
      alert("⚠️ Error uploading PDF");
    }

    setUploading(false);
  };

  // 💬 Send query to backend
  const sendQuery = async () => {
    if (!query.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 3 }),
      });

      const data = await res.json();

      if (data.answer) {
        setMessages((prev) => [...prev, { role: "bot", content: data.answer }]);
      } else {
        setMessages((prev) => [...prev, { role: "bot", content: "No results found." }]);
      }

    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { role: "bot", content: "⚠️ Error connecting to backend" }]);
    }

    setLoading(false);
    setQuery("");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-6">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl font-extrabold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text"
      >
        📚 Knowledge Graph Chat
      </motion.h1>

      {/* PDF Upload */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="mb-6 w-full max-w-2xl"
      >
        <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-blue-400 rounded-xl bg-white/10 hover:bg-white/20 transition cursor-pointer">
          <span className="text-blue-300"> Upload PDF</span>
          <input type="file" accept="application/pdf" onChange={handleUpload} className="hidden" />
        </label>
        {uploading && <p className="mt-2 text-sm text-blue-300">⏳ Uploading...</p>}

        {/* Show Graph button only after upload */}
        {graphAvailable && (
          <button
            onClick={() => window.open("http://127.0.0.1:8000/graph", "_blank")}
            className="mt-3 bg-gradient-to-r from-green-400 to-teal-500 text-white px-5 py-2 rounded-xl shadow hover:opacity-90 transition"
          >
            🌐 View Knowledge Graph
          </button>
        )}
      </motion.div>

      {/* Chat UI */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-2xl bg-white/10 backdrop-blur-xl rounded-2xl shadow-lg p-6 flex flex-col space-y-4 border border-white/20"
      >
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto max-h-[60vh] space-y-3 pr-2">
          {messages.map((msg, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: msg.role === "user" ? 50 : -50 }}
              animate={{ opacity: 1, x: 0 }}
              className={`p-3 rounded-xl max-w-[75%] whitespace-pre-line ${
                msg.role === "user"
                  ? "ml-auto bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-md"
                  : "mr-auto bg-gray-200 text-gray-900"
              }`}
            >
              {msg.content}
            </motion.div>
          ))}
        </div>

        {/* Input box */}
        <div className="flex space-x-2">
          <input
            type="text"
            className="flex-1 border border-gray-500 bg-gray-900/50 rounded-xl p-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Ask a question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendQuery()}
          />
          <button
            onClick={sendQuery}
            disabled={loading}
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-5 py-2 rounded-xl shadow hover:opacity-90 transition disabled:opacity-50"
          >
            {loading ? "⏳" : "Send"}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
