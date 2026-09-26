const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://ca-backend.kindrock-91ecbb54.southindia.azurecontainerapps.io';

export async function sendMessage(message, threadId = 'default_session') {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        thread_id: threadId,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API sendMessage error:', error);
    throw error;
  }
}

export async function resetSession(threadId = 'default_session') {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ thread_id: threadId }),
    });

    return await response.json();
  } catch (error) {
    console.error('API resetSession error:', error);
    throw error;
  }
}

export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return await response.json();
  } catch (error) {
    console.error('API health check error:', error);
    return { status: 'offline' };
  }
}
