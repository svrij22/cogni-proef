# Analysis: lyrics versus instrumental music

## Question

Do university students solve fewer mental-arithmetic sums correctly while hearing music with lyrics than while hearing the instrumental version of the same music?

The comparison is within person. A lower proportion correct with lyrics supports the hypothesis.

## Data

All trials come from `data/combined.csv` (478 rows, 29 people). That file stacks:

- `data/sep.csv`
- `data/seanna.csv`
- `data/anne.csv`
- Joseline’s seven exports, also stored together in `data/joseline.csv`

Session numbers in `participant` were shifted when the files were stacked, so the same session id is never reused. The person is `name`. The planned sample in the report is 28 students. These results use the 29 people present in the file.

## What entered the test

The outcome is the proportion of correct sums. `correct` is `true` or `false`. One lyrics trial (Participant 4) has no typed answer; that row is already marked `false`, so it counts as wrong.

One trial is stored as `Lyrics`. That label was treated as `lyrics`.

Condition `none` is silence. For 14 people it is the two opening practice sums, which the report leaves out of the scored data. Those 28 trials stay out of every test below. Joseline’s seven people have no silence rows. For 8 people (Bommel, Bram, Cas, Fay, Floor, Gerdien, Lotte, Lotte Jr) silence is a full block of three sums, in the same format as the music blocks and not always first. Those eight are the sample for the three condition differences.

The lyrics-versus-instrumental test uses all 29 people, because everyone completed both music conditions. That test uses 213 lyrics trials and 213 instrumental trials. People do not all have the same number of trials: most have 9 per condition, the named group from Sep has 3, aus has 6 instrumental trials, and Participant 3 has 12 instrumental trials.

## How the t-test was calculated

Trials from the same person are one observation. For each person:

1. Proportion correct with lyrics, \(p_L\).
2. Proportion correct with instrumental music, \(p_I\).
3. Difference \(d = p_L - p_I\).

A negative \(d\) means that person scored lower with lyrics. Someone with 9 trials and someone with 3 trials each contribute one difference.

The test is a one-sample t-test of those 29 differences against 0:

\[
t = \frac{\bar{d}}{s_d / \sqrt{n}}, \qquad df = n - 1
\]

\(\bar{d}\) is the mean difference, \(s_d\) its standard deviation, and \(n = 29\). The 95% confidence interval uses the same standard error and the critical value of \(t\) at \(df = 28\). The effect size is Cohen's \(d_z = \bar{d} / s_d\).

The reported p-value is two-sided. The hypothesis is directional (lyrics lower), so the one-sided p-value is reported as well.

## Differences

Proportions are rounded to one decimal in the table. The test used the unrounded values.

| Person | Lyrics trials | Instrumental trials | Lyrics % | Instrumental % | Difference (points) |
|---|---:|---:|---:|---:|---:|
| anne | 9 | 9 | 66.7 | 88.9 | −22.2 |
| aus | 9 | 6 | 77.8 | 83.3 | −5.6 |
| benjamin | 9 | 9 | 88.9 | 100.0 | −11.1 |
| Bommel | 3 | 3 | 100.0 | 100.0 | 0.0 |
| Bram | 3 | 3 | 33.3 | 33.3 | 0.0 |
| Cas | 3 | 3 | 66.7 | 66.7 | 0.0 |
| Deelnemer 1 | 9 | 9 | 100.0 | 66.7 | +33.3 |
| Deelnemer 2 | 9 | 9 | 33.3 | 0.0 | +33.3 |
| Deelnemer 3 | 9 | 9 | 55.6 | 55.6 | 0.0 |
| Deelnemer 4 | 9 | 9 | 33.3 | 55.6 | −22.2 |
| Deelnemer 5 | 9 | 9 | 66.7 | 66.7 | 0.0 |
| Deelnemer 6 | 9 | 9 | 66.7 | 77.8 | −11.1 |
| Deelnemer 7 | 9 | 9 | 66.7 | 66.7 | 0.0 |
| Fay | 3 | 3 | 66.7 | 100.0 | −33.3 |
| Floor | 3 | 3 | 66.7 | 100.0 | −33.3 |
| Gerdien | 3 | 3 | 66.7 | 66.7 | 0.0 |
| joran | 9 | 9 | 100.0 | 100.0 | 0.0 |
| Lotte | 3 | 3 | 33.3 | 33.3 | 0.0 |
| Lotte Jr | 3 | 3 | 100.0 | 100.0 | 0.0 |
| Mila | 9 | 9 | 33.3 | 55.6 | −22.2 |
| Milo | 9 | 9 | 88.9 | 100.0 | −11.1 |
| wouter | 9 | 9 | 55.6 | 88.9 | −33.3 |
| Participant 1 | 9 | 9 | 88.9 | 66.7 | +22.2 |
| Participant 2 | 9 | 9 | 88.9 | 66.7 | +22.2 |
| Participant 3 | 9 | 12 | 0.0 | 8.3 | −8.3 |
| Participant 4 | 9 | 9 | 55.6 | 66.7 | −11.1 |
| Participant 5 | 9 | 9 | 11.1 | 66.7 | −55.6 |
| Participant 6 | 9 | 9 | 44.4 | 77.8 | −33.3 |
| Participant 7 | 9 | 9 | 55.6 | 44.4 | +11.1 |

