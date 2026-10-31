/**
 * GreenMate AI - Conversational Botanical Chatbot
 * Floating assistant connected to live FastAPI AI backend.
 */

const Chatbot = {
  isOpen: false,
  history: [],

  init() {
    const trigger = document.getElementById('chatbot-trigger');
    const closeBtn = document.getElementById('chat-close-btn');
    const form = document.getElementById('chat-input-form');

    if (trigger) trigger.addEventListener('click', () => this.toggle());
    if (closeBtn) closeBtn.addEventListener('click', () => this.close());

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('chat-user-input');
        if (input && input.value.trim()) {
          const msg = input.value.trim();
          input.value = '';
          this.sendMessage(msg);
        }
      });
    }

    // Load recent history if logged in
    if (Auth.isAuthenticated()) {
      API.request('/api/ai/chat-history').then(records => {
        if (records && records.length > 0) {
          records.forEach(r => {
            this.appendMessage('user', r.user_message, false);
            this.appendMessage('bot', r.assistant_reply, false);
            this.history.push({ role: 'user', content: r.user_message });
            this.history.push({ role: 'assistant', content: r.assistant_reply });
          });
        }
      }).catch(() => {});
    }
  },

  toggle() {
    this.isOpen ? this.close() : this.open();
  },

  open() {
    const panel = document.getElementById('chatbot-panel');
    if (panel) {
      panel.classList.add('active');
      this.isOpen = true;
      const input = document.getElementById('chat-user-input');
      if (input) input.focus();
    }
  },

  close() {
    const panel = document.getElementById('chatbot-panel');
    if (panel) {
      panel.classList.remove('active');
      this.isOpen = false;
    }
  },

  appendMessage(role, text, scroll = true) {
    const body = document.getElementById('chat-body');
    if (!body) return;

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role}`;
    
    // Format bold and bullets simply
    const formatted = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
    
    bubble.innerHTML = formatted;
    body.appendChild(bubble);

    if (scroll) {
      body.scrollTop = body.scrollHeight;
    }
  },

  async sendMessage(text) {
    this.open();
    this.appendMessage('user', text);
    this.history.push({ role: 'user', content: text });

    const body = document.getElementById('chat-body');
    const loadingElem = document.createElement('div');
    loadingElem.className = 'chat-bubble bot';
    loadingElem.id = 'chat-bot-typing';
    loadingElem.innerHTML = '<span style="color:#5e7367; font-size:0.8rem; font-style:italic;">Botanist is thinking... 🌿</span>';
    body.appendChild(loadingElem);
    body.scrollTop = body.scrollHeight;

    try {
      const res = await API.sendChatMessage(text, null, this.history);
      
      const typing = document.getElementById('chat-bot-typing');
      if (typing) typing.remove();

      this.appendMessage('bot', res.reply);
      this.history.push({ role: 'assistant', content: res.reply });

      // Render suggested prompt pills if present
      if (res.suggested_followups && res.suggested_followups.length > 0) {
        this.renderSuggestedPrompts(res.suggested_followups);
      }
    } catch (err) {
      const typing = document.getElementById('chat-bot-typing');
      if (typing) typing.remove();
      this.appendMessage('bot', `I encountered an issue connecting to the AI: ${err.message}`);
    }
  },

  renderSuggestedPrompts(prompts) {
    const body = document.getElementById('chat-body');
    if (!body) return;

    const wrap = document.createElement('div');
    wrap.className = 'chat-quick-prompts';
    wrap.innerHTML = prompts.map(p => `
      <button class="prompt-pill-btn" onclick="Chatbot.sendMessage('${p.replace(/'/g, "\\'")}')">${p}</button>
    `).join('');

    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }
};

window.Chatbot = Chatbot;
document.addEventListener('DOMContentLoaded', () => Chatbot.init());
