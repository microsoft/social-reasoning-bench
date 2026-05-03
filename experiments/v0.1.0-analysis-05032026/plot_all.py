"""Run all analysis plots for v0.1.0.

Usage:
    cd experiments/v0.1.0-analysis-05032026
    python plot_all.py
"""

import plot_claim1_tc_vs_oo
import plot_claim2_oo_distribution
import plot_claim3_prompt_effect
import plot_arg2_heatmaps
import plot_objective_dd_heatmaps


def main():
    print("=" * 60)
    print("Generating all v0.1.0 analysis plots...")
    print("=" * 60)

    print("\n--- Claim 1: TC vs OO ---")
    plot_claim1_tc_vs_oo.main()

    print("\n--- Claim 2: OO Distribution ---")
    plot_claim2_oo_distribution.main()

    print("\n--- Claim 3: Prompt Effect ---")
    plot_claim3_prompt_effect.main()

    print("\n--- Claim 4: DoC Quadrants (LLM Judge DD) ---")
    plot_arg2_heatmaps.main()

    print("\n--- Claim 4: DoC Quadrants (Objective DD) ---")
    plot_objective_dd_heatmaps.main()

    print("\n" + "=" * 60)
    print("Done. All figures saved to outputs/v0.1.0/")
    print("=" * 60)


if __name__ == "__main__":
    main()
