"""
tabs/trustworthy_assurance.py
Trust Metric results table — loaded from eval_matric_result.xlsx.
"""

import json
import pandas as pd

try:
    from data_paths import EVAL_METRIC_RESULT_PATH
except ImportError:
    EVAL_METRIC_RESULT_PATH = None


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_trust_metrics_data():
    """
    Reads eval_matric_result.xlsx.
    Each sheet = one metric. Columns: Query, [any extra cols], score, reason …
    Pass/Fail logic: 0 = Pass, 1 = Fail.
    Returns:
        rows    – list of dicts, one per TC (TC011–TC015)
        metrics – ordered list of metric (sheet) names
    """
    if EVAL_METRIC_RESULT_PATH is None or not EVAL_METRIC_RESULT_PATH.exists():
        return [], []

    try:
        xl = pd.ExcelFile(EVAL_METRIC_RESULT_PATH)
        metrics = xl.sheet_names  # preserves sheet order

        row_map = {}  # index -> {tc_id, query, metrics: {metric_name: {...}}}

        for metric in metrics:
            df = xl.parse(metric)
            df.columns = [str(c).strip() for c in df.columns]
            # Drop any unnamed index columns Excel adds (e.g. "Unnamed: 0")
            df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]

            col_map   = {c.lower(): c for c in df.columns}
            query_col = col_map.get("query")
            score_col = col_map.get("score")

            for idx, row in df.iterrows():
                tc_id = f"TC0{11 + idx}"  # TC011 … TC015
                if idx not in row_map:
                    row_map[idx] = {
                        "tc_id":   tc_id,
                        "query":   str(row[query_col]).strip() if query_col else "",
                        "metrics": {}
                    }

                raw_score = row[score_col] if score_col else None
                try:
                    score = int(float(raw_score))
                except (TypeError, ValueError):
                    score = 0

                # 0 = Pass, 1 = Fail
                is_pass = (score == 0)

                # Capture ALL non-query, non-score columns dynamically
                extra_fields = {}
                for col in df.columns:
                    if col == query_col:
                        continue
                    if score_col and col == score_col:
                        continue          # skip score — rendered separately
                    if str(col).startswith("Unnamed:"):
                        continue          # skip unnamed index columns from Excel
                    val = row[col]
                    extra_fields[col] = "" if pd.isna(val) else str(val).strip()

                row_map[idx]["metrics"][metric] = {
                    "score":  score,
                    "result": "Pass" if is_pass else "Fail",
                    "fields": extra_fields,
                }

        rows = [row_map[k] for k in sorted(row_map.keys())]
        return rows, metrics

    except Exception as e:
        print(f"[trustworthy_assurance] load_trust_metrics_data error: {e}")
        return [], []


