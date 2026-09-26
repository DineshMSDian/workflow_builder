import dagre from '@dagrejs/dagre';
import { MarkerType } from '@xyflow/react';

const NODE_WIDTH  = 180;
const NODE_HEIGHT = 170;

/**
 * Auto-layout workflow nodes using Dagre (Left → Right).
 *
 * Converts raw backend JSON (flat {id, type, label, …} objects)
 * into properly positioned React Flow nodes with `data` payloads,
 * and styled edges with arrowheads and branch labels.
 */
export function layoutWorkflow(rawNodes = [], rawEdges = [], direction = 'LR') {
  if (!rawNodes.length) return { nodes: [], edges: [] };

  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({
    rankdir:  direction,
    ranksep:  130,   // horizontal gap between ranks
    nodesep:  70,    // vertical gap between nodes in same rank
    marginx:  80,
    marginy:  60,
  });

  /* ── Register nodes ── */
  rawNodes.forEach((n) => {
    g.setNode(n.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
  });

  /* ── Register edges ── */
  rawEdges.forEach((e) => {
    g.setEdge(e.source, e.target);
  });

  dagre.layout(g);

  /* ── Build React Flow nodes ── */
  const nodes = rawNodes.map((n) => {
    const pos = g.node(n.id);
    return {
      id:   n.id,
      type: n.type,
      position: {
        x: pos.x - NODE_WIDTH  / 2,
        y: pos.y - NODE_HEIGHT / 2,
      },
      targetPosition: direction === 'LR' ? 'left'  : 'top',
      sourcePosition: direction === 'LR' ? 'right' : 'bottom',
      data: {
        label:       n.label       || '',
        description: n.description || '',
        service:     n.service     || '',
      },
    };
  });

  /* ── Build React Flow edges ── */
  const edges = rawEdges.map((e) => {
    const isYes = e.label === 'Yes';
    const isNo  = e.label === 'No';

    const strokeColor = isYes ? '#059669'
                      : isNo  ? '#dc2626'
                      :         '#64748b';

    return {
      id:     `${e.source}→${e.target}`,
      source: e.source,
      target: e.target,
      type:   'smoothstep',
      animated: true,
      label:  e.label || undefined,

      style: {
        stroke:      strokeColor,
        strokeWidth: 2.5,
      },

      markerEnd: {
        type:   MarkerType.ArrowClosed,
        width:  18,
        height: 18,
        color:  strokeColor,
      },

      /* label styling */
      labelStyle: {
        fill:       isYes ? '#047857' : isNo ? '#be123c' : '#475569',
        fontWeight: 600,
        fontSize:   11,
      },
      labelBgStyle: {
        fill:   isYes ? '#d1fae5' : isNo ? '#fee2e2' : '#f1f5f9',
        rx:     4,
        ry:     4,
      },
      labelBgPadding: [4, 3],
      labelBgBorderRadius: 4,
    };
  });

  return { nodes, edges };
}
