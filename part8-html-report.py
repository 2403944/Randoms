#!/usr/bin/env python3
"""
Part 8: Master HTML Assembly (fully self-contained) + Final updates
Run: python build_part8.py

After this, NO original file is needed. The project is 100% standalone.
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
    print(f"Part 8: Master HTML assembly + final updates in ./{BASE}/\n")

    # ==================== templates/html_report.py ====================
    # This is the master function that assembles the ENTIRE HTML page.
    # Fully self-contained - NO dependency on original file.
    w("templates/html_report.py", r'''"""
Master HTML Report Assembly - FULLY SELF-CONTAINED.
No dependency on report_generator_original.py.

This module assembles the complete HTML report by calling all
separated template generators and combining them into one page.
"""
import json

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from templates.css_styles import get_modern_css
from templates.html_modal import get_modern_modal
from templates.js_pipeline import get_pipeline_javascript
from templates.js_disaggregated import get_disagg_js
from templates.js_upload_runs import get_upload_runs_js
from templates.js_tw_usecase import get_tw_usecase_js
from templates.js_tw_bias import get_tw_bias_eval_js
from templates.js_tw_explain_trust import get_tw_explain_trust_eval_js
from tabs.metrics_summary import generate_metrics_summary_table
from tabs.data_assurance import generate_augmentation_pipeline_html, generate_golden_dataset_html, get_coverage_edit_data
from tabs.model_quality_assurance import generate_interactive_details_table, load_recovery_loop_global
from tabs.mqa_evaluations_wizard import generate_evaluations_wizard_html
from tabs.secondary_llm import generate_secondary_llm_table
from techniques_loader import ALL_AUGMENTATION_TECHNIQUES


def generate_modern_html(config, report_timestamp, metrics_df, details_df,
                         all_metrics, charts, modal_data, metric_details_excel_path):
    """Assemble the complete HTML report page. Fully self-contained."""
    try:
        # 1. Generate all component pieces
        css = get_modern_css(config)
        metrics_table = generate_metrics_summary_table(metrics_df, config)
        pipeline_html = generate_augmentation_pipeline_html()
        golden_html = generate_golden_dataset_html()
        eval_wizard = generate_evaluations_wizard_html(all_metrics)
        details_table = generate_interactive_details_table(details_df, all_metrics)
        secondary_table = generate_secondary_llm_table(details_df, all_metrics)
        modal_html = get_modern_modal()

        # 2. Generate all JS templates
        pipeline_js = get_pipeline_javascript(ALL_AUGMENTATION_TECHNIQUES)
        upload_runs_js = get_upload_runs_js()
        disagg_js = get_disagg_js()
        tw_usecase_js = get_tw_usecase_js()
        tw_bias_js = get_tw_bias_eval_js()
        tw_explain_trust_js = get_tw_explain_trust_eval_js()

        # 3. Prepare JSON data for inline script
        recovery_global_data = load_recovery_loop_global(metric_details_excel_path)
        coverage_edit_data = get_coverage_edit_data()
        modal_data_json = json.dumps(modal_data, default=str)
        config_json = json.dumps(config, default=str)
        recovery_json = json.dumps(recovery_global_data, default=str)
        coverage_json = json.dumps(coverage_edit_data, default=str)

        metrics_count = metrics_df['Metrics'].notna().sum() if 'Metrics' in metrics_df.columns else 0
        all_metrics_clean = [str(m).strip() for m in all_metrics]
        theme = config['theme']

        # 4. Build the inline script (JS with Python data injected)
        inline_script = _build_inline_script(modal_data_json, config_json, recovery_json, coverage_json)

        # 5. Build custom augmentation modal HTML
        custom_aug_modal = _build_custom_aug_modal()

        # 6. Build trustworthy tab HTML
        tw_html = _build_trustworthy_tabs()

        # 7. Assemble the full page
        title = config['title']
        subtitle = config['subtitle']
        description = config['description']

        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><style>{css}</style><script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head><body>
<div class="container">
<div class="report-header"><div class="report-timestamp">Generated: {report_timestamp}</div><h1 class="report-title">{title}</h1><h2 class="report-subtitle">{subtitle}</h2><p class="report-description">{description}</p></div>
<nav class="tab-navigation"><button class="tab-button active" onclick="showTab('metrics', event)">Metrics Summary ({metrics_count})</button><button class="tab-button" onclick="showTab('analytics', event)">Data Assurance</button><button class="tab-button" onclick="showTab('details', event)">Model Quality Assurance</button><button class="tab-button" onclick="showTab('trustworthy', event)">Trustworthy Assurance</button><button class="tab-button" onclick="showTab('secondary_llm', event)">Secondary LLM</button></nav>
<div id="trustworthy_subtabs" style="display:none;flex-direction:row;gap:4px;border-bottom:2px solid #e2e8f0;margin-bottom:8px;padding:0 8px;width:fit-content;"><button id="tw-btn-usecase" onclick="showTWTab('tw_usecase')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #2E86AB;color:#2E86AB;border-radius:10px 10px 0 0;">Usecase Assessment</button><button id="tw-btn-bias-func" onclick="showTWTab('tw_bias_func')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Bias Evaluation</button><button id="tw-btn-explain" onclick="showTWTab('tw_explain')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Explainability</button><button id="tw-btn-trust" onclick="showTWTab('tw_trust')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Trust Metric</button></div>
<div id="analytics_subtabs" style="display:none;flex-direction:row;gap:4px;border-bottom:2px solid #e2e8f0;margin-bottom:8px;padding:0 8px;width:fit-content;"><button id="da-btn-augmentation" onclick="showDATab('analytics_augmentation')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #2E86AB;color:#2E86AB;">Augmentation</button><button id="da-btn-analytics" onclick="showDATab('analytics_analytics')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Analytics Dashboard</button></div>
<div id="augmentation_subtabs" style="display:none;flex-direction:row;gap:4px;border-bottom:2px solid #e2e8f0;margin-bottom:8px;margin-left:20px;margin-right:20px;padding:0 8px;width:fit-content;"><button id="aug-btn-pipeline" onclick="showAugSubTab('aug_pipeline')" style="padding:8px 18px;font-size:0.84rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #F18F01;color:#F18F01;">Augmentation Pipeline</button><button id="aug-btn-golden" onclick="showAugSubTab('aug_golden')" style="padding:8px 18px;font-size:0.84rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Golden Dataset</button></div>
<div id="details_subtabs" style="display:none;flex-direction:row;gap:4px;border-bottom:2px solid #e2e8f0;margin-bottom:8px;padding:0 8px;width:fit-content;"><button id="mqa-btn-evaluations" onclick="showMQATab('details_evaluations')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #2E86AB;color:#2E86AB;">Evaluations</button><button id="mqa-btn-analytics" onclick="showMQATab('details_analytics')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Analytics</button><button id="mqa-btn-results" onclick="showMQATab('details_results')" style="padding:10px 22px;font-size:0.88rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Results</button></div>
<main>
<div id="metrics" class="tab-content active"><div class="card"><div class="card-content">{metrics_table}</div></div></div>
<div id="analytics" class="tab-content"><div id="analytics_augmentation" class="sub-tab-content active"><div id="aug_pipeline" style="display:block;">{pipeline_html}</div><div id="aug_golden" style="display:none;">{golden_html}</div></div><div id="analytics_analytics" class="sub-tab-content"><div class="card"><div class="card-header" style="display:flex;justify-content:space-between;align-items:center;"><h3>Data Coverage</h3><select id="coverageViewSelect" onchange="loadPipelineCoverage()" style="padding:6px 12px;border:2px solid rgba(255,255,255,0.5);border-radius:6px;font-size:0.82rem;font-weight:600;color:white;cursor:pointer;background:rgba(255,255,255,0.15);"><option value="nonagentic" style="color:#333;">Non-Agentic</option><option value="agentic" style="color:#333;">Agentic</option></select></div><div class="card-content"><div id="pipelineCoverageTable"><p style="color:#888;text-align:center;padding:40px;">No coverage plan yet.</p></div></div></div></div></div>
<div id="details" class="tab-content"><div id="details_evaluations" class="sub-tab-content" style="display:block;">{eval_wizard}</div><div id="details_analytics" class="sub-tab-content" style="display:none;"><div class="charts-grid"><div class="chart-card"><div class="card-header"><h3>Overall Performance</h3></div><div class="card-content">{charts.get('overall','')}</div></div><div class="chart-card"><div class="card-header"><h3>Score vs Threshold</h3></div><div class="card-content"><div style="overflow-x:auto;">{charts.get('comparison','')}</div></div></div><div class="chart-card full-width"><div class="card-header"><h3>Metrics by Status</h3></div><div class="card-content"><div style="overflow-x:auto;">{charts.get('metrics','')}</div></div></div><div class="chart-card full-width"><div class="card-header"><h3>Run Comparison</h3></div><div class="card-content"><input type="file" id="prevRun"><input type="file" id="currRun"><br><br><button onclick="uploadRuns()">Compare Runs</button><div id="runComparisonResult" style="margin-top:20px;"><i>Upload files to compare</i></div></div></div><div class="chart-card full-width"><div class="card-content">{charts.get('disaggregated','')}</div></div></div></div><div id="details_results" class="sub-tab-content" style="display:none;"><div class="card-content p-0">{details_table}</div></div></div>
<div id="trustworthy" class="tab-content">{tw_html}</div>
<div id="secondary_llm" class="tab-content"><div class="card-content">{secondary_table}</div></div>
</main></div>
{modal_html}
<div id="coverageEditModal" class="modal"><div class="modal-content" style="max-width:900px;"><div class="modal-header"><h3>Edit Data Coverage</h3><button class="modal-close" onclick="closeCoverageEdit()">\u00d7</button></div><div class="modal-body" style="padding:25px;overflow-y:auto;flex-direction:column;"><div id="coverageEditTableWrapper"></div></div></div></div>
{custom_aug_modal}
{inline_script}
{pipeline_js}
<script>var _fns=['handleFileDrop','handleFileUpload','handleAgenticBulkUpload','goToWizardStep','addCoverageRow','updateCoverageTotal','saveCoveragePlan','toggleAugDropdown','toggleInputSelection','addSelectedTechnique','onTechCategoryChange','onTechSubCatChange','removeTech','setTechVariation','performAugmentation','setPreviewMode','switchDiffTechnique','renderReviewTable','downloadAugmented','saveAsGolden','loadGoldenDataset','downloadGoldenDataset','loadPipelineCoverage','openCustomAugModal','closeCustomAugModal','setCustomAugType','addFewShotRow','addCustomTechnique','addAgenticInputRow','saveAgenticConfig','renderAugResultPreview','renderUploadPreview','populateInputDropdown','populateTechCategories','updateAugmentBtn','renderTechChips','renderVariationCounts','renderInputChips','runCoverageCheck','computeWordDiff','loadAgenticCoverage','escapeHtmlPipe','csvEscape'];_fns.forEach(function(fn){{if(typeof window[fn]==='undefined')window[fn]=function(){{console.error('PIPELINE ERROR: '+fn+' not loaded.');}};}});</script>
{upload_runs_js}
{disagg_js}
{tw_usecase_js}
{tw_bias_js}
{tw_explain_trust_js}
</body></html>"""
        return html
    except Exception as e:
        logger.error(f"Error in HTML generation: {e}")
        import traceback
        traceback.print_exc()
        return f"""<!DOCTYPE html><html><body style="font-family:Arial;padding:40px;text-align:center;"><h1 style="color:#dc3545;">Report Generation Error</h1><p>{str(e)}</p></body></html>"""


