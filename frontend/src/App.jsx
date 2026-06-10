import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'System Online. Provide an enterprise task to begin execution loop.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        setMessages((prev) => [...prev, { role: 'assistant', text: data.response }]);
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', text: 'Error executing task.' }]);
      }
    } catch (error) {
      console.error('Error connecting to backend API:', error);
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Could not connect to AI microservice.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 IronLabs AIOPL Engine</h1>
        <div className="status-badge">🟢 Microservice Connected</div>
      </header>

      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message-row ${msg.role}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '⚙️'}</div>
            <div className="message-content">
              {/* Splitting system log evidence for better terminal-like presentation */}
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{msg.text}</pre>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-row assistant loading">
            <div className="avatar">⚙️</div>
            <div className="message-content animate-pulse">Agent is reasoning and triggering tools...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter enterprise task / scenario query..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>Execute</button>
      </form>
    </div>
  );
}

export default App;