"""Draw boxplots and diagrams for lyrics versus instrumental music.

Run from anywhere:

    uv run --with scipy --with matplotlib python data/out/plots.py

Figures are written to data/out/figures/. The scores come from
analyze.py, so every figure uses the same exclusions as the t-tests:
practice sums left out, and absolute error only for possible totals
(8 to 72). Silence is not shown; the comparison is lyrics against
instrumental only.
"""

from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats

from analyze import MAX_SUM, MIN_SUM, condition, load_rows, mean, person_scores, silence_group

OUT = Path(__file__).resolve().parent / "figures"

MUSIC = ("lyrics", "instrumental")

# One colour per condition, the same in every figure.
COLOURS = {"lyrics": "#2a78d6", "instrumental": "#eb6834"}
LABELS = {"lyrics": "Lyrics", "instrumental": "Instrumental"}
INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e4e3df"
TIE = "#c3c2b7"

# key, title, scale to display units, unit, whether higher is better
OUTCOMES = (
    ("acc", "Proportion correct", 100, "%", True),
    ("rt", "Mean response time", 1 / 1000, "s", False),
    ("abs", "Mean absolute error", 1, "points", False),
)

plt.rcParams.update({
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": "white",
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

BOX_STYLE = {
    "medianprops": {"color": INK, "linewidth": 2},
    "whiskerprops": {"color": MUTED},
    "capprops": {"color": MUTED},
    "boxprops": {"edgecolor": MUTED},
    "flierprops": {"marker": "o", "markersize": 4,
                   "markerfacecolor": MUTED, "markeredgecolor": "none"},
}


def person_means(scores, names, outcome, scale):
    """Per person, (lyrics, instrumental) means in display units.

    Only people with values in both conditions are kept, so the points
    in a figure are the same people the paired test used.
    """
    kept = []
    for name in names:
        lyrics = scores[name]["lyrics"][outcome]
        instrumental = scores[name]["instrumental"][outcome]
        if lyrics and instrumental:
            kept.append((name, mean(lyrics) * scale, mean(instrumental) * scale))
    return kept


def music_trials(rows):
    """Trial rows from the two music conditions."""
    return [row for row in rows if condition(row) in MUSIC]


def jitter(n, width=0.025):
    """Small fixed offsets so tied points stay visible without randomness."""
    return [((i % 7) - 3) * width for i in range(n)]


def save(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT / filename)
    plt.close(fig)


def music_boxplots(scores, names, filename):
    """Boxplot per condition with each person as a dot."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2))
    for ax, (outcome, label, scale, unit, _) in zip(axes, OUTCOMES):
        kept = person_means(scores, names, outcome, scale)
        columns = [[k[1] for k in kept], [k[2] for k in kept]]
        parts = ax.boxplot(columns, widths=0.45, patch_artist=True, showfliers=False,
                           **BOX_STYLE)
        for patch, cond in zip(parts["boxes"], MUSIC):
            patch.set_facecolor(COLOURS[cond])
            patch.set_alpha(0.35)
        offsets = jitter(len(kept))
        for pos, col, cond in zip((1, 2), columns, MUSIC):
            ax.scatter([pos + o for o in offsets], col, s=22, color=COLOURS[cond],
                       edgecolor="white", linewidth=0.8, zorder=3)
            ax.scatter([pos], [mean(col)], marker="D", s=40, color="white",
                       edgecolor=INK, linewidth=1.2, zorder=4)
        ax.set_xticks([1, 2], [LABELS[c] for c in MUSIC])
        ax.set_title(label)
        ax.set_ylabel(unit)
    fig.suptitle(f"Lyrics versus instrumental (n = {len(kept)} people)",
                 x=0.01, ha="left", fontweight="bold")
    fig.text(0.01, -0.03, "Box: median and quartiles. Diamond: mean. Dot: one person.",
             color=MUTED, fontsize=8)
    save(fig, filename)


def difference_boxplots(scores, names, filename):
    """Lyrics minus instrumental per person, one panel per outcome."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2))
    for ax, (outcome, label, scale, unit, _) in zip(axes, OUTCOMES):
        diffs = [a - b for _, a, b in person_means(scores, names, outcome, scale)]
        ax.axhline(0, color=MUTED, linewidth=1)
        parts = ax.boxplot([diffs], widths=0.4, patch_artist=True, showfliers=False,
                           **BOX_STYLE)
        parts["boxes"][0].set_facecolor("#cde2fb")
        ax.scatter([1 + o for o in jitter(len(diffs), 0.03)], diffs, s=22,
                   color=COLOURS["lyrics"], edgecolor="white", linewidth=0.8, zorder=3)

        # Mean difference with its 95% interval, beside the box.
        n = len(diffs)
        se = stats.tstd(diffs) / n**0.5
        low, high = stats.t.interval(0.95, n - 1, loc=mean(diffs), scale=se)
        ax.errorbar([1.4], [mean(diffs)], yerr=[[mean(diffs) - low], [high - mean(diffs)]],
                    fmt="D", color=INK, markerfacecolor="white", capsize=4, linewidth=1.5)
        ax.annotate(f"mean {mean(diffs):+.2f}\n95% CI", (1.4, high), xytext=(0, 6),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=8, color=MUTED)

        ax.set_xticks([1, 1.4], ["People", "Mean"])
        ax.set_xlim(0.6, 1.7)
        ax.set_title(label)
        ax.set_ylabel(f"Lyrics − instrumental ({unit})")
    fig.suptitle(f"Within-person difference, lyrics minus instrumental (n = {n})",
                 x=0.01, ha="left", fontweight="bold")
    save(fig, filename)


def mean_bars(scores, names, filename):
    """Group mean per condition with a 95% interval for each mean."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    for ax, (outcome, label, scale, unit, _) in zip(axes, OUTCOMES):
        kept = person_means(scores, names, outcome, scale)
        for pos, (cond, idx) in enumerate(zip(MUSIC, (1, 2))):
            values = [k[idx] for k in kept]
            n = len(values)
            se = stats.tstd(values) / n**0.5
            half = stats.t.ppf(0.975, n - 1) * se
            ax.bar(pos, mean(values), width=0.6, color=COLOURS[cond])
            ax.errorbar(pos, mean(values), yerr=half, color=INK, capsize=5, linewidth=1.5)
            ax.annotate(f"{mean(values):.1f}" if outcome == "acc" else f"{mean(values):.2f}", (pos, mean(values) + half), xytext=(0, 4),
                        textcoords="offset points", ha="center", fontsize=9, color=INK)
        ax.set_xticks([0, 1], [LABELS[c] for c in MUSIC])
        ax.set_title(label)
        ax.set_ylabel(unit)
    fig.suptitle("Group means with 95% confidence intervals",
                 x=0.01, ha="left", fontweight="bold")
    save(fig, filename)


def person_scatter(scores, names, filename):
    """Each person's lyrics score against their instrumental score.

    Points below the diagonal scored lower with lyrics. Several people
    share the same accuracy pair, so dot size shows how many.
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.3))
    for ax, (outcome, label, scale, unit, _) in zip(axes, OUTCOMES):
        kept = person_means(scores, names, outcome, scale)
        counts = defaultdict(int)
        for _, a, b in kept:
            counts[(round(b, 6), round(a, 6))] += 1
        xs = [x for x, _ in counts]
        ys = [y for _, y in counts]
        sizes = [30 * c for c in counts.values()]
        low = min(xs + ys)
        high = max(xs + ys)
        pad = (high - low) * 0.08
        ax.plot([low - pad, high + pad], [low - pad, high + pad], color=MUTED,
                linewidth=1, linestyle="--", zorder=1)
        ax.scatter(xs, ys, s=sizes, color=COLOURS["lyrics"], alpha=0.8,
                   edgecolor="white", linewidth=1, zorder=3)
        for (x, y), c in counts.items():
            if c > 1:
                ax.text(x, y, str(c), ha="center", va="center", fontsize=7,
                        color="white", zorder=4)
        ax.set_xlim(low - pad, high + pad)
        ax.set_ylim(low - pad, high + pad)
        ax.set_aspect("equal")
        ax.grid(axis="x", color=GRID)
        ax.set_xlabel(f"Instrumental ({unit})")
        ax.set_ylabel(f"Lyrics ({unit})")
        ax.set_title(label)
    fig.suptitle("Each person, lyrics against instrumental",
                 x=0.01, ha="left", fontweight="bold")
    fig.text(0.01, -0.03, "Dashed line: same score in both conditions. "
             "Number in a dot: people with that exact pair.", color=MUTED, fontsize=8)
    save(fig, filename)


