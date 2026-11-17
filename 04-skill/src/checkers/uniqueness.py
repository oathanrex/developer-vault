"""
AdSenseReady-AI: Lexical Diversity & Uniqueness Analyzer
-------------------------------------------------------
Mathematically quantifies vocabulary density, Type-Token Ratio (TTR),
and repetition penalties to protect publishers against scraped/spun content flags.
"""

import re
import math
from typing import Dict, Any, List


class UniquenessAnalyzer:
    """Evaluates lexical diversity, repetition patterns, and content originality metrics."""

    @classmethod
    def evaluate(cls, text: str) -> Dict[str, Any]:
        cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
        tokens = cleaned.split()
        total_tokens = len(tokens)

        if total_tokens < 30:
            return {
                "total_tokens": total_tokens,
                "lexical_diversity_score": 50.0,
                "status": "SAMPLE_TOO_SMALL",
                "summary": "Sample too small for rigorous lexical analysis."
            }

        unique_tokens = set(tokens)
        total_unique = len(unique_tokens)

        # 1. Type-Token Ratio (TTR)
        raw_ttr = total_unique / total_tokens

        # 2. Guiraud's Root TTR (Corrects for sample length bias: V / sqrt(N))
        root_ttr = total_unique / math.sqrt(total_tokens)

        # 3. Hapax Legomena (Words appearing exactly once)
        freq_map: Dict[str, int] = {}
        for t in tokens:
            freq_map[t] = freq_map.get(t, 0) + 1
        hapax_count = sum(1 for count in freq_map.values() if count == 1)
        hapax_ratio = hapax_count / total_tokens

        # 4. Trigram / Phrase Repetition Check (Detects spun or robotic loops)
        trigrams = [tuple(tokens[i:i+3]) for i in range(len(tokens) - 2)]
        total_trigrams = len(trigrams)
        unique_trigrams = len(set(trigrams))
        trigram_diversity = (unique_trigrams / total_trigrams) if total_trigrams > 0 else 1.0

        # Composite Lexical Score (0 - 100)
        # Healthy web article: Root TTR between 6.5 and 14, Trigram diversity > 0.85
        score_component_1 = min(50.0, (root_ttr / 10.0) * 50.0)
        score_component_2 = min(50.0, trigram_diversity * 50.0)
        composite_score = round(score_component_1 + score_component_2, 1)

        is_spun = trigram_diversity < 0.75 or raw_ttr < 0.25

        return {
            "total_tokens": total_tokens,
            "unique_tokens": total_unique,
            "raw_ttr": round(raw_ttr, 3),
            "root_ttr": round(root_ttr, 2),
            "hapax_ratio": round(hapax_ratio, 3),
            "trigram_diversity": round(trigram_diversity, 3),
            "composite_lexical_score": composite_score,
            "is_repetitive_or_spun": is_spun,
            "verdict": "HIGH_VOCABULARY_DEPTH" if composite_score >= 80 else ("ACCEPTABLE" if composite_score >= 60 else "LOW_DIVERSITY")
        }
