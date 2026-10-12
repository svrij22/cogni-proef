"""Reproduce the results in analysis_2.md.

Run from anywhere:

    uv run --with scipy python data/out/analyze.py

The data file is data/combined.csv, one folder up from this script.
Each person contributes one number per condition. A paired t-test then
asks whether the mean of the within-person differences is zero.
"""

import csv
from collections import defaultdict
from pathlib import Path

from scipy import stats

# combined.csv stacks Sep.csv, jeanne.csv, and anne.csv.
DATA = Path(__file__).resolve().parents[1] / "combined.csv"

# Eight digits drawn from 1 to 9 sum to something between 8 and 72.
# Answers outside that range, and blank answers, stay out of the
# absolute-error outcome. They still count as wrong for accuracy.
MIN_SUM = 8
MAX_SUM = 72

# Contrasts are always "first condition minus second condition".
# Negative accuracy means the first condition was less accurate.
# Positive time or error means the first condition was slower or farther off.
CONTRASTS = (
    ("lyrics", "instrumental"),
    ("lyrics", "none"),
    ("instrumental", "none"),
)


def condition(row):
    """One trial is stored as 'Lyrics'. Treat that as lyrics."""
    return row["condition"].strip().lower()


def load_rows():
    with DATA.open(newline="") as handle:
        return list(csv.DictReader(handle))


def silence_group(rows):
    """People whose silence rows are a real block, not the practice pair.

    Fourteen people start with exactly two sums in silence. The report
    leaves those practice sums out. Eight people have a silence block of
    three sums, in the same format as the music blocks. Only those eight
    enter the comparisons with silence.
    """
    blocks = defaultdict(list)
    for row in rows:
        name = row["name"]
        cond = condition(row)
        if not blocks[name] or blocks[name][-1][0] != cond:
            blocks[name].append([cond, 1])
        else:
            blocks[name][-1][1] += 1

    with_silence = []
    for name, person_blocks in blocks.items():
        if any(cond == "none" and size >= 3 for cond, size in person_blocks):
            with_silence.append(name)
    return sorted(with_silence, key=str.lower)


def person_scores(rows, with_silence):
    """One list of trial values per person, per condition, per outcome.

    Accuracy uses every trial: correct is 1, anything else is 0.
    Response time uses trials that have rt_ms. The person's score is
    the mean of those times, computed later.
    Absolute error uses diff, and only when the typed answer is a
    possible total. The person's score is the mean of those distances.
    Silence trials are kept only for the eight people with a real block.
    """
    scores = defaultdict(lambda: defaultdict(lambda: {"acc": [], "rt": [], "abs": []}))
    saw_fast_digits = set()

    for row in rows:
        cond = condition(row)
        if cond not in ("lyrics", "instrumental", "none"):
            continue
        if cond == "none" and row["name"] not in with_silence:
            continue

        bucket = scores[row["name"]][cond]
        bucket["acc"].append(1 if row["correct"] == "true" else 0)

        if row["show_s"] == "1.5" and cond != "none":
            saw_fast_digits.add(row["name"])

        if row["rt_ms"] != "":
            bucket["rt"].append(int(row["rt_ms"]))

        if row["answer"] != "" and row["diff"] != "":
            answer = float(row["answer"])
            if MIN_SUM <= answer <= MAX_SUM:
                bucket["abs"].append(int(row["diff"]))

    return scores, saw_fast_digits


def mean(values):
    return sum(values) / len(values)


