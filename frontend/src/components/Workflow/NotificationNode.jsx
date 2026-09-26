import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { MessageSquare, Send, Mail } from 'lucide-react';

export default function NotificationNode(props) {
  const data = props.data || props;
  const label = data?.label || 'Notification';
  const description = data?.description || '';

  const getIcon = () => {
    const l = (label || '').toLowerCase();
    if (l.includes('telegram')) return <Send className="w-5 h-5 text-purple-600" />;
    if (l.includes('email') || l.includes('gmail')) return <Mail className="w-5 h-5 text-purple-600" />;
    return <MessageSquare className="w-5 h-5 text-purple-600" />;
  };

  return (
    <div className="bg-white border border-slate-200/90 rounded-xl shadow-sm px-3.5 py-2.5 flex items-center gap-3 min-w-[210px] hover:shadow-md transition-all duration-200 group">
      <Handle
        type="target"
        position={Position.Left}
        className="!w-2.5 !h-2.5 !bg-purple-500 !border-2 !border-white"
      />
      <div className="p-2.5 rounded-lg bg-purple-50 border border-purple-100 text-purple-600 flex items-center justify-center">
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
        className="!w-2.5 !h-2.5 !bg-purple-500 !border-2 !border-white"
      />
    </div>
  );
}