def _build_inline_script(modal_data_json, config_json, recovery_json, coverage_json):
    """Build the inline <script> block with Python data injected into JS."""
    # Python data injection (these are the ONLY f-string interpolations)
    data_block = f"""<script>
const modalData={modal_data_json};
const config={config_json};
const RECOVERY_GLOBAL={recovery_json};
const COVERAGE_EDIT_DATA={coverage_json};
"""
    # Pure JavaScript functions (no Python interpolation needed - use regular string)
    js_functions = r"""
function showTab(n,e){document.querySelectorAll('.tab-content').forEach(t=>{t.classList.remove('active');t.style.display='none';});document.querySelectorAll('.tab-button').forEach(b=>b.classList.remove('active'));var s=document.getElementById(n);if(s){s.classList.add('active');s.style.display='block';}if(e&&e.target)e.target.classList.add('active');['analytics_subtabs','details_subtabs','trustworthy_subtabs','augmentation_subtabs'].forEach(id=>{var el=document.getElementById(id);if(el)el.style.display='none';});var as=document.getElementById('analytics_subtabs');var ds=document.getElementById('details_subtabs');var ts=document.getElementById('trustworthy_subtabs');if(as)as.style.display=n==='analytics'?'flex':'none';if(ds)ds.style.display=n==='details'?'flex':'none';if(ts)ts.style.display=n==='trustworthy'?'flex':'none';if(n==='analytics')showDATab('analytics_augmentation');if(n==='details')showMQATab('details_evaluations');if(n==='trustworthy')showTWTab('tw_usecase');}
function showDATab(n){['analytics_augmentation','analytics_analytics'].forEach(id=>{var el=document.getElementById(id);if(el){el.style.display=id===n?'block':'none';el.classList.toggle('active',id===n);}});document.getElementById('da-btn-augmentation').style.borderBottomColor=n==='analytics_augmentation'?'#2E86AB':'transparent';document.getElementById('da-btn-augmentation').style.color=n==='analytics_augmentation'?'#2E86AB':'#718096';document.getElementById('da-btn-analytics').style.borderBottomColor=n==='analytics_analytics'?'#2E86AB':'transparent';document.getElementById('da-btn-analytics').style.color=n==='analytics_analytics'?'#2E86AB':'#718096';var as=document.getElementById('augmentation_subtabs');if(n==='analytics_augmentation'){as.style.display='flex';showAugSubTab('aug_pipeline');}else as.style.display='none';if(n==='analytics_analytics')loadPipelineCoverage();}
function showAugSubTab(n){['aug_pipeline','aug_golden'].forEach(function(id,i){var el=document.getElementById(id);var btn=document.getElementById(['aug-btn-pipeline','aug-btn-golden'][i]);if(el)el.style.display=id===n?'block':'none';if(btn){btn.style.borderBottomColor=id===n?'#F18F01':'transparent';btn.style.color=id===n?'#F18F01':'#718096';}});if(n==='aug_golden')loadGoldenDataset();}
function showMQATab(n){['details_evaluations','details_analytics','details_results'].forEach(id=>{var el=document.getElementById(id);if(el){el.style.cssText=id===n?'display:block !important;':'display:none !important;';}});var bm={'details_evaluations':'mqa-btn-evaluations','details_analytics':'mqa-btn-analytics','details_results':'mqa-btn-results'};Object.keys(bm).forEach(function(t){var b=document.getElementById(bm[t]);if(b){b.style.borderBottomColor=t===n?'#2E86AB':'transparent';b.style.color=t===n?'#2E86AB':'#718096';}});}
function showTWTab(n){var tabs=['tw_usecase','tw_bias_func','tw_explain','tw_trust'];var btns=['tw-btn-usecase','tw-btn-bias-func','tw-btn-explain','tw-btn-trust'];for(var i=0;i<tabs.length;i++){var el=document.getElementById(tabs[i]);var btn=document.getElementById(btns[i]);if(el)el.style.cssText=tabs[i]===n?'display:block !important;':'display:none !important;';if(btn){btn.style.borderBottomColor=tabs[i]===n?'#2E86AB':'transparent';btn.style.color=tabs[i]===n?'#2E86AB':'#718096';}}if(n==='tw_bias_func')showTWBiasSubTab('twBiasUpload');else if(n==='tw_explain'){var es=document.getElementById('twExplainSubTabs');if(es)es.style.display='flex';showTWExplainSubTab('twExplainUpload');}else if(n==='tw_trust'){var ts=document.getElementById('twTrustSubTabs');if(ts)ts.style.display='flex';showTWTrustSubTab('twTrustUpload');}}
function closeModal(){var m=document.getElementById('detailModal');if(m)m.style.display='none';}
function closeRcaOutput(){document.getElementById("rcaOutputModal").style.display="none";}
function closeCustomAugModal(){var m=document.getElementById('customAugModal');if(m)m.style.display='none';}
function closeCoverageEdit(){document.getElementById('coverageEditModal').style.display='none';}
function toggleCollapsible(s){var c=document.getElementById(s+"Content");var ic=document.getElementById(s+"Icon");if(!c||!ic)return;if(c.classList.contains("collapsed")){c.classList.remove("collapsed");ic.classList.add("expanded");}else{c.classList.add("collapsed");ic.classList.remove("expanded");}}
function escapeHtml(s){if(s===null||s===undefined)return'';return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
function openModal(ri,mn){document.querySelectorAll(".modal-left .modal-section").forEach(el=>el.style.display="block");document.getElementById("scoreReasonBlock").style.display="block";document.querySelector(".collapsible-section").style.display="block";document.getElementById("rcaContainer").style.display="none";document.getElementById("secondaryContainer").style.display="none";document.getElementById("metricContainer").style.display="block";document.getElementById("secondaryContainer").innerHTML="";document.getElementById("rcaContainer").innerHTML="";const modal=document.getElementById('detailModal');if(!modal||!modalData[ri])return;const data=modalData[ri];const md=data.metrics[mn]||{};const msd=data.metric_fields?.[mn]||{};const ml=modal.querySelector('.modal-left');if(ml)ml.scrollTop=0;const rc=document.getElementById('responseContent');const ri2=document.getElementById('responseIcon');if(rc&&ri2){rc.classList.add('collapsed');ri2.classList.remove('expanded');}const ue=(id,c)=>{const el=document.getElementById(id);if(!el)return;el.innerHTML=(c===null||c===undefined||c==='')?'N/A':c;};ue('modalTitle',mn.replace(/_/g,' ').toUpperCase());ue('modalSubtitle','Threshold: '+(md.threshold||'N/A'));ue('modalQuestion',data.query);ue('modalResponse',data.response);function parseVal(v){if(v==null)return v;let cur=v;for(let i=0;i<10;i++){if(typeof cur!=='string')break;let s=cur.trim();if((s.startsWith('"')&&s.endsWith('"'))||(s.startsWith("'")&&s.endsWith("'")))s=s.slice(1,-1);if(s.includes('""'))s=s.replace(/""/g,'"');try{const p=JSON.parse(s);if(p===cur)break;cur=p;}catch{break;}}return cur;}
function stripHtml(v){if(typeof v!=='string')return v;const d=document.createElement('div');d.innerHTML=v;return d.textContent||d.innerText||'';}
function renderStatus(v){if(v==null)return'N/A';const t=String(v).toLowerCase().trim();if(t==='pass'||t==='passed'){const b=document.createElement('span');b.className='tb-badge tb-pass';b.innerHTML='\u2714 Pass';return b;}if(t==='fail'||t==='failed'){const b=document.createElement('span');b.className='tb-badge tb-fail';b.innerHTML='\u2716 Fail';return b;}return stripHtml(v);}
let uniqueTracebacks=[];const tracebackContainer=document.getElementById('tracebackFields');if(tracebackContainer)tracebackContainer.innerHTML='';
if(tracebackContainer){let tbRows=Array.isArray(msd)?msd:(msd&&typeof msd==='object'?[msd]:[]);if(tbRows.length>0){const TRACE_KEYS=Object.keys(tbRows[0]).filter(k=>['traceback','tracebacks'].includes(k.toLowerCase()));if(TRACE_KEYS.length>0){tbRows.forEach(row=>{const obj={};TRACE_KEYS.forEach(k=>obj[k]=row[k]);const s=JSON.stringify(obj);if(!uniqueTracebacks.some(u=>JSON.stringify(u)===s))uniqueTracebacks.push(obj);});function flattenObject(obj,prefix=''){const result={};Object.entries(obj).forEach(([key,value])=>{const fullKey=prefix?prefix+'.'+key:key;if(value&&typeof value==='object'&&!Array.isArray(value))Object.assign(result,flattenObject(value,fullKey));else result[fullKey]=value;});return result;}function createTracebackTable(data){const table=document.createElement('table');table.className='metric-table';let allKeys=new Set(),flattened=[];if(Array.isArray(data)){data.forEach(item=>{const f=flattenObject(item);flattened.push(f);Object.keys(f).forEach(k=>allKeys.add(k));});}else{const f=flattenObject(data);flattened.push(f);allKeys=new Set(Object.keys(f));}const keys=Array.from(allKeys);const thead=document.createElement('thead');const trH=document.createElement('tr');keys.forEach(k=>{const th=document.createElement('th');th.textContent=k.replace(/_/g,' ');trH.appendChild(th);});thead.appendChild(trH);table.appendChild(thead);const tbody=document.createElement('tbody');flattened.forEach(row=>{const tr=document.createElement('tr');keys.forEach(k=>{const td=document.createElement('td');const val=row[k];const rendered=renderStatus(val);if(rendered instanceof HTMLElement)td.appendChild(rendered);else td.textContent=rendered||'N/A';tr.appendChild(td);});tbody.appendChild(tr);});table.appendChild(tbody);return table;}uniqueTracebacks.forEach(row=>{TRACE_KEYS.forEach(h=>{const val=parseVal(row[h]);if(val==null)return;if(Array.isArray(val)&&val.length>0&&val[0]&&typeof val[0]==='object'){tracebackContainer.appendChild(createTracebackTable(val));return;}if(val&&typeof val==='object'){tracebackContainer.appendChild(createTracebackTable(val));return;}});});}}}
const tbSection=document.getElementById('tracebackFields')?.closest('.collapsible-section');if(tracebackContainer&&(!tracebackContainer.children.length||tracebackContainer.textContent.trim()===''||tracebackContainer.textContent.trim()==='N/A')){if(tbSection)tbSection.style.display='none';}else{if(tbSection)tbSection.style.display='';}
const metricFieldsContainer=document.getElementById('metricSheetFields');if(metricFieldsContainer){metricFieldsContainer.innerHTML='';let rows=Array.isArray(msd)?msd:(msd&&typeof msd==='object'?[msd]:[]);if(rows.length===0){metricFieldsContainer.innerHTML='<p>N/A</p>';}else{if(mn==="Hallucination CoVe")rows=rows.map(r=>{const c={...r};delete c["Actual Output"];return c;});function normalizeVal(v){if(v===null||v===undefined)return'';if(typeof v==='string')return v.replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim().toLowerCase();return JSON.stringify(v);}if(rows.length>1){const excludeKeys=new Set(['query','response','score','overall reason','overall_reason','overall score','overall_score','eval_name','timestamp','traceback','tracebacks']);const allHeaders=Object.keys(rows[0]).filter(k=>!excludeKeys.has(k.toLowerCase()));const constantCols=[],variableCols=[];allHeaders.forEach(col=>{const firstVal=normalizeVal(rows[0][col]);const same=rows.every(r=>normalizeVal(r[col])===firstVal);const textLength=rows[0][col]?String(rows[0][col]).length:0;if((same&&textLength>=80)||col.toLowerCase().startsWith("overall"))constantCols.push(col);else variableCols.push(col);});constantCols.forEach((col,index)=>{const sId="constant_"+index;const wrapper=document.createElement('div');wrapper.className='collapsible-section';const header=document.createElement('div');header.className='collapsible-header';header.setAttribute("onclick",`toggleCollapsible('${sId}')`);const title=document.createElement('h4');title.textContent=col.replace(/_/g,' ');const icon=document.createElement('span');icon.className='toggle-icon';icon.id=sId+"Icon";icon.textContent="\u25bc";header.appendChild(title);header.appendChild(icon);const cw=document.createElement('div');cw.className='collapsible-content collapsed';cw.id=sId+"Content";const cv=document.createElement('div');const v=rows[0][col];cv.innerHTML=(v===null||v===undefined||String(v).toLowerCase()==='nan')?'N/A':String(v).replace(/\n/g,"<br>");cw.appendChild(cv);wrapper.appendChild(header);wrapper.appendChild(cw);metricFieldsContainer.appendChild(wrapper);});function buildTable(cols){const table=document.createElement('table');table.className='metric-table';const thead=document.createElement('thead');const trH=document.createElement('tr');cols.forEach(col=>{const th=document.createElement('th');th.textContent=col.replace(/_/g,' ');trH.appendChild(th);});thead.appendChild(trH);table.appendChild(thead);const tbody=document.createElement('tbody');rows.forEach(row=>{const tr=document.createElement('tr');cols.forEach(col=>{const td=document.createElement('td');const v=row[col];if(v===null||v===undefined||String(v).toLowerCase()==='nan')td.innerHTML='N/A';else{const r=renderStatus(v);if(r instanceof HTMLElement)td.appendChild(r);else td.innerHTML=String(r).replace(/\n/g,"<br>");}tr.appendChild(td);});tbody.appendChild(tr);});table.appendChild(tbody);return table;}if(variableCols.length>0)metricFieldsContainer.appendChild(buildTable(variableCols));}else{const record=rows[0];const excludeKeys=new Set(['query','response','score','overall reason','overall_reason','overall score','overall_score','eval_name','timestamp','traceback','tracebacks']);const trajSections=[],normSections=[];Object.entries(record).forEach(([key,value])=>{if(excludeKeys.has(key.toLowerCase()))return;if(value===null||value===undefined||String(value).trim()===''||String(value).toLowerCase()==='nan')return;const section=document.createElement('div');section.className='modal-section';const heading=document.createElement('h4');heading.textContent=key.replace(/_/g,' ');section.appendChild(heading);const content=document.createElement('div');const rendered=renderStatus(value);if(rendered instanceof HTMLElement)content.appendChild(rendered);else content.innerHTML=String(rendered).replace(/\n/g,"<br>");section.appendChild(content);if(key.toLowerCase().includes("expected")||key.toLowerCase().includes("actual"))trajSections.push(section);else normSections.push(section);});if(trajSections.length>0){const wrapper=document.createElement('div');wrapper.className='trajectory-wrapper';trajSections.forEach(sec=>wrapper.appendChild(sec));metricFieldsContainer.appendChild(wrapper);}normSections.forEach(sec=>metricFieldsContainer.appendChild(sec));if(!metricFieldsContainer.hasChildNodes())metricFieldsContainer.innerHTML='<p></p>';}}requestAnimationFrame(()=>{const mfC=document.getElementById('metricSheetFields');if(!mfC)return;const mfSection=mfC.closest('.collapsible-section');const hasReal=mfC.querySelector('table,.modal-section');if(!hasReal){if(mfSection)mfSection.style.display='none';}else{if(mfSection)mfSection.style.display='';}});}
ue('modalReason',md.additional_fields?.reason||'No reason provided');
var existingGlobal=document.getElementById('recoveryGlobalSection');if(existingGlobal)existingGlobal.remove();
if(mn.toLowerCase().startsWith('recovery')&&RECOVERY_GLOBAL&&RECOVERY_GLOBAL.length>0){var gs=document.createElement('div');gs.id='recoveryGlobalSection';gs.className='collapsible-section';gs.style.marginTop='20px';var gh=document.createElement('div');gh.className='collapsible-header';gh.innerHTML='<h4>\ud83c\udf10 Recovery Loop Global</h4><span class="toggle-icon expanded" id="recoveryGlobalIcon">\u25bc</span>';gh.onclick=function(){toggleCollapsible('recoveryGlobal');};gs.appendChild(gh);var gc=document.createElement('div');gc.className='collapsible-content';gc.id='recoveryGlobalContent';var cols=Object.keys(RECOVERY_GLOBAL[0]);var tHtml='<table class="metric-table" style="margin-top:10px;"><thead><tr>';cols.forEach(function(c){tHtml+='<th>'+c.replace(/_/g,' ')+'</th>';});tHtml+='</tr></thead><tbody>';RECOVERY_GLOBAL.forEach(function(row){tHtml+='<tr>';cols.forEach(function(c){var v=row[c];tHtml+='<td>'+(v===null||v===undefined?'N/A':escapeHtml(String(v)))+'</td>';});tHtml+='</tr>';});tHtml+='</tbody></table>';gc.innerHTML=tHtml;gs.appendChild(gc);var mfSection=document.getElementById('metricSheetFields')?.closest('.collapsible-section');if(mfSection&&mfSection.parentNode)mfSection.parentNode.insertBefore(gs,mfSection.nextSibling);else document.querySelector('.modal-left').appendChild(gs);}
const se=document.getElementById('scorePieChart');if(se)se.innerHTML='';if(md.score&&md.score!='N/A'&&md.threshold&&md.threshold!='N/A')createScorePieChart(parseFloat(md.score),parseFloat(md.threshold),mn);modal.style.display='block';}
function createScorePieChart(sc,th,m){if(isNaN(sc)||isNaN(th))return;const rem=Math.max(0,1-sc);const ir=config.reverse_metrics?.includes(m)||false;const ip=ir?sc<=th:sc>=th;const pc=config.status_colors?.passed||'#28a745';const fc=config.status_colors?.failed||'#dc3545';try{Plotly.newPlot('scorePieChart',[{values:[sc,rem],labels:['Score','Remaining'],type:'pie',hole:0.4,marker:{colors:[ip?pc:fc,'#f0f0f0']},textinfo:'none'}],{showlegend:false,margin:{t:20,b:20,l:20,r:20},height:160,width:160,autosize:false,annotations:[{text:sc.toFixed(2)+'<br>'+(ip?'PASS':'FAIL'),x:0.5,y:0.5,font:{size:14,color:ip?pc:fc},showarrow:false}],plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'},{displayModeBar:false});}catch(e){}}
window.addEventListener('click',function(e){if(e.target===document.getElementById('detailModal'))closeModal();if(e.target===document.getElementById('coverageEditModal'))closeCoverageEdit();if(e.target===document.getElementById('customAugModal'))closeCustomAugModal();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeModal();closeCustomAugModal();}});
"""
    return data_block + js_functions + "</script>"


