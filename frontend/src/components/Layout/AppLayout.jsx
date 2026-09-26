import React from 'react';
import { Workflow, Layers, Cpu } from 'lucide-react';

export default function AppLayout({ chatPanel, workflowCanvas }) {
  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#141413] text-[#f4f3ee] select-none font-sans">
      {/* ── Top Header ── */}
      <header className="h-13 border-b border-[#282724] bg-[#1a1917]/95 px-5 flex items-center justify-between shrink-0 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded-xl bg-[#da7756] text-white shadow-sm flex items-center justify-center">
            <Workflow className="w-4 h-4" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold tracking-tight text-[#f4f3ee]">
              Workflow Builder
            </span>
            <span className="text-[10px] font-semibold bg-[#da7756]/15 text-[#da7756] border border-[#da7756]/30 px-2.5 py-0.5 rounded-full">
              Conversational Agent
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-medium text-[#a19f97]">
          <Cpu className="w-3.5 h-3.5 text-[#da7756]" />
          <span>AI Workflow Engine & Blueprint Canvas</span>
        </div>
      </header>

      {/* ── Main Split Panels ── */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Left Chat Panel (35% on desktop) */}
        <div className="w-full md:w-[38%] lg:w-[35%] h-1/2 md:h-full shrink-0">
          {chatPanel}
        </div>

        {/* Right Workflow Canvas (65% on desktop) */}
        <div className="w-full md:w-[62%] lg:w-[65%] h-1/2 md:h-full p-3 bg-[#141413] overflow-hidden flex flex-col">
          {workflowCanvas}
        </div>
      </div>
    </div>
  );
}
