#!/usr/bin/env python3
"""Plot buyer vs seller utilities from simulation results.
Usage: uv run python plot_utilities.py [path]
Examples:
  uv run python plot_utilities.py batch_20251111_184524         # searches in results/batch_*
  uv run python plot_utilities.py results/wiki_strategies-gpt   # absolute path
"""

import argparse
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt


def plot_buyer_seller_utilities(results_dir, buyer_name="buyer_1", seller_name="seller_1"):
    """
    Plot a scatterplot of buyer utility vs seller utility from all simulation results.

    Args:
        results_dir: Path to directory containing .db files
        buyer_name: Name of the buyer agent (default: "buyer_1")
        seller_name: Name of the seller agent (default: "seller_1")
    """
    buyer_utilities = []
    seller_utilities = []

    print(f"\n=== Collecting utilities from {results_dir} ===")
    print(f"Buyer: '{buyer_name}', Seller: '{seller_name}'")

    for db in sorted(results_dir.glob("*.db")):
        if db.stat().st_size == 0:
            print(f"  Skipping {db.name}: EMPTY")
            continue

        conn = sqlite3.connect(db)

        # Get buyer utility
        buyer_row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?", (buyer_name,)
        ).fetchone()

        # Get seller utility
        seller_row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?", (seller_name,)
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

    # Plot the scatterplot
    if buyer_utilities and seller_utilities:
        # Modern styling
        plt.style.use("seaborn-v0_8-darkgrid")
        fig, ax = plt.subplots(figsize=(9, 6), facecolor="white")

        # Get axis limits for quadrant shading
        x_min, x_max = min(buyer_utilities + [30]) - 5, max(buyer_utilities + [30]) + 5
        y_min, y_max = min(seller_utilities + [40]) - 5, max(seller_utilities + [40]) + 5

        # Modern pastel palette - light, airy, contemporary
        # Add colored quadrant backgrounds
        # Bottom left: Impossible (very light gray)
        ax.fill_between([x_min, 30], y_min, 40, color="#F5F5F7", alpha=0.6, zorder=0)
        # Top left: Exploited (soft coral/pink)
        ax.fill_between([x_min, 30], 40, y_max, color="#FFB4C8", alpha=0.25, zorder=0)
        # Top right: Win-Win (soft mint/green)
        ax.fill_between([30, x_max], 40, y_max, color="#A8E6CF", alpha=0.3, zorder=0)
        # Bottom right: Gullible (soft lavender/purple)
        ax.fill_between([30, x_max], y_min, 40, color="#D4BBFF", alpha=0.25, zorder=0)

        # Add quadrant labels with modern colors
        label_style = {"fontsize": 13, "fontweight": "600", "ha": "center", "va": "center"}
        ax.text((x_min + 30) / 2, (40 + y_max) / 2, "Exploitative", color="#E63E6D", **label_style)
        ax.text((30 + x_max) / 2, (40 + y_max) / 2, "Normal", color="#2D9F5D", **label_style)
        ax.text((30 + x_max) / 2, (y_min + 40) / 2, "Gullible", color="#9D4EDD", **label_style)
        ax.text((x_min + 30) / 2, (y_min + 40) / 2, "Impossible", color="#ADB5BD", **label_style)

        # Bright, modern accent color for data points
        scatter = ax.scatter(
            buyer_utilities,
            seller_utilities,
            c="#4A90E2",  # Modern bright blue
            alpha=0.4,  # More transparent to see overlaps
            s=100,
            edgecolors="none",
            zorder=3,
        )

        # Add initial utility reference lines
        ax.axvline(
            x=30,
            color="#495057",
            linestyle="--",
            linewidth=2,
            alpha=0.5,
            label="Buyer initial ($30)",
            zorder=2,
        )
        ax.axhline(
            y=40,
            color="#495057",
            linestyle="--",
            linewidth=2,
            alpha=0.5,
            label="Seller initial ($40)",
            zorder=2,
        )
        ax.legend(loc="best", framealpha=0.9, fontsize=10)

        # Set axis limits
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Modern styling with formulas
        ax.set_xlabel(
            "Buyer Utility = cash + 8 × beans", fontsize=14, fontweight="500", color="#2b2b2b"
        )
        ax.set_ylabel(
            "Seller Utility = cash + 4 × beans", fontsize=14, fontweight="500", color="#2b2b2b"
        )
        ax.set_title(
            f"Where Buyer Adopts Various Strategies",
            fontsize=18,
            fontweight="600",
            color="#1a1a1a",
            pad=20,
        )

        # Subtitle with simulation count
        ax.text(
            0.5,
            1.02,
            f"{len(buyer_utilities)} simulations",
            transform=ax.transAxes,
            ha="center",
            fontsize=11,
            color="#666666",
            style="italic",
        )

        # Modern grid
        ax.grid(True, alpha=0.2, linestyle="-", linewidth=0.5, color="#cccccc")
        ax.set_axisbelow(True)

        # Clean up spines
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#dddddd")
            ax.spines[spine].set_linewidth(1)

        plt.tight_layout()

        # Save the plot
        output_path = results_dir / "buyer_seller_utilities.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"\n=== Plot saved to {output_path} ===")

        # Show statistics
        print(f"\n=== Statistics ===")
        print(
            f"  Buyer - Mean: ${sum(buyer_utilities) / len(buyer_utilities):.2f}, "
            f"Min: ${min(buyer_utilities):.2f}, Max: ${max(buyer_utilities):.2f}"
        )
        print(
            f"  Seller - Mean: ${sum(seller_utilities) / len(seller_utilities):.2f}, "
            f"Min: ${min(seller_utilities):.2f}, Max: ${max(seller_utilities):.2f}"
        )

        plt.show()
    else:
        print("\n=== No valid data found to plot ===")