def direction_counts(scores, names, filename):
    """How many people did better with lyrics, the same, or better with
    instrumental, on each outcome. 'Better' means more correct, faster,
    or closer to the right total."""
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID)
    rows = []
    for outcome, label, scale, _, higher_better in OUTCOMES:
        better_lyrics = tie = better_instrumental = 0
        for _, a, b in person_means(scores, names, outcome, scale):
            if a == b:
                tie += 1
            elif (a > b) == higher_better:
                better_lyrics += 1
            else:
                better_instrumental += 1
        rows.append((label, better_lyrics, tie, better_instrumental))

    for i, (label, lyr, tie, ins) in enumerate(rows):
        left = 0
        for value, colour, ink in ((lyr, COLOURS["lyrics"], "white"), (tie, TIE, INK),
                                   (ins, COLOURS["instrumental"], "white")):
            if value:
                ax.barh(i, value, left=left, color=colour, edgecolor="white", linewidth=2,
                        height=0.6)
                ax.text(left + value / 2, i, str(value), ha="center", va="center",
                        color=ink, fontsize=9)
            left += value
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlabel("People")
    handles = [Patch(color=COLOURS["lyrics"], label="Better with lyrics"),
               Patch(color=TIE, label="No difference"),
               Patch(color=COLOURS["instrumental"], label="Better with instrumental")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3,
              frameon=False)
    ax.set_title("Which condition each person did better in", loc="left")
    save(fig, filename)


