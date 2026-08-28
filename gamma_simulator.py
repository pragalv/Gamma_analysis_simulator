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

                .panel-tag {
                    font-size: 10px;
                    font-weight: 700;
                    fill: #ffffff;
                }

                .dose-cell {
                    stroke: none;
                }

                .dose-crosshair {
                    stroke: rgba(255, 255, 255, 0.85);
                    stroke-width: 0.42;
                    stroke-dasharray: 1.2 1;
                    opacity: 0;
                }

                .dose-marker {
                    fill: rgba(255, 255, 255, 0.92);
                    stroke: rgba(15, 23, 42, 0.22);
                    stroke-width: 0.2;
                    opacity: 0;
                }

                .dose-axis-line {
                    stroke: rgba(15, 23, 42, 0.48);
                    stroke-width: 0.3;
                }

                .dose-axis-label,
                .dose-tick,
                .colorbar-label,
                .profile-legend-label,
                .annotation-text {
                    font-size: 4px;
                    fill: #102235;
                }

                .profile-legend-label,
                .annotation-text {
                    font-size: 3.8px;
                }

                .annotation-line {
                    stroke: rgba(15, 23, 42, 0.62);
                    stroke-width: 0.35;
                }

                .annotation-guide {
                    stroke: rgba(15, 23, 42, 0.32);
                    stroke-width: 0.3;
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
                            <input id="mech-slider" type="range" min="0.5" max="6.0" step="0.1" value="1.5" />
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
                            <input id="comparison-spatial-slider" type="range" min="0" max="5" step="0.1" value="0.8" />
                            <output id="comparison-spatial-output">0.8 mm</output>
                        </div>
                    </div>

                    <div class="control">
                        <label for="comparison-dose-factor-slider">Comparison Dose Difference</label>
                        <div class="control-row">
                            <input id="comparison-dose-factor-slider" type="range" min="0.2" max="2.6" step="0.05" value="1.4" />
                            <output id="comparison-dose-factor-output">1.40x ΔD</output>
                        </div>
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
                        <div class="plot-subtitle">Flat-top circular reference field with a sharp penumbra and a low-dose halo, matching the profile example.</div>
                        <svg id="reference-dose-svg" viewBox="0 0 112 96" style="width:100%; height:320px; display:block;">
                            <text x="15" y="13" class="panel-tag">(a)</text>
                            <rect x="12" y="8" width="74" height="74" rx="0" class="dose-frame"></rect>
                            <g id="reference-dose-map"></g>
                            <line x1="12" y1="82" x2="86" y2="82" class="dose-axis-line"></line>
                            <line x1="12" y1="8" x2="12" y2="82" class="dose-axis-line"></line>
                            <text x="12" y="87" class="dose-tick">-10</text>
                            <text x="30.5" y="87" text-anchor="middle" class="dose-tick">-5</text>
                            <text x="49" y="87" text-anchor="middle" class="dose-tick">0</text>
                            <text x="67.5" y="87" text-anchor="middle" class="dose-tick">5</text>
                            <text x="86" y="87" text-anchor="end" class="dose-tick">10</text>
                            <text x="8" y="12" text-anchor="end" class="dose-tick">-10</text>
                            <text x="8" y="30.5" text-anchor="end" class="dose-tick">-5</text>
                            <text x="8" y="49" text-anchor="end" class="dose-tick">0</text>
                            <text x="8" y="67.5" text-anchor="end" class="dose-tick">5</text>
                            <text x="8" y="82" text-anchor="end" class="dose-tick">10</text>
                            <text x="49" y="93" text-anchor="middle" class="dose-axis-label">X (cm)</text>
                            <text x="3" y="45" text-anchor="middle" transform="rotate(-90 3 45)" class="dose-axis-label">Y (cm)</text>
                        </svg>
                    </div>

                    <div class="plot-card wide plot-delivered-dose">
                        <div class="plot-title">Delivered 2D Dose Distribution</div>
                        <div class="plot-subtitle">Evaluated field with a slightly lower plateau and shifted penumbra so the profile reproduces the reference-versus-evaluated comparison.</div>
                        <svg id="delivered-dose-svg" viewBox="0 0 112 96" style="width:100%; height:320px; display:block;">
                            <text x="15" y="13" class="panel-tag">(b)</text>
                            <rect x="12" y="8" width="74" height="74" rx="0" class="dose-frame"></rect>
                            <g id="delivered-dose-map"></g>
                            <line x1="12" y1="82" x2="86" y2="82" class="dose-axis-line"></line>
                            <line x1="12" y1="8" x2="12" y2="82" class="dose-axis-line"></line>
                            <text x="12" y="87" class="dose-tick">-10</text>
                            <text x="30.5" y="87" text-anchor="middle" class="dose-tick">-5</text>
                            <text x="49" y="87" text-anchor="middle" class="dose-tick">0</text>
                            <text x="67.5" y="87" text-anchor="middle" class="dose-tick">5</text>
                            <text x="86" y="87" text-anchor="end" class="dose-tick">10</text>
                            <text x="8" y="12" text-anchor="end" class="dose-tick">-10</text>
                            <text x="8" y="30.5" text-anchor="end" class="dose-tick">-5</text>
                            <text x="8" y="49" text-anchor="end" class="dose-tick">0</text>
                            <text x="8" y="67.5" text-anchor="end" class="dose-tick">5</text>
                            <text x="8" y="82" text-anchor="end" class="dose-tick">10</text>
                            <text x="49" y="93" text-anchor="middle" class="dose-axis-label">X (cm)</text>
                            <text x="3" y="45" text-anchor="middle" transform="rotate(-90 3 45)" class="dose-axis-label">Y (cm)</text>
                        </svg>
                    </div>

                    <div class="plot-card full plot-normalization">
                        <div class="plot-title">Global vs Local Gamma Normalization</div>
                        <div class="plot-subtitle">Centerline profiles sampled from the same 2D reference and evaluated dose fields, shown in cGy with a flat-top beam and shifted penumbra.</div>
                        <div class="equation-block">
                            <div class="equation-title">Criteria Equations</div>
                            <div class="equation-text">Global: <em>&gamma;</em> = &radic;[(<span class="frac"><span class="frac-num"><em>&Delta;D</em></span><span class="frac-den"><em>D</em><sub>crit</sub></span></span>)<sup>2</sup> + (<span class="frac"><span class="frac-num"><em>&Delta;r</em></span><span class="frac-den"><em>r</em><sub>crit</sub></span></span>)<sup>2</sup>]</div>
                            <div class="equation-text">Local: <em>&gamma;</em> = &radic;[(<span class="frac"><span class="frac-num"><em>&Delta;D</em></span><span class="frac-den"><em>D</em><sub>crit</sub> &middot; <em>D</em><sub>ref,local</sub></span></span>)<sup>2</sup> + (<span class="frac"><span class="frac-num"><em>&Delta;r</em></span><span class="frac-den"><em>r</em><sub>crit</sub></span></span>)<sup>2</sup>]</div>
                        </div>
                        <svg id="normalization-svg" viewBox="0 0 118 82" style="width:100%; height:260px; display:block;">
                            <text x="18" y="12" class="annotation-text" style="font-weight:700;">(c)</text>
                            <rect x="16" y="10" width="72" height="56" fill="rgba(15,23,42,0.02)" stroke="rgba(148,163,184,0.18)"></rect>
                            <line x1="16" y1="66" x2="88" y2="66" class="profile-axis"></line>
                            <line x1="16" y1="10" x2="16" y2="66" class="profile-axis"></line>
                            <path id="normalization-reference-path" class="profile-ref"></path>
                            <path id="normalization-delivered-path" class="profile-delivered"></path>
                            <line id="normalization-sample-line" x1="50" y1="10" x2="50" y2="68" class="profile-sample-line"></line>
                            <circle id="normalization-reference-dot" cx="50" cy="24" r="1.4" class="profile-dot-ref"></circle>
                            <circle id="normalization-delivered-dot" cx="50" cy="28" r="1.4" class="profile-dot-delivered"></circle>
                            <line x1="86" y1="15" x2="92" y2="15" class="profile-ref"></line>
                            <text x="93" y="16.5" class="profile-legend-label">Reference</text>
                            <line x1="86" y1="20" x2="92" y2="20" class="profile-delivered"></line>
                            <text x="93" y="21.5" class="profile-legend-label">Evaluated</text>
                            <line id="left-dose-guide-ref" x1="24" y1="58" x2="24" y2="66" class="annotation-line"></line>
                            <line id="left-dose-guide-eval" x1="29" y1="58" x2="29" y2="66" class="annotation-line"></line>
                            <text id="left-dose-label" x="26.5" y="55" text-anchor="middle" class="annotation-text">10 cGy / 8 cGy</text>
                            <line id="plateau-guide-ref" x1="52" y1="18" x2="52" y2="10" class="annotation-line"></line>
                            <line id="plateau-guide-eval" x1="58" y1="20" x2="58" y2="10" class="annotation-line"></line>
                            <text id="plateau-dose-label" x="55" y="8" text-anchor="middle" class="annotation-text">210 cGy / 200 cGy</text>
                            <line id="edge-guide-ref" x1="74" y1="46" x2="74" y2="66" class="annotation-guide"></line>
                            <line id="edge-guide-eval" x1="78" y1="44" x2="78" y2="66" class="annotation-guide"></line>
                            <text id="edge-shift-label" x="76" y="42" text-anchor="middle" class="annotation-text">4.0 mm edge shift</text>
                            <text x="16" y="70.5" class="dose-tick">-10</text>
                            <text x="34" y="70.5" text-anchor="middle" class="dose-tick">-5</text>
                            <text x="52" y="70.5" text-anchor="middle" class="dose-tick">0</text>
                            <text x="70" y="70.5" text-anchor="middle" class="dose-tick">5</text>
                            <text x="88" y="70.5" text-anchor="end" class="dose-tick">10</text>
                            <text x="12.5" y="66" text-anchor="end" class="dose-tick">0</text>
                            <text x="12.5" y="54.8" text-anchor="end" class="dose-tick">50</text>
                            <text x="12.5" y="43.6" text-anchor="end" class="dose-tick">100</text>
                            <text x="12.5" y="32.4" text-anchor="end" class="dose-tick">150</text>
                            <text x="12.5" y="21.2" text-anchor="end" class="dose-tick">200</text>
                            <text x="12.5" y="10" text-anchor="end" class="dose-tick">250</text>
                            <text x="52" y="79" text-anchor="middle" class="dose-axis-label">X (cm)</text>
                            <text x="4" y="38" text-anchor="middle" transform="rotate(-90 4 38)" class="dose-axis-label">Dose (cGy)</text>
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
                const leftDoseGuideRef = document.getElementById('left-dose-guide-ref');
                const leftDoseGuideEval = document.getElementById('left-dose-guide-eval');
                const leftDoseLabel = document.getElementById('left-dose-label');
                const plateauGuideRef = document.getElementById('plateau-guide-ref');
                const plateauGuideEval = document.getElementById('plateau-guide-eval');
                const plateauDoseLabel = document.getElementById('plateau-dose-label');
                const edgeGuideRef = document.getElementById('edge-guide-ref');
                const edgeGuideEval = document.getElementById('edge-guide-eval');
                const edgeShiftLabel = document.getElementById('edge-shift-label');
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
                const doseGridSize = 72;
                const lowDoseFloorPct = 1;
                const doseScaleCgy = 2.1;
                let currentTime = 0;
                let isPlaying = false;
                let lastFrame = null;
                const normalizationMode = 'hotspot';
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

                function heatColorComponents(value) {
                    const clamped = clamp(value, 0, 1);
                    if (clamped < 0.33) {
                        const weight = clamped / 0.33;
                        return [mixChannel(9, 38, weight), mixChannel(45, 126, weight), mixChannel(99, 173, weight)];
                    }
                    if (clamped < 0.66) {
                        const weight = (clamped - 0.33) / 0.33;
                        return [mixChannel(38, 244, weight), mixChannel(126, 186, weight), mixChannel(173, 93, weight)];
                    }
                    const weight = (clamped - 0.66) / 0.34;
                    return [mixChannel(244, 210, weight), mixChannel(186, 69, weight), mixChannel(93, 55, weight)];
                }

                function heatColor(value) {
                    const [red, green, blue] = heatColorComponents(value);
                    return `rgb(${red}, ${green}, ${blue})`;
                }

                function normalizationReferenceDosePercent(normalizedX, normalizedY) {
                    const radius = Math.hypot(normalizedX, normalizedY);
                    const core = Math.exp(-Math.pow(radius / 0.54, 12));
                    const halo = 0.11 * Math.exp(-Math.pow(radius / 0.82, 2.4));
                    return clamp((0.93 * core + halo) * 100, 0, 100);
                }

                function doseCgyFromPercent(dosePct) {
                    return dosePct * doseScaleCgy;
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
                    const doseCgy = doseCgyFromPercent(dosePct);
                    return {
                        x: 16 + ((normalizedX + 1) / 2) * 72,
                        y: 66 - (clamp(doseCgy, 0, 250) / 250) * 56,
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

                function createNormalizationDoseSampler(sampleXNormalized, doseDiffPct, options = {}) {
                    const applyEdgeBlur = options.applyEdgeBlur ?? true;
                    const shift = Number(comparisonSpatialSlider.value) * 0.01;
                    const relativeScale = doseDiffPct / Math.max(Number(doseSlider.value), 0.1);
                    const mechScale = Number(mechSlider.value);
                    const edgeSlopeStrength = 0.028 + Math.max(0, mechScale - 1) * 0.016;
                    return (normalizedX, normalizedY, delivered) => {
                        if (!delivered) {
                            return normalizationReferenceDosePercent(normalizedX, normalizedY);
                        }

                        const shiftedX = normalizedX + shift;
                        const shiftedY = normalizedY;
                        const shiftedRadius = Math.hypot(shiftedX, shiftedY);
                        const edgeWeight = applyEdgeBlur ? Math.exp(-((shiftedRadius - 0.5) ** 2) / 0.04) : 0;
                        let adjustedX = shiftedX;
                        let adjustedY = shiftedY;

                        if (shiftedRadius > 1e-6 && edgeWeight > 1e-6) {
                            const edgeSlopeScale = 1 + edgeSlopeStrength * 12 * edgeWeight;
                            const adjustedRadius = 0.5 + (shiftedRadius - 0.5) / edgeSlopeScale;
                            const radiusScale = adjustedRadius / shiftedRadius;
                            adjustedX = shiftedX * radiusScale;
                            adjustedY = shiftedY * radiusScale;
                        }

                        const reference = normalizationReferenceDosePercent(adjustedX, adjustedY);

                        const centerWeight = Math.exp(-((shiftedX ** 2) / 0.16 + (shiftedY ** 2) / 0.16));
                        const entranceWeight = Math.exp(-(((shiftedX + 0.76) ** 2) / 0.03 + (shiftedY ** 2) / 0.07));
                        const exitWeight = Math.exp(-(((shiftedX - 0.48) ** 2) / 0.028 + (shiftedY ** 2) / 0.05));
                        const shoulderWeight = Math.exp(-(((shiftedX - sampleXNormalized) ** 2) / 0.022 + (shiftedY ** 2) / 0.042));
                        let dose = reference - 1.1 * doseDiffPct * centerWeight - 0.22 * doseDiffPct * entranceWeight - 0.35 * doseDiffPct * exitWeight;

                        if (normalizationMode === 'broadened') {
                            const broadenedReference = normalizationReferenceDosePercent(adjustedX - shift * 0.6, adjustedY);
                            const shoulderLift = 0.35 * doseDiffPct * Math.exp(-(((normalizedX - 0.24) ** 2) / 0.055 + ((normalizedY + 0.02) ** 2) / 0.1));
                            dose = broadenedReference - 0.7 * doseDiffPct * centerWeight + shoulderLift;
                        }

                        if (normalizationMode === 'coldspot') {
                            const valley = Math.exp(-(((shiftedX + 0.34) ** 2) / 0.02 + (shiftedY ** 2) / 0.04));
                            dose -= 0.55 * doseDiffPct * valley;
                        } else if (normalizationMode === 'hotspot') {
                            dose += 0.28 * doseDiffPct * shoulderWeight;
                        }

                        dose -= relativeScale * 0.8;
                        return clamp(dose, 0, 100);
                    };
                }

                function createAnimatedDeliveredDoseSampler(time, sampleXNormalized, doseDiffPct) {
                    const baseSampler = createNormalizationDoseSampler(sampleXNormalized, doseDiffPct, { applyEdgeBlur: false });
                    const shiftX = lateralSignal(time) * 0.028;
                    const shiftY = positionSignal(time) * 0.02;
                    const scaleX = 1 + doseSignal(time) * 0.006;
                    const scaleY = 1 - doseSignal(time) * 0.004;
                    return (normalizedX, normalizedY) => {
                        const animatedX = (normalizedX - shiftX) / scaleX;
                        const animatedY = (normalizedY - shiftY) / scaleY;
                        const baseDose = baseSampler(animatedX, animatedY, true);
                        const shimmer = 1.4 * Math.sin(4.2 * animatedX + time * 0.85) * Math.cos(3.6 * animatedY - time * 0.55);
                        return clamp(baseDose + shimmer, 0, 100);
                    };
                }

                function findProfileDoseCrossing(profileAt, targetDosePct, startX, endX) {
                    const steps = 160;
                    let previousX = startX;
                    let previousValue = profileAt(previousX) - targetDosePct;
                    for (let step = 1; step <= steps; step += 1) {
                        const currentX = startX + ((endX - startX) * step) / steps;
                        const currentValue = profileAt(currentX) - targetDosePct;
                        if ((previousValue <= 0 && currentValue >= 0) || (previousValue >= 0 && currentValue <= 0)) {
                            const ratio = previousValue === currentValue ? 0 : previousValue / (previousValue - currentValue);
                            return previousX + (currentX - previousX) * ratio;
                        }
                        previousX = currentX;
                        previousValue = currentValue;
                    }
                    return endX;
                }

                function updateNormalizationComparison() {
                    const sampleXNormalized = Number(samplePositionSlider.value);
                    const referenceDosePct = normalizationReferenceDosePercent(sampleXNormalized, 0);
                    const spatialYDev = Number(comparisonSpatialSlider.value);
                    const spatialZDev = 0;
                    const doseDiffPct = Number(doseSlider.value) * Number(comparisonDoseFactorSlider.value);
                    const normalizationDoseAt = createNormalizationDoseSampler(sampleXNormalized, doseDiffPct);
                    const deliveredDosePct = normalizationDoseAt(sampleXNormalized, 0, true);
                    const effectiveDoseDiffPct = deliveredDosePct - referenceDosePct;
                    const globalResult = gammaIndexForNormalization(effectiveDoseDiffPct, spatialYDev, spatialZDev, referenceDosePct, 'global');
                    const localResult = gammaIndexForNormalization(effectiveDoseDiffPct, spatialYDev, spatialZDev, referenceDosePct, 'local');
                    const refPoint = profileSvgPoint(sampleXNormalized, referenceDosePct);
                    const deliveredPoint = profileSvgPoint(sampleXNormalized, deliveredDosePct);
                    const leftRefX = -0.78;
                    const leftEvalX = -0.72;
                    const leftRefDosePct = normalizationDoseAt(leftRefX, 0, false);
                    const leftEvalDosePct = normalizationDoseAt(leftEvalX, 0, true);
                    const leftRefPoint = profileSvgPoint(leftRefX, leftRefDosePct);
                    const leftEvalPoint = profileSvgPoint(leftEvalX, leftEvalDosePct);
                    const plateauRefPoint = profileSvgPoint(0, normalizationDoseAt(0, 0, false));
                    const plateauEvalPoint = profileSvgPoint(0, normalizationDoseAt(0, 0, true));
                    const edgeTargetDosePct = 4.5;
                    const edgeRefX = findProfileDoseCrossing((normalizedX) => normalizationDoseAt(normalizedX, 0, false), edgeTargetDosePct, 0.15, 0.95);
                    const edgeEvalX = findProfileDoseCrossing((normalizedX) => normalizationDoseAt(normalizedX, 0, true), edgeTargetDosePct, 0.15, 0.95);
                    const edgeRefPoint = profileSvgPoint(edgeRefX, edgeTargetDosePct);
                    const edgeEvalPoint = profileSvgPoint(edgeEvalX, edgeTargetDosePct);
                    const edgeShiftMm = Math.abs(edgeEvalX - edgeRefX) * 100;

                    normalizationReferencePath.setAttribute('d', buildNormalizationProfilePath((normalizedX) => normalizationDoseAt(normalizedX, 0, false)));
                    normalizationDeliveredPath.setAttribute('d', buildNormalizationProfilePath((normalizedX) => normalizationDoseAt(normalizedX, 0, true)));
                    normalizationSampleLine.setAttribute('x1', refPoint.x.toFixed(2));
                    normalizationSampleLine.setAttribute('x2', refPoint.x.toFixed(2));
                    normalizationReferenceDot.setAttribute('cx', refPoint.x.toFixed(2));
                    normalizationReferenceDot.setAttribute('cy', refPoint.y.toFixed(2));
                    normalizationDeliveredDot.setAttribute('cx', deliveredPoint.x.toFixed(2));
                    normalizationDeliveredDot.setAttribute('cy', deliveredPoint.y.toFixed(2));
                    leftDoseGuideRef.setAttribute('x1', leftRefPoint.x.toFixed(2));
                    leftDoseGuideRef.setAttribute('x2', leftRefPoint.x.toFixed(2));
                    leftDoseGuideRef.setAttribute('y1', leftRefPoint.y.toFixed(2));
                    leftDoseGuideRef.setAttribute('y2', '66');
                    leftDoseGuideEval.setAttribute('x1', leftEvalPoint.x.toFixed(2));
                    leftDoseGuideEval.setAttribute('x2', leftEvalPoint.x.toFixed(2));
                    leftDoseGuideEval.setAttribute('y1', leftEvalPoint.y.toFixed(2));
                    leftDoseGuideEval.setAttribute('y2', '66');
                    leftDoseLabel.setAttribute('x', ((leftRefPoint.x + leftEvalPoint.x) / 2).toFixed(2));
                    leftDoseLabel.setAttribute('y', (Math.min(leftRefPoint.y, leftEvalPoint.y) - 4).toFixed(2));
                    leftDoseLabel.textContent = `${doseCgyFromPercent(leftRefDosePct).toFixed(0)} cGy / ${doseCgyFromPercent(leftEvalDosePct).toFixed(0)} cGy`;
                    plateauGuideRef.setAttribute('x1', plateauRefPoint.x.toFixed(2));
                    plateauGuideRef.setAttribute('x2', plateauRefPoint.x.toFixed(2));
                    plateauGuideRef.setAttribute('y1', plateauRefPoint.y.toFixed(2));
                    plateauGuideRef.setAttribute('y2', '10');
                    plateauGuideEval.setAttribute('x1', plateauEvalPoint.x.toFixed(2));
                    plateauGuideEval.setAttribute('x2', plateauEvalPoint.x.toFixed(2));
                    plateauGuideEval.setAttribute('y1', plateauEvalPoint.y.toFixed(2));
                    plateauGuideEval.setAttribute('y2', '10');
                    plateauDoseLabel.textContent = `${doseCgyFromPercent(normalizationDoseAt(0, 0, false)).toFixed(0)} cGy / ${doseCgyFromPercent(normalizationDoseAt(0, 0, true)).toFixed(0)} cGy`;
                    edgeGuideRef.setAttribute('x1', edgeRefPoint.x.toFixed(2));
                    edgeGuideRef.setAttribute('x2', edgeRefPoint.x.toFixed(2));
                    edgeGuideRef.setAttribute('y1', edgeRefPoint.y.toFixed(2));
                    edgeGuideRef.setAttribute('y2', '66');
                    edgeGuideEval.setAttribute('x1', edgeEvalPoint.x.toFixed(2));
                    edgeGuideEval.setAttribute('x2', edgeEvalPoint.x.toFixed(2));
                    edgeGuideEval.setAttribute('y1', edgeEvalPoint.y.toFixed(2));
                    edgeGuideEval.setAttribute('y2', '66');
                    edgeShiftLabel.setAttribute('x', ((edgeRefPoint.x + edgeEvalPoint.x) / 2).toFixed(2));
                    edgeShiftLabel.setAttribute('y', (Math.min(edgeRefPoint.y, edgeEvalPoint.y) - 3.5).toFixed(2));
                    edgeShiftLabel.textContent = `${edgeShiftMm.toFixed(1)} mm edge shift`;

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

                function buildDoseMapMarkup(doseAt) {
                    const rasterSize = 240;
                    const canvas = document.createElement('canvas');
                    canvas.width = rasterSize;
                    canvas.height = rasterSize;
                    const context = canvas.getContext('2d');
                    const image = context.createImageData(rasterSize, rasterSize);

                    for (let row = 0; row < rasterSize; row += 1) {
                        for (let col = 0; col < rasterSize; col += 1) {
                            const normalizedX = ((col + 0.5) / rasterSize) * 2 - 1;
                            const normalizedY = 1 - ((row + 0.5) / rasterSize) * 2;
                            const value = doseAt(normalizedX, normalizedY) / 100;
                            const [red, green, blue] = heatColorComponents(value);
                            const pixelIndex = (row * rasterSize + col) * 4;
                            image.data[pixelIndex] = red;
                            image.data[pixelIndex + 1] = green;
                            image.data[pixelIndex + 2] = blue;
                            image.data[pixelIndex + 3] = 255;
                        }
                    }

                    context.putImageData(image, 0, 0);
                    return `<image x="12" y="8" width="74" height="74" preserveAspectRatio="none" href="${canvas.toDataURL('image/png')}"></image>`;
                }

                function updateDoseMaps() {
                    const sampleXNormalized = Number(samplePositionSlider.value);
                    const doseDiffPct = Number(doseSlider.value) * Number(comparisonDoseFactorSlider.value);
                    const normalizationDoseAt = createNormalizationDoseSampler(sampleXNormalized, doseDiffPct);
                    const animatedDeliveredDoseAt = createAnimatedDeliveredDoseSampler(currentTime, sampleXNormalized, doseDiffPct);
                    referenceDoseMap.innerHTML = buildDoseMapMarkup((normalizedX, normalizedY) => normalizationDoseAt(normalizedX, normalizedY, false));
                    deliveredDoseMap.innerHTML = buildDoseMapMarkup((normalizedX, normalizedY) => animatedDeliveredDoseAt(normalizedX, normalizedY));
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
                        <text x="7" y="12" text-anchor="end" dominant-baseline="middle" class="tick-text">8</text>
                        <text x="7" y="24" text-anchor="end" dominant-baseline="middle" class="tick-text">4</text>
                        <text x="7" y="36" text-anchor="end" dominant-baseline="middle" class="tick-text">0</text>
                        <text x="7" y="48" text-anchor="end" dominant-baseline="middle" class="tick-text">-4</text>
                        <text x="7" y="60" text-anchor="end" dominant-baseline="middle" class="tick-text">-8</text>
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
                    const y = 36 - logFileSignal(t) * 3;
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
