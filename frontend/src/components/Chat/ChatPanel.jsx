import React, { useRef, useEffect } from 'react';
import Message from './Message';
import ChatInput from './ChatInput';
import { Bot, RefreshCw, MessageSquare } from 'lucide-react';

export default function ChatPanel({
  messages,
  extractedInfo,
  onSendMessage,
  onResetSession,
  isLoading,
}) {
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col h-full bg-[#181816] border-r border-[#282724]">
      {/* ── Header ── */}
      <div className="px-5 py-3.5 border-b border-[#282724] flex items-center justify-between bg-[#1f1e1c]/90 backdrop-blur">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-[#da7756]/15 text-[#da7756] border border-[#da7756]/30">
            <MessageSquare className="w-4 h-4" />
          </div>
          <div className="flex flex-col text-left">
            <h2 className="text-xs font-bold text-[#f4f3ee] tracking-tight">Automation Assistant</h2>
            <p className="text-[10px] text-[#a19f97]">Conversational Clarification</p>
          </div>
        </div>

        <button
          onClick={onResetSession}
          title="Reset Chat & Workflow"
          className="p-1.5 rounded-lg text-[#a19f97] hover:text-[#f4f3ee] hover:bg-[#282724] transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* ── Message List ── */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <Message
            key={index}
            message={msg}
            extractedInfo={index === messages.length - 1 ? extractedInfo : null}
          />
        ))}

        {isLoading && (
          <div className="flex gap-3 items-start">
            <div className="w-8 h-8 rounded-xl bg-[#da7756] text-white flex items-center justify-center shrink-0 shadow-sm">
              <Bot className="w-4 h-4" />
            </div>
            <div className="px-4 py-3 rounded-2xl bg-[#242320] border border-[#33312d] rounded-tl-xs flex items-center gap-1.5 shadow-xs">
              <span className="w-1.5 h-1.5 bg-[#da7756] rounded-full animate-bounce" />
              <span className="w-1.5 h-1.5 bg-[#da7756] rounded-full animate-bounce [animation-delay:0.2s]" />
              <span className="w-1.5 h-1.5 bg-[#da7756] rounded-full animate-bounce [animation-delay:0.4s]" />
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* ── Input ── */}
      <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} />
    </div>
  );
}
