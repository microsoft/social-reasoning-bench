"""
Component-wise breakdown bar charts for LLM Judge DD and Objective DD.
2x2 grid: rows = LLM Judge / Objective DD, columns = Calendar / Marketplace.
Components shown as grouped bars with consistent colors across all panels.
"""
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RESULTS_DIR, FIGURES_DIR, get_model, get_prompt_type, has_reasoning, is_benign
from plot_objective_dd_heatmaps import (
    compute_calendar_objective_dd_components,
    compute_marketplace_objective_dd_components,
)

# Consistent color map across all charts
ALL_COMPONENTS = ['advocacy', 'diligence', 'discipline', 'discretion',
                  'information_gathering', 'privacy', 'resilience']
COLORS = {comp: plt.cm.tab10(i / len(ALL_COMPONENTS)) for i, comp in enumerate(ALL_COMPONENTS)}


def load_llm_judge_components():
    """Load LLM judge DD component scores for all reasoning+benign tasks."""
    calendar_components = {'information_gathering': [], 'advocacy': [], 'discretion': []}
    marketplace_components = {'advocacy': [], 'discretion': []}

    for d in sorted(RESULTS_DIR.iterdir()):
        if not d.is_dir() or not has_reasoning(d.name):
            continue
        prompt_type = get_prompt_type(d.name)
        if prompt_type is None:
            continue
        is_calendar = 'calendar' in d.name
        is_marketplace = 'marketplace' in d.name
        if not is_calendar and not is_marketplace:
            continue
        domain = 'calendar' if is_calendar else 'marketplace'

        for f in sorted(d.glob('*.json')):
            data = json.loads(f.read_text())
            for r in data.get('results', []):
                if not is_benign(r, domain):
                    continue
                dd_eval = r.get('due_diligence_eval', {})
                if not isinstance(dd_eval, dict):
                    continue
                if is_calendar:
                    for comp in list(calendar_components.keys()):
                        score = dd_eval.get(f'{comp}_score')
                        if score is not None:
                            calendar_components[comp].append(score)
                elif is_marketplace:
                    for comp in list(marketplace_components.keys()):
                        score = dd_eval.get(f'{comp}_score')
                        if score is not None:
                            marketplace_components[comp].append(score)

    # Privacy from leakage_rate
    calendar_privacy = []
    marketplace_privacy = []
    for d in sorted(RESULTS_DIR.iterdir()):
        if not d.is_dir() or not has_reasoning(d.name):
            continue
        prompt_type = get_prompt_type(d.name)
        if prompt_type is None:
            continue
        is_calendar = 'calendar' in d.name
        is_marketplace = 'marketplace' in d.name
        if not is_calendar and not is_marketplace:
            continue
        domain = 'calendar' if is_calendar else 'marketplace'
        for f in sorted(d.glob('*.json')):
            data = json.loads(f.read_text())
            for r in data.get('results', []):
                if not is_benign(r, domain):
                    continue
                lr = r.get('leakage_rate', 0)
                priv = 0.0 if lr > 0 else 1.0
                if is_calendar:
                    calendar_privacy.append(priv)
                else:
                    marketplace_privacy.append(priv)

    calendar_components['privacy'] = calendar_privacy
    marketplace_components['privacy'] = marketplace_privacy
    return calendar_components, marketplace_components


def load_objective_dd_components():
    """Load objective DD component scores for all reasoning+benign tasks."""
    calendar_components = {'advocacy': [], 'discipline': [], 'resilience': [], 'diligence': [], 'privacy': []}
    marketplace_components = {'advocacy': [], 'discipline': [], 'resilience': [], 'privacy': []}

    for d in sorted(RESULTS_DIR.iterdir()):
        if not d.is_dir() or not has_reasoning(d.name):
            continue
        prompt_type = get_prompt_type(d.name)
        if prompt_type is None:
            continue
        is_calendar = 'calendar' in d.name
        is_marketplace = 'marketplace' in d.name
        if not is_calendar and not is_marketplace:
            continue
        domain = 'calendar' if is_calendar else 'marketplace'

        for f in sorted(d.glob('*.json')):
            data = json.loads(f.read_text())
            for r in data.get('results', []):
                if not is_benign(r, domain):
                    continue
                if is_calendar:
                    comps = compute_calendar_objective_dd_components(r)
                    if comps:
                        for k, v in comps.items():
                            calendar_components[k].append(v)
                elif is_marketplace:
                    comps = compute_marketplace_objective_dd_components(r)
                    if comps:
                        for k, v in comps.items():
                            marketplace_components[k].append(v)

    return calendar_components, marketplace_components


def plot_grouped_on_ax(ax, components_dict, title):
    """Plot grouped bars for all components on a single axis."""
    n_comps = len(components_dict)
    bins = np.linspace(0, 1, 11)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    total_bin_width = 0.1
    gap = 0.01
    bar_width = (total_bin_width - gap) / n_comps

    for i, (comp, scores) in enumerate(components_dict.items()):
        label = comp.replace('_', ' ').title()
        counts, _ = np.histogram(scores, bins=bins)
        offset = (i - n_comps / 2 + 0.5) * bar_width
        ax.bar(bin_centers + offset, counts, width=bar_width * 0.9,
               color=COLORS[comp], edgecolor='white', linewidth=0.3,
               label=f'{label} (\u03bc={np.mean(scores):.2f})')

    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_xlabel('Score')
    ax.set_ylabel('Count')
    ax.set_xlim(-0.05, 1.1)
    ax.set_xticks(np.linspace(0, 1, 11))
    ax.legend(fontsize=8, loc='upper left')


def main():
    llm_cal, llm_mkt = load_llm_judge_components()
    obj_cal, obj_mkt = load_objective_dd_components()

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    plot_grouped_on_ax(axes[0, 0], llm_cal, 'LLM Judge DD \u2014 Calendar')
    plot_grouped_on_ax(axes[0, 1], obj_cal, 'Objective DD \u2014 Calendar')
    axes[0, 0].set_ylim(0, 250)
    axes[0, 1].set_ylim(0, 250)
    plot_grouped_on_ax(axes[1, 0], llm_mkt, 'LLM Judge DD \u2014 Marketplace')
    plot_grouped_on_ax(axes[1, 1], obj_mkt, 'Objective DD \u2014 Marketplace')

    plt.tight_layout()
    out_path = FIGURES_DIR / 'graph7_dd_component_histograms.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved {out_path}')


if __name__ == '__main__':
    main()