def person_differences(scores, names, filename):
    """One row per person: proportion correct in each condition, sorted
    by lyrics minus instrumental."""
    kept = person_means(scores, names, "acc", 100)
    kept.sort(key=lambda item: item[1] - item[2])
    fig, ax = plt.subplots(figsize=(7, 8))
    ax.grid(axis="x", color=GRID)
    ax.grid(axis="y", visible=False)
    for i, (_, lyrics, instrumental) in enumerate(kept):
        ax.plot([instrumental, lyrics], [i, i], color=GRID, linewidth=2, zorder=1)
        # Small vertical offset so a tie still shows both dots.
        ax.scatter([instrumental], [i + 0.15], s=36, color=COLOURS["instrumental"],
                   zorder=3, edgecolor="white", linewidth=0.8)
        ax.scatter([lyrics], [i - 0.15], s=36, color=COLOURS["lyrics"],
                   zorder=3, edgecolor="white", linewidth=0.8)
    ax.set_yticks(range(len(kept)), [k[0] for k in kept])
    ax.invert_yaxis()
    ax.set_xlim(-5, 105)
    ax.set_xlabel("Proportion correct (%)")
    ax.scatter([], [], color=COLOURS["lyrics"], label="Lyrics")
    ax.scatter([], [], color=COLOURS["instrumental"], label="Instrumental")
    ax.legend(loc="lower left", frameon=False)
    ax.set_title("Proportion correct per person, largest drop with lyrics first",
                 loc="left")
    save(fig, filename)


def trial_rt_boxplot(rows, filename):
    """Trial-level response times, split by correct and wrong answers."""
    times = defaultdict(list)
    for row in music_trials(rows):
        if row["rt_ms"] != "":
            key = (condition(row), row["correct"] == "true")
            times[key].append(int(row["rt_ms"]) / 1000)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    positions, columns, colours, ticks = [], [], [], []
    for group, correct in enumerate((True, False)):
        for offset, cond in zip((-0.22, 0.22), MUSIC):
            positions.append(group + offset)
            columns.append(times[(cond, correct)])
            colours.append(COLOURS[cond])
            ticks.append((group + offset, f"{len(times[(cond, correct)])}"))
    parts = ax.boxplot(columns, positions=positions, widths=0.36, patch_artist=True,
                       **BOX_STYLE)
    for patch, colour in zip(parts["boxes"], colours):
        patch.set_facecolor(colour)
        patch.set_alpha(0.35)
    ax.set_xticks([0, 1], ["Correct answers", "Wrong answers"])
    for x, n in ticks:
        ax.text(x, -0.03, f"{n} trials", transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=7, color=MUTED)
    ax.tick_params(axis="x", pad=20)
    ax.set_ylabel("Response time (s)")
    handles = [Patch(facecolor=COLOURS[c], alpha=0.35, edgecolor=MUTED, label=LABELS[c])
               for c in MUSIC]
    ax.legend(handles=handles, loc="upper left", frameon=False)
    ax.set_title("Response time per trial, correct and wrong answers", loc="left")
    fig.text(0.01, -0.03, "Dots: trials beyond 1.5 × IQR.", color=MUTED, fontsize=8)
    save(fig, filename)