def _build_custom_aug_modal():
    """Build the custom augmentation modal HTML."""
    return """<div id="customAugModal" class="modal"><div class="modal-content" style="max-width:750px;"><div class="modal-header" style="background:linear-gradient(135deg,#A23B72 0%,#2E86AB 100%);"><h3 class="modal-title">Custom Augmentation</h3><button class="modal-close" onclick="closeCustomAugModal()">\u00d7</button></div><div class="modal-body" style="padding:25px;overflow-y:auto;flex-direction:column;max-height:70vh;">
<div style="display:flex;gap:10px;margin-bottom:20px;"><button id="customTypeNormal" onclick="setCustomAugType('normal')" style="flex:1;padding:12px;border:2px solid #2E86AB;border-radius:8px;font-weight:700;cursor:pointer;background:rgba(46,134,171,0.06);color:#2E86AB;">Normal Augmentation</button><button id="customTypeAgentic" onclick="setCustomAugType('agentic')" style="flex:1;padding:12px;border:2px solid #e2e8f0;border-radius:8px;font-weight:700;cursor:pointer;background:white;color:#718096;">Agentic Augmentation</button></div>
<div id="customNormalFields"><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;"><div><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Category *</label><input type="text" id="customCategory" placeholder="e.g., Linguistic" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;"></div><div><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Sub-category</label><input type="text" id="customSubCat" placeholder="e.g., Word Level" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;"></div></div><div style="margin-bottom:16px;"><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Technique Name *</label><input type="text" id="customName" placeholder="e.g., Slang Replacement" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;"></div><div style="margin-bottom:16px;"><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Description / Prompt</label><textarea id="customDesc" placeholder="Describe the augmentation..." rows="3" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;resize:vertical;"></textarea></div><div style="margin-bottom:16px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><label style="font-size:0.85rem;color:#555;font-weight:600;">Few-shot Examples</label><button class="btn btn-secondary" onclick="addFewShotRow()" style="padding:5px 14px;font-size:0.82rem;">+ Add</button></div><div id="fewShotExamples"></div></div><button class="btn btn-primary" onclick="addCustomTechnique()" style="width:100%;padding:12px;">+ Add Custom Technique</button></div>
<div id="customAgenticFields" style="display:none;"><div style="padding:12px 16px;background:#f8f0fc;border:1px solid #e2d0f0;border-radius:8px;margin-bottom:16px;font-size:0.85rem;color:#555;"><strong style="color:#A23B72;">How it works:</strong> Provide your agent specs and inputs. When you click "Run Augmentation", the LLM will generate 3 natural-language variations per input: <span style="color:#28a745;font-weight:600;">Positive</span>, <span style="color:#dc3545;font-weight:600;">Negative</span>, <span style="color:#F18F01;font-weight:600;">Edge</span>.</div><div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;padding:12px 16px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;"><div style="flex:1;"><div style="font-weight:600;font-size:0.9rem;color:#333;margin-bottom:2px;">Bulk Upload</div><div style="font-size:0.78rem;color:#888;">Upload an Excel/CSV with columns: <strong>Agent Name</strong>, <strong>SPEC</strong>, <strong>Input</strong></div></div><button class="btn btn-secondary" onclick="document.getElementById('agenticBulkFile').click();" style="border:2px solid #A23B72;color:#A23B72;font-weight:700;padding:8px 18px;white-space:nowrap;">Upload File</button><input type="file" id="agenticBulkFile" accept=".csv,.xlsx,.xls" style="display:none;" onchange="handleAgenticBulkUpload(this)"></div><div id="agenticBulkStatus" style="margin-bottom:12px;"></div>
<div style="display:flex;align-items:center;gap:16px;margin:20px 0;"><hr style="flex:1;border:none;border-top:1px solid #e2e8f0;"><span style="font-weight:700;color:#A23B72;font-size:0.9rem;padding:0 8px;background:white;">OR</span><hr style="flex:1;border:none;border-top:1px solid #e2e8f0;"></div>
<div style="margin-bottom:16px;"><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Agent Name *</label><input type="text" id="agenticAgentName" placeholder="e.g., Logistics Planner Agent" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;" oninput="checkAgenticSaveReady()"></div><div style="margin-bottom:16px;"><label style="font-size:0.85rem;color:#555;font-weight:600;display:block;margin-bottom:4px;">Agent Specification *</label><textarea id="agenticAgentSpec" placeholder="Paste the full agent specification here..." rows="5" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:8px;resize:vertical;" oninput="checkAgenticSaveReady()"></textarea></div><div style="margin-bottom:16px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><label style="font-size:0.85rem;color:#555;font-weight:600;">Inputs</label><button class="btn btn-secondary" onclick="addAgenticInputRow()" style="padding:5px 14px;font-size:0.82rem;">+ Add Input</button></div><div id="agenticInputRows"></div></div>
<button class="btn btn-primary" id="agenticSaveBtn" onclick="saveAgenticConfig()" disabled style="width:100%;padding:12px;font-size:1rem;background:linear-gradient(135deg,#A23B72,#2E86AB);">Save Agentic Configuration</button>
<div id="agenticStatus" style="margin-top:12px;"></div></div>
</div></div></div>"""


