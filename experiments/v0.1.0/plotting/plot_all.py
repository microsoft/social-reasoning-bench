"""Run every RQ plot script."""

import rq1_plot
import rq2_plot
import rq2a_plot
import rq4_plot
import rq6_plot


def main() -> None:
    for module in (rq1_plot, rq2_plot, rq2a_plot, rq4_plot, rq6_plot):
        module.main()


if __name__ == "__main__":
    main()
