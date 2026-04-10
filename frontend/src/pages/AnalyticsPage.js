import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import {
  RefreshCw, Activity, Brain, Zap, Users, MessageSquare,
  Clock, Target, AlertCircle, TrendingUp, BarChart3, Server,
} from 'lucide-react';
import { useApp } from '../App';

const COLORS = ['#58a6ff','#bc8cff','#3fb950','#d29922','#f778ba','#f85149','#79c0ff'];
const SENT_COLORS = {
  very_positive: '#3fb950', positive: '#56d364',
  neutral: '#484f58', negative: '#d29922', very_negative: '#f85149',
};

// ─── Tooltip ─────────────────────────────────────────────────────────────────
const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-solid rounded-xl p-2.5 border text-xs font-mono" style={{ borderColor: 'var(--border)' }}>
      {label && <p className="mb-1" style={{ color: 'var(--accent)' }}>{label}</p>}
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color || 'var(--text)' }}>
          {p.name}: {typeof p.value === 'number' ? p.value.toLocaleString() : p.value}
        </p>
      ))}
    </div>
  );
};

// ─── Stat Card ────────────────────────────────────────────────────────────────
function Stat({ icon: Icon, label, value, sub, col = '#58a6ff', trend }) {
  return (
    <div className="glass stat-card rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
      <div className="flex items-start justify-between mb-3">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
             style={{ background: `${col}18` }}>
          <Icon size={18} style={{ color: col }} />
        </div>
        {trend !== undefined && (
          <span className={`pill ${trend >= 0 ? 'pill-green' : 'pill-red'}`}>
            {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <p className="font-display font-bold text-xl sm:text-2xl" style={{ color: 'var(--text)' }}>{value ?? '—'}</p>
      <p className="text-sm font-medium mt-0.5" style={{ color: 'var(--text)' }}>{label}</p>
      {sub && <p className="text-xs mt-0.5" style={{ color: 'var(--muted)' }}>{sub}</p>}
    </div>
  );
}

// ─── Section Title ────────────────────────────────────────────────────────────
function Section({ icon: Icon, title }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <Icon size={15} style={{ color: 'var(--accent)' }} />
      <h3 className="font-display font-semibold text-sm" style={{ color: 'var(--text)' }}>{title}</h3>
    </div>
  );
}

export default function AnalyticsPage() {
  const { backendUrl } = useApp();
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);
  const [updated, setUpdated] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const { data: d } = await axios.get(`${backendUrl}/api/analytics/dashboard`);
      setData(d); setUpdated(new Date());
    } catch {
      setError('Cannot reach backend. Start the Python server.');
    } finally { setLoading(false); }
  }, [backendUrl]);

  useEffect(() => {
    fetchData();
    const t = setInterval(fetchData, 15000);
    return () => clearInterval(t);
  }, [fetchData]);

  // Derived data
  const intentData = data?.session_stats?.intent_distribution
    ? Object.entries(data.session_stats.intent_distribution)
        .sort((a, b) => b[1] - a[1]).slice(0, 8)
        .map(([name, count], i) => ({ name, count, fill: COLORS[i % COLORS.length] }))
    : [];

  const sentData = data?.session_stats?.sentiment_distribution
    ? Object.entries(data.session_stats.sentiment_distribution)
        .filter(([, v]) => v > 0)
        .map(([name, value]) => ({ name: name.replace('_', ' '), value, fill: SENT_COLORS[name] }))
    : [];

  const hourlyData = data?.session_stats?.hourly_activity
    ? Array.from({ length: 24 }, (_, h) => ({
        hour: `${h.toString().padStart(2, '0')}h`,
        msgs: data.session_stats.hourly_activity[h] || 0,
      }))
    : [];

  return (
    <div className="flex-1 overflow-y-auto chat-scroll relative z-10 bg-grid"
         style={{ paddingBottom: 'max(16px, var(--safe-bottom))' }}>
      <div className="p-3 sm:p-5 space-y-4 sm:space-y-5 max-w-5xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-display font-extrabold text-xl sm:text-2xl grad-text">Analytics</h1>
            <p className="text-xs font-mono mt-0.5" style={{ color: 'var(--muted)' }}>
              {updated ? `Updated ${updated.toLocaleTimeString()}` : 'Loading…'}
            </p>
          </div>
          <button onClick={fetchData} disabled={loading}
                  className="flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-sm font-semibold disabled:opacity-50"
                  style={{ background: 'linear-gradient(135deg,#1f6feb,#7c3aed)', color: '#fff' }}>
            <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="glass rounded-2xl p-4 flex items-start gap-3 border"
               style={{ borderColor: 'rgba(248,81,73,.3)' }}>
            <AlertCircle size={18} style={{ color: 'var(--red)', flexShrink: 0 }} className="mt-0.5" />
            <div>
              <p className="text-sm font-medium" style={{ color: '#ffa0a0' }}>{error}</p>
              <p className="text-xs mt-1 font-mono" style={{ color: 'var(--muted)' }}>
                cd backend && uvicorn main:socket_app --reload --port 8000
              </p>
            </div>
          </div>
        )}

        {/* Stat Cards — 2 cols on mobile, 4 on desktop */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <Stat icon={MessageSquare} label="Messages"   value={data?.session_stats?.total_messages ?? 0}   col="#58a6ff" trend={12} />
          <Stat icon={Users}         label="Sessions"   value={data?.session_stats?.total_sessions ?? 0}   col="#bc8cff" trend={5}  />
          <Stat icon={Clock}         label="Avg Response" value={data?.session_stats?.avg_response_time_ms ? `${data.session_stats.avg_response_time_ms}ms` : '—'} col="#3fb950" />
          <Stat icon={Target}        label="Confidence" value={data?.session_stats?.avg_confidence ? `${(data.session_stats.avg_confidence*100).toFixed(0)}%` : '—'} col="#d29922" />
        </div>

        {/* Real-time row — 2 on mobile, 4 on desktop */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { icon: Server,   label: 'Uptime',   val: data ? `${Math.floor((data.realtime?.server_uptime_seconds||0)/60)}m` : '—', col: 'var(--accent)' },
            { icon: Activity, label: 'NLP Ready', val: data?.realtime?.nlp_engine_ready ? '✅ Yes' : '⏳ No',                     col: 'var(--green)' },
            { icon: Brain,    label: 'ML Trained', val: data?.model_stats?.is_ready ? '✅ Yes' : '⏳ No',                         col: 'var(--purple)' },
            { icon: Zap,      label: 'Feedback',  val: `${data?.model_stats?.feedback_count || 0} samples`,                       col: 'var(--orange)' },
          ].map(({ icon: I, label, val, col }) => (
            <div key={label} className="glass rounded-xl p-3 flex items-center gap-2.5 border" style={{ borderColor: 'var(--border)' }}>
              <I size={16} style={{ color: col, flexShrink: 0 }} />
              <div className="overflow-hidden">
                <p className="text-xs truncate" style={{ color: 'var(--muted)' }}>{label}</p>
                <p className="font-mono font-bold text-sm truncate" style={{ color: col }}>{val}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Charts — stacked on mobile, side by side on desktop */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

          {/* Intent Bar Chart */}
          <div className="glass rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
            <Section icon={Target} title="Intent Distribution" />
            {intentData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={intentData} margin={{ top: 0, right: 0, bottom: 30, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.04)" />
                  <XAxis dataKey="name" tick={{ fill: 'var(--muted)', fontSize: 9 }}
                         tickLine={false} angle={-35} textAnchor="end" interval={0} />
                  <YAxis tick={{ fill: 'var(--muted)', fontSize: 9 }} tickLine={false} axisLine={false} />
                  <Tooltip content={<Tip />} />
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {intentData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[200px] flex items-center justify-center text-sm" style={{ color: 'var(--muted)' }}>
                No data yet — start chatting!
              </div>
            )}
          </div>

          {/* Sentiment Pie */}
          <div className="glass rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
            <Section icon={TrendingUp} title="Sentiment Breakdown" />
            {sentData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={sentData} cx="50%" cy="50%" innerRadius={50} outerRadius={75}
                       dataKey="value"
                       label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                       labelLine={{ stroke: 'rgba(255,255,255,.1)' }}>
                    {sentData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                  </Pie>
                  <Tooltip content={<Tip />} />
                  <Legend formatter={v => <span style={{ color: 'var(--text)', fontSize: 10 }}>{v}</span>} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[200px] flex items-center justify-center text-sm" style={{ color: 'var(--muted)' }}>
                No sentiment data yet
              </div>
            )}
          </div>
        </div>

        {/* Hourly Activity */}
        <div className="glass rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
          <Section icon={BarChart3} title="Hourly Activity" />
          <ResponsiveContainer width="100%" height={130}>
            <AreaChart data={hourlyData}>
              <defs>
                <linearGradient id="aGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#58a6ff" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#58a6ff" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.04)" />
              <XAxis dataKey="hour" tick={{ fill: 'var(--muted)', fontSize: 9 }} tickLine={false} interval={3} />
              <YAxis tick={{ fill: 'var(--muted)', fontSize: 9 }} tickLine={false} axisLine={false} />
              <Tooltip content={<Tip />} />
              <Area type="monotone" dataKey="msgs" name="Messages"
                    stroke="#58a6ff" strokeWidth={2} fill="url(#aGrad)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Model Details */}
        <div className="glass rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
          <Section icon={Brain} title="ML Model Details" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {[
              { label: 'Architecture', val: data?.model_stats?.architecture || 'MLP [9→64→32→16→7]', col: 'var(--accent)' },
              { label: 'Status',       val: data?.model_stats?.is_ready ? '✅ Trained' : '⏳ Training',   col: 'var(--green)' },
              { label: 'Feedback',     val: `${data?.model_stats?.feedback_count || 0} samples`,          col: 'var(--orange)' },
              { label: 'Auto-Retrain', val: `${data?.model_stats?.retrain_count || 0}× done`,             col: 'var(--purple)' },
            ].map(({ label, val, col }) => (
              <div key={label} className="flex items-start justify-between py-2 border-b" style={{ borderColor: 'var(--border)' }}>
                <span className="text-xs" style={{ color: 'var(--muted)' }}>{label}</span>
                <span className="text-xs font-mono font-semibold text-right ml-2" style={{ color: col }}>{val}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Intent Table */}
        {intentData.length > 0 && (
          <div className="glass rounded-2xl p-4 border" style={{ borderColor: 'var(--border)' }}>
            <Section icon={Zap} title="Intent Summary" />
            <div className="overflow-x-auto">
              <table className="w-full text-xs font-mono min-w-[300px]">
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}>
                    {['Intent', 'Count', '%', 'Bar'].map(h => (
                      <th key={h} className="text-left py-2 pr-4" style={{ color: 'var(--muted)' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {intentData.map(d => {
                    const total = intentData.reduce((s, x) => s + x.count, 0);
                    const pct = total ? (d.count / total * 100).toFixed(1) : 0;
                    return (
                      <tr key={d.name} style={{ borderBottom: '1px solid rgba(33,38,45,.5)' }}>
                        <td className="py-2 pr-4" style={{ color: d.fill }}>{d.name}</td>
                        <td className="pr-4" style={{ color: 'var(--text)' }}>{d.count}</td>
                        <td className="pr-4" style={{ color: 'var(--muted)' }}>{pct}%</td>
                        <td className="pr-4 w-24 sm:w-36">
                          <div className="h-1.5 rounded-full" style={{ background: 'var(--border)' }}>
                            <div className="h-1.5 rounded-full transition-all" style={{ background: d.fill, width: `${pct}%` }} />
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