def _build_trustworthy_tabs():
    """Build the entire Trustworthy Assurance tab HTML structure."""
    # This is the TW tab HTML with all sub-tabs for usecase, bias, explainability, trust
    return """<div id="tw_usecase" class="sub-tab-content" style="display:block;">
<div class="card"><div class="card-header"><h3>Usecase Assessment & Metric Suggestion</h3></div><div class="card-content">
<div id="twUsecaseForm">
<p style="color:#555;margin-bottom:20px;">Answer the following questions about your usecase to receive tailored Bias, Explainability, and Trustworthy metric recommendations.</p>
<div style="margin-bottom:20px;"><label style="font-weight:600;display:block;margin-bottom:6px;color:#333;">1. What does your AI system do? Describe the usecase in detail.</label><textarea id="twUcDesc" rows="3" placeholder="e.g., An AI-powered logistics planner..." style="width:100%;padding:12px;border:1px solid #ccc;border-radius:8px;font-size:0.9rem;resize:vertical;"></textarea></div>
<div style="margin-bottom:20px;"><label style="font-weight:600;display:block;margin-bottom:6px;color:#333;">2. Who are the primary end users?</label><textarea id="twUcUsers" rows="2" placeholder="e.g., Supply chain managers..." style="width:100%;padding:12px;border:1px solid #ccc;border-radius:8px;font-size:0.9rem;resize:vertical;"></textarea></div>
<div style="margin-bottom:20px;"><label style="font-weight:600;display:block;margin-bottom:6px;color:#333;">3. Targeted age group?</label><textarea id="twUcAge" rows="1" placeholder="e.g., 25-55" style="width:100%;padding:12px;border:1px solid #ccc;border-radius:8px;font-size:0.9rem;resize:vertical;"></textarea></div>
<div style="margin-bottom:24px;"><label style="font-weight:600;display:block;margin-bottom:6px;color:#333;">4. Guardrails or compliance requirements?</label><textarea id="twUcGuardrails" rows="2" placeholder="e.g., GDPR compliance..." style="width:100%;padding:12px;border:1px solid #ccc;border-radius:8px;font-size:0.9rem;resize:vertical;"></textarea></div>
<button class="btn btn-primary" onclick="suggestTWMetrics()" style="padding:14px 32px;font-size:1rem;">Suggest Metrics</button>
</div>
<div id="twSuggestLoading" style="display:none;text-align:center;padding:60px 20px;"><div style="display:inline-block;width:60px;height:60px;border:5px solid #e2e8f0;border-top-color:#2E86AB;border-radius:50%;animation:spin 1s linear infinite;"></div><h3 style="color:#2E86AB;margin-top:20px;">Analyzing Your Usecase...</h3><p style="color:#888;" id="twSuggestMsg">Reading usecase description...</p><div class="aug-progress" style="max-width:400px;margin:20px auto;"><div class="aug-progress-bar"><div class="aug-progress-fill" id="twSuggestFill" style="width:0%;"></div></div></div></div>
<div id="twSuggestResults" style="display:none;"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:20px;"><div style="display:flex;gap:4px;border:2px solid #e2e8f0;border-radius:14px;overflow:hidden;padding:3px;"><button class="tw-mc-tab active" onclick="filterTWMetrics('all',this)">All</button><button class="tw-mc-tab" onclick="filterTWMetrics('Bias Evaluation',this)">Bias</button><button class="tw-mc-tab" onclick="filterTWMetrics('Trustworthy',this)">Trustworthy</button><button class="tw-mc-tab" onclick="filterTWMetrics('Explainability',this)">Explainability</button></div><div style="display:flex;gap:10px;align-items:center;"><input type="text" id="twMetricSearch" placeholder="Search" oninput="filterTWMetrics(null,null)" style="padding:10px 14px;border:1px solid #ccc;border-radius:8px;width:220px;"><button class="btn btn-success" onclick="downloadTWConfig()">Download Config</button></div></div><div id="twMetricCardsGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px;"></div><div id="twMetricCount" style="margin-top:16px;font-weight:600;"></div></div>
</div></div></div>
<div id="tw_bias_func" class="sub-tab-content" style="display:none;">
<div style="display:flex;gap:0;border-bottom:2px solid #e2e8f0;margin-bottom:20px;"><button id="twBias-btn-upload" onclick="showTWBiasSubTab('twBiasUpload')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #e65100;color:#e65100;">Upload & Grouping</button><button id="twBias-btn-results" onclick="showTWBiasSubTab('twBiasResults')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Bias Results</button><button id="twBias-btn-analytics" onclick="showTWBiasSubTab('twBiasAnalytics')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Analytics</button></div>
<div id="twBiasUpload" style="display:block;"><div class="card"><div class="card-header"><h3>Upload Dataset for Bias Grouping</h3></div><div class="card-content"><p style="color:#555;margin-bottom:16px;">Upload your test data and a metric configuration file.</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;"><div><label style="font-weight:600;display:block;margin-bottom:8px;">Data File</label><div class="upload-zone" onclick="document.getElementById('twBiasFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twBiasHandleDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag data file</div></div><input type="file" id="twBiasFile" accept=".csv,.xlsx,.xls" style="display:none;" onchange="twBiasHandleUpload(this)"><div id="twBiasUploadStatus" style="margin-top:8px;"></div></div><div><label style="font-weight:600;display:block;margin-bottom:8px;">Config File</label><div class="upload-zone" onclick="document.getElementById('twBiasConfigFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twBiasHandleConfigDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag config file</div></div><input type="file" id="twBiasConfigFile" accept=".csv" style="display:none;" onchange="twBiasHandleConfigUpload(this)"><div id="twBiasConfigStatus" style="margin-top:8px;"></div></div></div><div style="margin-bottom:16px;"><label style="font-weight:600;display:block;margin-bottom:6px;">Grouping Criteria (optional)</label><textarea id="twBiasGroupCriteria" rows="2" placeholder="e.g., Group by shipping type..." style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;resize:vertical;"></textarea></div><div style="display:flex;gap:12px;"><button class="btn btn-primary" onclick="twBiasStartGrouping()" id="twBiasGroupBtn" disabled>Group Queries</button><button class="btn btn-primary" onclick="twBiasRunEval()" id="twBiasEvalBtnUpload" disabled style="background:#e65100;">Evaluate Bias</button></div><div id="twBiasPreview" style="display:none;margin-top:16px;"></div></div></div></div>
<div id="twBiasGroupingSection" style="display:none;margin-top:20px;"><div class="card"><div class="card-header"><h3>Bias Grouping Analysis</h3></div><div class="card-content"><div id="twBiasGroupLoading" style="display:none;text-align:center;padding:40px;"><div style="display:inline-block;width:50px;height:50px;border:4px solid #e2e8f0;border-top-color:#e65100;border-radius:50%;animation:spin 1s linear infinite;"></div><h4 style="color:#e65100;margin-top:16px;">Analyzing...</h4><p id="twBiasGroupMsg"></p></div><div id="twBiasGroupResults"></div></div></div></div>
<div id="twBiasResults" style="display:none;"><div class="card"><div class="card-header"><h3>Bias Evaluation Results</h3></div><div class="card-content"><div id="twBiasEvalLoading" style="display:none;text-align:center;padding:40px;"><div style="display:inline-block;width:50px;height:50px;border:4px solid #e2e8f0;border-top-color:#2E86AB;border-radius:50%;animation:spin 1s linear infinite;"></div><p id="twBiasEvalMsg">Initializing...</p><div class="aug-progress" style="max-width:400px;margin:20px auto;"><div class="aug-progress-bar"><div class="aug-progress-fill" id="twBiasEvalFill" style="width:0%;"></div></div></div></div><div id="twBiasEvalResults"><p style="text-align:center;padding:60px;color:#999;">Run Bias Evaluation first.</p></div></div></div></div>
<div id="twBiasAnalytics" style="display:none;"><div class="card"><div class="card-header"><h3>Bias Analytics</h3></div><div class="card-content"><div id="twBiasAnalyticsEmpty" style="text-align:center;color:#888;padding:40px;">Run evaluation first.</div><div id="twBiasAnalyticsContent" style="display:none;"><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;"><div class="chart-card"><div class="card-header"><h3>Pass / Fail</h3></div><div class="card-content"><div id="twBiasPassFailChart" style="width:100%;height:400px;"></div></div></div><div class="chart-card"><div class="card-header"><h3>Score Distribution</h3></div><div class="card-content"><div id="twBiasSpreadChart" style="width:100%;height:400px;"></div></div></div></div></div></div></div></div>
</div>
<div id="tw_explain" class="sub-tab-content" style="display:none;">
<div id="twExplainSubTabs" style="display:flex;gap:0;border-bottom:2px solid #e2e8f0;margin-bottom:20px;"><button id="twExplain-btn-upload" onclick="showTWExplainSubTab('twExplainUpload')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #00897b;color:#00897b;">Upload & Evaluate</button><button id="twExplain-btn-results" onclick="showTWExplainSubTab('twExplainResults')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Results</button><button id="twExplain-btn-analytics" onclick="showTWExplainSubTab('twExplainAnalytics')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Analytics</button></div>
<div id="twExplainUpload" style="display:block;"><div class="card"><div class="card-header"><h3>Upload for Explainability</h3></div><div class="card-content"><div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;"><div><label style="font-weight:600;display:block;margin-bottom:8px;">Data File</label><div class="upload-zone" onclick="document.getElementById('twExplainFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twExplainHandleDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag data file</div></div><input type="file" id="twExplainFile" accept=".csv,.xlsx,.xls" style="display:none;" onchange="twExplainHandleUpload(this)"><div id="twExplainUploadStatus" style="margin-top:8px;"></div></div><div><label style="font-weight:600;display:block;margin-bottom:8px;">Config File</label><div class="upload-zone" onclick="document.getElementById('twExplainConfigFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twExplainHandleConfigDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag config file</div></div><input type="file" id="twExplainConfigFile" accept=".csv" style="display:none;" onchange="twExplainHandleConfigUpload(this)"><div id="twExplainConfigStatus" style="margin-top:8px;"></div></div></div><div id="twExplainPreview" style="display:none;margin-top:16px;"></div><button class="btn btn-primary" onclick="twExplainRunEval()" id="twExplainEvalBtn" disabled style="margin-top:16px;">Run Explainability Evaluation</button></div></div></div>
<div id="twExplainResults" style="display:none;"><div class="card"><div class="card-header"><h3>Explainability Results</h3></div><div class="card-content"><div id="twExplainEvalLoading" style="display:none;text-align:center;padding:40px;"><div style="display:inline-block;width:50px;height:50px;border:4px solid #e2e8f0;border-top-color:#00897b;border-radius:50%;animation:spin 1s linear infinite;"></div><p id="twExplainEvalMsg">Initializing...</p><div class="aug-progress" style="max-width:400px;margin:20px auto;"><div class="aug-progress-bar"><div class="aug-progress-fill" id="twExplainEvalFill" style="width:0%;"></div></div></div></div><div id="twExplainEvalResultsContent"><p style="text-align:center;padding:60px;color:#999;">Run evaluation first.</p></div></div></div></div>
<div id="twExplainAnalytics" style="display:none;"><div class="card"><div class="card-header"><h3>Explainability Analytics</h3></div><div class="card-content"><div id="twExplainAnalyticsEmpty" style="text-align:center;color:#888;padding:40px;">Run evaluation first.</div><div id="twExplainAnalyticsContent" style="display:none;"><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;"><div class="chart-card"><div class="card-header"><h3>Pass / Fail</h3></div><div class="card-content"><div id="twExplainPassFailChart" style="width:100%;height:400px;"></div></div></div><div class="chart-card"><div class="card-header"><h3>Distribution</h3></div><div class="card-content"><div id="twExplainSpreadChart" style="width:100%;height:400px;"></div></div></div></div></div></div></div></div>
</div>
<div id="tw_trust" class="sub-tab-content" style="display:none;">
<div id="twTrustSubTabs" style="display:flex;gap:0;border-bottom:2px solid #e2e8f0;margin-bottom:20px;"><button id="twTrust-btn-upload" onclick="showTWTrustSubTab('twTrustUpload')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid #5c6bc0;color:#5c6bc0;">Upload & Evaluate</button><button id="twTrust-btn-results" onclick="showTWTrustSubTab('twTrustResults')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Results</button><button id="twTrust-btn-analytics" onclick="showTWTrustSubTab('twTrustAnalytics')" style="padding:10px 22px;font-size:0.85rem;font-weight:700;border:none;background:transparent;cursor:pointer;border-bottom:3px solid transparent;color:#718096;">Analytics</button></div>
<div id="twTrustUpload" style="display:block;"><div class="card"><div class="card-header"><h3>Upload for Trust Metric</h3></div><div class="card-content"><div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;"><div><label style="font-weight:600;display:block;margin-bottom:8px;">Data File</label><div class="upload-zone" onclick="document.getElementById('twTrustFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twTrustHandleDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag data file</div></div><input type="file" id="twTrustFile" accept=".csv,.xlsx,.xls" style="display:none;" onchange="twTrustHandleUpload(this)"><div id="twTrustUploadStatus" style="margin-top:8px;"></div></div><div><label style="font-weight:600;display:block;margin-bottom:8px;">Config File</label><div class="upload-zone" onclick="document.getElementById('twTrustConfigFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');twTrustHandleConfigDrop(event);" style="padding:24px;"><div style="font-size:0.95rem;font-weight:600;">Click or drag config file</div></div><input type="file" id="twTrustConfigFile" accept=".csv" style="display:none;" onchange="twTrustHandleConfigUpload(this)"><div id="twTrustConfigStatus" style="margin-top:8px;"></div></div></div><div id="twTrustPreview" style="display:none;margin-top:16px;"></div><button class="btn btn-primary" onclick="twTrustRunEval()" id="twTrustEvalBtn" disabled style="margin-top:16px;">Run Trust Evaluation</button></div></div></div>
<div id="twTrustResults" style="display:none;"><div class="card"><div class="card-header"><h3>Trust Metric Results</h3></div><div class="card-content"><div id="twTrustEvalLoading" style="display:none;text-align:center;padding:40px;"><div style="display:inline-block;width:50px;height:50px;border:4px solid #e2e8f0;border-top-color:#5c6bc0;border-radius:50%;animation:spin 1s linear infinite;"></div><p id="twTrustEvalMsg">Initializing...</p><div class="aug-progress" style="max-width:400px;margin:20px auto;"><div class="aug-progress-bar"><div class="aug-progress-fill" id="twTrustEvalFill" style="width:0%;"></div></div></div></div><div id="twTrustEvalResultsContent"><p style="text-align:center;padding:60px;color:#999;">Run evaluation first.</p></div></div></div></div>
<div id="twTrustAnalytics" style="display:none;"><div class="card"><div class="card-header"><h3>Trust Analytics</h3></div><div class="card-content"><div id="twTrustAnalyticsEmpty" style="text-align:center;color:#888;padding:40px;">Run evaluation first.</div><div id="twTrustAnalyticsContent" style="display:none;"><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;"><div class="chart-card"><div class="card-header"><h3>Pass / Fail</h3></div><div class="card-content"><div id="twTrustPassFailChart" style="width:100%;height:400px;"></div></div></div><div class="chart-card"><div class="card-header"><h3>Distribution</h3></div><div class="card-content"><div id="twTrustSpreadChart" style="width:100%;height:400px;"></div></div></div></div></div></div></div></div>
</div>"""
''')

    # ==================== Update report_generator.py - remove original dependency ====================
    w("report_generator.py", r'''"""
Main ReportGenerator class - FULLY SELF-CONTAINED.
No dependency on report_generator_original.py.
"""
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from config import get_default_config
from utils import (find_column, safe_numeric_conversion, normalize_text, text_equal, clean_text, normalize_query_match)
from tabs.metrics_summary import generate_metrics_summary_table
from tabs.data_assurance import create_test_coverage_sunburst, generate_augmented_data_table, get_coverage_edit_data
from tabs.model_quality_assurance import (generate_interactive_details_table, create_metrics_bar_chart, create_overall_pie_chart, create_score_comparison_chart, create_disaggregated_table, load_recovery_loop_global)
from tabs.secondary_llm import generate_secondary_llm_table


