"""Tavily web search wrapper with demo mode fallback for OSINT collection.

LIVE: Uses Tavily API for real-time web search when TAVILY_API_KEY is set.
Falls back to pre-loaded demo results when no API key is available.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class SearchResult:
    """A single web search result."""
    title: str = ""
    url: str = ""
    content: str = ""
    score: float = 0.0
    published_date: str = ""


DEMO_RESULTS: dict[str, list[dict[str, Any]]] = {
    "taiwan strait": [
        {
            "title": "PLA Launches Joint Sword-2026A Exercises Around Taiwan",
            "url": "https://www.reuters.com/world/asia-pacific/pla-exercises-taiwan-2026-03-15",
            "content": "China's military launched large-scale exercises around Taiwan on March 15, deploying naval vessels, aircraft, and missile units in what officials described as a rehearsal for a potential blockade. The exercises, code-named Joint Sword-2026A, involved the Eastern Theater Command and included live-fire drills in six zones surrounding Taiwan. Commercial shipping was forced to reroute, with major carriers Maersk and Evergreen reporting 3-5 day delays.",
            "score": 0.95,
            "published_date": "2026-03-15"
        },
        {
            "title": "TSMC Warns of Production Delays Amid Taiwan Strait Tensions",
            "url": "https://www.bloomberg.com/news/tsmc-production-delays-2026",
            "content": "Taiwan Semiconductor Manufacturing Co. issued a supply chain advisory warning customers including Apple and NVIDIA of potential production delays due to regional security concerns. CEO C.C. Wei stated that while fabrication facilities remain operational, logistics disruptions could affect wafer shipments. TSMC's Tainan Fab 18, which produces cutting-edge 3nm chips, relies on Kaohsiung port for material imports and finished product exports.",
            "score": 0.92,
            "published_date": "2026-03-18"
        },
        {
            "title": "US Carrier Strike Group Surges to Western Pacific",
            "url": "https://www.defense.gov/News/Releases/Release/Article/us-carrier-pacific-2026",
            "content": "The USS Ronald Reagan Carrier Strike Group has been ordered to the Western Pacific in response to PLA military exercises near Taiwan. Admiral Samuel Paparo, Commander of US Indo-Pacific Command, stated the deployment demonstrates 'ironclad commitment to a free and open Indo-Pacific.' The destroyer USS Mustin conducted a Taiwan Strait transit on March 17.",
            "score": 0.90,
            "published_date": "2026-03-17"
        },
        {
            "title": "Shipping Insurance Rates Spike 340% for Taiwan Strait Transit",
            "url": "https://www.lloydslist.com/insurance-taiwan-strait-2026",
            "content": "War risk insurance premiums for vessels transiting the Taiwan Strait have surged 340% following PLA military exercises. Lloyd's of London has designated the strait a 'listed area' requiring additional coverage. Maersk, Evergreen Marine, and Yang Ming have announced temporary rerouting of vessels through the Bashi Channel or around the Philippines, adding 3-7 days to transit times. Industry analysts estimate the disruption costs $1.2 billion per week in delayed shipments.",
            "score": 0.88,
            "published_date": "2026-03-19"
        },
        {
            "title": "Suspected State-Sponsored Cyber Attack Targets Taiwan Port Systems",
            "url": "https://www.wired.com/story/taiwan-port-cyber-attack-2026",
            "content": "Taiwan's Ministry of Digital Affairs confirmed a sophisticated cyber attack targeting port management systems at Kaohsiung and Keelung. The attack, attributed to a state-sponsored group, disrupted container tracking and automated crane operations for approximately 18 hours. Cybersecurity firm Mandiant identified tactics consistent with APT41, a Chinese cyber espionage group. The incident compounded existing supply chain disruptions from PLA military exercises.",
            "score": 0.85,
            "published_date": "2026-03-20"
        },
    ],
    "semiconductor supply chain disruption": [
        {
            "title": "Global Chip Shortage Warning as Taiwan Strait Tensions Escalate",
            "url": "https://www.ft.com/content/chip-shortage-taiwan-2026",
            "content": "The Semiconductor Industry Association warned that a prolonged disruption to Taiwan's chip production could trigger a global shortage exceeding the 2021-2023 crisis. TSMC produces over 90% of the world's most advanced semiconductors. Alternative foundries Samsung and Intel Foundry Services lack capacity to compensate. Apple, NVIDIA, AMD, and Qualcomm have begun activating contingency supply agreements.",
            "score": 0.93,
            "published_date": "2026-03-19"
        },
        {
            "title": "ASML Export License Review Adds Uncertainty to Chip Equipment Supply",
            "url": "https://www.semafor.com/article/asml-export-review-2026",
            "content": "The Dutch government has initiated a review of ASML's export licenses for EUV lithography equipment shipments to Taiwan, citing 'evolving security considerations.' ASML's TWINSCAN NXE:3800E scanners are essential for producing chips at 3nm and below. The review could delay critical equipment deliveries to TSMC by 3-6 months, potentially affecting the production ramp of next-generation chips for major customers.",
            "score": 0.89,
            "published_date": "2026-03-19"
        },
    ],
    "us military western pacific deployment": [
        {
            "title": "Pentagon Orders Additional Assets to Indo-Pacific Theater",
            "url": "https://www.militarytimes.com/pentagon-indopac-2026",
            "content": "The Department of Defense has ordered additional military assets to the Indo-Pacific theater, including the activation of Joint Task Force 7 at Naval Base Guam. The deployment includes an amphibious ready group, additional P-8 maritime patrol aircraft, and a submarine surge. Officials described the moves as 'prudent planning' in response to Chinese military exercises near Taiwan.",
            "score": 0.87,
            "published_date": "2026-03-18"
        },
    ],
}


def search_web(query: str, max_results: int = 5) -> list[SearchResult]:
    """Search the web using Tavily API or return demo results.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of SearchResult objects.
    """
    api_key = os.environ.get("TAVILY_API_KEY")

    if api_key:
        return _live_search(query, max_results, api_key)
    else:
        return _demo_search(query, max_results)


def _live_search(query: str, max_results: int, api_key: str) -> list[SearchResult]:
    """Execute live Tavily web search."""
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results, search_depth="advanced")

        results = []
        for item in response.get("results", [])[:max_results]:
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                content=item.get("content", ""),
                score=item.get("score", 0.0),
                published_date=item.get("published_date", ""),
            ))
        return results
    except Exception as e:
        print(f"Tavily search failed, falling back to demo mode: {e}")
        return _demo_search(query, max_results)


def _demo_search(query: str, max_results: int) -> list[SearchResult]:
    """Return pre-loaded demo results matching the query."""
    query_lower = query.lower()
    all_results: list[SearchResult] = []

    for key, items in DEMO_RESULTS.items():
        if any(term in query_lower for term in key.split()):
            for item in items:
                all_results.append(SearchResult(**item))

    # If no keyword match, return all demo results
    if not all_results:
        for items in DEMO_RESULTS.values():
            for item in items:
                all_results.append(SearchResult(**item))

    # Sort by score and limit
    all_results.sort(key=lambda r: r.score, reverse=True)
    return all_results[:max_results]
