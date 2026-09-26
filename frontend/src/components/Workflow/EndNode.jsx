import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Square } from 'lucide-react';

export default function EndNode(props) {
  const data = props.data || props;
  const label = data?.label || 'End';
  const description = data?.description || '';

  return (
    <div className="bg-white border border-rose-200/90 rounded-xl shadow-sm px-3.5 py-2.5 flex items-center gap-2.5 min-w-[120px] hover:shadow-md transition-all duration-200 group">
      <Handle
        type="target"
        position={Position.Left}
        className="!w-2.5 !h-2.5 !bg-rose-500 !border-2 !border-white"
      />
      <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-100 text-rose-600 flex items-center justify-center">
        <Square className="w-4 h-4 fill-rose-600" />
      </div>
      <div className="flex flex-col text-left">
        <span className="text-xs font-semibold text-slate-800 leading-tight">{label}</span>
        {description && (
          <span className="text-[10px] font-medium text-slate-400 leading-tight mt-0.5">
            {description}
          </span>
        )}
      </div>
    </div>
  );
}
