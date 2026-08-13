"""
MealMate's AI Buddy — a lightweight, rule + data driven assistant.

It doesn't call any external LLM API (so it works instantly, with zero
API keys and zero cost). Instead it understands intent from keywords,
then queries the real restaurant/menu data to give genuinely useful,
grounded answers: recommendations, budget filtering, mood-based
suggestions, order tracking, and small talk.

This keeps the "AI Buddy" honest — it never invents a dish that isn't
actually on a menu.
"""
import random
import re
from restaurants.models import MenuItem, Restaurant

GREETINGS = ["hi", "hello", "hey", "yo", "sup", "hii", "helo"]

MOOD_MAP = {
    "sad": ["dessert", "beverage"],
    "happy": ["main", "starter"],
    "stressed": ["dessert", "beverage"],
    "tired": ["beverage", "main"],
    "hungry": ["main", "starter"],
    "celebrat": ["dessert", "main"],
    "romantic": ["main", "dessert"],
}

SMALLTALK = {
    "how are you": "I'm running smoothly on zero calories, thanks for asking! How can I help — hungry for something?",
    "who are you": "I'm your MealMate AI Buddy 🤖🍜 — I help you find dishes, filter by budget or mood, and track your orders.",
    "thank": "Anytime! Enjoy your meal 🍽️",
    "bye": "Catch you later — happy eating! 👋",
}


def _extract_budget(text):
    match = re.search(r'(?:under|below|within|less than)?\s*(?:rs\.?|₹|inr)?\s*(\d{2,5})', text, re.I)
    if match:
        return int(match.group(1))
    return None


def _extract_veg_pref(text):
    if re.search(r'\bnon[\s-]?veg\b', text, re.I):
        return False
    if re.search(r'\bveg(etarian)?\b', text, re.I):
        return True
    return None


def _extract_cuisine(text, cuisines):
    for c in cuisines:
        if c and c.lower() in text.lower():
            return c
    return None


def _mood_categories(text):
    for mood, cats in MOOD_MAP.items():
        if mood in text.lower():
            return mood, cats
    return None, None


def get_reply(message, restaurant=None):
    """
    Core entry point. `restaurant` optionally scopes recommendations
    to the restaurant the user is currently browsing.
    """
    text = message.strip().lower()

    if not text:
        return "Say something and I'll help you find the perfect bite! 🍕"

    for key, reply in SMALLTALK.items():
        if key in text:
            return reply

    if any(g == text or text.startswith(g + " ") or text == g for g in GREETINGS):
        return random.choice([
            "Hey there! 👋 Craving something specific, or want me to surprise you?",
            "Hello! Tell me your mood or budget and I'll suggest a dish. 🍔",
        ])

    if "track" in text or "order status" in text or "where is my order" in text:
        return "Head to 'My Orders' → 'Track' to see live status. Want me to check the most recent one? Just say 'my last order'."

    qs = MenuItem.objects.filter(is_available=True)
    if restaurant:
        qs = qs.filter(restaurant=restaurant)

    cuisines = Restaurant.objects.values_list('cuisine', flat=True).distinct()
    cuisine = _extract_cuisine(text, cuisines)
    if cuisine:
        qs = qs.filter(restaurant__cuisine__iexact=cuisine)

    budget = _extract_budget(text)
    if budget:
        qs = qs.filter(price__lte=budget)

    veg = _extract_veg_pref(text)
    if veg is not None:
        qs = qs.filter(is_veg=veg)

    mood, mood_cats = _mood_categories(text)
    if mood_cats:
        qs = qs.filter(category__in=mood_cats)

    is_recommend_query = any(k in text for k in [
        "suggest", "recommend", "what should i", "hungry", "eat", "food",
        "dish", "order", "craving", "want", mood or ""
    ])

    if is_recommend_query:
        items = list(qs.select_related('restaurant').order_by('?')[:4])
        if not items:
            return "Hmm, I couldn't find a match for that. Try loosening the budget or dropping a filter — I want to get this right for you!"

        lines = []
        for item in items:
            veg_tag = "🟢 Veg" if item.is_veg else "🔴 Non-Veg"
            lines.append(f"• {item.name} — ₹{item.price} ({veg_tag}) @ {item.restaurant.name}")

        intro_bits = []
        if mood:
            intro_bits.append(f"since you're feeling {mood}")
        if budget:
            intro_bits.append(f"under ₹{budget}")
        if cuisine:
            intro_bits.append(f"in {cuisine} cuisine")
        intro = " and ".join(intro_bits)
        header = f"Here's what I'd pick {intro}:" if intro else "Here are a few things I think you'll love:"

        return header + "\n" + "\n".join(lines)

    return random.choice([
        "I can suggest dishes, filter by budget/mood/veg, or help track an order. Try: 'suggest something spicy under 200'.",
        "Not sure I follow — ask me things like 'I'm sad, suggest dessert' or 'veg food under 150'.",
    ])