Fourteen people scored lower with lyrics, five scored higher, and ten scored the same. Among Joseline’s seven, two scored higher with lyrics (Deelnemer 1 and Deelnemer 2), two scored lower, and three scored the same.

## Result

Mean proportion correct was 0.625 with lyrics and 0.691 with instrumental music. The mean difference was \(\bar{d} = -0.066\) (SD \(0.204\)), about 6.6 percentage points lower with lyrics.

\[
t(28) = -1.74, \quad p = .092 \text{ (two-sided)}, \quad p = .046 \text{ (one-sided)}
\]

The 95% confidence interval for the mean difference is \([-0.144, 0.012]\), from about 14.4 percentage points lower with lyrics to 1.2 points higher. Cohen's \(d_z = -0.32\).

The two-sided test does not show a reliable difference: the interval includes zero. The one-sided test, in the direction of the hypothesis, sits just under .05.

The 29 differences are compatible with a normal distribution (Shapiro–Wilk \(p = .14\)). A Wilcoxon signed-rank test on the same differences gives \(p = .098\) (two-sided).

## No music: three differences

The three within-person differences, for the 8 people who completed a silence block, are:

- lyrics minus instrumental
- lyrics minus silence
- instrumental minus silence

Each difference is again one number per person: the difference in proportion correct. Each paired t-test is a one-sample t-test of those 8 differences against 0, with \(df = 7\). Joseline’s sessions have no silence rows, so this group is unchanged.

Mean proportion correct in this group was 0.917 in silence, 0.750 with instrumental music, and 0.667 with lyrics.

| Person | Silence % | Instrumental % | Lyrics % | Lyrics − instrumental | Lyrics − silence | Instrumental − silence |
|---|---:|---:|---:|---:|---:|---:|
| Bommel | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 |
| Bram | 100.0 | 33.3 | 33.3 | 0.0 | −66.7 | −66.7 |
| Cas | 100.0 | 66.7 | 66.7 | 0.0 | −33.3 | −33.3 |
| Fay | 66.7 | 100.0 | 66.7 | −33.3 | 0.0 | +33.3 |
| Floor | 100.0 | 100.0 | 66.7 | −33.3 | −33.3 | 0.0 |
| Gerdien | 100.0 | 66.7 | 66.7 | 0.0 | −33.3 | −33.3 |
| Lotte | 100.0 | 33.3 | 33.3 | 0.0 | −66.7 | −66.7 |
| Lotte Jr | 66.7 | 100.0 | 100.0 | 0.0 | +33.3 | +33.3 |

| Contrast | Mean difference | \(t(7)\) | Two-sided \(p\) | 95% CI | \(d_z\) |
|---|---:|---:|---:|---|---:|
| Lyrics − instrumental | −0.083 | −1.53 | .17 | [−0.212, 0.046] | −0.54 |
| Lyrics − silence | −0.250 | −2.05 | .080 | [−0.538, 0.038] | −0.72 |
| Instrumental − silence | −0.167 | −1.18 | .28 | [−0.500, 0.166] | −0.42 |

A negative mean means the first condition was less accurate. Lyrics sit below both other conditions, and instrumental sits below silence. Each confidence interval includes zero, so none of the three differences is reliable in these 8 people.

Taken together, the three condition means do not differ, \(F(2, 14) = 2.58\), \(p = .11\).

Several differences are exactly 0 or exactly one trial in three (0.333), because each person has only three trials per condition. A Wilcoxon signed-rank test on the same pairs gives \(p = .50\), \(p = .16\), and \(p = .34\) for the three contrasts in the table order.

The lyrics-versus-instrumental result for all 29 people stays the planned comparison. It uses both music conditions from everyone. This section adds silence only where a silence block was actually collected.

## Check on digit duration

The report shows each digit for 1.8 seconds. Five people (anne, aus, wouter, Participant 6, Participant 7) saw each digit for 1.5 seconds. The test above keeps them in, because they completed both music conditions.

Repeating the same paired t-test on the other 24 people gives \(t(23) = -1.08\), \(p = .29\), mean difference \(-0.045\), 95% CI \([-0.131, 0.041]\). That interval includes zero.
