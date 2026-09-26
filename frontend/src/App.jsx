import React, { useState } from 'react';
import AppLayout from './components/Layout/AppLayout';
import ChatPanel from './components/Chat/ChatPanel';
import WorkflowCanvas from './components/Workflow/WorkflowCanvas';
import { sendMessage, resetSession } from './services/api';

export default function App() {
  const [messages, setMessages]       = useState([
    { role: 'assistant', content: 'Hello! Describe the workflow you want to automate.' },
  ]);
  const [workflow, setWorkflow]       = useState(null); // Initially empty, no generic diagram
  const [extractedInfo, setExtractedInfo] = useState({});
  const [isLoading, setIsLoading]     = useState(false);
  const [error, setError]             = useState(null);
  const [threadId, setThreadId]       = useState(`s_${Date.now()}`);

  /* ── Send message to backend ── */
  const handleSendMessage = async (text) => {
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    setIsLoading(true);
    setError(null);

    try {
      const res = await sendMessage(text, threadId);

      setMessages((prev) => [...prev, { role: 'assistant', content: res.message }]);

      if (res.extracted_info)  setExtractedInfo(res.extracted_info);
      if (res.status === 'complete' && res.workflow) setWorkflow(res.workflow);
    } catch (err) {
      setError(err.message);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Connection error — is the FastAPI backend running on port 8000?' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  /* ── Reset session ── */
  const handleReset = async () => {
    const newId = `s_${Date.now()}`;
    setThreadId(newId);
    setMessages([{ role: 'assistant', content: 'Session reset! What would you like to automate?' }]);
    setWorkflow(null);
    setExtractedInfo({});
    setError(null);
    await resetSession(newId).catch(() => {});
  };

  return (
    <AppLayout
      chatPanel={
        <ChatPanel
          messages={messages}
          extractedInfo={extractedInfo}
          onSendMessage={handleSendMessage}
          onResetSession={handleReset}
          isLoading={isLoading}
        />
      }
      workflowCanvas={
        <WorkflowCanvas
          rawWorkflow={workflow}
          isBuilding={isLoading}
          error={error}
        />
      }
    />
  );
}
