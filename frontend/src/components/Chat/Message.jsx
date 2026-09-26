import React from 'react';
import { Bot, User, CheckCircle2, Circle } from 'lucide-react';

const FIELD_LABELS = {
  trigger_source: 'Trigger Source',
  trigger_event: 'Trigger Event',
  condition: 'Condition',
  action: 'Action',
  destination: 'Destination',
  notification_channel: 'Notification Channel',
  duplicate_handling: 'Duplicate Handling',
};

export default function Message({ message, extractedInfo }) {
  const isBot = message.role === 'assistant';

  return (
    <div className={`flex gap-3 text-left ${isBot ? 'items-start' : 'items-start flex-row-reverse'}`}>
      <div
        className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs font-semibold shadow-xs ${
          isBot
            ? 'bg-[#da7756] text-white'
            : 'bg-[#2a2926] text-[#e0ded8] border border-[#3a3834]'
        }`}
      >
        {isBot ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
      </div>

      <div className={`flex flex-col max-w-[85%] ${isBot ? 'items-start' : 'items-end'}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-[11px] font-semibold text-[#a19f97]">
            {isBot ? 'Workflow Assistant' : 'You'}
          </span>
        </div>

        <div
          className={`px-4 py-3 rounded-2xl text-xs leading-relaxed ${
            isBot
              ? 'bg-[#242320] text-[#f4f3ee] border border-[#33312d] shadow-xs rounded-tl-xs'
              : 'bg-[#da7756] text-white shadow-xs rounded-tr-xs font-medium'
          }`}
        >
          {message.content}

          {/* Show Collected Info checklist table on bot's latest message if available */}
          {isBot && extractedInfo && Object.keys(extractedInfo).length > 0 && (
            <div className="mt-3 pt-3 border-t border-[#363430] w-full text-[11px]">
              <div className="font-semibold text-[#e5e3dc] mb-2 flex items-center gap-1.5">
                <span>Information Checklist</span>
              </div>
              <div className="grid grid-cols-1 gap-1.5">
                {Object.entries(FIELD_LABELS).map(([field, label]) => {
                  const val = extractedInfo[field];
                  return (
                    <div key={field} className="flex items-center gap-1.5 text-[#b4b2a9]">
                      {val ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      ) : (
                        <Circle className="w-3.5 h-3.5 text-[#52504a] shrink-0" />
                      )}
                      <span className={val ? 'text-[#f4f3ee] font-medium' : 'text-[#737169]'}>
                        {label}: {val || 'Pending'}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
