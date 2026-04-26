def calculate_final_score(scores):
    if not scores:
        return 0
    return round(sum(scores.values()) / len(scores), 2)


def identify_gaps(scores):
    return [skill for skill, score in scores.items() if score < 7]