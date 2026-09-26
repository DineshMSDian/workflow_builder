import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { FileText, Cpu, Database } from 'lucide-react';

export default function ActionNode(props) {
  const data = props.data || props;
  const label = data?.label || 'Action';
  const description = data?.description || '';

  const getIcon = () => {
    const l = (label || '').toLowerCase();
    if (l.includes('extract') || l.includes('invoice') || l.includes('file')) return <FileText className="w-5 h-5 text-sky-600" />;
    if (l.includes('db') || l.includes('sheet') || l.includes('drive')) return <Database className="w-5 h-5 text-sky-600" />;
    return <Cpu className="w-5 h-5 text-sky-600" />;
  };

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl shadow-sm px-3.5 py-2.5 flex items-center gap-3 min-w-[210px] hover:shadow-md transition-all duration-200 group">
      <Handle
        type="target"
        position={Position.Left}
        className="!w-2.5 !h-2.5 !bg-sky-500 !border-2 !border-white"
      />
      <div className="p-2.5 rounded-lg bg-sky-50 border border-sky-100 text-sky-600 flex items-center justify-center">
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
        className="!w-2.5 !h-2.5 !bg-sky-500 !border-2 !border-white"
      />
    </div>
  );
}
