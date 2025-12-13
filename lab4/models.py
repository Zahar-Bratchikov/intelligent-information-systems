from collections import defaultdict, Counter
from itertools import combinations

def relative_majority(profile: list[list[str]], alternatives: list[str]) -> tuple[str, dict[str, int]]:
    """Относительное большинство: побеждает тот, кто чаще стоит на 1-м месте."""
    first_choices = [ranking[0] for ranking in profile]
    counts = Counter(first_choices)
    winner = max(counts, key=counts.get)
    return winner, dict(counts)


def pairwise_comparison(profile: list[list[str]], a: str, b: str) -> int:
    """Возвращает разность: сколько предпочитают a над b минус наоборот."""
    score = 0
    for ranking in profile:
        if a in ranking and b in ranking:
            if ranking.index(a) < ranking.index(b):
                score += 1
            else:
                score -= 1
    return score


def condorcet_winner(profile: list[list[str]], alternatives: list[str]) -> str | None:
    """Явный победитель Кондорсе: побеждает всех в попарных сравнениях."""
    for a in alternatives:
        is_winner = True
        for b in alternatives:
            if a == b:
                continue
            if pairwise_comparison(profile, a, b) <= 0:
                is_winner = False
                break
        if is_winner:
            return a
    return None


def copeland_score(profile: list[list[str]], alternatives: list[str]) -> dict[str, int]:
    """Правило Копленда: +1 за победу, -1 за поражение, 0 за ничью."""
    scores = {a: 0 for a in alternatives}
    for a, b in combinations(alternatives, 2):
        diff = pairwise_comparison(profile, a, b)
        if diff > 0:
            scores[a] += 1
            scores[b] -= 1
        elif diff < 0:
            scores[a] -= 1
            scores[b] += 1
        # ничья: ничего не добавляем
    return scores


def simpson_score(profile: list[list[str]], alternatives: list[str]) -> dict[str, int]:
    """Правило Симпсона: минимальное число голосов, с которым кандидат побеждает любого другого."""
    scores = {}
    for a in alternatives:
        min_wins = float('inf')
        for b in alternatives:
            if a == b:
                continue
            wins = sum(1 for ranking in profile if ranking.index(a) < ranking.index(b))
            min_wins = min(min_wins, wins)
        scores[a] = min_wins
    return scores


def borda_count(profile: list[list[str]], alternatives: list[str]) -> dict[str, int]:
    """Модель Борда: p-1 очков за 1-е место, ..., 0 за последнее."""
    p = len(alternatives)
    scores = defaultdict(int)
    for ranking in profile:
        for i, alt in enumerate(ranking):
            scores[alt] += (p - 1 - i)
    # Убедимся, что все альтернативы присутствуют
    for alt in alternatives:
        scores.setdefault(alt, 0)
    return dict(scores)