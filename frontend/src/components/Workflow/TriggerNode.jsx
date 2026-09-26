import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Zap, Mail, Database, Globe, Layers } from 'lucide-react';

export default function TriggerNode(props) {
  const data = props.data || props;
  const label = data?.label || 'Trigger';
  const description = data?.description || '';

  const getIcon = () => {
    const l = (label || '').toLowerCase();
    if (l.includes('gmail') || l.includes('email')) return <Mail className="w-5 h-5 text-red-500" />;
    if (l.includes('db') || l.includes('database')) return <Database className="w-5 h-5 text-blue-500" />;
    if (l.includes('webhook') || l.includes('api')) return <Globe className="w-5 h-5 text-purple-500" />;
    if (l.includes('clash')) return <Layers className="w-5 h-5 text-amber-500" />;
    return <Zap className="w-5 h-5 text-amber-500" />;
  };

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl shadow-sm px-3.5 py-2.5 flex items-center gap-3 min-w-[210px] hover:shadow-md transition-all duration-200 group">
      <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 group-hover:bg-slate-100/80 transition-colors flex items-center justify-center">
        {getIcon()}
      </div>
      <div className="flex flex-col text-left">
        <span className="text-xs font-semibold text-slate-800 leading-tight">{label}</span>
        {description && (
          <span className="text-[11px] font-medium text-slate-500 leading-tight mt-0.5">
            ({description})
          </span>
        )}
      </div>
      <Handle
        type="source"
        position={Position.Right}
        className="!w-2.5 !h-2.5 !bg-blue-500 !border-2 !border-white"
      />
    </div>
  );
}