class ReportGenerator:
    def __init__(self, config=None):
        logger.info('Initializing ReportGenerator')
        self.config = config or get_default_config()
        self.report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metric_details_excel_path = Path(__file__).resolve().parent / "final_eval_results01.xlsx"

    def _get_chart_layout(self, theme):
        return {'font': {'family': theme['font_family'], 'size': 12}, 'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'height': self.config['chart_height'], 'margin': dict(l=60, r=60, t=80, b=100), 'xaxis': {'showgrid': True, 'gridcolor': theme['border_color'], 'tickangle': -45, 'tickfont': {'size': 10}}, 'yaxis': {'showgrid': True, 'gridcolor': theme['border_color'], 'tickfont': {'size': 10}}}

    def _calculate_status(self, df, metrics, thresholds):
        try:
            df_copy = df.copy()
            for metric in metrics:
                if metric not in df_copy.columns: continue
                status_col = f"{metric}_status"; reason_col = f"{metric}-reason"; threshold = thresholds.get(metric)
                if threshold is None: df_copy[status_col] = "Unknown"; continue
                if reason_col in df_copy.columns:
                    df_copy[status_col] = df_copy.apply(lambda row, m=metric, rc=reason_col, th=threshold: self._determine_status_with_reason(row, m, rc, th), axis=1)
                else:
                    df_copy[status_col] = df_copy[metric].apply(lambda x, m=metric, th=threshold: self._determine_status_simple(x, m, th))
            return df_copy
        except Exception as e: logger.error(f"Error calculating status: {e}"); return df

    def _determine_status_with_reason(self, row, metric, reason_col, threshold):
        reason = str(row.get(reason_col, "")).strip().upper()
        if reason == "NA": return "Skipped"
        score = safe_numeric_conversion(row[metric])
        if pd.isna(score): return "Failed"
        if metric in self.config['reverse_metrics']: return "Passed" if score <= threshold else "Failed"
        return "Passed" if score >= threshold else "Failed"

    def _determine_status_simple(self, value, metric, threshold):
        score = safe_numeric_conversion(value)
        if pd.isna(score): return "Failed"
        if metric in self.config['reverse_metrics']: return "Passed" if score <= threshold else "Failed"
        return "Passed" if score >= threshold else "Failed"

    def _prepare_modal_data(self, df, metrics, thresholds):
        try:
            modal_data = {}; metric_sheets = {}
            try:
                if self.metric_details_excel_path.exists():
                    xls = pd.ExcelFile(self.metric_details_excel_path)
                    for sheet in xls.sheet_names:
                        try: metric_sheets[sheet] = pd.read_excel(xls, sheet_name=sheet)
                        except: continue
            except Exception as e: logger.warning(f"Unable to read metric details excel: {e}")
            normalized_sheet_map = {str(s).strip().lower(): s for s in metric_sheets.keys()}
            for idx, row in df.iterrows():
                modal_data[idx] = {'query': clean_text(row.get('Query', 'N/A')), 'response': clean_text(row.get('Response', 'N/A')), 'timestamp': self.report_timestamp, 'metrics': {}}
                modal_data[idx]["metric_fields"] = {}
                for metric in metrics:
                    norm_metric = str(metric).strip().lower()
                    if norm_metric in normalized_sheet_map:
                        sheet_name = normalized_sheet_map[norm_metric]; metric_df = metric_sheets.get(sheet_name)
                        if isinstance(metric_df, pd.DataFrame):
                            query_col = find_column(metric_df, ['Query','query','Question']); found_entry = {}
                            if query_col and query_col in metric_df.columns:
                                metric_df[query_col] = metric_df[query_col].ffill(); details_query = normalize_text(row.get('Query', ''))
                                mask = metric_df[query_col].apply(lambda x: normalize_text(x) == details_query); matched = metric_df[mask]
                                if not matched.empty:
                                    found_entry = matched.iloc[0].replace({pd.NA: None}).to_dict() if len(matched)==1 else [r.replace({pd.NA: None}).to_dict() for _, r in matched.iterrows()]
                                else:
                                    mask2 = metric_df[query_col].apply(lambda x: text_equal(x, details_query)); matched2 = metric_df[mask2]
                                    if not matched2.empty: found_entry = matched2.iloc[0].replace({pd.NA: None}).to_dict() if len(matched2)==1 else [r.replace({pd.NA: None}).to_dict() for _, r in matched2.iterrows()]
                            modal_data[idx]["metric_fields"][str(metric).strip()] = found_entry
                        else: modal_data[idx]["metric_fields"][metric] = {}
                    else: modal_data[idx]["metric_fields"][metric] = {}
                for metric in metrics:
                    ms = str(metric).strip(); mn = normalize_text(ms)
                    md = {'score': clean_text(row.get(metric, 'N/A')), 'threshold': str(thresholds.get(metric, 'N/A')), 'status': clean_text(row.get(f"{metric}_status", 'Unknown')), 'additional_fields': {}}
                    for col in row.index:
                        cn = normalize_text(str(col).strip())
                        if cn == mn or cn.endswith("status"): continue
                        if cn.startswith(mn):
                            fn = cn.replace(mn,"").strip(" _-"); fv = clean_text(row.get(col, ''))
                            if fv != 'N/A': md['additional_fields'][fn] = fv
                    modal_data[idx]['metrics'][ms] = md
            return modal_data
        except Exception as e: logger.error(f"Error preparing modal data: {e}"); return {}

    def _create_modern_charts(self, summary_df, overall_df, metrics_df, metrics_col, score_col, threshold_col):
        try:
            charts = {}; layout_fn = self._get_chart_layout
            charts['metrics'] = create_metrics_bar_chart(summary_df, self.config, layout_fn)
            charts['overall'] = create_overall_pie_chart(overall_df, self.config, layout_fn)
            charts['comparison'] = create_score_comparison_chart(metrics_df, metrics_col, score_col, threshold_col, self.config, layout_fn)
            base_dir = Path(__file__).resolve().parent
            charts['coverage'] = create_test_coverage_sunburst(excel_path=base_dir / "Metrics_template02.xlsx", sheet_name='Test data coverage')
            charts['augmentation'] = generate_augmented_data_table(excel_path=base_dir / "agent_query_augmentations.xlsx", sheet_name='Sheet1')
            charts['disaggregated'] = create_disaggregated_table(base_dir / "Metrics_template02.xlsx")
            return charts
        except Exception as e: logger.error(f"Error creating charts: {e}"); return {}

    def generate_report(self, metrics_df, details_df, summary_df, overall_df):
        try:
            logger.info("Starting report generation")
            if any(df.empty for df in [metrics_df, details_df, summary_df, overall_df]):
                return self._generate_error_report("One or more input DataFrames are empty")
            mc = find_column(metrics_df, ['Metrics','Metric','metric']); tc = find_column(metrics_df, ['Threshold_Value','Threshold','threshold']); sc = find_column(metrics_df, ['aggregate_score','score','Score'])
            if not all([mc, tc, sc]): return self._generate_error_report("Required columns not found")
            all_metrics = [m for m in metrics_df[mc].dropna().astype(str).tolist() if m.strip().lower() != 'knowledge retention']
            thresholds = {k: v for k, v in zip(metrics_df[mc], metrics_df[tc]) if str(k).strip().lower() != 'knowledge retention'}
            details_df = self._calculate_status(details_df, all_metrics, thresholds)
            charts = self._create_modern_charts(summary_df, overall_df, metrics_df, mc, sc, tc)
            modal_data = self._prepare_modal_data(details_df, all_metrics, thresholds)
            from templates.html_report import generate_modern_html
            return generate_modern_html(config=self.config, report_timestamp=self.report_timestamp, metrics_df=metrics_df, details_df=details_df, all_metrics=all_metrics, charts=charts, modal_data=modal_data, metric_details_excel_path=self.metric_details_excel_path)
        except Exception as e: return self._generate_error_report(f"Error: {e}")

    def _generate_error_report(self, msg):
        return f"<!DOCTYPE html><html><body style='font-family:Arial;padding:40px;text-align:center;'><h1>Report Generation Error</h1><div style='color:#dc3545;margin:20px;'>{msg}</div></body></html>"
''')

    # ==================== Update run_all.py - no original file check ====================
    w("run_all.py", r'''#!/usr/bin/env python3
"""GenAI Monitor - Quick Start. Verifies setup and starts the app."""
import os, sys

def check_setup():
    errors, warnings = [], []
    if not os.path.exists("Metrics_template02.xlsx"):
        warnings.append("Metrics_template02.xlsx not found (required for report)")
    for f in ["final_eval_results01.xlsx","agent_query_augmentations.xlsx","Augmentations 2.xlsx"]:
        if not os.path.exists(f): warnings.append(f"{f} not found (optional)")
    if not os.path.exists(".env"): warnings.append(".env not found (needed for Azure OpenAI)")
    missing = []
    for dep in ['flask','pandas','plotly','openpyxl','requests']:
        try: __import__(dep)
        except ImportError: missing.append(dep)
    if missing: errors.append(f"Missing packages: {', '.join(missing)}\n  Fix: pip install {' '.join(missing)}")
    return errors, warnings

def main():
    print("="*60); print("GenAI Monitor - Setup Check"); print("="*60)
    errors, warnings = check_setup()
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings: print(f"  - {w}")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors: print(f"  - {e}")
        print("\nFix errors and try again."); sys.exit(1)
    print("\nAll checks passed! Starting Flask server...")
    print("="*60)
    from app import app
    app.run(debug=False, host="0.0.0.0", port=5000)

if __name__ == "__main__": main()
''')

    print(f"\n{'='*60}")
    print("Part 8 COMPLETE: Master HTML Assembly - FULLY SELF-CONTAINED")
    print(f"{'='*60}")
    print()
    print("ALL 8 PARTS COMPLETE!")
    print("NO ORIGINAL FILE NEEDED - project is 100% standalone.")
    print()
    print("To run:")
    print("  1. Copy data files into genai_monitor/")
    print("     cp Metrics_template02.xlsx genai_monitor/")
    print("     cp .env genai_monitor/")
    print("  2. cd genai_monitor")
    print("  3. python run_all.py")

if __name__ == "__main__":
    build()