# ─────────────────────────────────────────────────────────────────────────────
# HTML GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_trust_metrics_table(rows, metrics, primary_color="#2E86AB"):
    """
    Generates the Trust Metric results table HTML injected into #tw_trust.
    • Paginated table: TC ID | Query | one Pass/Fail badge per metric
    • Clicking a badge opens twTrustDetailModal
    • Pass/Fail: score 0 = Pass (green), score 1 = Fail (red)
    """
    cg = primary_color

    if not rows or not metrics:
        return (
            '<div class="card"><div class="card-content" style="text-align:center;padding:60px;">'
            '<div style="font-size:3rem;opacity:0.3;">📊</div>'
            '<h4 style="color:#999;margin-top:16px;">No Trust Metric data found</h4>'
            '<p style="color:#bbb;font-size:0.9rem;">Place <code>eval_matric_result.xlsx</code> '
            'in the <code>data/</code> folder.</p>'
            '</div></div>'
        )

    data_json = json.dumps(rows, ensure_ascii=False)

    # ── Table header ─────────────────────────────────────────────────────────
    header_cells = "<th>TC ID</th><th>Query</th>"
    for m in metrics:
        header_cells += f"<th>{m}</th>"

    # ── Table rows ───────────────────────────────────────────────────────────
    body_rows = ""
    for ri, row in enumerate(rows):
        query_short = row["query"][:80] + ("…" if len(row["query"]) > 80 else "")
        cells = (
            f'<td style="font-weight:700;color:{cg};">{row["tc_id"]}</td>'
            f'<td style="max-width:280px;white-space:normal;font-size:0.85rem;">{query_short}</td>'
        )
        for m in metrics:
            mdata   = row["metrics"].get(m, {})
            result  = mdata.get("result", "Fail")
            is_pass = result == "Pass"
            badge_style = (
                "background:#e8f5e9;color:#2e7d32;border:1px solid #a5d6a7;"
                if is_pass else
                "background:#ffebee;color:#c62828;border:1px solid #ef9a9a;"
            )
            icon = "✓" if is_pass else "✗"
            cells += (
                f'<td style="text-align:center;">'
                f'<span class="tw-trust-badge" '
                f'style="display:inline-flex;align-items:center;gap:4px;'
                f'padding:5px 14px;border-radius:8px;font-weight:700;font-size:0.82rem;'
                f'cursor:pointer;{badge_style}" '
                f'onclick="openTWTrustModal({ri},\'{m}\')">'
                f'{icon} {result}</span></td>'
            )
        body_rows += f"<tr>{cells}</tr>"

    html = f"""
<script>
var TW_TRUST_DATA = {data_json};
var TW_TRUST_METRICS = {json.dumps(metrics)};
</script>

<div class="card">
  <div class="card-header" style="display:flex;justify-content:space-between;align-items:center;">
    <h3>🔒 Trust Metric Results</h3>
    <span style="font-size:0.82rem;font-weight:600;opacity:0.8;">
      {len(rows)} test case{"s" if len(rows) != 1 else ""} &nbsp;·&nbsp; {len(metrics)} metric{"s" if len(metrics) != 1 else ""}
    </span>
  </div>
  <div class="card-content" style="padding:0;">
    <div class="table-container" style="overflow-x:auto;">
      <table class="modern-table details-table" id="twTrustTable" style="width:100%;min-width:600px;">
        <thead><tr>{header_cells}</tr></thead>
        <tbody id="twTrustTableBody">{body_rows}</tbody>
      </table>
    </div>
    <div class="pagination-container" id="twTrustPagination"
         style="display:flex;justify-content:center;align-items:center;gap:8px;padding:16px;">
    </div>
  </div>
</div>

<!-- ── Trust Metric Detail Modal ─────────────────────────────────────── -->
<div id="twTrustDetailModal" class="modal" style="display:none;">
  <div class="modal-content" style="max-width:720px;border-radius:16px;overflow:hidden;">
    <div class="modal-header" style="background:linear-gradient(135deg,{cg} 0%,#1B2965 100%);padding:20px 24px;">
      <h3 class="modal-title" id="twTrustModalTitle" style="color:white;margin:0;font-size:1.1rem;"></h3>
      <button class="modal-close" onclick="closeTWTrustModal()"
              style="color:white;background:none;border:none;font-size:1.6rem;cursor:pointer;line-height:1;">×</button>
    </div>
    <div class="modal-body" style="padding:24px;overflow-y:auto;max-height:70vh;display:flex;flex-direction:column;gap:12px;">

      <!-- Result badge -->
      <div id="twTrustModalBadge"></div>

      <!-- Score (rendered once, separately) -->
      <div style="background:#f8fafc;border-radius:10px;padding:16px;border-left:4px solid {cg};">
        <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#888;margin-bottom:6px;">Score</div>
        <div id="twTrustModalScore" style="font-size:2rem;font-weight:800;"></div>
      </div>

      <!-- Query -->
      <div style="background:#f8fafc;border-radius:10px;padding:16px;border-left:4px solid #F18F01;">
        <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#888;margin-bottom:8px;">Query</div>
        <div id="twTrustModalQuery" style="font-size:0.95rem;color:#333;line-height:1.6;"></div>
      </div>

      <!-- Dynamic extra fields (everything except query & score) -->
      <div id="twTrustModalFields" style="display:flex;flex-direction:column;gap:12px;"></div>

    </div>
  </div>
</div>

<script>
(function() {{
  var ROWS_PER_PAGE = 10;
  var currentPage  = 1;

  function renderPage() {{
    var tbody = document.getElementById('twTrustTableBody');
    if (!tbody) return;
    var start = (currentPage - 1) * ROWS_PER_PAGE;
    var end   = start + ROWS_PER_PAGE;
    var rows  = tbody.querySelectorAll('tr');
    rows.forEach(function(tr, i) {{
      tr.style.display = (i >= start && i < end) ? '' : 'none';
    }});
    renderPagination(rows.length);
  }}

  function renderPagination(total) {{
    var container = document.getElementById('twTrustPagination');
    if (!container) return;
    var pages = Math.ceil(total / ROWS_PER_PAGE);
    if (pages <= 1) {{ container.style.display = 'none'; return; }}
    container.style.display = 'flex';
    var h = '';
    for (var p = 1; p <= pages; p++) {{
      var active = p === currentPage;
      h += '<button class="page-btn" onclick="twTrustGoPage(' + p + ')" '
         + 'style="padding:6px 14px;border-radius:8px;border:1px solid #e2e8f0;cursor:pointer;'
         + 'font-weight:700;font-size:0.85rem;'
         + (active ? 'background:{cg};color:white;border-color:{cg};' : 'background:white;color:#555;')
         + '">' + p + '</button>';
    }}
    container.innerHTML = h;
  }}

  window.twTrustGoPage = function(p) {{
    currentPage = p;
    renderPage();
  }};

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', renderPage);
  }} else {{
    renderPage();
  }}
}})();

/* ── Open modal ──────────────────────────────────────────────────────── */
window.openTWTrustModal = function(rowIndex, metricName) {{
  var row   = TW_TRUST_DATA[rowIndex];
  var mdata = row.metrics[metricName] || {{}};
  // 0 = Pass, 1 = Fail
  var isPass = mdata.result === 'Pass';

  document.getElementById('twTrustModalTitle').textContent =
    row.tc_id + ' \u2014 ' + metricName;

  // Badge
  document.getElementById('twTrustModalBadge').innerHTML = isPass
    ? '<span style="display:inline-flex;align-items:center;gap:6px;background:#e8f5e9;color:#2e7d32;padding:8px 20px;border-radius:10px;font-weight:800;font-size:1rem;border:1px solid #a5d6a7;">\u2713 Pass</span>'
    : '<span style="display:inline-flex;align-items:center;gap:6px;background:#ffebee;color:#c62828;padding:8px 20px;border-radius:10px;font-weight:800;font-size:1rem;border:1px solid #ef9a9a;">\u2717 Fail</span>';

  // Score
  var scoreEl = document.getElementById('twTrustModalScore');
  scoreEl.textContent = (mdata.score != null) ? mdata.score : 'N/A';
  scoreEl.style.color = isPass ? '#2e7d32' : '#c62828';

  // Query
  document.getElementById('twTrustModalQuery').textContent = row.query || 'N/A';

  // Extra fields (no score column — already excluded in Python)
  var BORDER_COLORS = ['#6c757d','#A23B72','#F18F01','#2E86AB','#28a745','#6f42c1'];
  var fieldsEl = document.getElementById('twTrustModalFields');
  fieldsEl.innerHTML = '';
  Object.entries(mdata.fields || {{}}).forEach(function(entry, idx) {{
    var key = entry[0], val = entry[1];
    var displayVal = (val === '' || val == null) ? 'N/A' : val;
    var border = BORDER_COLORS[idx % BORDER_COLORS.length];
    var escaped = displayVal.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    fieldsEl.innerHTML +=
      '<div style="background:#f8fafc;border-radius:10px;padding:16px;border-left:4px solid ' + border + ';">'
      + '<div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;'
      + 'letter-spacing:0.6px;color:#888;margin-bottom:8px;">' + key.replace(/_/g,' ') + '</div>'
      + '<div style="font-size:0.9rem;color:#444;line-height:1.6;white-space:pre-wrap;">' + escaped + '</div>'
      + '</div>';
  }});

  document.getElementById('twTrustDetailModal').style.display = 'block';
}};

window.closeTWTrustModal = function() {{
  document.getElementById('twTrustDetailModal').style.display = 'none';
}};

document.getElementById('twTrustDetailModal').addEventListener('click', function(e) {{
  if (e.target === this) closeTWTrustModal();
}});
</script>
""".replace("{cg}", cg)

    return html