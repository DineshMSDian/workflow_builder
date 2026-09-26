/**
 * Dynamic icon mapping: resolves a service name + node type into
 * the correct Lucide icon component, colour, and background.
 *
 * Works by keyword matching against the service string the backend
 * attaches to every node, so "Gmail" renders a red Mail icon,
 * "Slack" renders a purple MessageSquare, "GPay" renders a blue
 * CreditCard, etc.
 */

import {
  Mail, Send, MessageSquare, MessageCircle,
  CreditCard, Wallet,
  Database, FileText, HardDrive, FileSpreadsheet,
  Globe, Link2,
  Zap, Square, CircleStop,
  Filter, SlidersHorizontal,
  Bell,
  ShoppingCart, Package,
  Clock, Calendar,
  Gamepad2,
  Cpu,
  GitFork,
  Shield,
  Cloud,
  Smartphone,
  Code, Terminal,
  Layers,
  CheckCircle2,
  Table,
} from 'lucide-react';

/* ── service keyword → visual config ──────────────────────── */
const SERVICE_MAP = [
  // Email
  { keys: ['gmail'],                icon: Mail,            color: '#EA4335', bg: '#FEE2E2' },
  { keys: ['outlook', 'hotmail'],   icon: Mail,            color: '#0078D4', bg: '#DBEAFE' },
  { keys: ['email', 'mail'],        icon: Mail,            color: '#EA4335', bg: '#FEE2E2' },

  // Payments
  { keys: ['gpay', 'google pay'],   icon: CreditCard,      color: '#4285F4', bg: '#DBEAFE' },
  { keys: ['stripe'],               icon: CreditCard,      color: '#635BFF', bg: '#EDE9FE' },
  { keys: ['razorpay'],             icon: CreditCard,      color: '#2563EB', bg: '#DBEAFE' },
  { keys: ['paypal'],               icon: Wallet,          color: '#003087', bg: '#DBEAFE' },

  // Messaging / Notifications
  { keys: ['slack'],                icon: MessageSquare,   color: '#4A154B', bg: '#F3E8FF' },
  { keys: ['telegram'],             icon: Send,            color: '#0088CC', bg: '#DBEAFE' },
  { keys: ['whatsapp'],             icon: MessageCircle,   color: '#25D366', bg: '#D1FAE5' },
  { keys: ['discord'],              icon: MessageSquare,   color: '#5865F2', bg: '#EDE9FE' },
  { keys: ['sms', 'text'],          icon: Smartphone,      color: '#10B981', bg: '#D1FAE5' },

  // Google Suite
  { keys: ['google sheets', 'sheets', 'spreadsheet'], icon: Table,  color: '#34A853', bg: '#D1FAE5' },
  { keys: ['google drive', 'gdrive', 'drive'],        icon: HardDrive, color: '#4285F4', bg: '#DBEAFE' },
  { keys: ['google docs', 'docs'],  icon: FileText,        color: '#4285F4', bg: '#DBEAFE' },
  { keys: ['google'],               icon: Globe,           color: '#4285F4', bg: '#DBEAFE' },

  // Databases / Storage
  { keys: ['notion'],               icon: FileText,        color: '#191919', bg: '#F1F5F9' },
  { keys: ['airtable'],             icon: Table,           color: '#18BFFF', bg: '#DBEAFE' },
  { keys: ['database', 'db', 'sql', 'postgres', 'mysql', 'mongo'], icon: Database, color: '#3B82F6', bg: '#DBEAFE' },
  { keys: ['excel'],                icon: FileSpreadsheet, color: '#217346', bg: '#D1FAE5' },

  // Gaming
  { keys: ['clash of clans', 'clash', 'coc'],  icon: Gamepad2, color: '#F59E0B', bg: '#FEF3C7' },
  { keys: ['game', 'gaming'],       icon: Gamepad2,        color: '#F59E0B', bg: '#FEF3C7' },

  // E-commerce
  { keys: ['shopify'],              icon: ShoppingCart,    color: '#96BF48', bg: '#D1FAE5' },
  { keys: ['woocommerce', 'ecommerce', 'shop', 'order'], icon: ShoppingCart, color: '#7B5EA7', bg: '#F3E8FF' },
  { keys: ['amazon'],               icon: Package,        color: '#FF9900', bg: '#FEF3C7' },

  // Dev / API
  { keys: ['webhook'],              icon: Globe,           color: '#8B5CF6', bg: '#EDE9FE' },
  { keys: ['api', 'rest', 'http'],  icon: Code,            color: '#8B5CF6', bg: '#EDE9FE' },
  { keys: ['github'],               icon: Code,            color: '#24292E', bg: '#F1F5F9' },

  // Schedule / Time
  { keys: ['schedule', 'cron', 'timer', 'weekly', 'daily', 'hourly'], icon: Clock, color: '#6366F1', bg: '#EDE9FE' },
  { keys: ['calendar'],             icon: Calendar,        color: '#6366F1', bg: '#EDE9FE' },

  // Cloud
  { keys: ['aws', 's3', 'cloud'],   icon: Cloud,           color: '#FF9900', bg: '#FEF3C7' },
  { keys: ['firebase', 'supabase'], icon: Database,        color: '#FFCA28', bg: '#FEF3C7' },

  // Security
  { keys: ['auth', 'security'],     icon: Shield,          color: '#10B981', bg: '#D1FAE5' },

  // Files
  { keys: ['file', 'document', 'pdf', 'invoice'], icon: FileText, color: '#3B82F6', bg: '#DBEAFE' },

  // Generic
  { keys: ['expense', 'money', 'payment', 'transaction', 'finance'], icon: CreditCard, color: '#10B981', bg: '#D1FAE5' },
  { keys: ['notification', 'alert', 'notify'], icon: Bell, color: '#8B5CF6', bg: '#EDE9FE' },
  { keys: ['filter', 'label', 'tag'], icon: Filter, color: '#10B981', bg: '#D1FAE5' },
  { keys: ['log', 'record', 'track', 'store'], icon: Database, color: '#3B82F6', bg: '#DBEAFE' },
];

/* ── node-type fallbacks ──────────────────────────────────── */
const TYPE_DEFAULTS = {
  trigger:      { icon: Zap,            color: '#F59E0B', bg: '#FEF3C7' },
  filter:       { icon: Filter,         color: '#10B981', bg: '#D1FAE5' },
  action:       { icon: Cpu,            color: '#3B82F6', bg: '#DBEAFE' },
  condition:    { icon: GitFork,        color: '#F59E0B', bg: '#FEF3C7' },
  notification: { icon: Bell,           color: '#8B5CF6', bg: '#EDE9FE' },
  end:          { icon: Square,         color: '#EF4444', bg: '#FEE2E2' },
};

/**
 * Resolve icon config for a workflow node.
 *
 * @param {string} nodeType  – "trigger" | "action" | "condition" | …
 * @param {string} service   – raw service string from the backend (e.g. "Gmail")
 * @param {string} label     – node label as a secondary hint
 * @returns {{ icon: Component, color: string, bg: string }}
 */
export function getNodeIcon(nodeType, service, label) {
  const haystack = `${service || ''} ${label || ''}`.toLowerCase();

  // Try matching against service keyword map
  for (const entry of SERVICE_MAP) {
    for (const key of entry.keys) {
      if (haystack.includes(key)) {
        return { icon: entry.icon, color: entry.color, bg: entry.bg };
      }
    }
  }

  // Fall back to node-type default
  return TYPE_DEFAULTS[nodeType] || TYPE_DEFAULTS.action;
}
