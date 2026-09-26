import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

export default function ChatInput({ onSendMessage, isLoading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-[#282724] bg-[#1f1e1c]/90 backdrop-blur">
      <div className="relative flex items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your automation or answer..."
          disabled={isLoading}
          className="w-full bg-[#252421] text-[#f4f3ee] placeholder-[#8a8880] text-xs rounded-xl pl-4 pr-12 py-3 border border-[#363430] focus:outline-none focus:border-[#da7756] focus:ring-1 focus:ring-[#da7756]/40 transition-all disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="absolute right-2 p-2 rounded-lg bg-[#da7756] hover:bg-[#c86849] text-white disabled:opacity-40 disabled:hover:bg-[#da7756] transition-colors shadow-xs"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </div>
    </form>
  );
}
