import React, { useEffect } from 'react';
import {
  ReactFlow,
  Controls,
  useNodesState,
  useEdgesState,
  useReactFlow,
  ReactFlowProvider,
} from '@xyflow/react';

import WorkflowNode from './WorkflowNode';
import { layoutWorkflow } from '../../utils/workflowLayout';
import { Sparkles, AlertCircle, Cpu, Play } from 'lucide-react';

/* Register node types */
const nodeTypes = {
  trigger:      WorkflowNode,
  filter:       WorkflowNode,
  action:       WorkflowNode,
  condition:    WorkflowNode,
  notification: WorkflowNode,
  end:          WorkflowNode,
};

/* ── Blueprint Watermark Background Component (White/Light Mode Schematic) ── */
function BlueprintBackground() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden select-none z-0">
      {/* ── Blueprint Grid ── */}
      <svg className="absolute inset-0 w-full h-full opacity-60">
        <defs>
          <pattern id="small-grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e2e8f0" strokeWidth="0.8" />
          </pattern>
          <pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse">
            <rect width="100" height="100" fill="url(#small-grid)" />
            <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#cbd5e1" strokeWidth="1.2" />
          </pattern>
          <pattern id="dots" width="40" height="40" patternUnits="userSpaceOnUse">
            <circle cx="20" cy="20" r="1.2" fill="#94a3b8" opacity="0.4" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        <rect width="100%" height="100%" fill="url(#dots)" />
      </svg>

      {/* ── Blueprint Technical Drafting Artwork (Right-Bottom Corner) ── */}
      <svg
        className="absolute right-0 bottom-0 w-[850px] h-[850px] opacity-[0.14] text-blue-600"
        viewBox="0 0 800 800"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Concentric Calibration Rings */}
        <circle cx="550" cy="550" r="380" stroke="currentColor" strokeWidth="1.5" strokeDasharray="6 4" />
        <circle cx="550" cy="550" r="320" stroke="currentColor" strokeWidth="2" />
        <circle cx="550" cy="550" r="260" stroke="currentColor" strokeWidth="1.2" />
        <circle cx="550" cy="550" r="180" stroke="currentColor" strokeWidth="2" strokeDasharray="12 6" />
        <circle cx="550" cy="550" r="80" stroke="currentColor" strokeWidth="1.5" />

        {/* Technical Gear teeth */}
        <g transform="translate(550, 550)">
          {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((deg) => (
            <rect
              key={deg}
              x="-14"
              y="-335"
              width="28"
              height="35"
              rx="4"
              fill="currentColor"
              transform={`rotate(${deg})`}
            />
          ))}
        </g>

        {/* Blueprint Curved Text Path */}
        <path
          id="text-path-curved"
          d="M 230 550 A 320 320 0 0 1 870 550"
          fill="none"
        />
        <text className="font-mono text-3xl font-black tracking-[0.25em] fill-current uppercase">
          <textPath href="#text-path-curved" startOffset="5%">
            AUTOMATION AI WORKFLOW
          </textPath>
        </text>

        {/* Blueprint Technical Lines & Measurement Markers */}
        <line x1="550" y1="0" x2="550" y2="800" stroke="currentColor" strokeWidth="1" strokeDasharray="4 4" />
        <line x1="0" y1="550" x2="800" y2="550" stroke="currentColor" strokeWidth="1" strokeDasharray="4 4" />

        {/* Dimension Arrow & Specs */}
        <line x1="180" y1="230" x2="480" y2="230" stroke="currentColor" strokeWidth="1.5" />
        <path d="M 180 230 L 195 224 L 195 236 Z" fill="currentColor" />
        <path d="M 480 230 L 465 224 L 465 236 Z" fill="currentColor" />
        <text x="330" y="220" textAnchor="middle" className="font-mono text-xs font-bold fill-current tracking-widest">
          R-320.00mm // AI_SCHEMA
        </text>

        {/* Technical Hatching Lines */}
        {[0, 20, 40, 60, 80, 100, 120].map((offset) => (
          <line
            key={offset}
            x1={450 + offset}
            y1={650}
            x2={550 + offset}
            y2={750}
            stroke="currentColor"
            strokeWidth="1"
          />
        ))}
      </svg>

      {/* ── Top Left Blueprint Technical Stamp ── */}
      <div className="absolute top-5 left-6 text-slate-400 font-mono text-[10px] tracking-wider leading-relaxed opacity-70">
        <p className="font-bold text-slate-600">SYS // AUTOMATION_AI_WORKFLOW_v1.0</p>
        <p>SCALE: 1:1 • NODE CANVAS LAYOUT</p>
        <p>STATUS: AGENT READY</p>
      </div>

      {/* ── Bottom Left Blueprint Scale Marker ── */}
      <div className="absolute bottom-5 left-6 flex items-center gap-3 text-slate-400 font-mono text-[10px] opacity-70">
        <div className="flex items-center gap-1">
          <div className="w-8 h-2 border border-slate-400 border-t-0 border-b-0 flex">
            <div className="w-1/2 h-full bg-slate-400" />
          </div>
          <span>100px</span>
        </div>
        <span>•</span>
        <span>AUTONOMOUS ENGINE</span>
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────────────────── */
function FlowCanvas({ rawWorkflow, isBuilding, error }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { fitView } = useReactFlow();

  /* Re-layout whenever backend sends a new workflow */
  useEffect(() => {
    if (!rawWorkflow?.nodes?.length) {
      setNodes([]);
      setEdges([]);
      return;
    }

    const { nodes: laid, edges: styled } = layoutWorkflow(
      rawWorkflow.nodes,
      rawWorkflow.edges,
      'LR',
    );

    setNodes(laid);
    setEdges(styled);

    /* Fit after DOM paint */
    requestAnimationFrame(() => {
      setTimeout(() => fitView({ padding: 0.4, duration: 400 }), 40);
    });
  }, [rawWorkflow, fitView, setNodes, setEdges]);

  return (
    <div className="w-full h-full relative rounded-2xl overflow-hidden flex flex-col bg-white border border-gray-200 shadow-sm">

      {/* ── Light Blueprint Background ── */}
      <BlueprintBackground />

      {/* ── Top Badge Pill ── */}
      <div className="absolute top-4 left-5 z-10 flex items-center gap-2">
        <span className="inline-flex items-center gap-2 text-xs font-semibold
                         text-[#da7756] bg-white/90 backdrop-blur border border-[#da7756]/30
                         px-3.5 py-1.5 rounded-full shadow-xs">
          <Sparkles className="w-3.5 h-3.5 text-[#da7756]" />
          {rawWorkflow ? 'Generated AI Workflow' : 'AI Automation Canvas'}
        </span>
      </div>

      {/* ── States ── */}
      {error ? (
        <div className="relative z-10 flex-1 flex flex-col items-center justify-center gap-2.5 text-center p-6 bg-white/60 backdrop-blur-xs">
          <AlertCircle className="w-10 h-10 text-rose-500" />
          <p className="text-sm font-bold text-gray-800">Unable to render workflow</p>
          <p className="text-xs text-gray-500 max-w-sm">{error}</p>
        </div>
      ) : !rawWorkflow && !isBuilding ? (
        /* ── Initial Clean Blueprint View (No generic workflow loaded) ── */
        <div className="relative z-10 flex-1 flex flex-col items-center justify-center p-8 text-center">
          <div className="bg-white/90 backdrop-blur-md p-8 rounded-2xl border border-slate-200/90 shadow-md max-w-md flex flex-col items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-[#da7756]/10 border border-[#da7756]/30 flex items-center justify-center">
              <Cpu className="w-7 h-7 text-[#da7756]" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-800 tracking-tight">
                Automation Canvas Ready
              </h3>
              <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
                Describe your workflow in the chat panel on the left. The AI agent will ask clarification questions and render your custom blueprint workflow diagram here.
              </p>
            </div>
            <div className="flex items-center gap-2 text-[11px] font-semibold text-[#da7756] bg-[#da7756]/10 px-3 py-1.5 rounded-full">
              <Play className="w-3 h-3 fill-current" />
              Start by typing your automation request
            </div>
          </div>
        </div>
      ) : isBuilding && !rawWorkflow ? (
        <div className="relative z-10 flex-1 flex flex-col items-center justify-center gap-3 p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-3 border-[#da7756]/20 border-t-[#da7756]" />
          <p className="text-xs font-semibold text-slate-600">Generating AI Workflow Blueprint…</p>
        </div>
      ) : (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          minZoom={0.3}
          maxZoom={1.8}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          proOptions={{ hideAttribution: true }}
          className="z-15"
        >
          <Controls showInteractive={false} position="bottom-right" />
        </ReactFlow>
      )}
    </div>
  );
}

export default function WorkflowCanvas(props) {
  return (
    <ReactFlowProvider>
      <FlowCanvas {...props} />
    </ReactFlowProvider>
  );
}
