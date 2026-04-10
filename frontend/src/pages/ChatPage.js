import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../App';
import axios from 'axios';
import toast from 'react-hot-toast';
import { v4 as uuidv4 } from 'uuid';
import ReactMarkdown from 'react-markdown';
import {
  Send, Trash2, Download, RotateCcw, ChevronDown,
  Brain, Zap, Clock, Target, Activity,
  ThumbsUp, ThumbsDown, Copy, Check, Wifi, WifiOff, Menu,
} from 'lucide-react';

const QUICK = [
  '👋 Hello!', '😄 Tell me a joke', '🤖 What is AI?',
  '☕ What is Java?', '🐍 What is Python?', '❓ What can you do?',
  '😔 I feel sad', '⏰ What time is it?',
];

const SENT_MAP = {
  very_positive: { pill: 'pill-green',  label: '😄 Great' },
  positive:      { pill: 'pill-green',  label: '🙂 Positive' },
  neutral:       { pill: 'pill-gray',   label: '😐 Neutral' },
  negative:      { pill: 'pill-orange', label: '😟 Negative' },
  very_negative: { pill: 'pill-red',    label: '😢 Sad' },
};

// ─── Typing Indicator ─────────────────────────────────────────────────────────
function Typing() {
  return (
    <div className="flex items-end gap-2 msg-in px-1">
      <div className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-sm glow-blue"
           style={{ background: 'linear-gradient(135deg,#1f6feb,#7c3aed)' }}>🤖</div>
      <div className="bubble-bot px-4 py-3">
        <div className="flex items-center gap-1.5">
          <div className="dot" /><div className="dot" /><div className="dot" />
          <span className="text-xs ml-2 font-mono" style={{ color: 'var(--muted)', fontSize: 10 }}>Thinking…</span>
        </div>
      </div>
    </div>
  );
}

// ─── Copy Button ──────────────────────────────────────────────────────────────
function CopyBtn({ text }) {
  const [copied, setCopied] = useState(false);
  return (
    <button onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
            style={{ color: 'var(--muted)' }} className="transition-colors p-1 rounded hover:opacity-70">
      {copied ? <Check size={12} /> : <Copy size={12} />}
    </button>
  );
}