def error_histogram(rows, filename):
    """How far wrong answers were from the right total, by condition.
    Correct answers (distance 0) are left out to show the misses."""
    misses = defaultdict(list)
    for row in music_trials(rows):
        if row["answer"] == "" or row["diff"] == "":
            continue
        if MIN_SUM <= float(row["answer"]) <= MAX_SUM and int(row["diff"]) > 0:
            misses[condition(row)].append(int(row["diff"]))
    top = max(max(v) for v in misses.values())
    bins = [b - 0.5 for b in range(1, top + 2)]
    fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True, sharey=True)
    for ax, cond in zip(axes, MUSIC):
        ax.hist(misses[cond], bins=bins, color=COLOURS[cond], edgecolor="white", linewidth=2)
        ax.set_title(f"{LABELS[cond]}: {len(misses[cond])} wrong answers", loc="left")
        ax.set_ylabel("Trials")
    axes[-1].set_xlabel("Distance from the correct total (points)")
    save(fig, filename)


def accuracy_by_position(rows, filename):
    """Proportion correct by position within a three-sum block, pooled
    over people. A rough check for practice or fatigue within blocks."""
    counts = defaultdict(lambda: [0, 0])
    for row in music_trials(rows):
        position = (int(row["trial"]) - 1) % 3 + 1
        counts[(condition(row), position)][0] += row["correct"] == "true"
        counts[(condition(row), position)][1] += 1
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for offset, cond in zip((-0.2, 0.2), MUSIC):
        xs = [1, 2, 3]
        ys = [100 * counts[(cond, x)][0] / counts[(cond, x)][1] for x in xs]
        ax.bar([x + offset for x in xs], ys, width=0.38, color=COLOURS[cond],
               label=LABELS[cond])
        for x, y in zip(xs, ys):
            ax.text(x + offset, y + 1.5, f"{y:.0f}", ha="center", fontsize=8, color=INK)
    ax.set_xticks([1, 2, 3], ["1st sum", "2nd sum", "3rd sum"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Proportion correct (%)")
    ax.set_title("Proportion correct by position in a three-sum block", loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)
    save(fig, filename)


def accuracy_heatmap(scores, names, filename):
    """Person by condition grid of proportion correct."""
    grid = [[100 * mean(scores[name][c]["acc"]) for c in MUSIC] for name in names]
    fig, ax = plt.subplots(figsize=(4.2, 9))
    image = ax.imshow(grid, cmap="Blues", vmin=0, vmax=100, aspect="auto")
    ax.grid(False)
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            ax.text(j, i, f"{value:.0f}", ha="center", va="center", fontsize=8,
                    color="white" if value > 60 else INK)
    ax.set_xticks(range(2), [LABELS[c] for c in MUSIC])
    ax.set_yticks(range(len(names)), names)
    ax.xaxis.tick_top()
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(image, ax=ax, label="Proportion correct (%)", shrink=0.5)
    ax.set_title("Proportion correct per person", loc="left", pad=28)
    save(fig, filename)


def main():
    OUT.mkdir(exist_ok=True)
    rows = load_rows()
    scores, _ = person_scores(rows, silence_group(rows))
    everyone = sorted(scores, key=str.lower)

    music_boxplots(scores, everyone, "01_boxplots.png")
    difference_boxplots(scores, everyone, "02_boxplots_difference.png")
    mean_bars(scores, everyone, "03_means_with_ci.png")
    person_scatter(scores, everyone, "04_lyrics_against_instrumental.png")
    direction_counts(scores, everyone, "05_who_did_better.png")
    person_differences(scores, everyone, "06_accuracy_per_person.png")
    trial_rt_boxplot(rows, "07_rt_correct_and_wrong.png")
    error_histogram(rows, "08_error_size.png")
    accuracy_by_position(rows, "09_accuracy_by_position.png")
    accuracy_heatmap(scores, everyone, "10_accuracy_heatmap.png")
    print(f"figures written to {OUT}")


if __name__ == "__main__":
    main()
