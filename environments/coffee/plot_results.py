#!/usr/bin/env python3
"""Plot buyer vs seller utilities from simulation results with feasible region.
Usage: uv run python plot_results.py [path]
Examples:
  uv run python plot_results.py batch_20251111_184524         # searches in results/batch_*
  uv run python plot_results.py results/wiki_strategies-gpt   # absolute path
"""
import argparse
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


def plot_feasible_region(results_dir, buyer_name="buyer_1", seller_name="seller_1"):
    """
    Plot the feasible outcome region as a parallelogram.

    Game setup:
    - Buyer: $30 cash, 0 beans, values at $8/bean -> initial reward = $30
    - Seller: $0 cash, 10 beans, values at $4/bean -> initial reward = $40

    If trade Q beans at price P:
    - Buyer reward: (30 - P×Q) + 8×Q = 30 + Q×(8-P)
    - Seller reward: P×Q + 4×(10-Q) = 40 + Q×(P-4)

    Constraints: 0 ≤ Q ≤ 10, P×Q ≤ 30, P ≥ 0
    """
    # Collect actual data points
    buyer_utilities = []
    seller_utilities = []

    print(f"\n=== Collecting utilities from {results_dir} ===")
    print(f"Buyer: '{buyer_name}', Seller: '{seller_name}'")

    for db in sorted(results_dir.glob("*.db")):
        if db.stat().st_size == 0:
            print(f"  Skipping {db.name}: EMPTY")
            continue

        conn = sqlite3.connect(db)
        buyer_row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?",
            (buyer_name,)
        ).fetchone()
        seller_row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?",
            (seller_name,)
        ).fetchone()
        conn.close()

        if buyer_row and seller_row:
            buyer_utility = buyer_row[0] * buyer_row[2] + buyer_row[1]
            seller_utility = seller_row[0] * seller_row[2] + seller_row[1]
            buyer_utilities.append(buyer_utility)
            seller_utilities.append(seller_utility)
            print(f"  {db.name}: Buyer=${buyer_utility:.2f}, Seller=${seller_utility:.2f}")
        else:
            missing = []
            if not buyer_row:
                missing.append(buyer_name)
            if not seller_row:
                missing.append(seller_name)
            print(f"  Skipping {db.name}: Player(s) not found: {', '.join(missing)}")

    if not buyer_utilities:
        print("\n=== No valid data found to plot ===")
        return

    # Feasible region vertices (parallelogram)
    vertices = np.array([
        [30, 40],    # No trade: Q=0
        [110, 0],    # Q=10, P=0 (free beans to buyer)
        [80, 30],    # Q=10, P=3 (buyer spends all $30)
        [0, 70],     # Q→0, P→∞ (buyer spends all on ~0 beans)
    ])

    # Create figure
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(9, 6), facecolor='white')

    # Determine plot limits
    all_x = list(vertices[:, 0]) + buyer_utilities + [30]
    all_y = list(vertices[:, 1]) + seller_utilities + [40]
    x_min, x_max = min(all_x) - 10, max(all_x) + 10
    y_min, y_max = min(all_y) - 10, max(all_y) + 10

    # Fill entire plot area with gray (impossible region)
    ax.fill_between([x_min, x_max], y_min, y_max, color='#E8E8E8', alpha=0.7, zorder=0, label='Impossible')

    # Draw feasible region (parallelogram) - white background
    feasible_poly_bg = Polygon(vertices, facecolor='white', edgecolor='none', linewidth=0, zorder=1)
    ax.add_patch(feasible_poly_bg)

    # Re-draw the parallelogram border on top
    feasible_poly_border = Polygon(vertices, facecolor='none', edgecolor='#888888',
                                  linewidth=1.5, zorder=5, linestyle='-', label='Feasible Region')
    ax.add_patch(feasible_poly_border)

    # Plot data points
    ax.scatter(buyer_utilities, seller_utilities,
               c='#4A90E2',  # Blue
               alpha=0.3,
               s=100,
               edgecolors='none',
               zorder=10,
               label=f'Actual outcomes ({len(buyer_utilities)})')

    # Reference lines for initial utilities
    ax.axvline(x=30, color='#6B9BD1', linestyle='--', linewidth=1.5, alpha=0.7,
              label='Buyer initial ($30)', zorder=4)
    ax.axhline(y=40, color='#D1916B', linestyle='--', linewidth=1.5, alpha=0.7,
              label='Seller initial ($40)', zorder=4)

    # Labels and title
    ax.set_xlabel('Buyer Utility = cash + 8 × beans', fontsize=12)
    ax.set_ylabel('Seller Utility = cash + 4 × beans', fontsize=12)
    ax.set_title('Where Buyer Adopts Various Strategies',
                fontsize=15, pad=15)

    # Legend
    ax.legend(loc='upper right', framealpha=0.95, fontsize=9.5)

    # Set limits
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Grid
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5, color='#BBBBBB', zorder=1)
    ax.set_axisbelow(True)

    # Clean spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#DDDDDD')
        ax.spines[spine].set_linewidth(1)

    plt.tight_layout()

    # Save
    output_path = results_dir / "feasible_region.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n=== Plot saved to {output_path} ===")

    # Statistics
    print("\n=== Statistics ===")
    print(f"  Buyer - Mean: ${sum(buyer_utilities)/len(buyer_utilities):.2f}, "
          f"Min: ${min(buyer_utilities):.2f}, Max: ${max(buyer_utilities):.2f}")
    print(f"  Seller - Mean: ${sum(seller_utilities)/len(seller_utilities):.2f}, "
          f"Min: ${min(seller_utilities):.2f}, Max: ${max(seller_utilities):.2f}")

    plt.show()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Plot buyer vs seller utilities with feasible region")
    parser.add_argument("directory", nargs="?", default="results",
                        help="Results directory (absolute or under results/)")
    parser.add_argument("--buyer", default="buyer_1", help="Buyer agent name")
    parser.add_argument("--seller", default="seller_1", help="Seller agent name")
    args = parser.parse_args()

    # Get directory: absolute path or prefix under results/
    results_dir = Path(args.directory) if Path(args.directory).exists() else Path(f"results/{args.directory}")

    if not results_dir.exists():
        print(f"Error: Directory {results_dir} not found")
        exit(1)

    plot_feasible_region(results_dir, args.buyer, args.seller)
