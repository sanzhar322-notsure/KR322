"""Regenerate the report figures from the survey response counts (n = 40).

Figures are numbered in the order they appear in the Results section:
1 study interaction, 2 reasons, 3 social/loneliness, 4 social-life effect.
"""
import math
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import Patch

N = 40
OUT = sys.argv[1] if len(sys.argv) > 1 else 'figures'
r0 = lambda x: int(math.floor(x + 0.5))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': '#888',
                     'xtick.color': '#555', 'ytick.color': '#333'})
INK, MUTED = '#222', '#666'
LEV = ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']
COL = ['#b8312f', '#ec8a85', '#c9c8c3', '#6da7ec', '#1c5cab']

# Likert counts in LEV order (from the Microsoft Forms export)
LIKERT = {
    'Q3': [4, 11, 7, 17, 1], 'Q4': [4, 8, 3, 21, 4], 'Q5': [0, 10, 6, 18, 6],
    'Q6': [0, 4, 8, 22, 6], 'Q7': [1, 7, 7, 17, 8], 'Q8': [4, 12, 8, 15, 1],
    'Q9': [4, 7, 7, 20, 2], 'Q10': [7, 20, 7, 4, 2], 'Q11': [2, 15, 7, 12, 4],
}
Q12 = [('It is available anytime', 17), ('It gives better answers', 10), ('It is faster', 7),
       ('I feel less embarrassed', 5), ('Other', 1)]
Q13 = [('No effect', 14), ('It makes me rely on AI too much', 12),
       ('It helps me communicate in another language', 8),
       ('It makes me spend less time with friends', 4), ('It helps me talk to new people', 2)]


def likert(items, fname, title):
    fig, ax = plt.subplots(figsize=(8.6, 0.62 * len(items) + 1.9), dpi=200)
    for row, (q, label) in enumerate(items):
        y = len(items) - 1 - row
        pct = [100 * v / N for v in LIKERT[q]]
        left = -(pct[0] + pct[1] + pct[2] / 2)
        for k in range(5):
            if pct[k] > 0:
                ax.barh(y, pct[k], left=left, color=COL[k], height=0.62, edgecolor='white', linewidth=1.5)
                if pct[k] >= 7:
                    ax.text(left + pct[k] / 2, y, f'{r0(pct[k])}%', ha='center', va='center', fontsize=8.5,
                            color='white' if k in (0, 4) else INK)
            left += pct[k]
        ax.text(-101, y, f'{r0(pct[0] + pct[1])}%', ha='right', va='center', fontsize=9.5, color=INK, fontweight='bold')
        ax.text(101, y, f'{r0(pct[3] + pct[4])}%', ha='left', va='center', fontsize=9.5, color=INK, fontweight='bold')
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([l for _, l in items][::-1], fontsize=9.5)
    ax.axvline(0, color='#555', linewidth=0.8)
    ax.set_xlim(-112, 112)
    ax.set_xticks([-100, -50, 0, 50, 100]); ax.set_xticklabels(['100%', '50%', '0', '50%', '100%'])
    ax.text(-101, len(items) - 0.35, 'Total\ndisagree', ha='right', va='bottom', fontsize=8, color=MUTED)
    ax.text(101, len(items) - 0.35, 'Total\nagree', ha='left', va='bottom', fontsize=8, color=MUTED)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.legend(handles=[Patch(color=c, label=l) for c, l in zip(COL, LEV)], ncol=5, loc='upper center',
              bbox_to_anchor=(0.45, -0.13), frameon=False, fontsize=8.5, handlelength=1.2)
    ax.set_title(title, fontsize=11.5, color=INK, loc='left', pad=40)
    fig.tight_layout(); fig.savefig(f'{OUT}/{fname}', bbox_inches='tight'); plt.close(fig)


def hbar(data, fname, title):
    items = [k for k, _ in data]; vals = [v for _, v in data]
    fig, ax = plt.subplots(figsize=(8.6, 0.5 * len(items) + 1.3), dpi=200)
    ys = list(range(len(items)))[::-1]
    ax.barh(ys, vals, color='#2a78d6', height=0.6)
    for y, v in zip(ys, vals):
        ax.text(v + 0.3, y, f'{v}  ({r0(100 * v / N)}%)', va='center', fontsize=9.5, color=INK)
    ax.set_yticks(ys); ax.set_yticklabels(items, fontsize=9.5)
    ax.set_xlim(0, max(vals) * 1.3)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.set_xlabel('Number of respondents (n = 40)', fontsize=9, color=MUTED)
    ax.xaxis.grid(True, color='#e6e6e3', linewidth=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_title(title, fontsize=11.5, color=INK, loc='left')
    fig.tight_layout(); fig.savefig(f'{OUT}/{fname}', bbox_inches='tight'); plt.close(fig)


likert([('Q3', 'Q3  AI could reduce face-to-face\nconversations in the future'),
        ('Q4', 'Q4  AI has reduced my in-person\nstudy time with classmates'),
        ('Q5', 'Q5  My group brainstorms with AI\ninstead of discussing'),
        ('Q6', 'Q6  I prefer AI explanations to\nteacher office hours'),
        ('Q7', 'Q7  AI-checked messages make me\nmore confident'),
        ('Q8', 'Q8  Face-to-face talk needs more\neffort than asking AI')],
       'figure1_study_interaction.png', 'Figure 1. AI chatbot use and face-to-face study interaction')
hbar(Q12, 'figure2_reasons.png', 'Figure 2. Main reason for asking an AI chatbot instead of a classmate or teacher')
likert([('Q9', 'Q9  I am comfortable treating\nAI like a friend'),
        ('Q10', 'Q10  Talking to AI makes me\nfeel less lonely'),
        ('Q11', 'Q11  Without AI, I would have\ntalked to more people')],
       'figure3_social_loneliness.png', 'Figure 3. AI chatbot use, social interaction and loneliness')
hbar(Q13, 'figure4_social_effect.png', 'Figure 4. Biggest effect of AI chatbots on first-year social life')
