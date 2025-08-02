import React from 'react';
import './App.css';
import { Card } from 'primereact/card';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
// import 'primereact/resources/themes/arya-orange/theme.css';      // Orange theme
import 'primereact/resources/themes/lara-light-indigo/theme.css'; // Indigo theme
// import 'primereact/resources/themes/lara-dark-purple/theme.css';  // Dark theme
import { ProgressSpinner } from 'primereact/progressspinner';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

function App() {
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState("");
  const url = "http://127.0.0.1:8000"; // Adjust URL if needed

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: "user", content: input };
    setMessages((msgs) => [...msgs, userMessage]);
    setInput("");

    try {
      const res = await fetch(url + "/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });
      const data = await res.json();
      const botMessage = { role: "assistant", content: <span dangerouslySetInnerHTML={{ __html: data.answer }} /> };
      setMessages((msgs) => [...msgs, botMessage]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "Error: Unable to get response." },
      ]);
    }
  };

  return (
    <div className="App">
      <div className="chat-container" style={{ maxWidth: 900, margin: '2rem auto' }}>
        <Card 
          title="TCG Helper Bot"
          style={{ backgroundColor: '#bdbdbeff' }} // Change this color as needed
        >
          <div className="messages" style={{ minHeight: 200, marginBottom: '1rem' }}>
            {messages.map((msg, idx) => (
              <div
          key={idx}
          className={`message-card ${msg.role} ${idx % 2 === 0 ? 'even' : 'odd'}`}
          
              >
          <span style={{ fontWeight: "bold", marginRight: "0.5rem" }}>
            {msg.role === "user" ? "You:" : "TCG Helper:"}
          </span>
          {msg.content}
              </div>
            ))}
          </div>
          <div className="input-area" style={{ display: 'flex', gap: '0.5rem' }}>
            <InputText
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") sendMessage(); }}
              placeholder="Type your question..."
              style={{ flex: 1 }}
            />
            <Button label="Send" icon="pi pi-send" onClick={sendMessage} />
          </div>
        </Card>
      </div>
    </div>
  );
}

export default App;