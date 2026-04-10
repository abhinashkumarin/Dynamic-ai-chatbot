import React, { createContext, useContext, useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { io } from 'socket.io-client';
import { v4 as uuidv4 } from 'uuid';
import { MessageSquare, BarChart3, Bot } from 'lucide-react';

import Canvas        from './components/Canvas';
import Sidebar       from './components/Sidebar';
import ChatPage      from './pages/ChatPage';
import AnalyticsPage from './pages/AnalyticsPage';

export const AppCtx = createContext(null);
export const useApp = () => useContext(AppCtx);

const BACKEND = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

// ─── Mobile Bottom Navigation ──────────────────────────────────────────────
function BottomNav() {
  const location  = useLocation();
  const navigate  = useNavigate();
  const { connected } = useApp();

  const tabs = [
    { path: '/chat',      icon: MessageSquare, label: 'Chat' },
    { path: '/analytics', icon: BarChart3,     label: 'Analytics' },
  ];

  return (
    <div className="bottom-nav">
      {tabs.map(({ path, icon: Icon, label }) => (
        <button
          key={path}
          onClick={() => navigate(path)}
          className={`bottom-nav-btn ${location.pathname === path ? 'active' : ''}`}
        >
          <Icon />
          <span>{label}</span>
        </button>
      ))}
    </div>
  );
}

export default function App() {
  const [socket,      setSocket]      = useState(null);
  const [connected,   setConnected]   = useState(false);
  const [activeUsers, setActiveUsers] = useState(0);
  const [sidebar,     setSidebar]     = useState(true);

  const [sessionId] = useState(() => {
    const stored = localStorage.getItem('ai_session_id');
    if (stored) return stored;
    const id = uuidv4();
    localStorage.setItem('ai_session_id', id);
    return id;
  });

  useEffect(() => {
    const s = io(BACKEND, {
      transports: ['websocket', 'polling'],
      reconnectionAttempts: 8,
      reconnectionDelay: 1500,
    });
    s.on('connect',    () => { setConnected(true); setSocket(s); });
    s.on('disconnect', () => setConnected(false));
    s.on('user_count', ({ count }) => setActiveUsers(count));
    return () => s.disconnect();
  }, []);

  const ctx = {
    socket, connected, sessionId, activeUsers,
    sidebar, setSidebar, backendUrl: BACKEND,
  };

  return (
    <AppCtx.Provider value={ctx}>
      <BrowserRouter>
        <div className="flex h-full overflow-hidden" style={{ background: 'var(--dark)' }}>
          <Canvas />

          {/* Desktop Sidebar */}
          <div className="desktop-sidebar">
            <Sidebar />
          </div>

          {/* Main Content */}
          <main className="flex-1 flex flex-col overflow-hidden relative z-10 main-with-bottom-nav">
            <Routes>
              <Route path="/"          element={<Navigate to="/chat" replace />} />
              <Route path="/chat"      element={<ChatPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
            </Routes>
          </main>

          {/* Mobile Bottom Nav */}
          <BottomNav />
        </div>

        <Toaster
          position="top-center"
          toastOptions={{
            style: {
              background: '#0d1117',
              color: '#c9d1d9',
              border: '1px solid #21262d',
              borderRadius: '12px',
              fontFamily: "'DM Sans', sans-serif",
              fontSize: '14px',
              maxWidth: '90vw',
            },
          }}
        />
      </BrowserRouter>
    </AppCtx.Provider>
  );
}