def paired(scores, names, outcome, first, second):
    """Paired t-test on one outcome.

    For each person, d = score(first) - score(second). People missing
    either condition are skipped. Then:

        t = mean(d) / (sd(d) / sqrt(n)),  df = n - 1

    The 95% interval is mean(d) plus or minus the critical t times the
    standard error. Cohen's dz is mean(d) / sd(d). The p-value is
    two-sided. Wilcoxon is reported because a few differences are tied
    or skewed, so the t-test is not the only check.
    """
    differences = []
    first_scores = []
    second_scores = []
    for name in names:
        a = scores[name][first][outcome]
        b = scores[name][second][outcome]
        if not a or not b:
            continue
        first_scores.append(mean(a))
        second_scores.append(mean(b))
        differences.append(mean(a) - mean(b))

    n = len(differences)
    result = stats.ttest_1samp(differences, popmean=0)
    sd = stats.tstd(differences)
    standard_error = sd / n**0.5
    low, high = stats.t.interval(0.95, n - 1, loc=mean(differences), scale=standard_error)
    wilcoxon = stats.wilcoxon(differences, alternative="two-sided")
    shapiro = stats.shapiro(differences)

    return {
        "n": n,
        "mean_first": mean(first_scores),
        "mean_second": mean(second_scores),
        "mean_d": mean(differences),
        "sd": sd,
        "t": result.statistic,
        "df": n - 1,
        "p": result.pvalue,
        "ci": (low, high),
        "dz": mean(differences) / sd,
        "wilcoxon_p": wilcoxon.pvalue,
        "shapiro_p": shapiro.pvalue,
        "lower": sum(d < 0 for d in differences),
        "higher": sum(d > 0 for d in differences),
        "tie": sum(d == 0 for d in differences),
    }


def print_test(title, result, unit=""):
    suffix = f" {unit}" if unit else ""
    low, high = result["ci"]
    print(title)
    print(
        f"  means {result['mean_first']:.3f} vs {result['mean_second']:.3f}"
        f"   difference {result['mean_d']:+.3f}{suffix}"
        f"   SD {result['sd']:.3f}"
    )
    print(
        f"  t({result['df']}) = {result['t']:.2f}"
        f"   p = {result['p']:.4f}"
        f"   95% CI [{low:.3f}, {high:.3f}]"
        f"   dz = {result['dz']:.2f}"
    )
    print(
        f"  lower {result['lower']}, higher {result['higher']}, tie {result['tie']}"
        f"   Shapiro p = {result['shapiro_p']:.4f}"
        f"   Wilcoxon p = {result['wilcoxon_p']:.4f}"
    )


def main():
    rows = load_rows()
    with_silence = silence_group(rows)
    scores, saw_fast_digits = person_scores(rows, with_silence)
    everyone = sorted(scores, key=str.lower)

    print(f"rows {len(rows)}   people {len(everyone)}   silence block {len(with_silence)}")
    print("silence block:", ", ".join(with_silence))
    print()

    # Planned comparison: lyrics versus instrumental, every person who
    # did both music conditions. Practice sums are already omitted.
    print("Lyrics versus instrumental, all people")
    for outcome, unit in (("acc", ""), ("rt", "ms"), ("abs", "points")):
        print_test(outcome, paired(scores, everyone, outcome, "lyrics", "instrumental"), unit)
        print()

    # Same three outcomes, now with silence, and only for the eight
    # people who completed a silence block. Each contrast is its own
    # paired t-test on that group's within-person differences.
    print("Three differences, silence-block group")
    for outcome, unit in (("acc", ""), ("rt", "ms"), ("abs", "points")):
        for first, second in CONTRASTS:
            title = f"{outcome}: {first} - {second}"
            print_test(title, paired(scores, with_silence, outcome, first, second), unit)
            print()

    # The report shows each digit for 1.8 s. Five people saw 1.5 s.
    # Repeat the planned comparison without them.
    at_report_duration = [name for name in everyone if name not in saw_fast_digits]
    print(f"Without 1.5 s digits, n = {len(at_report_duration)}")
    print("left out:", ", ".join(sorted(saw_fast_digits, key=str.lower)))
    for outcome, unit in (("acc", ""), ("rt", "ms"), ("abs", "points")):
        print_test(outcome, paired(scores, at_report_duration, outcome, "lyrics", "instrumental"), unit)
        print()


if __name__ == "__main__":
    main()