// ─── Single Message ───────────────────────────────────────────────────────────
function Message({ msg, onFeedback }) {
  const isUser   = msg.role === 'user';
  const [open, setOpen] = useState(false);
  const meta     = msg.metadata;
  const sentCfg  = meta?.sentiment ? SENT_MAP[meta.sentiment.label] : null;

  return (
    <div className={`flex items-end gap-2 msg-in px-1 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold ${isUser ? '' : 'glow-blue'}`}
           style={{ background: isUser ? 'linear-gradient(135deg,#7c3aed,#f778ba)' : 'linear-gradient(135deg,#1f6feb,#7c3aed)', minWidth: 28 }}>
        {isUser ? '👤' : '🤖'}
      </div>

      <div className={`flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}
           style={{ maxWidth: 'min(72%, 520px)' }}>
        {/* Bubble */}
        <div className={`px-4 py-3 ${isUser ? 'bubble-user' : 'bubble-bot'}`}>
          {isUser ? (
            <p className="text-sm leading-relaxed">{msg.content}</p>
          ) : (
            <div className="prose-chat text-sm leading-relaxed">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Meta row */}
        <div className={`flex items-center gap-1.5 flex-wrap px-1 ${isUser ? 'flex-row-reverse' : ''}`}>
          <span className="font-mono" style={{ color: 'var(--muted)', fontSize: 10 }}>
            {new Date(msg.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
          {!isUser && meta && (
            <>
              {sentCfg && <span className={`pill ${sentCfg.pill}`}>{sentCfg.label}</span>}
              {meta.emotion && <span className="pill pill-purple">💙 {meta.emotion}</span>}
              {meta.intent?.intent && meta.intent.intent !== 'fallback' && (
                <span className="pill pill-blue hidden sm:inline-flex">⚡ {meta.intent.intent}</span>
              )}
              <CopyBtn text={msg.content} />
              <button onClick={() => setOpen(o => !o)}
                      className="flex items-center gap-0.5 transition-colors p-0.5"
                      style={{ color: 'var(--muted)', fontSize: 10 }}>
                <Activity size={10} />
                <ChevronDown size={9} style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }} />
              </button>
            </>
          )}
        </div>

        {/* Expanded NLP Analysis */}
        {open && meta && (
          <div className="glass rounded-xl p-3 w-full space-y-2 text-xs">
            <p className="font-display font-semibold" style={{ color: 'var(--accent)', fontSize: 11 }}>🔬 NLP Analysis</p>
            <div className="flex flex-wrap gap-1">
              <span className="pill pill-purple"><Target size={9} /> {meta.intent?.intent}</span>
              <span className="pill pill-orange"><Zap size={9} /> {((meta.intent?.confidence || 0) * 100).toFixed(0)}%</span>
              <span className="pill pill-blue"><Clock size={9} /> {meta.processing_time_ms}ms</span>
              {meta.sentiment && <span className="pill pill-gray">Score: {meta.sentiment.score}</span>}
            </div>
            {meta.sentiment?.positive_words?.length > 0 && (
              <p className="font-mono" style={{ color: 'var(--green)', fontSize: 9 }}>
                ✅ {meta.sentiment.positive_words.join(', ')}
              </p>
            )}
            {meta.sentiment?.negative_words?.length > 0 && (
              <p className="font-mono" style={{ color: 'var(--red)', fontSize: 9 }}>
                ❌ {meta.sentiment.negative_words.join(', ')}
              </p>
            )}
            {meta.multi_intents?.length > 1 && (
              <p className="font-mono" style={{ color: 'var(--purple)', fontSize: 9 }}>
                🔀 Multi-intent: {meta.multi_intents.map(i => i.intent).join(' + ')}
              </p>
            )}
            {/* Feedback */}
            <div className="flex items-center gap-2 pt-1 border-t" style={{ borderColor: 'var(--border)' }}>
              <span style={{ color: 'var(--muted)', fontSize: 9 }}>Helpful?</span>
              <button onClick={() => onFeedback(msg, true)}  className="pill pill-green cursor-pointer"><ThumbsUp size={9} /> Yes</button>
              <button onClick={() => onFeedback(msg, false)} className="pill pill-red cursor-pointer"><ThumbsDown size={9} /> No</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Chat Page ────────────────────────────────────────────────────────────────
export default function ChatPage() {
  const { socket, connected, sessionId, setSidebar, backendUrl } = useApp();

  const [messages, setMessages] = useState([{
    id: uuidv4(), role: 'bot', ts: new Date().toISOString(),
    content: "Hello! 👋 I'm your **Dynamic AI Chatbot**!\n\nI'm built with **Python + FastAPI + NLP** and I can:\n\n• 🤖 Answer **tech questions** — Java, Python, AI, ML, APIs...\n• 😊 Provide **emotional support**\n• 🔀 Handle **multiple questions** at once\n• 💬 Remember our **conversation context**\n• 🎭 Tell **jokes** & have fun!\n\nTry asking: *'What is Java?'* or *'I feel sad today'* 🚀",
    metadata: { intent: { intent: 'greeting', confidence: 1 }, sentiment: { label: 'positive', score: 0.5, emoji: '🙂', positive_words: [], negative_words: [] }, processing_time_ms: 0, multi_intents: [] },
  }]);

  const [input,   setInput]   = useState('');
  const [typing,  setTyping]  = useState(false);
  const [useWS,   setUseWS]   = useState(true);
  const bottomRef  = useRef(null);
  const textareaRef = useRef(null);
  const chatRef    = useRef(null);

  // Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  // Socket listeners
  useEffect(() => {
    if (!socket) return;
    socket.on('bot_typing',   ({ typing }) => setTyping(typing));
    socket.on('bot_response', ({ message, metadata }) => {
      setTyping(false);
      setMessages(p => [...p, { id: uuidv4(), role: 'bot', content: message, ts: new Date().toISOString(), metadata }]);
    });
    return () => { socket.off('bot_typing'); socket.off('bot_response'); };
  }, [socket]);

  const send = useCallback(async (text) => {
    const msg = (text ?? input).trim();
    if (!msg || typing) return;
    setMessages(p => [...p, { id: uuidv4(), role: 'user', content: msg, ts: new Date().toISOString() }]);
    setInput('');
    if (textareaRef.current) { textareaRef.current.style.height = '48px'; textareaRef.current.focus(); }

    if (useWS && socket && connected) {
      socket.emit('chat_message', { message: msg, session_id: sessionId });
      return;
    }

    setTyping(true);
    try {
      const { data } = await axios.post(`${backendUrl}/api/chat/message`, { message: msg, session_id: sessionId });
      setTyping(false);
      setMessages(p => [...p, { id: uuidv4(), role: 'bot', content: data.message, ts: data.timestamp, metadata: data.metadata }]);
    } catch {
      setTyping(false);
      toast.error('Backend offline — start server first');
      setMessages(p => [...p, { id: uuidv4(), role: 'bot', ts: new Date().toISOString(),
        content: "⚠️ **Backend not reachable.**\n\n```bash\ncd backend\nuvicorn main:socket_app --reload --port 8000\n```" }]);
    }
  }, [input, typing, socket, connected, sessionId, useWS, backendUrl]);

  const handleFeedback = useCallback(async (msg, helpful) => {
    if (!msg.metadata?.intent?.intent) return;
    try {
      await axios.post(`${backendUrl}/api/chat/feedback`, {
        session_id: sessionId, message_content: msg.content,
        rating: helpful ? 5 : 1, was_helpful: helpful,
        correct_intent: msg.metadata.intent.intent,
      });
      toast.success(helpful ? '👍 Thanks! Model is learning.' : '👎 Noted! I\'ll improve.');
    } catch { toast.error('Feedback save failed'); }
  }, [sessionId, backendUrl]);

  const clearChat = async () => {
    try { await axios.delete(`${backendUrl}/api/chat/history/${sessionId}`); } catch {}
    setMessages([{ id: uuidv4(), role: 'bot', ts: new Date().toISOString(),
      content: 'Chat cleared! 🤖 Starting fresh. How can I help you?',
      metadata: { intent: { intent: 'greeting', confidence: 1 }, sentiment: { label: 'neutral', score: 0, emoji: '😐', positive_words: [], negative_words: [] }, processing_time_ms: 0 } }]);
    toast.success('Chat cleared!');
  };

  const exportChat = () => {
    const text = messages.map(m => `[${m.ts}] ${m.role.toUpperCase()}: ${m.content}`).join('\n\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
    a.download = `chat-${sessionId.slice(0,8)}.txt`;
    a.click();
    toast.success('Exported!');
  };

  const onKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  };

  const onInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  };

  return (
    <div className="flex flex-col h-full bg-grid relative" style={{ overflow: 'hidden' }}>

      {/* ── Header ─────────────────────────────────────────────────── */}
      <header className="glass-solid border-b px-3 sm:px-4 py-3 flex items-center justify-between z-10 flex-shrink-0 chat-header"
              style={{ borderColor: 'var(--border)' }}>
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Mobile menu button */}
          <button className="sm:hidden p-1.5 rounded-lg transition-colors"
                  style={{ color: 'var(--muted)' }}
                  onClick={() => setSidebar(true)}>
            <Menu size={18} />
          </button>

          <div className="flex items-center gap-2">
            <div className="relative">
              <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl flex items-center justify-center text-base glow-blue"
                   style={{ background: 'linear-gradient(135deg,#1f6feb,#7c3aed)' }}>🤖</div>
              <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2"
                   style={{ background: connected ? '#3fb950' : '#f85149', borderColor: 'var(--dark)' }} />
            </div>
            <div>
              <p className="font-display font-bold text-sm" style={{ color: 'var(--text)' }}>Dynamic AI Chatbot</p>
              <p className="font-mono hidden sm:block" style={{ color: connected ? 'var(--green)' : 'var(--red)', fontSize: 10 }}>
                {connected ? '● Socket.IO Live' : '● REST Fallback'}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1 sm:gap-2">
          <button onClick={() => setUseWS(u => !u)}
                  className={`pill cursor-pointer hidden sm:inline-flex ${useWS ? 'pill-blue' : 'pill-gray'}`}>
            {useWS ? <Wifi size={9} /> : <WifiOff size={9} />}
            {useWS ? 'Socket' : 'REST'}
          </button>
          <button onClick={exportChat} className="p-2 rounded-lg transition-colors" style={{ color: 'var(--muted)' }}
                  onMouseEnter={e=>e.currentTarget.style.color='var(--accent)'}
                  onMouseLeave={e=>e.currentTarget.style.color='var(--muted)'} title="Export">
            <Download size={15} />
          </button>
          <button onClick={clearChat} className="p-2 rounded-lg transition-colors" style={{ color: 'var(--muted)' }}
                  onMouseEnter={e=>e.currentTarget.style.color='var(--red)'}
                  onMouseLeave={e=>e.currentTarget.style.color='var(--muted)'} title="Clear">
            <Trash2 size={15} />
          </button>
        </div>
      </header>

      {/* ── Messages ───────────────────────────────────────────────── */}
      <div ref={chatRef} className="flex-1 overflow-y-auto chat-scroll py-3 sm:py-4 space-y-3 sm:space-y-4">
        {messages.map(m => <Message key={m.id} msg={m} onFeedback={handleFeedback} />)}
        {typing && <Typing />}
        <div ref={bottomRef} className="h-1" />
      </div>

      {/* ── Quick Prompts ───────────────────────────────────────────── */}
      <div className="flex gap-2 overflow-x-auto scrollbar-hide flex-shrink-0 quick-prompts px-3 sm:px-4 py-2"
           style={{ borderTop: '1px solid rgba(33,38,45,0.5)' }}>
        {QUICK.map(q => (
          <button key={q} onClick={() => send(q)}
                  className="flex-shrink-0 pill pill-gray cursor-pointer whitespace-nowrap"
                  style={{ fontSize: 11, padding: '4px 10px' }}>
            {q}
          </button>
        ))}
      </div>

      {/* ── Input Area ─────────────────────────────────────────────── */}
      <div className="glass-solid border-t flex-shrink-0 input-area px-3 sm:px-4 pt-3 pb-3"
           style={{ borderColor: 'var(--border)' }}>
        <div className="flex items-end gap-2 sm:gap-3">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={onInput}
            onKeyDown={onKey}
            placeholder="Type a message… (Enter to send)"
            rows={1}
            className="input-chat"
            style={{ minHeight: 48, maxHeight: 120 }}
          />
          <button onClick={() => send()} disabled={!input.trim() || typing} className="btn-send">
            {typing ? <RotateCcw size={17} className="animate-spin" /> : <Send size={17} />}
          </button>
        </div>
        <div className="flex justify-between mt-1.5 px-1">
          <p className="font-mono" style={{ color: 'var(--muted)', fontSize: 10 }}>
            Session: <span style={{ color: 'var(--accent)' }}>{sessionId.slice(0,8)}…</span>
          </p>
          <p className="font-mono" style={{ color: input.length > 900 ? 'var(--red)' : 'var(--muted)', fontSize: 10 }}>
            {input.length}/1000
          </p>
        </div>
      </div>
    </div>
  );
}
