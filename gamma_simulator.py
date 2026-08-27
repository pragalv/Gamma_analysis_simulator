import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Gamma Index and Log-File QA Simulator", layout="wide")


def render_simulator() -> None:
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                :root {
                    --bg: #f4f7fb;
                    --panel: rgba(255, 255, 255, 0.94);
                    --border: rgba(148, 163, 184, 0.22);
                    --text: #102235;
                    --muted: #54708b;
                    --blue: #2f6fed;
                    --green: #079669;
                    --red: #d14343;
                    --wave: rgba(75, 85, 99, 0.82);
                }

                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    font-family: "Segoe UI", system-ui, sans-serif;
                    background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
                    color: var(--text);
                }

                .shell {
                    background: var(--panel);
                    border: 1px solid var(--border);
                    border-radius: 28px;
                    box-shadow: 0 18px 60px rgba(15, 23, 42, 0.08);
                    overflow: hidden;
                }

                .header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 16px;
                    padding: 16px 18px;
                    border-bottom: 1px solid rgba(148, 163, 184, 0.18);
                    flex-wrap: wrap;
                }

                .title {
                    font-size: 18px;
                    font-weight: 700;
                    color: #0f1f31;
                }

                .header-right {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    flex-wrap: wrap;
                }

                .presets {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                }

                .preset {
                    border: 1px solid rgba(148, 163, 184, 0.26);
                    background: #f8fafc;
                    color: var(--muted);
                    border-radius: 999px;
                    padding: 8px 14px;
                    font-size: 13px;
                    font-weight: 700;
                    cursor: pointer;
                }

                .preset.active {
                    background: var(--blue);
                    color: white;
                    border-color: var(--blue);
                    box-shadow: 0 8px 20px rgba(47, 111, 237, 0.24);
                }

                .play-btn {
                    width: 44px;
                    height: 44px;
                    border: none;
                    border-radius: 50%;
                    background: #f3f4f6;
                    color: #1f3247;
                    font-weight: 800;
                    font-size: 16px;
                    cursor: pointer;
                }

                .plots {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 18px;
                    padding: 18px 18px 12px;
                }

                .plot-card {
                    padding: 6px 8px 0;
                }

                .plot-card.wide {
                    grid-column: span 1;
                }

                .plot-card.full {
                    grid-column: span 1;
                }

                .plot-ellipsoid {
                    grid-column: 1;
                    grid-row: 1;
                }

                .plot-wave {
                    grid-column: 2;
                    grid-row: 1;
                }

                .plot-reference-dose {
                    grid-column: 1;
                    grid-row: 2;
                }

                .plot-delivered-dose {
                    grid-column: 2;
                    grid-row: 2;
                }

                .plot-normalization {
                    grid-column: 3;
                    grid-row: 1 / span 2;
                    align-self: start;
                }

                .plot-title {
                    font-size: 18px;
                    font-weight: 700;
                    color: #1f3247;
                    margin: 0 0 6px;
                }

                .plot-subtitle {
                    font-size: 13px;
                    color: var(--muted);
                    margin: 0 0 10px;
                }

                .dose-frame {
                    fill: rgba(15, 23, 42, 0.02);
                    stroke: rgba(148, 163, 184, 0.18);
                }

                .dose-cell {
                    stroke: rgba(255, 255, 255, 0.16);
                    stroke-width: 0.18;
                }

                .dose-crosshair {
                    stroke: rgba(255, 255, 255, 0.85);
                    stroke-width: 0.42;
                    stroke-dasharray: 1.2 1;
                }

                .dose-marker {
                    fill: rgba(255, 255, 255, 0.92);
                    stroke: rgba(15, 23, 42, 0.22);
                    stroke-width: 0.2;
                }

                .profile-axis {
                    stroke: rgba(15, 23, 42, 0.16);
                    stroke-width: 0.35;
                }

                .profile-ref {
                    fill: none;
                    stroke: #0f766e;
                    stroke-width: 0.9;
                }

                .profile-delivered {
                    fill: none;
                    stroke: #d14343;
                    stroke-width: 0.9;
                }

                .profile-sample-line {
                    stroke: rgba(17, 24, 39, 0.65);
                    stroke-width: 0.45;
                    stroke-dasharray: 1.3 1.1;
                }

                .profile-dot-ref {
                    fill: #0f766e;
                }

                .profile-dot-delivered {
                    fill: #d14343;
                }

                .normalization-modes {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                    margin: 10px 0 12px;
                }

                .normalization-mode {
                    border: 1px solid rgba(148, 163, 184, 0.26);
                    background: #fffaf0;
                    color: var(--muted);
                    border-radius: 999px;
                    padding: 7px 12px;
                    font-size: 12px;
                    font-weight: 700;
                    cursor: pointer;
                }

                .normalization-mode.active {
                    background: #c2410c;
                    color: white;
                    border-color: #c2410c;
                }

                .compare-stats {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 12px;
                    margin-top: 12px;
                }

                .compare-stat {
                    border: 1px solid rgba(148, 163, 184, 0.22);
                    border-radius: 16px;
                    background: rgba(248, 250, 252, 0.92);
                    padding: 12px 14px;
                }

                .compare-label {
                    font-size: 12px;
                    font-weight: 700;
                    color: #41576e;
                    text-transform: uppercase;
                    letter-spacing: 0.02em;
                    margin-bottom: 4px;
                }

                .compare-value {
                    font-size: 18px;
                    font-weight: 700;
                    color: #111827;
                }

                .plot-card.full .compare-value {
                    font-size: 16px;
                }

                .equation-block {
                    margin: 12px 0;
                    padding: 12px 14px;
                    border: 1px solid rgba(148, 163, 184, 0.22);
                    border-radius: 16px;
                    background: rgba(248, 250, 252, 0.92);
                }

                .equation-title {
                    font-size: 12px;
                    font-weight: 700;
                    color: #41576e;
                    text-transform: uppercase;
                    letter-spacing: 0.02em;
                    margin-bottom: 8px;
                }

                .equation-text {
                    font-family: "Cambria Math", "Times New Roman", serif;
                    font-size: 15px;
                    line-height: 1.5;
                    color: #102235;
                }

                .equation-text + .equation-text {
                    margin-top: 8px;
                }

                .frac {
                    display: inline-flex;
                    flex-direction: column;
                    align-items: center;
                    vertical-align: middle;
                    margin: 0 2px;
                }

                .frac-num {
                    border-bottom: 1px solid rgba(16, 34, 53, 0.7);
                    line-height: 1.1;
                    padding: 0 3px 1px;
                }

                .frac-den {
                    line-height: 1.1;
                    padding: 1px 3px 0;
                }

                .metrics {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    border-top: 1px solid rgba(148, 163, 184, 0.18);
                    border-bottom: 1px solid rgba(148, 163, 184, 0.18);
                }

                .metric {
                    text-align: center;
                    padding: 14px 10px 16px;
                }

                .metric-label {
                    font-size: 14px;
                    color: var(--muted);
                    margin-bottom: 2px;
                }

                .metric-value {
                    font-size: 18px;
                    font-weight: 700;
                    color: #111827;
                }

                .controls {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 16px;
                    padding: 18px;
                    background: rgba(248, 250, 252, 0.92);
                }

                .control label {
                    display: block;
                    font-size: 13px;
                    font-weight: 700;
                    color: #41576e;
                    margin-bottom: 8px;
                }

                .control-row {
                    display: grid;
                    grid-template-columns: minmax(0, 1fr) auto;
                    align-items: center;
                    gap: 12px;
                }

                .control output {
                    min-width: 62px;
                    text-align: right;
                    font-size: 14px;
                    font-weight: 700;
                    color: #111827;
                }

                input[type="range"] {
                    width: 100%;
                    accent-color: var(--blue);
                }

                .caption {
                    padding: 0 18px 18px;
                    color: var(--muted);
                    font-size: 13px;
                }

                .axis-text {
                    fill: var(--muted);
                    font-size: 4px;
                    font-weight: 500;
                }

                .tick-text {
                    fill: #64748b;
                    font-size: 3.2px;
                    font-weight: 500;
                }

                .grid-line {
                    stroke: rgba(15, 23, 42, 0.1);
                    stroke-width: 0.35;
                }

                @media (max-width: 900px) {
                    .plots,
                    .compare-stats,
                    .metrics,
                    .controls {
                        grid-template-columns: 1fr;
                    }

                    .plot-ellipsoid,
                    .plot-wave,
                    .plot-reference-dose,
                    .plot-delivered-dose,
                    .plot-normalization {
                        grid-column: auto;
                        grid-row: auto;
                    }
                }
            </style>
        </head>
        <body>
            <div class="shell">
                <div class="header">
                    <div class="title">Gamma Index & Log-File QA Simulator</div>
                    <div class="header-right">
                        <div class="presets">
                            <button class="preset" data-dose="2" data-distance="2">2%/2mm</button>
                            <button class="preset active" data-dose="3" data-distance="3">3%/3mm</button>
                            <button class="preset" data-dose="5" data-distance="4">5%/4mm</button>
                        </div>
                        <button id="play-btn" class="play-btn">▶</button>
                    </div>
                </div>

                <div class="plots">
                    <div class="plot-card plot-ellipsoid">
                        <div class="plot-title">Acceptance Ellipsoid Bound</div>
                        <svg id="ellipse-svg" viewBox="0 0 100 86" style="width:100%; height:340px; display:block;">
                            <g id="ellipsoid-guides"></g>
                            <path id="ellipsoid-shell-yz" fill="rgba(7,150,105,0.06)" stroke="#079669" stroke-width="0.55"></path>
                            <path id="ellipsoid-shell-dose-y" fill="none" stroke="#079669" stroke-width="0.5" stroke-opacity="0.9"></path>
                            <path id="ellipsoid-shell-dose-z" fill="none" stroke="#079669" stroke-width="0.5" stroke-opacity="0.55"></path>
                            <line id="axis-y" x1="46" y1="44" x2="71" y2="38" stroke="rgba(84,112,139,0.55)" stroke-width="0.45"></line>
                            <line id="axis-z" x1="46" y1="44" x2="28" y2="23" stroke="rgba(84,112,139,0.55)" stroke-width="0.45"></line>
                            <line id="axis-dose" x1="46" y1="44" x2="61" y2="20" stroke="rgba(84,112,139,0.55)" stroke-width="0.45"></line>
                            <g id="ellipsoid-axis-ticks"></g>
                            <line id="gamma-vector" x1="46" y1="44" x2="58" y2="34" stroke="#079669" stroke-width="0.7"></line>
                            <circle id="gamma-point" cx="58" cy="34" r="1.8" fill="#079669"></circle>
                            <circle cx="46" cy="44" r="0.8" fill="rgba(84,112,139,0.55)"></circle>
                            <text x="75" y="40" text-anchor="middle" class="axis-text">X Spatial (mm)</text>
                            <text x="24" y="19" text-anchor="middle" class="axis-text">Y Spatial (mm)</text>
                            <text x="64" y="17" text-anchor="middle" class="axis-text">Dose (%)</text>
                        </svg>
                    </div>

                    <div class="plot-card plot-wave">
                        <div class="plot-title">Log-File Position Error (mm)</div>
                        <svg id="wave-svg" viewBox="0 0 100 86" style="width:100%; height:340px; display:block;">
                            <rect x="9" y="12" width="78" height="48" fill="rgba(59,130,246,0.08)" stroke="rgba(148,163,184,0.16)" stroke-dasharray="1.4 1.4"></rect>
                            <line x1="9" y1="36" x2="87" y2="36" stroke="rgba(15,23,42,0.18)" stroke-width="0.35"></line>
                            <g id="wave-y-ticks"></g>
                            <path id="wave-path" d="" fill="none" stroke="rgba(75,85,99,0.82)" stroke-width="0.7"></path>
                            <line id="cursor-line" x1="20" y1="12" x2="20" y2="76" stroke="#2F6FED" stroke-width="0.55"></line>
                            <circle id="cursor-dot" cx="20" cy="36" r="1.6" fill="#2F6FED"></circle>
                            <text x="9" y="82" class="axis-text">0s</text>
                            <text x="87" y="82" text-anchor="end" class="axis-text">10s</text>
                        </svg>
                    </div>

                    <div class="plot-card wide plot-reference-dose">
                        <div class="plot-title">Reference 2D Dose Distribution</div>
                        <div class="plot-subtitle">Static example beam profile with a broad high-dose core and softer penumbra.</div>
                        <svg id="reference-dose-svg" viewBox="0 0 100 86" style="width:100%; height:320px; display:block;">
                            <rect x="11" y="8" width="74" height="74" rx="4" class="dose-frame"></rect>
                            <g id="reference-dose-map"></g>
                            <line x1="48" y1="8" x2="48" y2="82" class="dose-crosshair"></line>
                            <line x1="11" y1="45" x2="85" y2="45" class="dose-crosshair"></line>
                            <circle cx="48" cy="45" r="1.8" class="dose-marker"></circle>
                            <text x="11" y="84" class="axis-text">-X</text>
                            <text x="85" y="84" text-anchor="end" class="axis-text">+X</text>
                            <text x="8" y="13" text-anchor="end" class="axis-text">+Y</text>
                            <text x="8" y="81" text-anchor="end" class="axis-text">-Y</text>
                        </svg>
                    </div>

                    <div class="plot-card wide plot-delivered-dose">
                        <div class="plot-title">Delivered 2D Dose Distribution</div>
                        <div class="plot-subtitle">The example field shifts and warps with the same playback perturbations used in the gamma model.</div>
                        <svg id="delivered-dose-svg" viewBox="0 0 100 86" style="width:100%; height:320px; display:block;">
                            <rect x="11" y="8" width="74" height="74" rx="4" class="dose-frame"></rect>
                            <g id="delivered-dose-map"></g>
                            <line id="dose-crosshair-v" x1="48" y1="8" x2="48" y2="82" class="dose-crosshair"></line>
                            <line id="dose-crosshair-h" x1="11" y1="45" x2="85" y2="45" class="dose-crosshair"></line>
                            <circle id="dose-marker" cx="48" cy="45" r="1.8" class="dose-marker"></circle>
                            <text x="11" y="84" class="axis-text">-X</text>
                            <text x="85" y="84" text-anchor="end" class="axis-text">+X</text>
                            <text x="8" y="13" text-anchor="end" class="axis-text">+Y</text>
                            <text x="8" y="81" text-anchor="end" class="axis-text">-Y</text>
                        </svg>
                    </div>

                    <div class="plot-card full plot-normalization">
                        <div class="plot-title">Global vs Local Gamma Normalization</div>
                        <div class="plot-subtitle">Use the extra controls below to move the sampled point, add spatial error, and scale the dose difference so you can create pass-fail splits on demand.</div>
                        <div class="normalization-modes">
                            <button class="normalization-mode active" data-mode="hotspot">Penumbra Hotspot</button>
                            <button class="normalization-mode" data-mode="broadened">Broadened Field</button>
                            <button class="normalization-mode" data-mode="coldspot">Cold Shoulder</button>
                        </div>
                        <div class="equation-block">
                            <div class="equation-title">Criteria Equations</div>
                            <div class="equation-text">Global: <em>&gamma;</em> = &radic;[(<span class="frac"><span class="frac-num"><em>&Delta;D</em></span><span class="frac-den"><em>D</em><sub>crit</sub></span></span>)<sup>2</sup> + (<span class="frac"><span class="frac-num"><em>&Delta;r</em></span><span class="frac-den"><em>r</em><sub>crit</sub></span></span>)<sup>2</sup>]</div>
                            <div class="equation-text">Local: <em>&gamma;</em> = &radic;[(<span class="frac"><span class="frac-num"><em>&Delta;D</em></span><span class="frac-den"><em>D</em><sub>crit</sub> &middot; <em>D</em><sub>ref,local</sub></span></span>)<sup>2</sup> + (<span class="frac"><span class="frac-num"><em>&Delta;r</em></span><span class="frac-den"><em>r</em><sub>crit</sub></span></span>)<sup>2</sup>]</div>
                        </div>
                        <svg id="normalization-svg" viewBox="0 0 100 58" style="width:100%; height:220px; display:block;">
                            <rect x="8" y="8" width="84" height="40" fill="rgba(15,23,42,0.02)" stroke="rgba(148,163,184,0.18)"></rect>
                            <line x1="10" y1="42" x2="90" y2="42" class="profile-axis"></line>
                            <line x1="10" y1="12" x2="10" y2="42" class="profile-axis"></line>
                            <path id="normalization-reference-path" class="profile-ref"></path>
                            <path id="normalization-delivered-path" class="profile-delivered"></path>
                            <line id="normalization-sample-line" x1="50" y1="10" x2="50" y2="44" class="profile-sample-line"></line>
                            <circle id="normalization-reference-dot" cx="50" cy="24" r="1.4" class="profile-dot-ref"></circle>
                            <circle id="normalization-delivered-dot" cx="50" cy="28" r="1.4" class="profile-dot-delivered"></circle>
                            <text x="10" y="48" class="axis-text">Low-dose edge</text>
                            <text x="90" y="48" text-anchor="end" class="axis-text">High-dose core</text>
                            <text x="10" y="10" class="axis-text">100%</text>
                        </svg>
                        <div class="compare-stats">
                            <div class="compare-stat">
                                <div class="compare-label">Sample Position</div>
                                <div id="sample-position" class="compare-value">0.00</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Local Ref Dose</div>
                                <div id="local-ref-dose" class="compare-value">0.0%</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Spatial Term</div>
                                <div id="sample-spatial-term" class="compare-value">0.0 mm</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Dose Difference</div>
                                <div id="sample-dose-diff" class="compare-value">0.0%</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Global Status</div>
                                <div id="global-status" class="compare-value">PASS</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Local Status</div>
                                <div id="local-status" class="compare-value">FAIL</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Global Tol</div>
                                <div id="global-dose-tol" class="compare-value">0.0%</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Local Tol</div>
                                <div id="local-dose-tol" class="compare-value">0.0%</div>
                            </div>
                            <div class="compare-stat">
                                <div class="compare-label">Gamma G / L</div>
                                <div id="global-local-gamma" class="compare-value">γ 0.00 / γ 0.00</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Dose Dev ΔD</div>
                        <div id="dose-metric" class="metric-value">0.00%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Pos Dev Δd</div>
                        <div id="pos-metric" class="metric-value">0.00 mm</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Gamma Index (Global)</div>
                        <div id="gamma-metric" class="metric-value" style="color:#079669;">γ 0.00</div>
                    </div>
                </div>

                <div class="controls">
                    <div class="control">
                        <label for="dose-slider">Dose Criteria (ΔD max)</label>
                        <div class="control-row">
                            <input id="dose-slider" type="range" min="1" max="5" step="0.5" value="3" />
                            <output id="dose-output">3.0%</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="distance-slider">Distance Criteria (Δd max)</label>
                        <div class="control-row">
                            <input id="distance-slider" type="range" min="1" max="5" step="0.5" value="3" />
                            <output id="distance-output">3.0 mm</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="mech-slider">Mechanical Perturbation</label>
                        <div class="control-row">
                            <input id="mech-slider" type="range" min="0.5" max="4.0" step="0.1" value="1.5" />
                            <output id="mech-output">1.5x</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="sample-position-slider">Normalization Sample Position</label>
                        <div class="control-row">
                            <input id="sample-position-slider" type="range" min="-0.9" max="0.9" step="0.01" value="-0.78" />
                            <output id="sample-position-output">-0.78 x</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="comparison-spatial-slider">Comparison Spatial Error</label>
                        <div class="control-row">
                            <input id="comparison-spatial-slider" type="range" min="0" max="3" step="0.1" value="0" />
                            <output id="comparison-spatial-output">0.0 mm</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="comparison-dose-factor-slider">Comparison Dose Difference</label>
                        <div class="control-row">
                            <input id="comparison-dose-factor-slider" type="range" min="0.1" max="1.6" step="0.05" value="0.9" />
                            <output id="comparison-dose-factor-output">0.90x ΔD</output>
                        </div>
                    </div>
                </div>

                <div id="caption" class="caption"></div>
            </div>

            <script>
                const presets = Array.from(document.querySelectorAll('.preset'));
                const playButton = document.getElementById('play-btn');
                const doseSlider = document.getElementById('dose-slider');
                const distanceSlider = document.getElementById('distance-slider');
                const mechSlider = document.getElementById('mech-slider');
                const samplePositionSlider = document.getElementById('sample-position-slider');
                const comparisonSpatialSlider = document.getElementById('comparison-spatial-slider');
                const comparisonDoseFactorSlider = document.getElementById('comparison-dose-factor-slider');
                const normalizationModes = Array.from(document.querySelectorAll('.normalization-mode'));
                const doseOutput = document.getElementById('dose-output');
                const distanceOutput = document.getElementById('distance-output');
                const mechOutput = document.getElementById('mech-output');
                const samplePositionOutput = document.getElementById('sample-position-output');
                const comparisonSpatialOutput = document.getElementById('comparison-spatial-output');
                const comparisonDoseFactorOutput = document.getElementById('comparison-dose-factor-output');
                const doseMetric = document.getElementById('dose-metric');
                const posMetric = document.getElementById('pos-metric');
                const gammaMetric = document.getElementById('gamma-metric');
                const caption = document.getElementById('caption');
                const ellipsoidShellYZ = document.getElementById('ellipsoid-shell-yz');
                const ellipsoidShellDoseY = document.getElementById('ellipsoid-shell-dose-y');
                const ellipsoidShellDoseZ = document.getElementById('ellipsoid-shell-dose-z');
                const gammaVector = document.getElementById('gamma-vector');
                const gammaPoint = document.getElementById('gamma-point');
                const wavePath = document.getElementById('wave-path');
                const cursorLine = document.getElementById('cursor-line');
                const cursorDot = document.getElementById('cursor-dot');
                const ellipsoidGuides = document.getElementById('ellipsoid-guides');
                const ellipsoidAxisTicks = document.getElementById('ellipsoid-axis-ticks');
                const waveYTicks = document.getElementById('wave-y-ticks');
                const referenceDoseMap = document.getElementById('reference-dose-map');
                const deliveredDoseMap = document.getElementById('delivered-dose-map');
                const doseMarker = document.getElementById('dose-marker');
                const doseCrosshairV = document.getElementById('dose-crosshair-v');
                const doseCrosshairH = document.getElementById('dose-crosshair-h');
                const normalizationReferencePath = document.getElementById('normalization-reference-path');
                const normalizationDeliveredPath = document.getElementById('normalization-delivered-path');
                const normalizationSampleLine = document.getElementById('normalization-sample-line');
                const normalizationReferenceDot = document.getElementById('normalization-reference-dot');
                const normalizationDeliveredDot = document.getElementById('normalization-delivered-dot');
                const samplePosition = document.getElementById('sample-position');
                const localRefDose = document.getElementById('local-ref-dose');
                const sampleSpatialTerm = document.getElementById('sample-spatial-term');
                const sampleDoseDiff = document.getElementById('sample-dose-diff');
                const globalStatus = document.getElementById('global-status');
                const localStatus = document.getElementById('local-status');
                const globalDoseTol = document.getElementById('global-dose-tol');
                const localDoseTol = document.getElementById('local-dose-tol');
                const globalLocalGamma = document.getElementById('global-local-gamma');

                const timeAxis = Array.from({ length: 201 }, (_, index) => (10 * index) / 200);
                const doseGridSize = 18;
                const lowDoseFloorPct = 1;
                let currentTime = 0;
                let isPlaying = false;
                let lastFrame = null;
                let normalizationMode = 'hotspot';
                let logWaveProfile = null;
                const ellipsoidCenter = { x: 46, y: 44 };
                const projectionBasis = {
                    dose: { x: 14, y: -21 },
                    y: { x: 20, y: -4 },
                    z: { x: -16, y: -18 },
                };

                function clamp(value, min, max) {
                    return Math.max(min, Math.min(value, max));
                }

                function mixChannel(start, end, weight) {
                    return Math.round(start + (end - start) * weight);
                }

                function heatColor(value) {
                    const clamped = clamp(value, 0, 1);
                    if (clamped < 0.33) {
                        const weight = clamped / 0.33;
                        return `rgb(${mixChannel(9, 38, weight)}, ${mixChannel(45, 126, weight)}, ${mixChannel(99, 173, weight)})`;
                    }
                    if (clamped < 0.66) {
                        const weight = (clamped - 0.33) / 0.33;
                        return `rgb(${mixChannel(38, 244, weight)}, ${mixChannel(126, 186, weight)}, ${mixChannel(173, 93, weight)})`;
                    }
                    const weight = (clamped - 0.66) / 0.34;
                    return `rgb(${mixChannel(244, 210, weight)}, ${mixChannel(186, 69, weight)}, ${mixChannel(93, 55, weight)})`;
                }

                function doseIntensityAt(normalizedX, normalizedY, time, delivered) {
                    const radialCore = Math.exp(-((normalizedX * normalizedX) / 0.22 + (normalizedY * normalizedY) / 0.16));
                    const shoulder = 0.52 * Math.exp(-(((normalizedX + 0.24) ** 2) / 0.08 + ((normalizedY - 0.18) ** 2) / 0.12));
                    const tail = 0.36 * Math.exp(-(((normalizedX - 0.28) ** 2) / 0.18 + ((normalizedY + 0.16) ** 2) / 0.1));
                    let x = normalizedX;
                    let y = normalizedY;

                    if (delivered) {
                        const shiftX = lateralSignal(time) * 0.07;
                        const shiftY = positionSignal(time) * 0.07;
                        const warp = 1 + doseSignal(time) * 0.025;
                        x = (normalizedX - shiftX) / warp;
                        y = (normalizedY - shiftY) * warp;
                    }

                    const deliveredCore = Math.exp(-((x * x) / 0.22 + (y * y) / 0.16));
                    const deliveredShoulder = 0.52 * Math.exp(-(((x + 0.24) ** 2) / 0.08 + ((y - 0.18) ** 2) / 0.12));
                    const deliveredTail = 0.36 * Math.exp(-(((x - 0.28) ** 2) / 0.18 + ((y + 0.16) ** 2) / 0.1));
                    const base = delivered ? deliveredCore + deliveredShoulder + deliveredTail : radialCore + shoulder + tail;
                    const ripple = delivered ? 0.08 * Math.sin(5 * x + time * 0.8) * Math.cos(4 * y - time * 0.5) : 0;
                    return clamp(base + ripple, 0, 1.4);
                }

                function gammaColor(value) {
                    return value <= 1 ? '#079669' : '#D14343';
                }

                function formatGamma(value) {
                    return value > 9.99 ? 'γ > 9.99' : `γ ${value.toFixed(2)}`;
                }

                function dosePercentAt(normalizedX, normalizedY, time, delivered) {
                    return (doseIntensityAt(normalizedX, normalizedY, time, delivered) / 1.4) * 100;
                }

                function gammaIndexForNormalization(doseDiffPct, spatialYDev, spatialZDev, referenceDosePct, normalizationMode) {
                    const doseCriteria = Number(doseSlider.value);
                    const distanceCriteria = Number(distanceSlider.value);
                    const normalizationFactor = normalizationMode === 'local'
                        ? Math.max(referenceDosePct, lowDoseFloorPct) / 100
                        : 1;
                    const effectiveDoseCriteria = doseCriteria * normalizationFactor;

                    return {
                        gamma: Math.sqrt(
                            (Math.abs(doseDiffPct) / effectiveDoseCriteria) ** 2
                            + (Math.abs(spatialYDev) / distanceCriteria) ** 2
                            + (Math.abs(spatialZDev) / distanceCriteria) ** 2
                        ),
                        doseTolerancePct: effectiveDoseCriteria,
                    };
                }

                function profileSvgPoint(normalizedX, dosePct) {
                    return {
                        x: 10 + ((normalizedX + 1) / 2) * 80,
                        y: 42 - clamp(dosePct, 0, 100) * 0.28,
                    };
                }

                function buildNormalizationProfilePath(profileAt) {
                    const points = [];
                    for (let sample = 0; sample <= 64; sample += 1) {
                        const normalizedX = -1 + (2 * sample) / 64;
                        const dosePct = profileAt(normalizedX);
                        const point = profileSvgPoint(normalizedX, dosePct);
                        points.push(`${sample === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`);
                    }
                    return points.join(' ');
                }

                function buildNormalizationDeliveredProfile(sampleXNormalized, doseDiffPct) {
                    const shift = Number(comparisonSpatialSlider.value) * 0.045;
                    const deliveredAt = (normalizedX) => {
                        const shiftedX = normalizedX - shift;
                        const reference = dosePercentAt(shiftedX, 0, 0, false);
                        const gaussian = Math.exp(-((normalizedX - sampleXNormalized) ** 2) / 0.018);

                        if (normalizationMode === 'broadened') {
                            const broadLift = 0.75 * doseDiffPct * Math.exp(-((normalizedX - sampleXNormalized) ** 2) / 0.16);
                            const shoulderLift = 0.3 * doseDiffPct * Math.exp(-((normalizedX - 0.15) ** 2) / 0.08);
                            return clamp(reference * 1.06 + broadLift + shoulderLift, 0, 100);
                        }

                        if (normalizationMode === 'coldspot') {
                            const dip = 0.95 * doseDiffPct * Math.exp(-((normalizedX - sampleXNormalized) ** 2) / 0.02);
                            const distalDrop = 0.35 * doseDiffPct * Math.exp(-((normalizedX + 0.12) ** 2) / 0.06);
                            return clamp(reference - dip - distalDrop + 0.12 * doseDiffPct * gaussian, 0, 100);
                        }

                        const hotspot = doseDiffPct * gaussian;
                        const trailingShoulder = 0.35 * doseDiffPct * Math.exp(-((normalizedX - (sampleXNormalized + 0.1)) ** 2) / 0.05);
                        return clamp(reference + hotspot + trailingShoulder, 0, 100);
                    };

                    const sampledDosePct = deliveredAt(sampleXNormalized);
                    return {
                        deliveredAt,
                        sampledDosePct,
                        effectiveDoseDiffPct: sampledDosePct - dosePercentAt(sampleXNormalized, 0, 0, false),
                    };
                }

                function updateNormalizationComparison() {
                    const sampleXNormalized = Number(samplePositionSlider.value);
                    const referenceDosePct = dosePercentAt(sampleXNormalized, 0, 0, false);
                    const spatialYDev = Number(comparisonSpatialSlider.value);
                    const spatialZDev = 0;
                    const doseDiffPct = Number(doseSlider.value) * Number(comparisonDoseFactorSlider.value);
                    const deliveredProfile = buildNormalizationDeliveredProfile(sampleXNormalized, doseDiffPct);
                    const deliveredDosePct = deliveredProfile.sampledDosePct;
                    const effectiveDoseDiffPct = deliveredProfile.effectiveDoseDiffPct;
                    const globalResult = gammaIndexForNormalization(effectiveDoseDiffPct, spatialYDev, spatialZDev, referenceDosePct, 'global');
                    const localResult = gammaIndexForNormalization(effectiveDoseDiffPct, spatialYDev, spatialZDev, referenceDosePct, 'local');
                    const refPoint = profileSvgPoint(sampleXNormalized, referenceDosePct);
                    const deliveredPoint = profileSvgPoint(sampleXNormalized, deliveredDosePct);

                    normalizationReferencePath.setAttribute('d', buildNormalizationProfilePath((normalizedX) => dosePercentAt(normalizedX, 0, 0, false)));
                    normalizationDeliveredPath.setAttribute('d', buildNormalizationProfilePath(deliveredProfile.deliveredAt));
                    normalizationSampleLine.setAttribute('x1', refPoint.x.toFixed(2));
                    normalizationSampleLine.setAttribute('x2', refPoint.x.toFixed(2));
                    normalizationReferenceDot.setAttribute('cx', refPoint.x.toFixed(2));
                    normalizationReferenceDot.setAttribute('cy', refPoint.y.toFixed(2));
                    normalizationDeliveredDot.setAttribute('cx', deliveredPoint.x.toFixed(2));
                    normalizationDeliveredDot.setAttribute('cy', deliveredPoint.y.toFixed(2));

                    samplePosition.textContent = `${sampleXNormalized.toFixed(2)} x`;
                    samplePositionOutput.textContent = `${sampleXNormalized.toFixed(2)} x`;
                    localRefDose.textContent = `${referenceDosePct.toFixed(1)}%`;
                    sampleSpatialTerm.textContent = `${spatialYDev.toFixed(1)} mm`;
                    comparisonSpatialOutput.textContent = `${spatialYDev.toFixed(1)} mm`;
                    sampleDoseDiff.textContent = `${effectiveDoseDiffPct >= 0 ? '+' : ''}${effectiveDoseDiffPct.toFixed(1)}%`;
                    comparisonDoseFactorOutput.textContent = `${Number(comparisonDoseFactorSlider.value).toFixed(2)}x ΔD`;
                    globalStatus.textContent = globalResult.gamma <= 1 ? 'PASS' : 'FAIL';
                    globalStatus.style.color = gammaColor(globalResult.gamma);
                    localStatus.textContent = localResult.gamma <= 1 ? 'PASS' : 'FAIL';
                    localStatus.style.color = gammaColor(localResult.gamma);
                    globalDoseTol.textContent = `${globalResult.doseTolerancePct.toFixed(2)}%`;
                    localDoseTol.textContent = `${localResult.doseTolerancePct.toFixed(2)}%`;
                    globalLocalGamma.textContent = `${formatGamma(globalResult.gamma)} / ${formatGamma(localResult.gamma)}`;
                    globalLocalGamma.style.color = '#111827';
                }

                function buildDoseMapMarkup(time, delivered) {
                    const cellSize = 74 / doseGridSize;
                    let markup = '';
                    for (let row = 0; row < doseGridSize; row += 1) {
                        for (let col = 0; col < doseGridSize; col += 1) {
                            const x = 11 + col * cellSize;
                            const y = 8 + row * cellSize;
                            const normalizedX = ((col + 0.5) / doseGridSize) * 2 - 1;
                            const normalizedY = 1 - ((row + 0.5) / doseGridSize) * 2;
                            const value = doseIntensityAt(normalizedX, normalizedY, time, delivered) / 1.4;
                            markup += `<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${cellSize.toFixed(2)}" height="${cellSize.toFixed(2)}" class="dose-cell" fill="${heatColor(value)}"></rect>`;
                        }
                    }
                    return markup;
                }

                function updateDoseMaps() {
                    referenceDoseMap.innerHTML = buildDoseMapMarkup(0, false);
                    deliveredDoseMap.innerHTML = buildDoseMapMarkup(currentTime, true);

                    const markerX = 48 + lateralSignal(currentTime) * 5.4;
                    const markerY = 45 - positionSignal(currentTime) * 5.4;
                    doseMarker.setAttribute('cx', markerX.toFixed(2));
                    doseMarker.setAttribute('cy', markerY.toFixed(2));
                    doseCrosshairV.setAttribute('x1', markerX.toFixed(2));
                    doseCrosshairV.setAttribute('x2', markerX.toFixed(2));
                    doseCrosshairH.setAttribute('y1', markerY.toFixed(2));
                    doseCrosshairH.setAttribute('y2', markerY.toFixed(2));
                }

                function buildGrid() {
                    let guideMarkup = '';
                    for (let step = -2; step <= 2; step += 1) {
                        const yStart = projectPoint(0, step, -2.5);
                        const yEnd = projectPoint(0, step, 2.5);
                        const zStart = projectPoint(0, -2.5, step);
                        const zEnd = projectPoint(0, 2.5, step);
                        guideMarkup += `<line x1="${yStart.x.toFixed(2)}" y1="${yStart.y.toFixed(2)}" x2="${yEnd.x.toFixed(2)}" y2="${yEnd.y.toFixed(2)}" class="grid-line"></line>`;
                        guideMarkup += `<line x1="${zStart.x.toFixed(2)}" y1="${zStart.y.toFixed(2)}" x2="${zEnd.x.toFixed(2)}" y2="${zEnd.y.toFixed(2)}" class="grid-line"></line>`;
                    }
                    ellipsoidGuides.innerHTML = guideMarkup;

                    ellipsoidAxisTicks.innerHTML = `
                        <text x="46" y="48" text-anchor="end" class="tick-text">0</text>
                        <text x="58" y="45" text-anchor="middle" class="tick-text">+1</text>
                        <text x="70" y="41" text-anchor="middle" class="tick-text">+2</text>
                        <text x="37" y="33" text-anchor="middle" class="tick-text">+1</text>
                        <text x="29" y="24" text-anchor="middle" class="tick-text">+2</text>
                        <text x="55" y="33" text-anchor="middle" class="tick-text">+1</text>
                        <text x="61" y="22" text-anchor="middle" class="tick-text">+2</text>
                    `;

                    waveYTicks.innerHTML = `
                        <text x="7" y="12" text-anchor="end" dominant-baseline="middle" class="tick-text">2</text>
                        <text x="7" y="24" text-anchor="end" dominant-baseline="middle" class="tick-text">1</text>
                        <text x="7" y="36" text-anchor="end" dominant-baseline="middle" class="tick-text">0</text>
                        <text x="7" y="48" text-anchor="end" dominant-baseline="middle" class="tick-text">-1</text>
                        <text x="7" y="60" text-anchor="end" dominant-baseline="middle" class="tick-text">-2</text>
                    `;
                }

                function positionSignal(t) {
                    const scale = Number(mechSlider.value);
                    const raw = (
                        0.62 * Math.sin(2 * Math.PI * 0.23 * t + 0.4)
                        + 0.36 * Math.sin(2 * Math.PI * 0.79 * t + 2.2)
                        + 0.21 * Math.cos(2 * Math.PI * 0.11 * t - 0.2)
                    );
                    return raw * scale;
                }

                function lateralSignal(t) {
                    const scale = Number(mechSlider.value);
                    const raw = (
                        0.48 * Math.cos(2 * Math.PI * 0.19 * t - 0.2)
                        + 0.33 * Math.sin(2 * Math.PI * 0.51 * t + 1.1)
                        - 0.18 * Math.cos(2 * Math.PI * 0.77 * t)
                    );
                    return raw * scale;
                }

                function doseSignal(t) {
                    const scale = Number(mechSlider.value);
                    const raw = (
                        0.95 * Math.sin(2 * Math.PI * 0.12 * t - 0.7)
                        + 0.52 * Math.cos(2 * Math.PI * 0.31 * t + 0.5)
                        + 0.18 * Math.sin(2 * Math.PI * 0.57 * t - 1.1)
                    );
                    const scaled = raw * (0.9 + scale * 0.2);
                    return Math.max(-4.95, Math.min(scaled, 4.95));
                }

                function gammaIndex(doseDev, spatialYDev, spatialZDev) {
                    const doseCriteria = Number(doseSlider.value);
                    const distanceCriteria = Number(distanceSlider.value);
                    return Math.sqrt(
                        (Math.abs(doseDev) / doseCriteria) ** 2
                        + (Math.abs(spatialYDev) / distanceCriteria) ** 2
                        + (Math.abs(spatialZDev) / distanceCriteria) ** 2
                    );
                }

                function projectPoint(doseCoord, yCoord, zCoord) {
                    return {
                        x: ellipsoidCenter.x + projectionBasis.dose.x * doseCoord + projectionBasis.y.x * yCoord + projectionBasis.z.x * zCoord,
                        y: ellipsoidCenter.y + projectionBasis.dose.y * doseCoord + projectionBasis.y.y * yCoord + projectionBasis.z.y * zCoord,
                    };
                }

                function pathFromPlane(pointFactory) {
                    const samples = [];
                    for (let step = 0; step <= 64; step += 1) {
                        const theta = (Math.PI * 2 * step) / 64;
                        const point = pointFactory(theta);
                        samples.push(`${step === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`);
                    }
                    return samples.join(' ');
                }

                function updateEllipsoidShell() {
                    const doseRadius = Number(doseSlider.value) / 3;
                    const spatialRadius = Number(distanceSlider.value) / 3;

                    ellipsoidShellYZ.setAttribute(
                        'd',
                        pathFromPlane((theta) => projectPoint(0, spatialRadius * Math.cos(theta), spatialRadius * Math.sin(theta)))
                    );
                    ellipsoidShellDoseY.setAttribute(
                        'd',
                        pathFromPlane((theta) => projectPoint(doseRadius * Math.sin(theta), spatialRadius * Math.cos(theta), 0))
                    );
                    ellipsoidShellDoseZ.setAttribute(
                        'd',
                        pathFromPlane((theta) => projectPoint(doseRadius * Math.sin(theta), 0, spatialRadius * Math.cos(theta)))
                    );
                }

                function createLogWaveProfile() {
                    return {
                        components: [
                            {
                                amplitude: 0.45 + Math.random() * 0.4,
                                frequency: 0.14 + Math.random() * 0.18,
                                phase: Math.random() * Math.PI * 2,
                                kind: 'sin',
                            },
                            {
                                amplitude: 0.18 + Math.random() * 0.32,
                                frequency: 0.35 + Math.random() * 0.45,
                                phase: Math.random() * Math.PI * 2,
                                kind: 'cos',
                            },
                            {
                                amplitude: 0.08 + Math.random() * 0.22,
                                frequency: 0.7 + Math.random() * 0.55,
                                phase: Math.random() * Math.PI * 2,
                                kind: Math.random() > 0.5 ? 'sin' : 'cos',
                            },
                        ],
                        bias: (Math.random() * 0.4) - 0.2,
                    };
                }

                function logFileSignal(t) {
                    const scale = Number(mechSlider.value);
                    const profile = logWaveProfile || createLogWaveProfile();
                    logWaveProfile = profile;
                    const raw = profile.components.reduce((sum, component) => {
                        const angle = 2 * Math.PI * component.frequency * t + component.phase;
                        return sum + component.amplitude * (component.kind === 'sin' ? Math.sin(angle) : Math.cos(angle));
                    }, profile.bias);
                    return raw * scale;
                }

                function wavePoint(t) {
                    const x = 9 + (78 * t) / 10;
                    const y = 36 - logFileSignal(t) * 9.5;
                    return { x, y };
                }

                function updateWavePath() {
                    const path = timeAxis.map((t, index) => {
                        const point = wavePoint(t);
                        return `${index === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`;
                    }).join(' ');
                    wavePath.setAttribute('d', path);
                }

                function updateScene() {
                    const doseDev = doseSignal(currentTime);
                    const spatialYDev = positionSignal(currentTime);
                    const spatialZDev = lateralSignal(currentTime);
                    const spatialMagnitude = Math.hypot(spatialYDev, spatialZDev);
                    const gamma = gammaIndex(doseDev, spatialYDev, spatialZDev);
                    const gammaStateColor = gammaColor(gamma);

                    const doseCriteria = Number(doseSlider.value);
                    const distanceCriteria = Number(distanceSlider.value);
                    const doseRadius = doseCriteria / 3;
                    const spatialRadius = distanceCriteria / 3;
                    const projectedPoint = projectPoint(
                        (doseDev / doseCriteria) * doseRadius,
                        (spatialYDev / distanceCriteria) * spatialRadius,
                        (spatialZDev / distanceCriteria) * spatialRadius,
                    );

                    updateEllipsoidShell();
                    gammaVector.setAttribute('x1', ellipsoidCenter.x.toFixed(2));
                    gammaVector.setAttribute('y1', ellipsoidCenter.y.toFixed(2));
                    gammaVector.setAttribute('x2', projectedPoint.x.toFixed(2));
                    gammaVector.setAttribute('y2', projectedPoint.y.toFixed(2));
                    gammaVector.setAttribute('stroke', gammaStateColor);
                    gammaPoint.setAttribute('cx', projectedPoint.x.toFixed(2));
                    gammaPoint.setAttribute('cy', projectedPoint.y.toFixed(2));
                    gammaPoint.setAttribute('fill', gammaStateColor);

                    const wave = wavePoint(currentTime);
                    cursorLine.setAttribute('x1', wave.x.toFixed(2));
                    cursorLine.setAttribute('x2', wave.x.toFixed(2));
                    cursorDot.setAttribute('cx', wave.x.toFixed(2));
                    cursorDot.setAttribute('cy', wave.y.toFixed(2));

                    doseMetric.textContent = `${doseDev.toFixed(2)}%`;
                    posMetric.textContent = `${spatialMagnitude.toFixed(2)} mm`;
                    gammaMetric.textContent = formatGamma(gamma);
                    gammaMetric.style.color = gammaStateColor;

                    doseOutput.textContent = `${doseCriteria.toFixed(1)}%`;
                    distanceOutput.textContent = `${distanceCriteria.toFixed(1)} mm`;
                    mechOutput.textContent = `${Number(mechSlider.value).toFixed(1)}x`;
                    updateDoseMaps();
                    updateNormalizationComparison();
                    caption.textContent = `Playback time ${currentTime.toFixed(2)} s. Use the added normalization controls to move from high-dose core to low-dose edge, then adjust spatial error and dose-difference factor to see when global and local gamma agree or diverge.`;
                }

                function animate(frameTime) {
                    if (!isPlaying) {
                        lastFrame = null;
                        return;
                    }
                    if (lastFrame === null) {
                        lastFrame = frameTime;
                    }
                    const elapsed = (frameTime - lastFrame) / 1000;
                    lastFrame = frameTime;
                    const nextTime = currentTime + elapsed;
                    if (nextTime >= 10) {
                        logWaveProfile = createLogWaveProfile();
                        updateWavePath();
                    }
                    currentTime = nextTime % 10;
                    updateScene();
                    requestAnimationFrame(animate);
                }

                playButton.addEventListener('click', () => {
                    isPlaying = !isPlaying;
                    playButton.textContent = isPlaying ? '▌▌' : '▶';
                    if (isPlaying) {
                        requestAnimationFrame(animate);
                    }
                });

                [doseSlider, distanceSlider, mechSlider, samplePositionSlider, comparisonSpatialSlider, comparisonDoseFactorSlider].forEach((slider) => {
                    slider.addEventListener('input', () => {
                        updateWavePath();
                        updateScene();
                    });
                });

                presets.forEach((button) => {
                    button.addEventListener('click', () => {
                        presets.forEach((candidate) => candidate.classList.remove('active'));
                        button.classList.add('active');
                        doseSlider.value = button.dataset.dose;
                        distanceSlider.value = button.dataset.distance;
                        updateScene();
                    });
                });

                normalizationModes.forEach((button) => {
                    button.addEventListener('click', () => {
                        normalizationModes.forEach((candidate) => candidate.classList.remove('active'));
                        button.classList.add('active');
                        normalizationMode = button.dataset.mode;
                        updateScene();
                    });
                });

                buildGrid();
                logWaveProfile = createLogWaveProfile();
                updateWavePath();
                updateScene();
            </script>
        </body>
        </html>
        """
        components.html(html, height=1320, scrolling=False)


render_simulator()
