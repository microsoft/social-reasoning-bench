/**
 * BoxPlot - A reusable CSS-based box-and-whisker plot library
 * Requires Tailwind CSS for styling
 */
const BoxPlot = (function() {
  // Default color palette (Tailwind classes)
  const defaultColors = [
    { bg: 'bg-blue-600', border: 'border-blue-600', text: 'text-blue-600' },
    { bg: 'bg-green-600', border: 'border-green-600', text: 'text-green-600' },
    { bg: 'bg-purple-600', border: 'border-purple-600', text: 'text-purple-600' },
    { bg: 'bg-orange-500', border: 'border-orange-500', text: 'text-orange-500' },
    { bg: 'bg-pink-600', border: 'border-pink-600', text: 'text-pink-600' },
    { bg: 'bg-teal-600', border: 'border-teal-600', text: 'text-teal-600' },
    { bg: 'bg-red-600', border: 'border-red-600', text: 'text-red-600' },
    { bg: 'bg-yellow-500', border: 'border-yellow-500', text: 'text-yellow-500' },
    { bg: 'bg-amber-600', border: 'border-amber-600', text: 'text-amber-600' },
    { bg: 'bg-gray-600', border: 'border-gray-600', text: 'text-gray-600' },
  ];

  /**
   * Calculate median of a sorted array
   * @param {number[]} arr - Sorted array of numbers
   * @returns {number} The median value
   */
  function getMedian(arr) {
    if (arr.length === 0) return 0;
    const mid = Math.floor(arr.length / 2);
    if (arr.length % 2 === 0) {
      return (arr[mid - 1] + arr[mid]) / 2;
    }
    return arr[mid];
  }

  /**
   * Compute box plot statistics from an array of values
   * @param {number[]} values - Array of numeric values
   * @returns {{min: number, q1: number, median: number, q3: number, max: number, mean: number, values: number[]}}
   */
  function computeBoxPlotStats(values) {
    if (!values || values.length === 0) {
      return { min: 0, q1: 0, median: 0, q3: 0, max: 0, mean: 0, values: [] };
    }
    const sorted = [...values].sort((a, b) => a - b);
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const median = getMedian(sorted);
    const q1 = getMedian(sorted.slice(0, Math.floor(sorted.length / 2)));
    const q3 = getMedian(sorted.slice(Math.ceil(sorted.length / 2)));
    const mean = values.reduce((a, b) => a + b, 0) / values.length;

    return { min, q1, median, q3, max, mean, values: sorted };
  }

  /**
   * Get color by index with wraparound
   * @param {number} idx - Color index
   * @param {Array} colors - Optional custom color array
   * @returns {{bg: string, border: string, text: string}}
   */
  function getColorForIndex(idx, colors) {
    const palette = colors || defaultColors;
    return palette[idx % palette.length];
  }

  /**
   * Render a box plot chart
   * @param {string|HTMLElement} container - Container element or ID
   * @param {Array} data - Array of groups with series data
   * @param {Object} options - Rendering options
   *
   * Data format:
   * [
   *   {
   *     label: 'Group A',
   *     series: [
   *       { label: 'Series 1', values: [10, 20, 30, 40] },
   *       { label: 'Series 2', values: [15, 25, 35] }
   *     ]
   *   }
   * ]
   *
   * Options:
   * - scale: { min: 0, max: 100 } - Y-axis scale
   * - ticks: [0, 25, 50, 75, 100] - Grid line positions
   * - xAxisLabel: 'Metric %' - Label for X-axis
   * - colors: [...] - Custom Tailwind color classes
   * - showLegend: true - Show/hide legend
   * - labelWidth: 'w-36' - Width class for series labels
   * - valueWidth: 'w-14' - Width class for value column
   * - formatValue: (v) => v.toFixed(1) + '%' - Value formatter
   * - pointThreshold: 2 - Proximity threshold for grouping points
   * - escapeHtml: (s) => s - HTML escape function (required)
   */
  function render(container, data, options = {}) {
    // Get container element
    const containerEl = typeof container === 'string'
      ? document.getElementById(container)
      : container;

    if (!containerEl) {
      console.error('BoxPlot: Container not found');
      return;
    }

    // Merge options with defaults
    const opts = {
      scale: { min: 0, max: 100 },
      ticks: [0, 25, 50, 75, 100],
      xAxisLabel: '%',
      colors: defaultColors,
      showLegend: true,
      labelWidth: 'w-36',
      valueWidth: 'w-14',
      formatValue: (v) => v.toFixed(1) + '%',
      pointThreshold: 2,
      escapeHtml: (s) => s, // Default no-op, caller should provide proper escaping
      ...options
    };

    const { scale, ticks, xAxisLabel, colors, showLegend, labelWidth, valueWidth, formatValue, pointThreshold, escapeHtml } = opts;
    const scaleMin = scale.min;
    const scaleMax = scale.max;
    const toPercent = (v) => ((v - scaleMin) / (scaleMax - scaleMin)) * 100;

    // Collect all unique series labels for legend
    const allSeriesLabels = [];
    const seriesLabelSet = new Set();
    data.forEach(group => {
      group.series.forEach((series, idx) => {
        if (!seriesLabelSet.has(series.label)) {
          seriesLabelSet.add(series.label);
          allSeriesLabels.push({ label: series.label, colorIdx: idx });
        }
      });
    });

    // Build HTML
    let html = '<div class="space-y-4 pt-2">';

    data.forEach((group) => {
      html += `<div class="space-y-1.5">`;
      html += `<div class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">${escapeHtml(group.label)}</div>`;

      group.series.forEach((series, seriesIdx) => {
        const stats = computeBoxPlotStats(series.values);
        const color = getColorForIndex(seriesIdx, colors);
        const label = series.label || 'All';

        if (stats.values.length === 0) {
          // No data - show placeholder
          html += `
            <div class="flex items-center gap-2">
              <div class="${labelWidth} text-xs ${color.text} font-medium truncate" title="${escapeHtml(label)}">${escapeHtml(label)}</div>
              <div class="flex-1 relative h-5 bg-gray-100 dark:bg-gray-700 rounded">
                <div class="absolute inset-0 flex items-center justify-center text-xs text-gray-400">No data</div>
              </div>
              <div class="${valueWidth} text-xs text-gray-400 text-right">-</div>
            </div>
          `;
          return;
        }

        const { min, max, q1, q3, median, mean } = stats;

        // Group overlapping data points
        const points = stats.values.map((val) => ({ value: val, percent: toPercent(val) }));
        const groups = [];
        const used = new Set();

        points.forEach((p, i) => {
          if (used.has(i)) return;
          const pointGroup = [p];
          used.add(i);
          points.forEach((p2, j) => {
            if (used.has(j)) return;
            if (Math.abs(p.percent - p2.percent) < pointThreshold) {
              pointGroup.push(p2);
              used.add(j);
            }
          });
          groups.push(pointGroup);
        });

        // Calculate row height based on stacked points
        const maxGroupSize = groups.length > 0 ? Math.max(...groups.map(g => g.length)) : 1;
        const actualStackHeight = 6 + (maxGroupSize - 1) * 2;
        const minRowHeight = Math.max(20, actualStackHeight + 8);

        html += `
          <div class="flex items-center gap-2">
            <div class="${labelWidth} text-xs ${color.text} font-medium truncate" title="${escapeHtml(label)}">${escapeHtml(label)}</div>
            <div class="flex-1 relative bg-gray-100 dark:bg-gray-700 rounded overflow-visible" style="height: ${minRowHeight}px">
              <!-- Grid lines -->
              ${ticks.map(t => `<div class="absolute h-full border-l border-dashed border-gray-200 dark:border-gray-600" style="left: ${t}%"></div>`).join('')}

              <!-- Whisker line (min to max) -->
              <div class="absolute top-1/2 h-0.5 ${color.bg} opacity-50 -translate-y-1/2" style="left: ${toPercent(min)}%; width: ${Math.max(toPercent(max) - toPercent(min), 0.5)}%"></div>

              <!-- Min cap -->
              <div class="absolute top-1/2 w-0.5 h-2.5 ${color.bg} -translate-y-1/2 -translate-x-1/2" style="left: ${toPercent(min)}%"></div>

              <!-- Max cap -->
              <div class="absolute top-1/2 w-0.5 h-2.5 ${color.bg} -translate-y-1/2 -translate-x-1/2" style="left: ${toPercent(max)}%"></div>

              <!-- Box (Q1 to Q3) -->
              <div class="absolute top-1/2 h-3.5 ${color.bg} opacity-30 rounded -translate-y-1/2" style="left: ${toPercent(q1)}%; width: ${Math.max(toPercent(q3) - toPercent(q1), 0.5)}%"></div>
              <div class="absolute top-1/2 h-3.5 border ${color.border} rounded -translate-y-1/2" style="left: ${toPercent(q1)}%; width: ${Math.max(toPercent(q3) - toPercent(q1), 0.5)}%"></div>

              <!-- Median marker (vertical line) -->
              <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-10" style="left: ${toPercent(median)}%">
                <div class="w-1 h-4 ${color.bg} cursor-pointer rounded-sm shadow-sm border border-white/50"></div>
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-[70]">
                  <div class="font-medium">Median</div>
                  <div class="text-gray-300">${formatValue(median)}</div>
                  <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
                </div>
              </div>

              <!-- Mean marker (diamond) -->
              <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-10" style="left: ${toPercent(mean)}%">
                <div class="w-1.5 h-1.5 ${color.bg} rotate-45 cursor-pointer border border-white/50"></div>
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-[70]">
                  <div class="font-medium">Mean</div>
                  <div class="text-gray-300">${formatValue(mean)}</div>
                  <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
                </div>
              </div>

              <!-- Data points - stacked when overlapping -->
              ${groups.map(pointGroup => {
                const avgPercent = pointGroup.reduce((sum, p) => sum + p.percent, 0) / pointGroup.length;
                const medianPercent = toPercent(median);
                const meanPercent = toPercent(mean);
                const includeMedian = Math.abs(avgPercent - medianPercent) < pointThreshold;
                const includeMean = Math.abs(avgPercent - meanPercent) < pointThreshold;

                // Build tooltip items
                const tooltipItems = [
                  ...pointGroup.map((p, gi) => `
                    <div class="${gi > 0 ? 'mt-1 pt-1 border-t border-gray-600' : ''}"><span class="text-gray-300">${formatValue(p.value)}</span></div>
                  `),
                  ...(includeMedian ? [`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Median:</span> <span class="text-gray-300">${formatValue(median)}</span></div>`] : []),
                  ...(includeMean ? [`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Mean:</span> <span class="text-gray-300">${formatValue(mean)}</span></div>`] : [])
                ];

                if (pointGroup.length === 1) {
                  const p = pointGroup[0];
                  return `
                    <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-20" style="left: ${p.percent}%">
                      <div class="w-1.5 h-1.5 ${color.bg} rounded-full border border-white cursor-pointer"></div>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-[70]">
                        ${tooltipItems.join('')}
                        <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
                      </div>
                    </div>`;
                } else {
                  const stackHeight = 6 + (pointGroup.length - 1) * 2;
                  return `
                    <div class="absolute -translate-x-1/2 group z-20" style="left: ${avgPercent}%; top: 50%; transform: translateX(-50%) translateY(-${stackHeight / 2}px)">
                      <div class="relative flex flex-col items-center">
                        ${pointGroup.map((p, gi) => `
                          <div class="w-1.5 h-1.5 ${color.bg} rounded-full border border-white cursor-pointer ${gi > 0 ? '-mt-1' : ''}"></div>
                        `).join('')}
                      </div>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-[70]">
                        ${tooltipItems.join('')}
                        <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
                      </div>
                    </div>`;
                }
              }).join('')}
            </div>
            <div class="${valueWidth} text-xs text-gray-600 dark:text-gray-400 text-right" title="Median: ${formatValue(median)}">${formatValue(median)}</div>
          </div>
        `;
      });

      html += '</div>';
    });

    // X-axis labels
    html += `
      <div class="flex items-center gap-2 mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
        <div class="${labelWidth} text-xs text-gray-500 dark:text-gray-400 font-medium">${escapeHtml(xAxisLabel)}</div>
        <div class="flex-1 relative h-5">
          ${ticks.map(t => `<div class="absolute text-xs text-gray-400 -translate-x-1/2" style="left: ${t}%">${t}%</div>`).join('')}
        </div>
        <div class="${valueWidth}"></div>
      </div>
    `;

    // Legend
    if (showLegend) {
      html += `
        <div class="flex flex-wrap items-center gap-3 mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-400">
          <div class="flex items-center gap-1.5">
            <div class="w-1 h-4 bg-gray-500 rounded-sm shadow-sm border border-white/50"></div>
            <span>Median</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 bg-gray-500 rotate-45 border border-white/50"></div>
            <span>Mean</span>
          </div>
          ${allSeriesLabels.length > 1 ? allSeriesLabels.map((item) => {
            const color = getColorForIndex(item.colorIdx, colors);
            return `
              <div class="flex items-center gap-1.5">
                <div class="w-2.5 h-2.5 ${color.bg} rounded-full border border-white shadow-sm"></div>
                <span class="${color.text} font-medium">${escapeHtml(item.label)}</span>
              </div>
            `;
          }).join('') : ''}
        </div>
      `;
    }

    html += '</div>';
    containerEl.innerHTML = html;
  }

  // Public API
  return {
    render,
    computeBoxPlotStats,
    getMedian,
    getColorForIndex,
    defaultColors
  };
})();

// Support both module and global usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BoxPlot;
}
