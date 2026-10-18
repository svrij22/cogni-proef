# Analysis 2: accuracy, response time, and size of the miss

## Approach

The report's hypothesis is about the number of sums solved correctly. The usual analysis for this task is to test that accuracy on its own, and to test response time on its own. The size of the miss, how far the typed total was from the right total, is a third description of the mistakes.

The single score in the report adds a 10-point penalty for a wrong answer, the size of the miss, and the response time. Those parts are in different units. In milliseconds the total is almost only the response time. In seconds the 10-point penalty dominates. One impossible answer, such as 300, can outweigh the rest of a person's trials. This analysis leaves that combined score out and tests the three parts separately.

A higher proportion correct is better. A higher response time is slower. A higher absolute error is farther from the right total.

## Data

All trials come from `data/combined.csv` (478 rows, 29 people), stacked from `data/sep.csv`, `data/seanna.csv`, `data/anne.csv`, and Joseline’s seven exports. The person is `name`. The planned sample is 28 students. These results use the 29 people in the file.

One trial stored as `Lyrics` was treated as `lyrics`.

## What entered each test

**Proportion correct.** Every scored trial counts. `correct` is `true` or `false`. A blank answer is already marked `false`, so it counts as wrong. Impossible answers such as 300 also count as wrong.

**Response time.** The time is `rt_ms`, in milliseconds. Trials with no recorded time are left out of this outcome only. Every person still has at least one time in both music conditions, so all 29 people stay in the test. The score for a person is the mean of that person's trial times.

**Absolute error.** The value is `diff`, the distance from the correct sum. A trial enters this outcome when the typed answer is a possible total for eight digits from 1 to 9, so the answer is between 8 and 72. Three music trials stay out: Participant 3 typed 300, Participant 4 left the answer blank, and Participant 5 typed 3. The score for a person is the mean of the remaining distances.

**Silence.** For 14 people, condition `none` is the two opening practice sums. Those 28 trials stay out of every test. Joseline’s seven people have no silence rows. For 8 people (Bommel, Bram, Cas, Fay, Floor, Gerdien, Lotte, Lotte Jr), silence is a block of three sums in the same format as the music blocks. Those eight are the sample for the three condition differences.

The lyrics-versus-instrumental tests use all 29 people: 213 lyrics trials and 213 instrumental trials. Most people have 9 trials per condition. Sep’s named group has 3. aus has 6 instrumental trials. Participant 3 has 12 instrumental trials.

## How the tests were calculated

Each person contributes one number per condition. For accuracy that number is the proportion correct. For response time it is the mean time. For absolute error it is the mean distance on possible answers.

The lyrics-versus-instrumental test is a paired t-test. For each person, \(d\) is the lyrics value minus the instrumental value. A one-sample t-test asks whether the mean of those differences is zero:

\[
t = \frac{\bar{d}}{s_d / \sqrt{n}}, \qquad df = n - 1
\]

The 95% confidence interval uses the same standard error. The effect size is Cohen's \(d_z = \bar{d} / s_d\). The reported p-value is two-sided.

The same paired t-test is used for the other two contrasts, lyrics minus silence and instrumental minus silence, on the 8 people who completed a silence block.

Where the differences are a poor fit to a normal curve, a Wilcoxon signed-rank test on the same pairs is reported next to the t-test.

## Proportion correct

Mean proportion correct was 0.625 with lyrics and 0.691 with instrumental music. The mean difference was \(-0.066\) (SD \(0.204\)): about 6.6 percentage points lower with lyrics.

\[
t(28) = -1.74, \quad p = .092, \quad d_z = -0.32
\]

The 95% confidence interval is \([-0.144, 0.012]\). It includes zero. Fourteen people scored lower with lyrics, five scored higher, and ten scored the same. A Wilcoxon test gives \(p = .098\).

In the full sample, the two-sided test does not show a reliable accuracy difference. The hypothesis is directional, and the one-sided p-value is .046.

## Response time

Mean response time was 3290 ms with lyrics and 3087 ms with instrumental music. The mean difference was \(+203\) ms (SD \(539\)): people were slower with lyrics.

\[
t(28) = 2.02, \quad p = .053, \quad d_z = 0.38
\]