def plot_feasible_region(results_dir, buyer_name="buyer_1", seller_name="seller_1"):
    """
    Plot the feasible outcome region as a parallelogram with game theory zones.

    Game setup:
    - Buyer: $30 cash, 0 beans, values at $8/bean -> initial reward = $30
    - Seller: $0 cash, 10 beans, values at $4/bean -> initial reward = $40

    If trade Q beans at price P:
    - Buyer reward: (30 - P×Q) + 8×Q = 30 + Q×(8-P)
    - Seller reward: P×Q + 4×(10-Q) = 40 + Q×(P-4)

    Constraints: 0 ≤ Q ≤ 10, P×Q ≤ 30, P ≥ 0
    """
    import numpy as np
    from matplotlib.patches import Polygon

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
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?", (buyer_name,)
        ).fetchone()
        seller_row = conn.execute(
            "SELECT coffee_beans, cash, utility_per_bean FROM agents WHERE name=?", (seller_name,)
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
    # Derived from game constraints
    vertices = np.array(
        [
            [30, 40],  # No trade: Q=0
            [110, 0],  # Q=10, P=0 (free beans to buyer)
            [80, 30],  # Q=10, P=3 (buyer spends all $30)
            [0, 70],  # Q→0, P→∞ (buyer spends all on ~0 beans)
        ]
    )

    # Create figure
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="white")

    # Determine plot limits (extend beyond parallelogram to show "impossible" region)
    all_x = list(vertices[:, 0]) + buyer_utilities + [30]
    all_y = list(vertices[:, 1]) + seller_utilities + [40]
    x_min, x_max = min(all_x) - 10, max(all_x) + 10
    y_min, y_max = min(all_y) - 10, max(all_y) + 10

    # Fill entire plot area with gray (impossible region)
    ax.fill_between([x_min, x_max], y_min, y_max, color="#E8E8E8", alpha=0.7, zorder=0)

    # Draw feasible region (parallelogram) - white background first
    feasible_poly_bg = Polygon(vertices, facecolor="white", edgecolor="none", linewidth=0, zorder=1)
    ax.add_patch(feasible_poly_bg)

    # Now clip the colored zones to be ONLY inside the parallelogram
    # We need to calculate intersection of each quadrant with the parallelogram

    from matplotlib.path import Path

    # Create path for parallelogram
    para_path = Path(vertices)

    # Calculate intersection points:
    # Edge 3: (80,30) → (0,70), parametric: (80-80t, 30+40t) for t∈[0,1]
    # Intersection with seller=40: 30+40t=40 => t=0.25 => (60, 40)
    # Intersection with buyer=30: 80-80t=30 => t=0.625 => (30, 55)

    # Safe zone: buyer≥30, seller≥40 (clipped to parallelogram)
    safe_verts = np.array(
        [
            [30, 40],  # Corner point
            [60, 40],  # Edge 3 ∩ seller=40
            [30, 55],  # Edge 3 ∩ buyer=30
        ]
    )
    safe_poly = Polygon(safe_verts, facecolor="#A8D5BA", alpha=0.5, zorder=2, label="Safe")
    ax.add_patch(safe_poly)

    # Seller Loses Money zone: buyer≥30, seller≤40 (clipped to parallelogram)
    seller_gullible_verts = np.array(
        [
            [30, 40],  # Corner point
            [110, 0],  # Parallelogram vertex
            [80, 30],  # Parallelogram vertex
            [60, 40],  # Edge 3 ∩ seller=40
        ]
    )
    seller_gullible_poly = Polygon(
        seller_gullible_verts, facecolor="#B8A4E5", alpha=0.5, zorder=2, label="Seller Loses Money"
    )
    ax.add_patch(seller_gullible_poly)

    # Buyer Loses Money zone: buyer≤30, seller≥40 (clipped to parallelogram)
    buyer_gullible_verts = np.array(
        [
            [30, 40],  # Corner point
            [30, 55],  # Edge 3 ∩ buyer=30
            [0, 70],  # Parallelogram vertex
        ]
    )
    buyer_gullible_poly = Polygon(
        buyer_gullible_verts, facecolor="#FFB5C5", alpha=0.5, zorder=2, label="Buyer Loses Money"
    )
    ax.add_patch(buyer_gullible_poly)

    # Re-draw the parallelogram border on top
    feasible_poly_border = Polygon(
        vertices, facecolor="none", edgecolor="#888888", linewidth=1.5, zorder=5, linestyle="-"
    )
    ax.add_patch(feasible_poly_border)

    # Plot data points
    scatter = ax.scatter(
        buyer_utilities,
        seller_utilities,
        c="#4A90E2",  # Blue
        alpha=0.3,
        s=100,
        edgecolors="none",
        zorder=10,
    )

    # Reference lines for initial utilities
    ax.axvline(
        x=30,
        color="#6B9BD1",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label="Buyer initial ($30)",
        zorder=4,
    )
    ax.axhline(
        y=40,
        color="#D1916B",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label="Seller initial ($40)",
        zorder=4,
    )

    # Labels
    ax.set_xlabel("Buyer Final", fontsize=12)
    ax.set_ylabel("Seller Final", fontsize=12)

    # Legend - reorder to put zones together and add borders to patches
    from matplotlib.patches import Patch

    handles, labels = ax.get_legend_handles_labels()

    # Reorder: zones first, then reference lines, then actual outcomes
    zone_order = ["Safe", "Seller Loses Money", "Buyer Loses Money"]
    reordered = []
    reordered_labels = []

    # Add zones first with borders
    zone_colors = {
        "Safe": "#A8D5BA",
        "Seller Loses Money": "#B8A4E5",
        "Buyer Loses Money": "#FFB5C5",
        "Impossible": "#E8E8E8",
    }

    for zone in zone_order:
        if zone in labels:
            # Create a new patch with border for legend
            patch = Patch(
                facecolor=zone_colors[zone], edgecolor="#666666", linewidth=0.8, alpha=0.7
            )
            reordered.append(patch)
            reordered_labels.append(zone)

    # Add remaining items
    for h, l in zip(handles, labels):
        if l not in zone_order:
            reordered.append(h)
            reordered_labels.append(l)

    ax.legend(reordered, reordered_labels, loc="upper right", framealpha=0.95, fontsize=9.5)

    # Set limits
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Grid
    ax.grid(True, alpha=0.25, linestyle="-", linewidth=0.5, color="#BBBBBB", zorder=1)
    ax.set_axisbelow(True)

    # Clean spines
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#DDDDDD")
        ax.spines[spine].set_linewidth(1)

    plt.tight_layout()

    # Save
    output_path = results_dir / "feasible_region.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"\n=== Feasible region plot saved to {output_path} ===")

    # Statistics
    print(f"\n=== Statistics ===")
    print(
        f"  Buyer - Mean: ${sum(buyer_utilities) / len(buyer_utilities):.2f}, "
        f"Min: ${min(buyer_utilities):.2f}, Max: ${max(buyer_utilities):.2f}"
    )
    print(
        f"  Seller - Mean: ${sum(seller_utilities) / len(seller_utilities):.2f}, "
        f"Min: ${min(seller_utilities):.2f}, Max: ${max(seller_utilities):.2f}"
    )

    plt.show()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Plot buyer vs seller utilities")
    parser.add_argument(
        "directory",
        nargs="?",
        default="results",
        help="Results directory (absolute or under results/)",
    )
    parser.add_argument("--buyer", default="buyer_1", help="Buyer agent name")
    parser.add_argument("--seller", default="seller_1", help="Seller agent name")
    parser.add_argument(
        "--feasible",
        action="store_true",
        help="Plot feasible region (parallelogram) instead of quadrants",
    )
    args = parser.parse_args()

    # Get directory: absolute path or prefix under results/
    results_dir = (
        Path(args.directory) if Path(args.directory).exists() else Path(f"results/{args.directory}")
    )

    if not results_dir.exists():
        print(f"Error: Directory {results_dir} not found")
        exit(1)

    if args.feasible:
        plot_feasible_region(results_dir, args.buyer, args.seller)
    else:
        plot_buyer_seller_utilities(results_dir, args.buyer, args.seller)
