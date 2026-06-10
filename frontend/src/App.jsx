import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot, User, Terminal, Zap, Activity, Paperclip } from 'lucide-react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'System Online. Provide an enterprise task to begin execution loop.' }
  ]);
  const [telemetry, setTelemetry] = useState([
    "INIT: RAG Core connected.",
    "INIT: Tool Harness loaded. Awaiting instructions."
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const messagesEndRef = useRef(null);
  const telemetryEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    telemetryEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [telemetry]);

  const handleFileUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);
  
  setTelemetry((prev) => [...prev, `\n> UPLOADING: ${file.name} to RAG engine...`]);

  try {
    const response = await fetch('http://127.0.0.1:8000/api/upload', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    setTelemetry((prev) => [...prev, `[SYSTEM] ${data.message}`]);
  } catch (error) {
    setTelemetry((prev) => [...prev, `[ERROR] Failed to ingest document.`]);
  }
};

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setTelemetry((prev) => [...prev, `\n> USER DISPATCH: ${userMessage}`]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        // Split the conversational answer from the hidden system logs
        const parts = data.response.split('[SYSTEM LOG - EVIDENCE OF EXECUTION]');
        const chatResponse = parts[0].trim();
        const logs = parts.length > 1 ? parts[1].trim() : "No trace provided.";

        setMessages((prev) => [...prev, { role: 'assistant', text: chatResponse }]);
        setTelemetry((prev) => [...prev, `\n[AGENT TRACE]\n${logs}`]);
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', text: 'Error executing task.' }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Could not connect to AI microservice.' }]);
      setTelemetry((prev) => [...prev, `\n[CRITICAL ERROR] Microservice unreachable.`]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      {/* HEADER */}
      <header className="top-nav">
        <div className="brand">
          <Zap className="accent-icon" />
          <h1>IronLabs AIOPL Engine</h1>
        </div>
        <div className="status-indicator">
          <Activity size={16} className="pulse-icon" /> Microservice Active
        </div>
      </header>

      <div className="workspace">
        {/* LEFT PANEL: Chat Interface */}
        <section className="chat-panel">
          <div className="chat-history">
            {messages.map((msg, index) => (
              <div key={index} className={`message-wrapper ${msg.role}`}>
                <div className="avatar">
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className="message-bubble">
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message-wrapper assistant">
                <div className="avatar"><Bot size={20} /></div>
                <div className="message-bubble loading-pulse">Reasoning and routing tools...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSend} className="chat-input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g., Look up records for ID 992 and process a refund of $45..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>Execute</button>
          </form>
        </section>

        {/* RIGHT PANEL: Live Telemetry & Logs */}
        <aside className="telemetry-panel">
          <div className="telemetry-header">
            <Terminal size={18} />
            <h2>Live Execution Trace</h2>
          </div>
          <div className="telemetry-logs">
            {telemetry.map((log, index) => (
              <pre key={index} className="log-entry">{log}</pre>
            ))}
            <div ref={telemetryEndRef} />
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;