The 95% confidence interval is \([-2, 407]\) ms. It includes zero, by about 2 ms. Twenty people were slower with lyrics and nine were faster. The differences are skewed (Shapiro–Wilk \(p = .016\)). A Wilcoxon test gives \(p = .009\).

The t-test is compatible with no difference. The rank test, which fits these skewed differences better, shows longer times with lyrics.

## Absolute error

On possible answers, the mean distance from the correct sum was 1.57 with lyrics and 1.33 with instrumental music. The mean difference was \(+0.24\) points (SD \(1.60\)).

\[
t(28) = 0.81, \quad p = .42, \quad d_z = 0.15
\]

The 95% confidence interval is \([-0.37, 0.85]\). A few people still miss by many points inside the possible range, especially Participant 3, so the differences are skewed (Shapiro–Wilk \(p < .001\)). A Wilcoxon test gives \(p = .47\).

In the full sample, the size of the miss does not show a reliable lyrics effect.

## No music: three differences

For the 8 people with a silence block, each condition has three trials. Means:

| Outcome | Silence | Instrumental | Lyrics |
|---|---:|---:|---:|
| Proportion correct | 0.917 | 0.750 | 0.667 |
| Mean response time (ms) | 2643 | 2983 | 3351 |
| Mean absolute error | 0.17 | 0.33 | 0.67 |

Lyrics are the least accurate, the slowest, and the farthest from the right total. Silence is the most accurate and the fastest.

| Outcome | Contrast | Mean difference | \(t(7)\) | \(p\) | 95% CI | \(d_z\) |
|---|---|---:|---:|---:|---|---:|
| Proportion correct | Lyrics − instrumental | −0.083 | −1.53 | .17 | [−0.212, 0.046] | −0.54 |
| Proportion correct | Lyrics − silence | −0.250 | −2.05 | .080 | [−0.538, 0.038] | −0.72 |
| Proportion correct | Instrumental − silence | −0.167 | −1.18 | .28 | [−0.500, 0.166] | −0.42 |
| Response time (ms) | Lyrics − instrumental | +368 | 5.83 | <.001 | [218, 517] | 2.06 |
| Response time (ms) | Lyrics − silence | +708 | 9.35 | <.001 | [529, 887] | 3.31 |
| Response time (ms) | Instrumental − silence | +340 | 2.92 | .022 | [65, 616] | 1.03 |
| Absolute error | Lyrics − instrumental | +0.33 | 1.87 | .10 | [−0.09, 0.75] | 0.66 |
| Absolute error | Lyrics − silence | +0.50 | 1.73 | .13 | [−0.18, 1.18] | 0.61 |
| Absolute error | Instrumental − silence | +0.17 | 0.68 | .52 | [−0.41, 0.74] | 0.24 |

Accuracy and absolute error: each confidence interval includes zero. In these 8 people, none of those differences is reliable. Each person has only three trials per condition, so several accuracy differences are exactly 0 or exactly one trial in three.

Response time: all 8 people were slower with lyrics than with instrumental music, and all 8 were slower with lyrics than in silence. Seven of 8 were slower with instrumental music than in silence. Those three time differences are reliable in this group. Wilcoxon tests give \(p = .008\), \(p = .008\), and \(p = .016\).

This time effect is stronger than the time effect in the full sample of 29. The result to quote for the planned lyrics-versus-instrumental comparison is the test on all 29 people. The table above describes the eight people who also did a silence block.

## Check on digit duration

The report shows each digit for 1.8 seconds. Five people (anne, aus, wouter, Participant 6, Participant 7) saw each digit for 1.5 seconds. The tests above keep them in.

Repeating the lyrics-versus-instrumental tests on the other 24 people:

| Outcome | Mean difference | Test | 95% CI |
|---|---:|---|---|
| Proportion correct | −0.045 | \(t(23) = -1.08\), \(p = .29\) | [−0.131, 0.041] |
| Response time (ms) | +183 | \(t(23) = 1.61\), \(p = .12\) | [−51, 416] |
| Absolute error | +0.19 | \(t(23) = 0.55\), \(p = .59\) | [−0.53, 0.92] |

Each t-test interval includes zero. On response time in this subset the differences are still skewed, and a Wilcoxon test gives \(p = .027\).
