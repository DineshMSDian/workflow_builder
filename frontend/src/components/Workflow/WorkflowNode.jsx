/**
 * Workflow Node — large, vertical, icon-forward design.
 *
 * Layout:
 * ┌──────────────────────────┐
 * │  ═══ color accent bar ═══│
 * │                          │
 * │      ┌──────────┐        │
 * │      │          │        │
 * │      │  [ICON]  │  ← 48 px icon in 64 px container
 * │      │          │        │
 * │      └──────────┘        │
 * │                          │
 * │      Title Text          │
 * │     (description)        │
 * │     ╌╌ type badge ╌╌     │
 * └──────────────────────────┘
 */

import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { getNodeIcon } from '../../utils/iconMap';

/* human-friendly type labels */
const TYPE_LABELS = {
  trigger:      'Trigger',
  filter:       'Filter',
  action:       'Action',
  condition:    'Condition',
  notification: 'Notify',
  end:          'End',
};

export default function WorkflowNode({ id, type, data }) {
  const label       = data?.label       || '';
  const description = data?.description || '';
  const service     = data?.service     || '';

  const { icon: Icon, color, bg } = getNodeIcon(type, service, label);

  const isEnd       = type === 'end';
  const isTrigger   = type === 'trigger';
  const isCondition = type === 'condition';

  return (
    <div className="group relative">
      {/* ── Target handle ── */}
      {!isTrigger && (
        <Handle
          type="target"
          position={Position.Left}
          className="!w-3 !h-3 !border-[2.5px] !border-white !-left-1.5 !shadow-sm"
          style={{ background: color }}
        />
      )}

      {/* ── Card ── */}
      <div
        className={`
          bg-white rounded-2xl border border-gray-200/90
          shadow-[0_2px_12px_rgba(0,0,0,0.06)]
          group-hover:shadow-[0_4px_20px_rgba(0,0,0,0.10)]
          transition-all duration-250 ease-out
          group-hover:-translate-y-0.5
          flex flex-col items-center text-center
          w-[160px] overflow-hidden
        `}
      >
        {/* ── Top accent bar ── */}
        <div
          className="w-full h-[3px]"
          style={{ background: `linear-gradient(90deg, ${color}88, ${color})` }}
        />

        {/* ── Icon container ── */}
        <div className="pt-4 pb-2">
          <div className="relative">
            {/* pulse ring on trigger */}
            {isTrigger && (
              <div
                className="absolute inset-0 rounded-2xl animate-ping opacity-20"
                style={{ background: bg }}
              />
            )}
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center
                         shadow-sm transition-transform duration-200 group-hover:scale-105"
              style={{
                background: `linear-gradient(135deg, ${bg}, ${bg}dd)`,
                border: `1.5px solid ${color}22`,
              }}
            >
              <Icon
                className="w-8 h-8"
                style={{ color }}
                strokeWidth={1.8}
              />
            </div>
          </div>
        </div>

        {/* ── Text ── */}
        <div className="px-3 pb-1">
          <p className="text-[13px] font-bold text-gray-800 leading-snug">
            {label}
          </p>
          {description && (
            <p
              className="text-[11px] text-gray-500 leading-snug mt-0.5 line-clamp-2"
              title={description}
            >
              {description}
            </p>
          )}
        </div>

        {/* ── Type badge ── */}
        <div className="pb-3 pt-1.5">
          <span
            className="inline-flex items-center gap-1 text-[9px] font-semibold
                       uppercase tracking-wider px-2.5 py-[3px] rounded-full"
            style={{
              color: color,
              background: `${bg}`,
              border: `1px solid ${color}20`,
            }}
          >
            <span
              className="w-1.5 h-1.5 rounded-full"
              style={{ background: color }}
            />
            {TYPE_LABELS[type] || type}
          </span>
        </div>
      </div>

      {/* ── Source handle ── */}
      {!isEnd && (
        <Handle
          type="source"
          position={Position.Right}
          className="!w-3 !h-3 !border-[2.5px] !border-white !-right-1.5 !shadow-sm"
          style={{ background: color }}
        />
      )}
    </div>
  );
}
