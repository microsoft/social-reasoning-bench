#!/usr/bin/env python3
"""Simple BFS Wikipedia Crawler - saves each page as separate yaml file"""

import re
import time
from collections import deque
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

# Seed topics - diverse coverage
SEEDS = [
    # Negotiation & Persuasion
    "Negotiation", "Persuasion", "Rhetoric", "Argumentation_theory", "Debate",
    "Influence", "Manipulation_(psychology)", "Deception", "Social_engineering_(security)",

    # # Psychology & Behavior
    # "Social_psychology", "Personality_psychology", "Cognitive_bias", "Emotional_intelligence",
    # "Body_language", "Empathy", "Trust_(social_science)", "Authority", "Conformity",

    # # Business & Economics
    # "Marketing", "Sales", "Trade", "Information_asymmetry", "Game_theory",
    # "Strategic_thinking", "Entrepreneurship", "Branding", "Consumer_behaviour",

    # # Communication
    # "Nonverbal_communication", "Active_listening", "Framing_(social_sciences)",
    # "Public_speaking", "Storytelling", "Rapport", "Conflict_resolution",

    # # Technology & AI
    # "Large_language_model", "Artificial_intelligence", "Machine_learning", "Prompt_engineering",
    # "Prompt_injection", "Natural_language_processing", "Neural_network", "Deep_learning",

    # # Politics & Society
    # "Political_psychology", "Propaganda", "Public_opinion", "Diplomacy", "Lobbying",
    # "Political_campaign", "Voting_behavior", "Political_polarization", "Ideology",

    # # Culture & Products
    # "Coffee", "Wine", "Luxury_goods", "Status_symbol", "Fashion", "Brand_loyalty",

    # # Strategy & Competition
    # "Bluffing", "Poker", "Chess", "Competition", "Zero-sum_game", "Cooperation",

    # # Philosophy & Ethics
    # "Ethics", "Moral_psychology", "Utilitarianism", "Consequentialism", "Virtue_ethics",

    # # Misc Relevant
    # "Obfuscation", "Credibility", "Scarcity", "Social_proof", "Reciprocity_(social_psychology)",
    # "Heuristic", "Decision-making", "Risk_assessment", "Behavioral_economics",
]

MAX_PAGES = 5000
MAX_DEPTH = 0
OUTPUT_DIR = Path("pages")

visited = set()
queue = deque()

# Setup
OUTPUT_DIR.mkdir(exist_ok=True)

# Add seeds
for seed in SEEDS:
    queue.append((seed, 0))

# BFS crawl
while queue and len(visited) < MAX_PAGES:
    title, depth = queue.popleft()

    if title in visited or depth > MAX_DEPTH:
        continue

    # Check if page already exists
    safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title.replace('_', ' '))
    filename = OUTPUT_DIR / f"{safe_name}.yaml"

    if filename.exists():
        print(f"[{len(visited)+1}/{MAX_PAGES}] Depth {depth}: {title} (cached - extracting links)")
        visited.add(title)

        # Still need to extract links for BFS even if content is cached
        if depth < MAX_DEPTH:
            try:
                url = f"https://en.wikipedia.org/wiki/{title}"
                headers = {'User-Agent': 'WikiCrawler/1.0 (Educational Research; Contact: your@email.com)'}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    content_div = soup.find('div', {'id': 'mw-content-text'})
                    if content_div:
                        links = content_div.find_all('a', href=re.compile(r'^/wiki/[^:]+$'))
                        for link in links[:50]:
                            link_title = link['href'].replace('/wiki/', '')
                            if link_title not in visited:
                                queue.append((link_title, depth + 1))
                time.sleep(0.5)  # Shorter delay for cached pages
            except Exception:
                pass
        continue

    print(f"[{len(visited)+1}/{MAX_PAGES}] Depth {depth}: {title}")

    url = f"https://en.wikipedia.org/wiki/{title}"
    headers = {'User-Agent': 'WikiCrawler/1.0 (Educational Research; Contact: your@email.com)'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get main content
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        continue

    # Extract text from paragraphs
    paragraphs = content_div.find_all('p')
    text = '\n\n'.join([p.get_text() for p in paragraphs])

    # Get title
    h1 = soup.find('h1', {'id': 'firstHeading'})
    page_title = h1.get_text() if h1 else title.replace('_', ' ')

    # Extract links
    link_elements = content_div.find_all('a', href=re.compile(r'^/wiki/[^:]+$'))
    links = [link['href'].replace('/wiki/', '') for link in link_elements]

    # Save as yaml file
    safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in page_title)
    filename = OUTPUT_DIR / f"{safe_name}.yaml"

    page_data = {
        'title': page_title,
        'url': url,
        'depth': depth,
        'content': text,
        'links': links[:100],  # Store first 100 links
        'total_links': len(links)
    }

    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(page_data, f, allow_unicode=True, default_flow_style=False)

    visited.add(title)

    # Add links to queue
    if depth < MAX_DEPTH:
        for link_title in links[:50]:
            if link_title not in visited:
                queue.append((link_title, depth + 1))

    time.sleep(1)


print(f"\nDone! Saved {len(visited)} pages to {OUTPUT_DIR}/")
