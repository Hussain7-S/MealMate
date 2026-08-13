/*
  AI Buddy widget — floating chat button that talks to /ai/chat/.
  Reads window.MEALMATE_RESTAURANT_ID (set per-page, optional) so
  the AI Buddy can scope suggestions to the restaurant being viewed.
*/
(function () {
  const toggle = document.getElementById('ai-buddy-toggle');
  const panel = document.getElementById('ai-buddy-panel');
  const closeBtn = document.getElementById('ai-buddy-close');
  const messages = document.getElementById('ai-buddy-messages');
  const form = document.getElementById('ai-buddy-form');
  const input = document.getElementById('ai-buddy-input-field');
  const chips = document.querySelectorAll('.ai-suggest-chips button');

  if (!toggle || !panel) return;

  function addMessage(text, who) {
    const div = document.createElement('div');
    div.className = 'ai-msg ' + who;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  async function sendMessage(text) {
    addMessage(text, 'user');
    input.value = '';
    try {
      const res = await fetch('/ai/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          message: text,
          restaurant_id: window.MEALMATE_RESTAURANT_ID || null,
        }),
      });
      const data = await res.json();
      addMessage(data.reply || "Sorry, I glitched for a second — try again?", 'bot');
    } catch (err) {
      addMessage("Hmm, I couldn't reach the kitchen. Check your connection and try again.", 'bot');
    }
  }

  toggle.addEventListener('click', () => {
    panel.classList.toggle('open');
    if (panel.classList.contains('open') && messages.children.length === 0) {
      addMessage("Hey, I'm your MealMate AI Buddy 🤖 Ask me for a dish, or tap a suggestion below.", 'bot');
    }
  });
  closeBtn.addEventListener('click', () => panel.classList.remove('open'));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (text) sendMessage(text);
  });

  chips.forEach((chip) => {
    chip.addEventListener('click', () => sendMessage(chip.dataset.msg));
  });
})();
