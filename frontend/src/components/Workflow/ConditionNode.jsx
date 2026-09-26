import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { GitFork } from 'lucide-react';

export default function ConditionNode(props) {
  const data = props.data || props;
  const label = data?.label || 'Condition';
  const description = data?.description || '';

  return (
    <div className="bg-white border border-amber-200/90 rounded-xl shadow-sm px-3.5 py-2.5 flex items-center gap-3 min-w-[220px] hover:shadow-md transition-all duration-200 group">
      <Handle
        type="target"
        position={Position.Left}
        className="!w-2.5 !h-2.5 !bg-amber-500 !border-2 !border-white"
      />
      <div className="p-2.5 rounded-lg bg-amber-50 border border-amber-100 text-amber-600 flex items-center justify-center">
        <GitFork className="w-5 h-5 rotate-90" />
      </div>
      <div className="flex flex-col text-left">
        <span className="text-xs font-semibold text-slate-800 leading-tight">{label}</span>
        {description && (
          <span className="text-[11px] font-medium text-amber-700 leading-tight mt-0.5 max-w-[160px] truncate">
            ({description})
          </span>
        )}
      </div>
      <Handle
        type="source"
        position={Position.Right}
        className="!w-2.5 !h-2.5 !bg-amber-500 !border-2 !border-white"
      />
    </div>
  );
}
