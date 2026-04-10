import { useNavigate, useLocation } from 'react-router-dom';
import { useApp } from '../App';
import {
  Bot, MessageSquare, BarChart3, ChevronLeft, ChevronRight,
  Wifi, WifiOff, Users, Brain, Zap, Activity,
} from 'lucide-react';

const NAV = [
  { path: '/chat',      icon: MessageSquare, label: 'Chat',      sub: 'Real-time NLP' },
  { path: '/analytics', icon: BarChart3,     label: 'Analytics', sub: 'Live Dashboard' },
];

export default function Sidebar() {
  const { connected, activeUsers, sidebar, setSidebar } = useApp();
  const navigate       = useNavigate();
  const { pathname }   = useLocation();

  return (
    <aside
      className="glass-solid relative z-20 flex flex-col h-full transition-all duration-300 flex-shrink-0"
      style={{ width: sidebar ? 220 : 60, borderRight: '1px solid var(--border)' }}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-3 py-4 border-b flex-shrink-0"
           style={{ borderColor: 'var(--border)', minHeight: 64 }}>
        <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 glow-blue"
             style={{ background: 'linear-gradient(135deg,#1f6feb,#7c3aed)', minWidth: 36 }}>
          <Bot size={19} color="#fff" />
        </div>
        {sidebar && (
          <div className="overflow-hidden">
            <p className="font-display font-bold text-sm grad-text leading-tight whitespace-nowrap">Dynamic AI</p>
            <p className="text-xs whitespace-nowrap" style={{ color: 'var(--muted)', fontFamily: "'JetBrains Mono',monospace" }}>FastAPI + NLP</p>
          </div>
        )}
      </div>

      {/* Status */}
      {sidebar && (
        <div className="mx-2 my-2 rounded-lg p-2 flex items-center gap-2 flex-shrink-0"
             style={{ background: 'rgba(13,17,23,.9)', border: '1px solid var(--border)' }}>
          <div className="relative flex-shrink-0">
            <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-500'}`} />
            {connected && <div className="ping absolute inset-0 rounded-full bg-green-400" />}
          </div>
          <span className="text-xs flex-1 truncate" style={{ color: 'var(--muted)' }}>
            {connected ? 'Live' : 'Offline'}
          </span>
          <span className="pill pill-blue text-xs flex items-center gap-1 flex-shrink-0">
            <Users size={9} /> {activeUsers}
          </span>
        </div>
      )}

      {/* Nav */}
      <nav className="flex-1 px-2 py-1 space-y-0.5 overflow-y-auto">
        {NAV.map(({ path, icon: Icon, label, sub }) => (
          <button key={path} onClick={() => navigate(path)}
                  className={`nav-btn ${pathname === path ? 'active' : ''}`}>
            <Icon size={17} className="flex-shrink-0" />
            {sidebar && (
              <div className="text-left overflow-hidden">
                <p className="text-sm font-medium leading-tight truncate">{label}</p>
                <p className="text-xs truncate" style={{ color: 'var(--muted)', fontFamily: "'JetBrains Mono',monospace", fontSize: 9 }}>{sub}</p>
              </div>
            )}
          </button>
        ))}
      </nav>

      {/* AI Stack */}
      {sidebar && (
        <div className="px-3 py-3 border-t flex-shrink-0" style={{ borderColor: 'var(--border)' }}>
          <p className="text-xs font-display font-semibold uppercase tracking-widest mb-2" style={{ color: 'var(--muted)', fontSize: 9 }}>AI Stack</p>
          {[
            { icon: Brain,    label: 'NLP',       val: 'Naive Bayes',  col: 'var(--accent)' },
            { icon: Zap,      label: 'Sentiment', val: 'VADER',        col: 'var(--green)' },
            { icon: Activity, label: 'ML Model',  val: 'MLP Net',      col: 'var(--purple)' },
            { icon: connected ? Wifi : WifiOff,
              label: 'Socket', val: connected ? 'Live' : 'Off',        col: connected ? 'var(--green)' : 'var(--red)' },
          ].map(({ icon: I, label, val, col }) => (
            <div key={label} className="flex items-center justify-between text-xs mb-1">
              <span className="flex items-center gap-1.5 truncate" style={{ color: 'var(--muted)' }}>
                <I size={10} className="flex-shrink-0" /> {label}
              </span>
              <span className="font-mono font-semibold ml-1 flex-shrink-0" style={{ color: col, fontSize: 9 }}>{val}</span>
            </div>
          ))}
        </div>
      )}

      {/* Toggle */}
      <button onClick={() => setSidebar(s => !s)}
              className="flex items-center justify-center py-3 border-t flex-shrink-0 transition-colors"
              style={{ borderColor: 'var(--border)', color: 'var(--muted)' }}
              onMouseEnter={e => e.currentTarget.style.color = 'var(--accent)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--muted)'}>
        {sidebar ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
      </button>
    </aside>
  );
}
