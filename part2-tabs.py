#!/usr/bin/env python3
"""
Part 2: All 5 Tab Files
Run: python build_part2.py
"""
import os

BASE = "genai_monitor"

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {path}")

def build():
    print(f"Part 2: Building tab files in ./{BASE}/tabs/\n")

    # ==================== tabs/metrics_summary.py ====================
    w("tabs/metrics_summary.py", r'''"""Metrics Summary tab - generates the metrics summary table."""
import pandas as pd
from utils import find_column, safe_numeric_conversion


def get_score_cell_class(row, score_col, threshold_col, metrics_col, config):
    try:
        if not all([score_col, threshold_col, metrics_col]):
            return ''
        score = safe_numeric_conversion(row.get(score_col))
        threshold = safe_numeric_conversion(row.get(threshold_col))
        metric = row.get(metrics_col, '')
        if pd.isna(score) or pd.isna(threshold):
            return ''
        if metric in config['reverse_metrics']:
            if score > threshold:
                return 'below-threshold'
        else:
            if score < threshold:
                return 'below-threshold'
        if abs(score - threshold) < 0.001:
            return 'equal-threshold'
        return ''
    except Exception:
        return ''


def generate_metrics_summary_table(df, config):
    try:
        if df.empty:
            return "<div class='text-center p-3'>No metrics data available</div>"
        threshold_col = find_column(df, ['Threshold_Value', 'Threshold'])
        score_col = find_column(df, ['aggregate_score', 'score', 'Score'])
        metrics_col = find_column(df, ['Metrics', 'Metric'])
        html = ['<div class="table-container"><table class="modern-table"><thead><tr>']
        for col in df.columns:
            html.append(f'<th>{col.replace("_", " ").title()}</th>')
        html.append('</tr></thead><tbody>')
        for _, row in df.iterrows():
            html.append('<tr>')
            for col in df.columns:
                value = row[col]
                if isinstance(value, (int, float)) and not pd.isna(value):
                    value = f'{value:.2f}' if col in [threshold_col, score_col] else (f'{value:.2f}' if value != int(value) else str(int(value)))
                if pd.isna(value) or value is None:
                    value = 'N/A'
                else:
                    value = str(value).replace('\n', '<br>').replace('\r', '')
                cell_class = ''
                if col == score_col and threshold_col and score_col:
                    cell_class = get_score_cell_class(row, score_col, threshold_col, metrics_col, config)
                if cell_class:
                    html.append(f'<td class="metric-score"><span class="{cell_class}">{value}</span></td>')
                else:
                    html.append(f'<td class="metric-score">{value}</td>')
            html.append('</tr>')
        html.append('</tbody></table></div>')
        return '\n'.join(html)
    except Exception as e:
        return f"<div class='alert alert-error'>Error generating table: {e}</div>"
''')

    # ==================== tabs/data_assurance.py ====================
    w("tabs/data_assurance.py", r'''"""Data Assurance tab - coverage sunburst, augmentation pipeline, golden dataset."""
import json
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.offline as plot

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from utils import highlight_diff


def create_test_coverage_sunburst(excel_path, sheet_name):
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df["topic"] = df["topic"].astype(str).str.strip().str.upper()
        df["sub_topic"] = df["sub_topic"].astype(str).str.strip().str.title()
        df["sub_subtopic"] = df["sub_subtopic"].astype(str).str.strip().replace({"": None, "nan": None, "None": None})
        has_expected = "expected_record_count" in df.columns
        agg_cols = {"count": ("query", lambda x: x.notna().sum())}
        if has_expected:
            agg_cols["expected"] = ("expected_record_count", "sum")
        sunburst_df = df.groupby(["topic", "sub_topic", "sub_subtopic"], dropna=False).agg(**agg_cols).reset_index()
        table_rows = ""
        for _, row in sunburst_df.iterrows():
            actual = int(row["count"])
            sub_sub = row["sub_subtopic"] if pd.notna(row["sub_subtopic"]) else "-"
            expected_val = int(row["expected"]) if has_expected and pd.notna(row.get("expected")) else "-"
            table_rows += f"<tr><td>{row['topic']}</td><td>{row['sub_topic']}</td><td>{sub_sub}</td><td>{expected_val}</td><td>{actual}</td></tr>"
        table_html = f'<div style="width:100%;margin-bottom:32px;"><div class="table-container" style="width:100%;max-width:100%;overflow-x:auto;"><table class="modern-table" style="width:100%;"><thead><tr><th>Topic</th><th>Sub Topic</th><th>Sub Subtopic</th><th>Expected Record Count</th><th>Actual Record Count</th></tr></thead><tbody>{table_rows}</tbody></table></div></div>'
        fig = px.sunburst(sunburst_df, path=["topic", "sub_topic", "sub_subtopic"], values="count", color="topic", branchvalues="total", maxdepth=2)
        fig.update_traces(texttemplate="<b>%{label}</b><br>Count: %{value}<br>%{percentRoot:.0%}", hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percentRoot:.0%}<extra></extra>", textfont=dict(size=14))
        fig.update_layout(sunburstcolorway=px.colors.qualitative.Pastel, margin=dict(t=60, l=20, r=20, b=20))
        chart_html = plot.plot(fig, output_type="div", include_plotlyjs=False)
        return table_html + f'<div style="display:flex;justify-content:center;width:100%;"><div style="width:fit-content;">{chart_html}</div></div>'
    except Exception as e:
        return "<div class='text-center p-3'><b>Error loading test coverage</b></div>"


def generate_augmented_data_table(excel_path, sheet_name):
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        if df.empty:
            return "<div class='text-center p-3'>No augmentation data available</div>"
        df.columns = [str(c).strip() for c in df.columns]
        base_col = aug_col = case_col = None
        for c in df.columns:
            nm = c.lower()
            if "base" in nm and "query" in nm:
                base_col = c
            if "augmented" in nm:
                aug_col = c
            if nm.strip() == "case":
                case_col = c
        display_cols = [c for c in df.columns if case_col is None or c != case_col]
        case_styles = {"P": ("P", "#1565C0", "#E3F2FD"), "N": ("N", "#B71C1C", "#FFEBEE"), "E": ("E", "#1B5E20", "#E8F5E9")}
        html = ['<div class="table-container"><table class="modern-table"><thead><tr>']
        for col in display_cols:
            html.append(f'<th>{col.replace("_", " ").title()}</th>')
        html.append('</tr></thead><tbody>')
        for _, row in df.iterrows():
            html.append('<tr>')
            bq = str(row[base_col]) if base_col and pd.notna(row.get(base_col)) else ""
            aq = str(row[aug_col]) if aug_col and pd.notna(row.get(aug_col)) else ""
            badge = ""
            if case_col and pd.notna(row.get(case_col)):
                raw = str(row[case_col]).strip().lower()
                key = "P" if raw.startswith("p") else ("N" if raw.startswith("n") else ("E" if raw.startswith("e") else ""))
                if key in case_styles:
                    lb, fg, bg = case_styles[key]
                    badge = f"<span style='display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.75rem;font-weight:800;background:{bg};color:{fg};border:1px solid {fg};'>{lb}</span>"
            for col in display_cols:
                val = row.get(col, "")
                if col == aug_col:
                    dh = highlight_diff(bq, aq)
                    if badge:
                        cc = f"<div style='position:relative;min-height:24px;'><div style='position:absolute;top:0;right:0;'>{badge}</div><div style='padding-right:36px;'>{dh}</div></div>"
                    else:
                        cc = dh
                    html.append(f'<td>{cc}</td>')
                else:
                    html.append(f'<td>{"N/A" if pd.isna(val) else str(val)}</td>')
            html.append('</tr>')
        html.append('</tbody></table></div>')
        return '\n'.join(html)
    except Exception as e:
        return f"<div class='alert alert-error'>Error: {e}</div>"


def get_coverage_edit_data():
    try:
        excel_path = Path(__file__).resolve().parent.parent / "Metrics_template02.xlsx"
        df = pd.read_excel(excel_path, sheet_name='Test data coverage')
        df["topic"] = df["topic"].astype(str).str.strip().str.upper()
        df["sub_topic"] = df["sub_topic"].astype(str).str.strip().str.title()
        df["sub_subtopic"] = df["sub_subtopic"].astype(str).str.strip().replace({"nan": None, "None": None, "": None})
        has_expected = "expected_record_count" in df.columns
        agg_cols = {"count": ("query", lambda x: x.notna().sum())}
        if has_expected:
            agg_cols["expected_record_count"] = ("expected_record_count", "first")
        agg = df.groupby(["topic", "sub_topic", "sub_subtopic"], dropna=False).agg(**agg_cols).reset_index()
        rows = []
        for _, row in agg.iterrows():
            rows.append({
                "topic": row["topic"], "sub_topic": row["sub_topic"],
                "sub_subtopic": row["sub_subtopic"] if pd.notna(row["sub_subtopic"]) else "-",
                "expected_record_count": int(row["expected_record_count"]) if has_expected and pd.notna(row.get("expected_record_count")) else "",
                "actual_record_count": int(row["count"]),
            })
        return rows
    except Exception:
        return []
''')

    # ==================== tabs/model_quality_assurance.py ====================
    w("tabs/model_quality_assurance.py", r'''"""Model Quality Assurance tab - charts, details table, disaggregated view, recovery loop."""
import json
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.offline as plot

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from utils import find_column, safe_numeric_conversion, truncate_text, normalize_query_match, normalize_text, text_equal


def create_metrics_bar_chart(summary_df, config, layout_fn):
    try:
        theme = config['theme']
        mc = find_column(summary_df, ['Metrics', 'Metric'])
        pc = find_column(summary_df, ["Passed"])
        fc = find_column(summary_df, ["Failed"])
        metrics = summary_df[mc].astype(str).tolist()
        failed = summary_df[fc].fillna(0).tolist()
        passed = summary_df[pc].fillna(0).tolist()
        fig = go.Figure()
        fig.add_bar(x=metrics, y=failed, name='Failed', marker_color=config['status_colors']['Failed'])
        fig.add_bar(x=metrics, y=passed, name='Passed', marker_color=config['status_colors']['Passed'])
        fig.update_layout(barmode='group', title='Metrics Performance Overview', xaxis_title='Metrics', yaxis_title='Number of Test Cases', bargap=0.25, bargroupgap=0.05, width=len(metrics) * 140, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5), **layout_fn(theme))
        fig.update_yaxes(autorange=True)
        return plot.plot(fig, output_type='div', include_plotlyjs=False)
    except Exception as e:
        return f"<div>Error creating metrics chart: {e}</div>"


def create_overall_pie_chart(overall_df, config, layout_fn):
    try:
        theme = config['theme']
        passed = int(overall_df[[c for c in overall_df.columns if 'passed' in c.lower()][0]].sum())
        failed = int(overall_df[[c for c in overall_df.columns if 'failed' in c.lower()][0]].sum())
        labels, values, colors = [], [], []
        if passed > 0:
            labels.append(f"Passed ({passed})"); values.append(passed); colors.append(config['status_colors']['passed'])
        if failed > 0:
            labels.append(f"Failed ({failed})"); values.append(failed); colors.append(config['status_colors']['failed'])
        total = sum(values)
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors), textinfo="label+percent", hoverinfo="label+percent+value")])
        fig.update_layout(title="Overall Performance Distribution", **layout_fn(theme), annotations=[dict(text=f"Total<br>{total}", x=0.5, y=0.5, font_size=16, showarrow=False)])
        return plot.plot(fig, output_type='div', include_plotlyjs=False)
    except Exception as e:
        return f"<div>Error creating overall chart: {e}</div>"


def create_score_comparison_chart(metrics_df, metrics_col, score_col, threshold_col, config, layout_fn):
    try:
        theme = config['theme']
        metrics = metrics_df[metrics_col].tolist()
        scores = [safe_numeric_conversion(x) for x in metrics_df[score_col].tolist()]
        thresholds = [safe_numeric_conversion(x) for x in metrics_df[threshold_col].tolist()]
        bar_colors = []
        for score, threshold, metric in zip(scores, thresholds, metrics):
            if pd.isna(score) or pd.isna(threshold):
                bar_colors.append(theme['border_color']); continue
            if metric in config['reverse_metrics']:
                color = config['status_colors']['passed'] if score <= threshold else config['status_colors']['failed']
            else:
                color = config['status_colors']['passed'] if score >= threshold else config['status_colors']['failed']
            bar_colors.append(color)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=metrics, y=scores, name='Actual Score', marker_color=bar_colors, hovertemplate="<b>%{x}</b><br>Score: %{y:.3f}<extra></extra>", opacity=0.8))
        fig.add_trace(go.Scatter(x=metrics, y=thresholds, mode='lines+markers', name='Threshold', line=dict(color=theme['accent_color'], width=3, dash='dash'), marker=dict(size=8, color=theme['accent_color']), hovertemplate="<b>%{x}</b><br>Threshold: %{y:.3f}<extra></extra>"))
        fig.update_layout(**layout_fn(theme), title="Score vs Threshold Comparison", xaxis_title="Metrics", yaxis_title="Score", bargap=0.25, width=len(metrics) * 140, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        fig.update_yaxes(range=[0, 1.1])
        return plot.plot(fig, output_type='div', include_plotlyjs=False)
    except Exception as e:
        return f"<div>Error creating comparison chart: {e}</div>"


def create_run_comparison_chart(prev_df, curr_df, theme):
    try:
        if prev_df.empty or curr_df.empty:
            return "<div class='text-center p-3'><b>No data available</b></div>"
        def fe(df, c):
            for x in c:
                if x in df.columns:
                    return x
            return None
        mc_p = fe(prev_df, ["Metric", "Metrics", "metric"]); sc_p = fe(prev_df, ["Score", "aggregate_score", "score"])
        mc_c = fe(curr_df, ["Metric", "Metrics", "metric"]); sc_c = fe(curr_df, ["Score", "aggregate_score", "score"])
        if not all([mc_p, sc_p, mc_c, sc_c]):
            return "<div class='text-center p-3'><b>No data available</b></div>"
        prev_df = prev_df[[mc_p, sc_p]].rename(columns={mc_p: "Metric", sc_p: "Previous"})
        curr_df = curr_df[[mc_c, sc_c]].rename(columns={mc_c: "Metric", sc_c: "Current"})
        merged = pd.merge(prev_df, curr_df, on="Metric", how="inner")
        if merged.empty:
            return "<div class='text-center p-3'><b>No data available</b></div>"
        fig = go.Figure()
        fig.add_bar(x=merged["Metric"], y=pd.to_numeric(merged["Previous"], errors="coerce"), name="Previous Run", marker_color=theme["secondary_color"])
        fig.add_bar(x=merged["Metric"], y=pd.to_numeric(merged["Current"], errors="coerce"), name="Current Run", marker_color=theme["primary_color"])
        fig.update_layout(barmode="group", title="Run Comparison", xaxis_title="Metrics", yaxis_title="Score")
        return plot.plot(fig, output_type="div", include_plotlyjs=False)
    except Exception:
        return "<div class='text-center p-3'><b>No data available</b></div>"


def create_disaggregated_table(excel_path):
    try:
        df = pd.read_excel(excel_path, sheet_name="Disaggregated View", header=None)
        agg_scores = {}
        for col in range(2, len(df.columns)):
            metric = str(df.iloc[0, col]).strip()
            val = df.iloc[1, col]
            if metric and metric.lower() != "nan":
                try:
                    agg_scores[metric] = float(val)
                except (ValueError, TypeError):
                    agg_scores[metric] = None
        parsed = []
        i = 0
        while i < len(df):
            cell = str(df.iloc[i, 2]).strip().lower()
            if cell == "topic":
                if i + 4 >= len(df):
                    i += 1; continue
                topic = str(df.iloc[i + 1, 2]).strip()
                sub_topic = str(df.iloc[i + 1, 3]).strip()
                pass_row = df.iloc[i + 2]; fail_row = df.iloc[i + 3]
                metrics_data = {}
                for col in range(4, len(df.columns)):
                    mn = str(df.iloc[i, col]).strip()
                    if not mn or mn.lower() == "nan":
                        continue
                    try:
                        pm = int(str(pass_row[col]).split()[0]); fm = int(str(fail_row[col]).split()[0])
                    except (ValueError, IndexError):
                        continue
                    metrics_data[mn] = {"passed": pm, "failed": fm, "aggregate_score": agg_scores.get(mn)}
                parsed.append({"topic": topic, "sub_topic": sub_topic, "metrics": metrics_data})
                i += 5
            else:
                i += 1
        return f"""<div class="card-header"><h3>Disaggregated Analysis</h3></div><div class="card-content"><label>Topic</label><br><select id="topicSelect"></select><br><br><label>Sub-topic</label><br><div id="subTopicWrapper" class="multi-select"><div id="selectedSubTopics" class="chips"></div><input id="subTopicInput" placeholder="Select sub-topics" readonly/><div id="subTopicDropdown" class="dropdown"></div></div><br><br><div class="chart-scroll"><div id="disaggChart"></div></div></div><script>const DISAGG_DATA = {json.dumps(parsed)};</script>"""
    except Exception:
        return "<div class='text-center p-3'><b>Error loading disaggregated data</b></div>"


def load_recovery_loop_global(metric_details_excel_path):
    try:
        if not metric_details_excel_path.exists():
            return []
        xls = pd.ExcelFile(metric_details_excel_path)
        match = next((s for s in xls.sheet_names if s.strip().lower() == 'recovery loop global'), None)
        if not match:
            return []
        df = pd.read_excel(xls, sheet_name=match)
        if df.empty:
            return []
        return [{str(k): (None if pd.isna(v) else v) for k, v in row.items()} for _, row in df.iterrows()]
    except Exception:
        return []


def generate_interactive_details_table(df, metrics):
    try:
        if df.empty:
            return "<div class='text-center p-3'>No details data available</div>"
        html = ['<div class="table-container"><table class="details-table"><thead><tr>']
        html.append('<th style="position:sticky;left:0;z-index:11;min-width:50px;text-align:center;background:linear-gradient(135deg,#2E86AB 0%,#A23B72 100%);">#</th>')
        html.append('<th>TC ID</th><th>Question</th><th>Response</th>')
        for metric in metrics:
            html.append(f'<th class="text-center">{metric.replace("_", " ").title()}</th>')
        html.append('</tr></thead><tbody id="tableBody"></tbody></table></div>')
        html.append(_generate_pagination_controls())
        html.append(_generate_table_javascript(df, metrics))
        return '\n'.join(html)
    except Exception as e:
        return f"<div class='alert alert-error'>Error: {e}</div>"


def _generate_pagination_controls():
    return '<div class="pagination-container"><div class="pagination-controls"><select id="rowsPerPage" class="rows-selector" onchange="changeRowsPerPage()"><option value="10">10 rows/page</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select></div><div class="pagination-controls" id="paginationButtons"></div><div class="page-info"><span id="pageInfo">Page 1 of 1</span></div></div>'


def _generate_table_javascript(df, metrics):
    try:
        td = []
        for idx, row in df.iterrows():
            qs = str(row.get('Query', 'N/A')).replace('\\n', '<br>').replace('\n', '<br>')
            rs = truncate_text(str(row.get('Response', 'N/A')), 100).replace('\\n', '<br>').replace('\n', '<br>')
            ti = str(row.get('TC ID', 'N/A'))
            mc = {}
            for m in metrics:
                st = row.get(f"{m}_status", 'Unknown')
                sc = row.get(m, 'N/A')
                fs = f'{sc:.2f}' if pd.notna(sc) and isinstance(sc, (int, float)) else ('NAE')
                cc = 'status-warning' if pd.isna(sc) else ('status-passed' if str(st).lower() == 'passed' else ('status-failed' if str(st).lower() == 'failed' else ('status-skipped' if str(st).lower() == 'skipped' else 'status-unknown')))
                mc[m.strip()] = {'value': fs, 'status': st, 'class': cc, 'clickable': fs != 'NAE'}
            td.append({'index': int(idx), 'tc_id': ti, 'query': qs, 'response': rs, 'metrics': mc})
        return f"""<script>let currentPage=1,rowsPerPage=10,totalRows=0;let allTableData={json.dumps(td)};let allMetrics={json.dumps(metrics)};function initializeTable(){{totalRows=allTableData.length;displayPage();}}function displayPage(){{const si=(currentPage-1)*rowsPerPage;const ei=Math.min(si+rowsPerPage,totalRows);const tb=document.getElementById('tableBody');if(!tb)return;let h='';for(let i=si;i<ei;i++){{const rd=allTableData[i];const rn=(currentPage-1)*rowsPerPage+(i-si)+1;h+='<tr>';h+=`<td style="position:sticky;left:0;z-index:5;background:#f8f9fa;text-align:center;font-weight:700;color:#555;border-right:2px solid #dee2e6;min-width:50px;">${{rn}}</td>`;h+=`<td>${{rd.tc_id}}</td><td>${{rd.query}}</td><td>${{rd.response}}</td>`;allMetrics.forEach(m=>{{const md=rd.metrics[m]||{{value:"NAE",class:"status-skipped",clickable:false}};if(md.clickable)h+=`<td class="text-center"><span class="status-cell ${{md.class}}" onclick="openModal(${{rd.index}},'${{m}}')">${{md.value}}</span></td>`;else h+=`<td class="text-center"><span class="status-cell status-warning" title="Not Applicable for Execution">NAE</span></td>`;}});h+='</tr>';}}tb.innerHTML=h;updatePaginationInfo();}}function updatePaginationInfo(){{const tp=Math.ceil(totalRows/rowsPerPage);const el=document.getElementById('pageInfo');if(el)el.textContent=`Page ${{currentPage}} of ${{tp}}`;const c=document.getElementById('paginationButtons');if(c)c.innerHTML=`<button class="page-btn" onclick="previousPage()" ${{currentPage===1?"disabled":""}}>Prev</button><span class="page-btn disabled">${{currentPage}} / ${{tp}}</span><button class="page-btn" onclick="nextPage()" ${{currentPage===tp?"disabled":""}}>Next</button>`;}}function nextPage(){{if(currentPage<Math.ceil(totalRows/rowsPerPage)){{currentPage++;displayPage();}}}}function previousPage(){{if(currentPage>1){{currentPage--;displayPage();}}}}function changeRowsPerPage(){{const s=document.getElementById('rowsPerPage');if(s){{rowsPerPage=parseInt(s.value);currentPage=1;displayPage();}}}}document.addEventListener('DOMContentLoaded',initializeTable);</script>"""
    except Exception as e:
        return f"<script>console.error('Error: {e}');</script>"
''')

    # ==================== tabs/trustworthy_assurance.py ====================
    w("tabs/trustworthy_assurance.py", r'''"""Trustworthy Assurance tab - trustworthy table with pagination."""
import json
import pandas as pd
from pathlib import Path

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


def generate_trustworthy_table(excel_file, sheet_name, table_id, auto_render=False):
    try:
        excel_path = Path(__file__).resolve().parent.parent / excel_file
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        if df.empty:
            return "<div class='text-center p-3'>No data available</div>"
        columns = list(df.columns)
        rows = []
        for _, row in df.iterrows():
            cells = []
            for col in columns:
                val = row[col]
                if pd.isna(val) or val is None:
                    cells.append("N/A")
                else:
                    sv = str(val).strip()
                    if str(col).strip().lower() == "result":
                        if sv.lower() == "pass":
                            cells.append("<span style='display:inline-flex;align-items:center;gap:5px;background:#28a745;color:white;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;'>&#10003; Pass</span>")
                        elif sv.lower() == "fail":
                            cells.append("<span style='display:inline-flex;align-items:center;gap:5px;background:#dc3545;color:white;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;'>&#10007; Fail</span>")
                        else:
                            cells.append(sv)
                    else:
                        cells.append(sv.replace('\n', '<br>').replace('\r', '').replace("'", "&#39;"))
            rows.append(cells)
        rj = json.dumps(rows)
        cl = json.dumps([str(c).strip().lower() for c in columns])
        tid = f"{table_id}Body"
        rid = f"{table_id}Rpp"
        pid = f"{table_id}PgBtns"
        iid = f"{table_id}PgInfo"
        rfn = f"render{table_id[0].upper()}{table_id[1:]}"
        ajs = f'document.addEventListener("DOMContentLoaded", function() {{ render(); }});' if auto_render else ''
        html = ['<div class="table-container"><table class="details-table"><thead><tr>']
        for col in columns:
            al = ' style="text-align:center;"' if str(col).strip().lower() == "result" else ''
            html.append(f'<th{al}>{str(col).replace("_", " ").title()}</th>')
        html.append(f'</tr></thead><tbody id="{tid}"></tbody></table></div>')
        html.append(f'<div class="pagination-container"><div class="pagination-controls"><select id="{rid}" class="rows-selector"><option value="10">10 rows/page</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select></div><div class="pagination-controls" id="{pid}"></div><div class="page-info"><span id="{iid}">Page 1 of 1</span></div></div>')
        html.append(f"""<script>(function(){{var rows={rj};var colsLower={cl};var curPage=1;function getRpp(){{var el=document.getElementById('{rid}');return el?parseInt(el.value):10;}}function render(){{var rpp=getRpp(),total=rows.length;var tp=Math.max(1,Math.ceil(total/rpp));if(curPage>tp)curPage=tp;var s=(curPage-1)*rpp,e=Math.min(s+rpp,total);var tbody=document.getElementById('{tid}');if(!tbody)return;var h='';for(var i=s;i<e;i++){{h+='<tr>';for(var ci=0;ci<rows[i].length;ci++){{var ir=colsLower[ci]==='result';var ts=ir?' style="text-align:center;"':'';h+='<td'+ts+'>'+rows[i][ci]+'</td>';}}h+='</tr>';}}tbody.innerHTML=h;var info=document.getElementById('{iid}');if(info)info.textContent='Page '+curPage+' of '+tp;var pb=document.getElementById('{pid}');if(pb){{pb.innerHTML='<button class="page-btn" id="{table_id}Prev">Prev</button><span class="page-btn disabled">'+curPage+' / '+tp+'</span><button class="page-btn" id="{table_id}Next">Next</button>';var pv=document.getElementById('{table_id}Prev');var nx=document.getElementById('{table_id}Next');if(curPage<=1)pv.disabled=true;if(curPage>=tp)nx.disabled=true;pv.addEventListener('click',function(){{if(curPage>1){{curPage--;render();}}}});nx.addEventListener('click',function(){{if(curPage<tp){{curPage++;render();}}}});}}}}var rEl=document.getElementById('{rid}');if(rEl)rEl.addEventListener('change',function(){{curPage=1;render();}});window['{rfn}']=render;{ajs}}})();</script>""")
        return '\n'.join(html)
    except Exception as e:
        return f"<div class='text-center p-3'><b>Error loading {sheet_name}: {e}</b></div>"
''')

    # ==================== tabs/secondary_llm.py ====================
    w("tabs/secondary_llm.py", r'''"""Secondary LLM tab - secondary LLM comparison table."""
import json
import pandas as pd
from pathlib import Path

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from utils import find_column, truncate_text, normalize_query_match


def generate_secondary_llm_table(df, metrics):
    try:
        if df.empty:
            return "<div class='text-center p-3'>No details data available</div>"
        html = ['<div class="table-container"><table class="details-table"><thead><tr>']
        html.append('<th style="position:sticky;left:0;z-index:11;min-width:50px;text-align:center;background:linear-gradient(135deg,#2E86AB 0%,#A23B72 100%);">#</th>')
        html.append('<th>Question</th><th>Response</th>')
        for m in metrics:
            html.append(f'<th>Primary_{m}</th><th>Secondary_{m}</th>')
        html.append('</tr></thead><tbody id="secondaryTableBody"></tbody></table></div>')
        html.append(_generate_secondary_pagination_controls())
        html.append(_generate_secondary_llm_javascript(df, metrics))
        return "\n".join(html)
    except Exception as e:
        return f"<div class='alert alert-error'>Error: {e}</div>"


def _generate_secondary_pagination_controls():
    return '<div class="pagination-container"><div class="pagination-controls"><select id="secondaryRowsPerPage" class="rows-selector" onchange="secondaryChangeRowsPerPage()"><option value="10">10 rows/page</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select></div><div class="pagination-controls" id="secondaryPaginationButtons"></div><div class="page-info"><span id="secondaryPageInfo">Page 1 of 1</span></div></div>'


def _generate_secondary_llm_javascript(df, metrics):
    try:
        td = []
        for idx, row in df.iterrows():
            qs = str(row.get('Query', 'N/A')).replace('\\n', '<br>').replace('\n', '<br>')
            rs = truncate_text(str(row.get('Response', 'N/A')), 100).replace('\\n', '<br>').replace('\n', '<br>')
            qk = normalize_query_match(qs)
            mc = {}
            for m in metrics:
                st = row.get(f"{m}_status", 'Unknown')
                sc = row.get(m, 'N/A')
                fs = f'{sc:.2f}' if pd.notna(sc) and isinstance(sc, (int, float)) else (str(sc) if sc != 'N/A' else 'N/A')
                cc = 'status-warning' if pd.isna(sc) else ('status-passed' if str(st).lower() == 'passed' else ('status-failed' if str(st).lower() == 'failed' else ('status-skipped' if str(st).lower() == 'skipped' else 'status-unknown')))
                mc[m.strip()] = {'value': fs, 'status': st, 'class': cc, 'clickable': True}
            td.append({'index': int(idx), 'query': qs, 'query_key': qk, 'response': rs, 'metrics': mc})

        smm = {}
        try:
            fp = Path(__file__).resolve().parent.parent / "Metrics_template02.xlsx"
            if fp.exists():
                xls = pd.ExcelFile(fp)
                if "Secondary LLM" in xls.sheet_names:
                    sdf = pd.read_excel(xls, sheet_name="Secondary LLM")
                    sdf = sdf.rename(columns=lambda c: str(c).strip())
                    for _, sr in sdf.iterrows():
                        en = str(sr.get("Eval_Name", "")).strip()
                        qv = str(sr.get("Query", "")).strip()
                        if not en:
                            continue
                        mk = en.strip().lower()
                        qk2 = normalize_query_match(qv)
                        meta = {}
                        for col in sdf.columns:
                            if str(col).strip().lower() in ("eval_name", "trace_id"):
                                continue
                            val = sr.get(col)
                            meta[col] = None if pd.isna(val) else val
                        existing = smm.setdefault(mk, {}).setdefault(qk2, [])
                        if meta.get("Few_Shot_Example"):
                            existing.insert(0, meta)
                        else:
                            existing.append(meta)
        except Exception as e:
            logger.warning(f"Unable to read Secondary LLM sheet: {e}")

        return f"""<script>let secondaryCurrentPage=1,secondaryRowsPerPage=10;const secondaryTableData={json.dumps(td)};const secondaryMetaMap={json.dumps(smm)};let allSecondaryMetrics={json.dumps(metrics)};function renderSecondaryTable(){{const tb=document.getElementById("secondaryTableBody");if(!tb)return;const s=(secondaryCurrentPage-1)*secondaryRowsPerPage;const e=Math.min(s+secondaryRowsPerPage,secondaryTableData.length);let h="";for(let i=s;i<e;i++){{const r=secondaryTableData[i];const rn=(secondaryCurrentPage-1)*secondaryRowsPerPage+(i-s)+1;h+="<tr>";h+=`<td style="position:sticky;left:0;z-index:5;background:#f8f9fa;text-align:center;font-weight:700;color:#555;border-right:2px solid #dee2e6;min-width:50px;">${{rn}}</td>`;h+=`<td>${{r.query}}</td><td>${{r.response}}</td>`;allSecondaryMetrics.forEach(m=>{{const md=r.metrics[m]||{{value:"N/A",class:"status-skipped",clickable:false}};if(md.clickable)h+=`<td class="text-center"><span class="status-cell ${{md.class}}" onclick="openModal(${{r.index}},'${{m}}')">${{md.value}}</span></td>`;else h+=`<td class="text-center"><span class="status-cell status-skipped">N/A</span></td>`;const mm=secondaryMetaMap[m.toLowerCase()]||{{}};const ml=mm[r.query_key]||[];const mt=ml.length>0?ml[0]:null;const et=(mt&&mt.Error_Type!=null&&mt.Error_Type!=="")?String(mt.Error_Type):"none";const bc=et.toLowerCase()!=="none"?"status-failed":"status-passed";const bl=et.toLowerCase()!=="none"?et:"No Violation";h+=`<td class="text-center"><button class="status-cell ${{bc}}" onclick="openSecondaryModal(${{i}},'${{escapeHtml(m)}}')" style="border:none;padding:8px 10px;border-radius:8px;">${{bl}}</button></td>`;}});h+="</tr>";}}tb.innerHTML=h;const tp=Math.ceil(secondaryTableData.length/secondaryRowsPerPage);document.getElementById("secondaryPageInfo").innerText=`Page ${{secondaryCurrentPage}} of ${{tp}}`;const c=document.getElementById("secondaryPaginationButtons");if(c)c.innerHTML=`<button class="page-btn" onclick="secondaryPreviousPage()" ${{secondaryCurrentPage===1?"disabled":""}}>Prev</button><span class="page-btn disabled">${{secondaryCurrentPage}} / ${{tp}}</span><button class="page-btn" onclick="secondaryNextPage()" ${{secondaryCurrentPage===tp?"disabled":""}}>Next</button>`;}}function secondaryNextPage(){{if(secondaryCurrentPage<Math.ceil(secondaryTableData.length/secondaryRowsPerPage)){{secondaryCurrentPage++;renderSecondaryTable();}}}}function secondaryPreviousPage(){{if(secondaryCurrentPage>1){{secondaryCurrentPage--;renderSecondaryTable();}}}}function secondaryChangeRowsPerPage(){{const s=document.getElementById("secondaryRowsPerPage");secondaryRowsPerPage=parseInt(s.value);secondaryCurrentPage=1;renderSecondaryTable();}}function openSecondaryModal(ri,mn){{const modal=document.getElementById('detailModal');if(!modal)return;modal.querySelectorAll('.modal-left .modal-section').forEach(s=>s.style.display='none');const col=modal.querySelector('.collapsible-section');if(col)col.style.display='none';document.getElementById("scoreReasonBlock").style.display="none";document.getElementById("metricContainer").style.display="none";document.getElementById("secondaryContainer").style.display="block";document.getElementById("rcaContainer").style.display="none";document.getElementById("tracebackFields").innerHTML="";document.getElementById("metricSheetFields").innerHTML="";document.getElementById("rcaContainer").innerHTML="";document.getElementById('modalTitle').textContent=mn+' - Secondary LLM Details';document.getElementById('modalSubtitle').textContent='';const ct=document.getElementById('secondaryContainer');ct.innerHTML='';const r=secondaryTableData[ri];const qk=r.query_key;const mm=secondaryMetaMap[mn.toLowerCase()]||{{}};const ml=mm[qk]||[];if(ml.length===0){{const sec=document.createElement('div');sec.className='modal-section';sec.innerHTML='<h4>No metadata</h4><p>N/A</p>';ct.appendChild(sec);}}else{{ml.forEach((mt,idx)=>{{const keys=Object.keys(mt||{{}}).filter(k=>k&&k.toLowerCase()!=='eval_name'&&k.toLowerCase()!=='trace_id');if(keys.length===0){{const sec=document.createElement('div');sec.className='modal-section';sec.innerHTML=`<h4>Row ${{idx+1}}</h4><p>N/A</p>`;ct.appendChild(sec);}}else{{keys.forEach(k=>{{let v=mt[k];const sec=document.createElement('div');sec.className='modal-section';const hd=document.createElement('h4');hd.textContent=String(k).replace(/_/g,' ');sec.appendChild(hd);const cn=document.createElement('div');if(v===null||v===undefined)cn.innerHTML='<p>N/A</p>';else if(typeof v==='object')cn.innerHTML=`<pre>${{escapeHtml(JSON.stringify(v,null,2)).replace(/\\n/g,"<br>")}}</pre>`;else cn.innerHTML=`<p>${{escapeHtml(String(v)).replace(/\\n/g,"<br>")}}</p>`;sec.appendChild(cn);ct.appendChild(sec);}});}}}});}}modal.style.display='block';}}document.addEventListener("DOMContentLoaded",renderSecondaryTable);</script>"""
    except Exception as e:
        return f"<script>console.error('Error: {e}');</script>"
''')

    print(f"\n{'='*60}")
    print("Part 2 COMPLETE: All 5 tab files created")
    print(f"{'='*60}")
    print("Next: Run build_part3.py for Templates (CSS + JS + HTML) + report_generator.py")

if __name__ == "__main__":
    build()
