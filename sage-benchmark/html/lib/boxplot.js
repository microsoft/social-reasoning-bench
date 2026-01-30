/**
 * BoxPlot - A reusable CSS-based box-and-whisker plot library
 * Requires Tailwind CSS for styling
 */
const BoxPlot = (function() {
  // Default color palette (Tailwind classes)
  const defaultColors = [
    { bg: 'bg-blue-600', border: 'border-blue-600', borderLight: 'border-blue-300', text: 'text-blue-600' },
    { bg: 'bg-green-600', border: 'border-green-600', borderLight: 'border-green-300', text: 'text-green-600' },
    { bg: 'bg-purple-600', border: 'border-purple-600', borderLight: 'border-purple-300', text: 'text-purple-600' },
    { bg: 'bg-orange-500', border: 'border-orange-500', borderLight: 'border-orange-300', text: 'text-orange-500' },
    { bg: 'bg-pink-600', border: 'border-pink-600', borderLight: 'border-pink-300', text: 'text-pink-600' },
    { bg: 'bg-teal-600', border: 'border-teal-600', borderLight: 'border-teal-300', text: 'text-teal-600' },
    { bg: 'bg-red-600', border: 'border-red-600', borderLight: 'border-red-300', text: 'text-red-600' },
    { bg: 'bg-yellow-500', border: 'border-yellow-500', borderLight: 'border-yellow-300', text: 'text-yellow-500' },
    { bg: 'bg-amber-600', border: 'border-amber-600', borderLight: 'border-amber-300', text: 'text-amber-600' },
    { bg: 'bg-gray-600', border: 'border-gray-600', borderLight: 'border-gray-300', text: 'text-gray-600' },
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
   * Data format (simple - single color per series):
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
   * Data format (subseries - multiple colors per box plot):
   * [
   *   {
   *     label: 'Group A',
   *     series: [
   *       {
   *         label: 'Series 1',
   *         subseries: [
   *           { label: 'Model A', values: [10, 20], color: { bg: 'bg-blue-600', ... } },
   *           { label: 'Model B', values: [30, 40], color: { bg: 'bg-green-600', ... } }
   *         ]
   *       }
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
   * - showZoomControls: true - Show/hide zoom controls
   * - showHorizontalZoom: true - Show/hide horizontal range slider
   * - horizontalZoom: { start: 0, end: 100 } - Initial horizontal zoom range (percentage)
   * - zoomLevel: 1 - Initial zoom level (1 = default, 2 = 2x height, etc.)
   * - labelWidth: 'w-36' - Width class for series labels
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
      showZoomControls: true,
      showHorizontalZoom: true,
      horizontalZoom: { start: 0, end: 100 },
      zoomLevel: 1,
      labelWidth: 'w-36',
      formatValue: (v) => v.toFixed(1) + '%',
      pointThreshold: 2,
      escapeHtml: (s) => s, // Default no-op, caller should provide proper escaping
      ...options
    };

    const { scale, ticks, xAxisLabel, colors, showLegend, showZoomControls, showHorizontalZoom, horizontalZoom, zoomLevel, labelWidth, formatValue, pointThreshold, escapeHtml } = opts;
    const scaleMin = scale.min;
    const scaleMax = scale.max;
    
    // Horizontal zoom: map values to the zoomed range
    const hzStart = horizontalZoom.start;
    const hzEnd = horizontalZoom.end;
    const hzRange = hzEnd - hzStart;
    
    // toPercent maps a value to its position in the ZOOMED view (0-100%)
    // Values outside the zoom range will be < 0 or > 100
    const toPercent = (v) => {
      const fullPercent = ((v - scaleMin) / (scaleMax - scaleMin)) * 100;
      return ((fullPercent - hzStart) / hzRange) * 100;
    };
    
    // Check if a value is within the visible range
    const isVisible = (v) => {
      const fullPercent = ((v - scaleMin) / (scaleMax - scaleMin)) * 100;
      return fullPercent >= hzStart && fullPercent <= hzEnd;
    };

    // Get tooltip positioning classes based on percent position
    // Avoids tooltips being cut off at edges
    const getTooltipPosition = (percent) => {
      if (percent < 15) {
        // Near left edge - align tooltip to the left
        return {
          container: 'left-0',
          arrow: 'left-2'
        };
      } else if (percent > 85) {
        // Near right edge - align tooltip to the right
        return {
          container: 'right-0',
          arrow: 'right-2'
        };
      } else {
        // Center - default centered positioning
        return {
          container: 'left-1/2 -translate-x-1/2',
          arrow: 'left-1/2 -translate-x-1/2'
        };
      }
    };

    // Generate tooltip HTML with proper edge positioning
    const makeTooltip = (percent, content) => {
      const pos = getTooltipPosition(percent);
      return `
        <div class="absolute bottom-full ${pos.container} mb-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded shadow-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-[100]">
          ${content}
          <div class="absolute top-full ${pos.arrow} border-4 border-transparent border-t-gray-900 dark:border-t-gray-700"></div>
        </div>`;
    };

    // Neutral color for box/whiskers when series has subseries with multiple colors
    const neutralColor = { bg: 'bg-gray-400', border: 'border-gray-400', borderLight: 'border-gray-200', text: 'text-gray-400' };

    // Collect all unique series labels for legend (including subseries)
    const allSeriesLabels = [];
    const seriesLabelSet = new Set();
    const allSubseriesLabels = [];
    const subseriesLabelSet = new Set();

    data.forEach(group => {
      group.series.forEach((series, idx) => {
        if (series.subseries && series.subseries.length > 0) {
          // Collect subseries labels with their colors
          series.subseries.forEach(sub => {
            if (!subseriesLabelSet.has(sub.label)) {
              subseriesLabelSet.add(sub.label);
              allSubseriesLabels.push({ label: sub.label, color: sub.color });
            }
          });
        } else {
          // Collect regular series labels
          if (!seriesLabelSet.has(series.label)) {
            seriesLabelSet.add(series.label);
            allSeriesLabels.push({ label: series.label, colorIdx: idx });
          }
        }
      });
    });

    // Store data and options on container for zoom re-rendering
    containerEl._boxplotData = data;
    containerEl._boxplotOptions = opts;

    // Zoom control SVG icons
    const zoomInIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>`;
    const zoomOutIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>`;
    const resetIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/></svg>`;

    // Build HTML
    let html = '<div class="space-y-4 pt-2">';

    // Ensure container has an ID for event handlers
    const containerId = containerEl.id || `boxplot-${Date.now()}`;
    if (!containerEl.id) containerEl.id = containerId;

    // Zoom controls
    if (showZoomControls) {
      html += `
        <div class="flex justify-end gap-1 mb-2">
          <button onclick="BoxPlot.zoom('${containerId}', 0.5)" class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors" title="Zoom out (smaller rows)">
            ${zoomOutIcon}
          </button>
          <button onclick="BoxPlot.zoom('${containerId}', 0)" class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors" title="Reset zoom">
            ${resetIcon}
          </button>
          <button onclick="BoxPlot.zoom('${containerId}', 2)" class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors" title="Zoom in (larger rows)">
            ${zoomInIcon}
          </button>
        </div>
      `;
    }

    // Horizontal zoom range slider
    if (showHorizontalZoom) {
      html += `
        <div class="flex items-center gap-2 mb-3">
          <div class="${labelWidth} text-xs text-gray-500 dark:text-gray-400 font-medium">X-Axis Range</div>
          <div class="flex-1 relative">
            <div class="boxplot-hzoom-container relative h-6 select-none" data-container-id="${containerId}">
              <!-- Track background -->
              <div class="absolute top-1/2 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-600 rounded -translate-y-1/2"></div>
              <!-- Selected range highlight -->
              <div class="boxplot-hzoom-range absolute top-1/2 h-1 bg-blue-400 dark:bg-blue-500 rounded -translate-y-1/2" style="left: ${hzStart}%; right: ${100 - hzEnd}%"></div>
              <!-- Start handle -->
              <div class="boxplot-hzoom-handle boxplot-hzoom-start absolute top-1/2 w-3 h-3 bg-white border-2 border-blue-500 rounded-full cursor-ew-resize -translate-x-1/2 -translate-y-1/2 hover:scale-110 transition-transform" style="left: ${hzStart}%" data-handle="start"></div>
              <!-- End handle -->
              <div class="boxplot-hzoom-handle boxplot-hzoom-end absolute top-1/2 w-3 h-3 bg-white border-2 border-blue-500 rounded-full cursor-ew-resize -translate-x-1/2 -translate-y-1/2 hover:scale-110 transition-transform" style="left: ${hzEnd}%" data-handle="end"></div>
              <!-- Tick marks -->
              ${[0, 25, 50, 75, 100].map(t => `<div class="absolute top-full text-[10px] text-gray-400 -translate-x-1/2 mt-0.5" style="left: ${t}%">${t}</div>`).join('')}
            </div>
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400 w-20 text-right">
            <span class="boxplot-hzoom-label">${hzStart.toFixed(0)}% - ${hzEnd.toFixed(0)}%</span>
          </div>
          <button onclick="BoxPlot.resetHorizontalZoom('${containerId}')" class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400 transition-colors" title="Reset horizontal zoom">
            ${resetIcon}
          </button>
        </div>
      `;
    }

    data.forEach((group) => {
      html += `<div class="space-y-1.5">`;
      if (group.label) {
        html += `<div class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">${escapeHtml(group.label)}</div>`;
      }

      group.series.forEach((series, seriesIdx) => {
        const hasSubseries = series.subseries && series.subseries.length > 0;
        const label = series.label || 'All';

        // Compute stats: flatten subseries values or use direct values
        const allValues = hasSubseries
          ? series.subseries.flatMap(sub => sub.values)
          : series.values;
        const stats = computeBoxPlotStats(allValues);

        // Use neutral color for box/whiskers when subseries present, otherwise series color
        const boxColor = hasSubseries ? neutralColor : getColorForIndex(seriesIdx, colors);
        const labelColor = hasSubseries ? neutralColor : boxColor;

        if (stats.values.length === 0) {
          // No data - show placeholder
          html += `
            <div class="flex items-center gap-2">
              <div class="${labelWidth} text-xs ${labelColor.text} font-medium truncate" title="${escapeHtml(label)}">${escapeHtml(label)}</div>
              <div class="flex-1 relative h-5 bg-gray-100 dark:bg-gray-700 rounded">
                <div class="absolute inset-0 flex items-center justify-center text-xs text-gray-400">No data</div>
              </div>
            </div>
          `;
          return;
        }

        const { min, max, q1, q3, median, mean } = stats;

        // Build points array with colors
        let points;
        if (hasSubseries) {
          // Each point gets its subseries color and label
          points = series.subseries.flatMap(sub =>
            sub.values.map(val => ({
              value: val,
              percent: toPercent(val),
              color: sub.color,
              subseriesLabel: sub.label
            }))
          );
        } else {
          // All points get the same series color
          points = stats.values.map(val => ({
            value: val,
            percent: toPercent(val),
            color: boxColor,
            subseriesLabel: null
          }));
        }

        // Group overlapping data points
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

        // Calculate sizes based on zoom level
        // Marker sizes stay fixed - only row height changes
        const pointSize = 8;      // w-2 h-2 - fixed
        const medianWidth = 6;    // w-1.5 - fixed
        const meanSize = 8;       // w-2 h-2 - fixed

        // Calculate row height - scale the base row height directly
        const maxGroupSize = groups.length > 0 ? Math.max(...groups.map(g => g.length)) : 1;
        const baseRowHeight = 28;
        const minRowHeight = Math.round(baseRowHeight * zoomLevel);

        // Box and cap sizes as proportion of row height (ensures they match)
        const boxHeight = Math.round(minRowHeight * 0.71);  // ~71% of row
        const capHeight = Math.round(minRowHeight * 0.57);  // ~57% of row
        const medianHeight = Math.round(minRowHeight * 0.86);  // ~86% of row

        html += `
          <div class="flex items-center gap-2">
            <div class="${labelWidth} text-xs ${labelColor.text} font-medium truncate" title="${escapeHtml(label)}">${escapeHtml(label)}</div>
            <div class="flex-1 relative bg-gray-100 dark:bg-gray-700 rounded" style="height: ${minRowHeight}px; overflow-x: clip; overflow-y: visible;">
              <!-- Grid lines -->
              ${ticks.map(t => `<div class="absolute h-full border-l border-dashed border-gray-200 dark:border-gray-600" style="left: ${t}%"></div>`).join('')}

              <!-- Whisker line (min to max) -->
              <div class="absolute top-1/2 ${boxColor.bg} opacity-50 -translate-y-1/2" style="left: ${toPercent(min)}%; width: ${Math.max(toPercent(max) - toPercent(min), 0.5)}%; height: ${Math.max(2, Math.round(2 * zoomLevel))}px"></div>

              <!-- Min cap -->
              <div class="absolute top-1/2 ${boxColor.bg} -translate-y-1/2 -translate-x-1/2" style="left: ${toPercent(min)}%; width: 2px; height: ${capHeight}px"></div>

              <!-- Max cap -->
              <div class="absolute top-1/2 ${boxColor.bg} -translate-y-1/2 -translate-x-1/2" style="left: ${toPercent(max)}%; width: 2px; height: ${capHeight}px"></div>

              <!-- Box (Q1 to Q3) -->
              <div class="absolute top-1/2 ${boxColor.bg} opacity-30 rounded -translate-y-1/2" style="left: ${toPercent(q1)}%; width: ${Math.max(toPercent(q3) - toPercent(q1), 0.5)}%; height: ${boxHeight}px"></div>
              <div class="absolute top-1/2 border ${boxColor.border} rounded -translate-y-1/2" style="left: ${toPercent(q1)}%; width: ${Math.max(toPercent(q3) - toPercent(q1), 0.5)}%; height: ${boxHeight}px"></div>

              <!-- Q1 edge (hoverable) -->
              ${(() => {
                const q1Percent = toPercent(q1);
                const q1Items = [`<div class="flex items-center"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rounded-sm mr-1.5"></span><span class="font-medium">Q1 (25th)</span></div><div class="text-gray-300">${formatValue(q1)}</div>`];
                if (Math.abs(q1Percent - toPercent(min)) < pointThreshold) {
                  q1Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Min:</span> <span class="text-gray-300">${formatValue(min)}</span></div>`);
                }
                if (Math.abs(q1Percent - toPercent(median)) < pointThreshold) {
                  q1Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Median:</span> <span class="text-gray-300">${formatValue(median)}</span></div>`);
                }
                if (Math.abs(q1Percent - toPercent(mean)) < pointThreshold) {
                  q1Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Mean:</span> <span class="text-gray-300">${formatValue(mean)}</span></div>`);
                }
                // Check for overlapping data points
                points.filter(p => Math.abs(p.percent - q1Percent) < pointThreshold).forEach(p => {
                  const colorDot = `<span class="inline-block w-2.5 h-2.5 ${p.color.bg} rounded-full mr-1.5 align-middle"></span>`;
                  const labelPart = p.subseriesLabel ? `<span class="font-medium">${escapeHtml(p.subseriesLabel)}:</span> ` : '';
                  q1Items.push(`<div class="flex items-center mt-1 pt-1 border-t border-gray-600">${colorDot}${labelPart}<span class="text-gray-300">${formatValue(p.value)}</span></div>`);
                });
                return `
              <div class="absolute top-1/2 -translate-y-1/2 group z-[8]" style="left: ${q1Percent}%">
                <div class="cursor-pointer -translate-x-1/2" style="width: ${medianWidth}px; height: ${boxHeight}px"></div>
                ${makeTooltip(q1Percent, q1Items.join(''))}
              </div>`;
              })()}

              <!-- Q3 edge (hoverable) -->
              ${(() => {
                const q3Percent = toPercent(q3);
                const q3Items = [`<div class="flex items-center"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rounded-sm mr-1.5"></span><span class="font-medium">Q3 (75th)</span></div><div class="text-gray-300">${formatValue(q3)}</div>`];
                if (Math.abs(q3Percent - toPercent(max)) < pointThreshold) {
                  q3Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Max:</span> <span class="text-gray-300">${formatValue(max)}</span></div>`);
                }
                if (Math.abs(q3Percent - toPercent(median)) < pointThreshold) {
                  q3Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Median:</span> <span class="text-gray-300">${formatValue(median)}</span></div>`);
                }
                if (Math.abs(q3Percent - toPercent(mean)) < pointThreshold) {
                  q3Items.push(`<div class="mt-1 pt-1 border-t border-gray-600"><span class="font-medium">Mean:</span> <span class="text-gray-300">${formatValue(mean)}</span></div>`);
                }
                // Check for overlapping data points
                points.filter(p => Math.abs(p.percent - q3Percent) < pointThreshold).forEach(p => {
                  const colorDot = `<span class="inline-block w-2.5 h-2.5 ${p.color.bg} rounded-full mr-1.5 align-middle"></span>`;
                  const labelPart = p.subseriesLabel ? `<span class="font-medium">${escapeHtml(p.subseriesLabel)}:</span> ` : '';
                  q3Items.push(`<div class="flex items-center mt-1 pt-1 border-t border-gray-600">${colorDot}${labelPart}<span class="text-gray-300">${formatValue(p.value)}</span></div>`);
                });
                return `
              <div class="absolute top-1/2 -translate-y-1/2 group z-[8]" style="left: ${q3Percent}%">
                <div class="cursor-pointer -translate-x-1/2" style="width: ${medianWidth}px; height: ${boxHeight}px"></div>
                ${makeTooltip(q3Percent, q3Items.join(''))}
              </div>`;
              })()}

              <!-- Median marker (vertical line) -->
              <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-10" style="left: ${toPercent(median)}%">
                <div class="${boxColor.bg} cursor-pointer rounded-sm shadow-sm border ${boxColor.borderLight || 'border-white/50'}" style="width: ${medianWidth}px; height: ${medianHeight}px"></div>
                ${makeTooltip(toPercent(median), `
                  <div class="font-medium">Median</div>
                  <div class="text-gray-300">${formatValue(median)}</div>
                `)}
              </div>

              <!-- Mean marker (diamond) -->
              <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-10" style="left: ${toPercent(mean)}%">
                <div class="${boxColor.bg} rotate-45 cursor-pointer border ${boxColor.borderLight || 'border-white/50'}" style="width: ${meanSize}px; height: ${meanSize}px"></div>
                ${makeTooltip(toPercent(mean), `
                  <div class="font-medium">Mean</div>
                  <div class="text-gray-300">${formatValue(mean)}</div>
                `)}
              </div>

              <!-- Data points - stacked when overlapping, with per-point colors for subseries -->
              ${groups.map(pointGroup => {
                const avgPercent = pointGroup.reduce((sum, p) => sum + p.percent, 0) / pointGroup.length;
                const q1Percent = toPercent(q1);
                const q3Percent = toPercent(q3);
                const medianPercent = toPercent(median);
                const meanPercent = toPercent(mean);
                const includeQ1 = Math.abs(avgPercent - q1Percent) < pointThreshold;
                const includeQ3 = Math.abs(avgPercent - q3Percent) < pointThreshold;
                const includeMedian = Math.abs(avgPercent - medianPercent) < pointThreshold;
                const includeMean = Math.abs(avgPercent - meanPercent) < pointThreshold;

                // Build tooltip items - include colored indicator and subseries label if present
                const tooltipItems = [
                  ...pointGroup.map((p, gi) => {
                    const colorDot = `<span class="inline-block w-2.5 h-2.5 ${p.color.bg} rounded-full mr-1.5 align-middle"></span>`;
                    const labelPart = p.subseriesLabel ? `<span class="font-medium">${escapeHtml(p.subseriesLabel)}:</span> ` : '';
                    return `<div class="flex items-center ${gi > 0 ? 'mt-1 pt-1 border-t border-gray-600' : ''}">${colorDot}${labelPart}<span class="text-gray-300">${formatValue(p.value)}</span></div>`;
                  }),
                  ...(includeQ1 ? [`<div class="flex items-center mt-1 pt-1 border-t border-gray-600"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rounded-sm mr-1.5"></span><span class="font-medium">Q1:</span> <span class="text-gray-300 ml-1">${formatValue(q1)}</span></div>`] : []),
                  ...(includeMedian ? [`<div class="flex items-center mt-1 pt-1 border-t border-gray-600"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rounded-sm mr-1.5"></span><span class="font-medium">Median:</span> <span class="text-gray-300 ml-1">${formatValue(median)}</span></div>`] : []),
                  ...(includeMean ? [`<div class="flex items-center mt-1 pt-1 border-t border-gray-600"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rotate-45 mr-1.5"></span><span class="font-medium">Mean:</span> <span class="text-gray-300 ml-1">${formatValue(mean)}</span></div>`] : []),
                  ...(includeQ3 ? [`<div class="flex items-center mt-1 pt-1 border-t border-gray-600"><span class="inline-block w-2.5 h-2.5 ${boxColor.bg} rounded-sm mr-1.5"></span><span class="font-medium">Q3:</span> <span class="text-gray-300 ml-1">${formatValue(q3)}</span></div>`] : [])
                ];

                if (pointGroup.length === 1) {
                  const p = pointGroup[0];
                  return `
                    <div class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 group z-20" style="left: ${p.percent}%">
                      <div class="${p.color.bg} rounded-full border ${p.color.borderLight || 'border-white'} cursor-pointer" style="width: ${pointSize}px; height: ${pointSize}px"></div>
                      ${makeTooltip(p.percent, tooltipItems.join(''))}
                    </div>`;
                } else {
                  // Distribute stacked points evenly within row height
                  // Point centers at: rowHeight/(n+1), 2*rowHeight/(n+1), ..., n*rowHeight/(n+1)
                  // First point margin: rowHeight/(n+1) - pointSize/2 (positions center correctly)
                  // Subsequent margins: rowHeight/(n+1) - pointSize (gap between centers minus one point)
                  const n = pointGroup.length;
                  const spacing = minRowHeight / (n + 1);
                  const firstMargin = spacing - pointSize / 2;
                  const subsequentMargin = spacing - pointSize;
                  return `
                    <div class="absolute -translate-x-1/2 group z-20" style="left: ${avgPercent}%; top: 0; height: ${minRowHeight}px;">
                      <div class="flex flex-col items-center">
                        ${pointGroup.map((p, i) => `
                          <div class="${p.color.bg} rounded-full border ${p.color.borderLight || 'border-white'} cursor-pointer" style="width: ${pointSize}px; height: ${pointSize}px; margin-top: ${i === 0 ? firstMargin : subsequentMargin}px;"></div>
                        `).join('')}
                      </div>
                      ${makeTooltip(avgPercent, tooltipItems.join(''))}
                    </div>`;
                }
              }).join('')}
            </div>
          </div>
        `;
      });

      html += '</div>';
    });

    // X-axis labels - show actual values based on horizontal zoom range
    // Generate ticks that span the visible range
    const xAxisTicks = [0, 25, 50, 75, 100]; // Positions in the zoomed view
    const xAxisLabels = xAxisTicks.map(t => {
      // Convert zoomed position back to actual value
      const actualValue = hzStart + (t / 100) * hzRange;
      return { position: t, label: `${actualValue.toFixed(0)}%` };
    });
    
    html += `
      <div class="flex items-center gap-2 mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
        <div class="${labelWidth} text-xs text-gray-500 dark:text-gray-400 font-medium">${escapeHtml(xAxisLabel)}</div>
        <div class="flex-1 relative h-5">
          ${xAxisLabels.map(t => `<div class="absolute text-xs text-gray-400 -translate-x-1/2" style="left: ${t.position}%">${t.label}</div>`).join('')}
        </div>
      </div>
    `;

    // Legend
    if (showLegend) {
      html += `
        <div class="flex flex-wrap items-center gap-3 mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-600 dark:text-gray-400">
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-6 bg-gray-500 rounded-sm shadow-sm border border-white/50"></div>
            <span>Median</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 bg-gray-500 rotate-45 border border-white/50"></div>
            <span>Mean</span>
          </div>
          ${allSeriesLabels.length > 1 ? allSeriesLabels.map((item) => {
            const color = getColorForIndex(item.colorIdx, colors);
            return `
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 ${color.bg} rounded-full border ${color.borderLight || 'border-white'} shadow-sm"></div>
                <span class="${color.text} font-medium">${escapeHtml(item.label)}</span>
              </div>
            `;
          }).join('') : ''}
          ${allSubseriesLabels.length > 0 ? allSubseriesLabels.map((item) => {
            return `
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 ${item.color.bg} rounded-full border ${item.color.borderLight || 'border-white'} shadow-sm"></div>
                <span class="${item.color.text} font-medium">${escapeHtml(item.label)}</span>
              </div>
            `;
          }).join('') : ''}
        </div>
      `;
    }

    html += '</div>';
    containerEl.innerHTML = html;

    // Set up horizontal zoom slider event handlers
    if (showHorizontalZoom) {
      setupHorizontalZoomHandlers(containerEl, containerId);
    }
  }

  /**
   * Set up drag handlers for horizontal zoom sliders
   */
  function setupHorizontalZoomHandlers(containerEl, containerId) {
    const hzoomContainer = containerEl.querySelector('.boxplot-hzoom-container');
    if (!hzoomContainer) return;

    const startHandle = hzoomContainer.querySelector('.boxplot-hzoom-start');
    const endHandle = hzoomContainer.querySelector('.boxplot-hzoom-end');
    const rangeBar = hzoomContainer.querySelector('.boxplot-hzoom-range');
    const label = containerEl.querySelector('.boxplot-hzoom-label');

    let isDragging = false;
    let activeHandle = null;

    const getPercentFromEvent = (e) => {
      const rect = hzoomContainer.getBoundingClientRect();
      const x = e.clientX - rect.left;
      return Math.max(0, Math.min(100, (x / rect.width) * 100));
    };

    const updateVisuals = (start, end) => {
      startHandle.style.left = `${start}%`;
      endHandle.style.left = `${end}%`;
      rangeBar.style.left = `${start}%`;
      rangeBar.style.right = `${100 - end}%`;
      if (label) {
        label.textContent = `${start.toFixed(0)}% - ${end.toFixed(0)}%`;
      }
    };

    const onMouseDown = (e, handle) => {
      e.preventDefault();
      isDragging = true;
      activeHandle = handle;
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    };

    const onMouseMove = (e) => {
      if (!isDragging || !activeHandle) return;

      const opts = containerEl._boxplotOptions;
      const hz = opts.horizontalZoom;
      const percent = getPercentFromEvent(e);

      if (activeHandle === 'start') {
        const newStart = Math.min(percent, hz.end - 5); // Minimum 5% range
        updateVisuals(newStart, hz.end);
        hz.start = newStart;
      } else {
        const newEnd = Math.max(percent, hz.start + 5); // Minimum 5% range
        updateVisuals(hz.start, newEnd);
        hz.end = newEnd;
      }
    };

    const onMouseUp = () => {
      if (!isDragging) return;
      isDragging = false;
      activeHandle = null;
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);

      // Re-render with new horizontal zoom
      const opts = containerEl._boxplotOptions;
      render(containerEl, containerEl._boxplotData, opts);
    };

    startHandle.addEventListener('mousedown', (e) => onMouseDown(e, 'start'));
    endHandle.addEventListener('mousedown', (e) => onMouseDown(e, 'end'));
  }

  /**
   * Adjust zoom level for a box plot and re-render
   * @param {string|HTMLElement} container - Container element or ID
   * @param {number} newZoom - New zoom level (0 = reset to 1, otherwise use as multiplier)
   */
  function zoom(container, newZoom) {
    const containerEl = typeof container === 'string'
      ? document.getElementById(container)
      : container;

    if (!containerEl || !containerEl._boxplotData || !containerEl._boxplotOptions) {
      console.error('BoxPlot: Cannot zoom - container not found or not initialized');
      return;
    }

    const currentZoom = containerEl._boxplotOptions.zoomLevel || 1;
    let targetZoom;

    if (newZoom === 0) {
      // Reset to default
      targetZoom = 1;
    } else if (newZoom < 1) {
      // Zoom out (multiply by fraction, e.g., 0.5 means halve)
      targetZoom = Math.max(0.5, currentZoom * newZoom);
    } else {
      // Zoom in (multiply by factor, e.g., 2 means double)
      targetZoom = Math.min(4, currentZoom * newZoom);
    }

    // Re-render with new zoom level
    render(containerEl, containerEl._boxplotData, {
      ...containerEl._boxplotOptions,
      zoomLevel: targetZoom
    });
  }

  /**
   * Reset horizontal zoom to show full range (0-100%)
   * @param {string|HTMLElement} container - Container element or ID
   */
  function resetHorizontalZoom(container) {
    const containerEl = typeof container === 'string'
      ? document.getElementById(container)
      : container;

    if (!containerEl || !containerEl._boxplotData || !containerEl._boxplotOptions) {
      console.error('BoxPlot: Cannot reset horizontal zoom - container not found or not initialized');
      return;
    }

    // Re-render with full horizontal range
    render(containerEl, containerEl._boxplotData, {
      ...containerEl._boxplotOptions,
      horizontalZoom: { start: 0, end: 100 }
    });
  }

  /**
   * Set horizontal zoom to a specific range
   * @param {string|HTMLElement} container - Container element or ID
   * @param {number} start - Start percentage (0-100)
   * @param {number} end - End percentage (0-100)
   */
  function setHorizontalZoom(container, start, end) {
    const containerEl = typeof container === 'string'
      ? document.getElementById(container)
      : container;

    if (!containerEl || !containerEl._boxplotData || !containerEl._boxplotOptions) {
      console.error('BoxPlot: Cannot set horizontal zoom - container not found or not initialized');
      return;
    }

    // Validate range
    const validStart = Math.max(0, Math.min(100, start));
    const validEnd = Math.max(validStart + 5, Math.min(100, end));

    // Re-render with new horizontal range
    render(containerEl, containerEl._boxplotData, {
      ...containerEl._boxplotOptions,
      horizontalZoom: { start: validStart, end: validEnd }
    });
  }

  // Public API
  return {
    render,
    zoom,
    resetHorizontalZoom,
    setHorizontalZoom,
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
