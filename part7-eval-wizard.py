#!/usr/bin/env python3
"""
Part 7: Fully self-contained Evaluations Wizard
Run: python build_part7.py
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
    print(f"Part 7: Evaluations Wizard (self-contained) in ./{BASE}/templates/\n")

    w("templates/js_evaluations_wizard.py", r'''"""
Evaluations Wizard HTML + JS generator - FULLY SELF-CONTAINED.
No dependency on original file.
"""
import json


def get_evaluations_wizard_html(all_metrics):
    eval_metrics = []
    short_descs = {
        "coherence": "Checks if the response has proper logical structure and flow.",
        "error detection": "Detects factual or logical errors in the generated output.",
        "exact match check": "Verifies if the output exactly matches the ground truth.",
        "bert similarity": "Measures semantic similarity between output and ground truth using BERT.",
        "rouge score": "Measures text overlap between the output and reference summary.",
        "meteor score": "Evaluates output quality using precision, recall, and synonymy.",
        "qa score": "Checks if the output covers all key aspects of the expected answer.",
        "contradiction check": "Detects if the output contradicts the source content.",
        "qa relevancy": "Measures how relevant the generated answer is to the question.",
        "faithfulness": "Checks if the answer is faithful to the provided context.",
        "context relevancy": "Measures if retrieved context is relevant to the query.",
        "answer correctness": "Measures correctness of the answer against ground truth.",
        "hallucination check": "Detects hallucinated content not supported by the source.",
        "hallucination cove": "Detects hallucinations using chain-of-verification approach.",
        "toxicity check": "Detects toxic or harmful content in model responses.",
        "recovery loop": "Evaluates the model's ability to recover from errors.",
    }
    for m in all_metrics:
        m_lower = m.strip().lower()
        desc = short_descs.get(m_lower, f"Evaluates the {m} metric for model output quality.")
        eval_metrics.append({"name": m.strip(), "cat": "Model Quality", "desc": desc})
    static_metrics = [
        {"name":"Average Words Per Sentence","desc":"Average number of words in each sentence of the text."},
        {"name":"Compression Ratio","desc":"Ratio of summary length to original source length."},
        {"name":"Email Address Count","desc":"Number of email addresses detected in the text."},
        {"name":"Text Length","desc":"Total character count of the text."},
        {"name":"Lexical Density","desc":"Ratio of unique content words to total words."},
        {"name":"Word Count","desc":"Total number of words in the text."},
        {"name":"Sentence Count","desc":"Total number of sentences in the text."},
        {"name":"Syllable Count","desc":"Total number of syllables across all words."},
        {"name":"Flesch Reading Ease","desc":"Readability score from 0 (hardest) to 100 (easiest)."},
        {"name":"Gunning Fog Index","desc":"Estimates years of education needed to understand the text."},
        {"name":"URL Count","desc":"Number of URLs or hyperlinks found in the text."},
        {"name":"Number Count","desc":"Count of numerical values present in the text."},
        {"name":"Punctuation Density","desc":"Ratio of punctuation marks to total characters."},
        {"name":"Uppercase Ratio","desc":"Ratio of uppercase characters to total characters."},
        {"name":"Stopword Ratio","desc":"Ratio of common stopwords to total words."},
        {"name":"Type Token Ratio","desc":"Ratio of unique tokens to total tokens (vocabulary richness)."},
    ]
    llm_providers = {
        "Azure OpenAI":{"models":["GPT-4o","GPT-4 Turbo","GPT-4","GPT-3.5 Turbo"],"fields":[{"key":"endpoint","label":"Endpoint URL","placeholder":"https://your-resource.openai.azure.com"},{"key":"api_key","label":"API Key","placeholder":"Enter API key","secret":True},{"key":"deployment","label":"Deployment Name","placeholder":"gpt-4o"},{"key":"api_version","label":"API Version","placeholder":"2024-12-01-preview"}]},
        "Anthropic":{"models":["Claude Opus 4","Claude Sonnet 4","Claude Sonnet 3.5","Claude Haiku 3.5"],"fields":[{"key":"api_key","label":"API Key","placeholder":"sk-ant-...","secret":True}]},
        "OpenAI":{"models":["GPT-4o","GPT-4 Turbo","o1","o3-mini"],"fields":[{"key":"api_key","label":"API Key","placeholder":"sk-...","secret":True}]},
        "Gemini":{"models":["Gemini 2.0 Flash","Gemini 2.0 Pro","Gemini 1.5 Pro"],"fields":[{"key":"api_key","label":"API Key","placeholder":"Enter API key","secret":True}]},
        "AWS Bedrock":{"models":["Claude Sonnet 4 (Bedrock)","Llama 3.1 70B (Bedrock)"],"fields":[{"key":"access_key","label":"Access Key ID","placeholder":"AKIA...","secret":True},{"key":"secret_key","label":"Secret Access Key","placeholder":"Enter secret key","secret":True},{"key":"region","label":"Region","placeholder":"us-east-1"}]},
        "Meta":{"models":["Llama 3.1 70B","Llama 3.1 8B"],"fields":[{"key":"api_key","label":"API Key","placeholder":"Enter API key","secret":True}]},
    }
    metrics_json = json.dumps(eval_metrics)
    static_json = json.dumps(static_metrics)
    llm_json = json.dumps(llm_providers)
    return f"""<div>
<div class="wizard-steps" id="evalWizardSteps">
<div class="wizard-step active" onclick="goToEvalStep(1)"><div class="wizard-step-num">1</div><div class="wizard-step-label">Upload Data</div></div><div class="wizard-connector"></div>
<div class="wizard-step" onclick="goToEvalStep(2)"><div class="wizard-step-num">2</div><div class="wizard-step-label">Configuration</div></div><div class="wizard-connector"></div>
<div class="wizard-step" onclick="goToEvalStep(3)"><div class="wizard-step-num">3</div><div class="wizard-step-label">Configure Metrics</div></div><div class="wizard-connector"></div>
<div class="wizard-step" onclick="goToEvalStep(4)"><div class="wizard-step-num">4</div><div class="wizard-step-label">Review &amp; Run</div></div>
</div>
<div class="wizard-body" id="evalStep1" style="display:block;"><div class="card"><div class="card-header"><h3>\U0001f4c1 Upload Evaluation Data</h3></div><div class="card-content">
<p style="color:#555;margin-bottom:16px;">Upload a CSV or Excel file with columns: <strong>Topic</strong>, <strong>Sub-topic</strong>, <strong>Input</strong>, and <strong>Expected Output</strong> (case-insensitive).</p>
<div class="upload-zone" id="evalUploadZone" onclick="document.getElementById('evalDatasetFile').click();" ondragover="event.preventDefault();this.classList.add('dragover');" ondragleave="this.classList.remove('dragover');" ondrop="event.preventDefault();this.classList.remove('dragover');evalHandleFileDrop(event);"><div style="font-size:1.1rem;font-weight:600;">Click or drag &amp; drop your file here</div><div style="font-size:0.85rem;color:#888;margin-top:6px;">Supports .csv, .xlsx, .xls</div></div>
<input type="file" id="evalDatasetFile" accept=".csv,.xlsx,.xls" style="display:none;" onchange="evalHandleFileUpload(this)">
<div id="evalUploadStatus" style="margin-top:12px;"></div><div id="evalUploadPreview" class="preview-table" style="display:none;margin-top:16px;"></div>
</div></div><div class="wizard-actions"><div></div><button class="btn btn-primary" id="evalStep1Next" disabled onclick="goToEvalStep(2)">Next \u2192</button></div></div>
<div class="wizard-body" id="evalStep2" style="display:none;"><div class="card"><div class="card-header"><h3>Configuration</h3></div><div class="card-content">
<h4 style="color:#2E86AB;margin-bottom:12px;">LLM Provider</h4>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:16px;" id="evalLLMCards"></div>
<div id="evalLLMModelSelect" style="display:none;margin-bottom:16px;"><label style="font-weight:600;display:block;margin-bottom:6px;">Model</label><select id="evalModelDropdown" onchange="evalUpdateConfigBtn()" style="width:100%;max-width:300px;padding:10px;border:1px solid #ccc;border-radius:8px;"></select></div>
<div id="evalLLMFields" style="display:none;margin-bottom:24px;"></div>
<hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;">
<h4 style="color:#2E86AB;margin-bottom:12px;">Observability Platform</h4>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-bottom:16px;" id="evalObsCards">
<div class="eval-platform-card" data-platform="Arize AX" onclick="selectEvalObs('Arize AX')"><div style="font-weight:700;">Arize AX</div></div>
<div class="eval-platform-card" data-platform="Langsmith" onclick="selectEvalObs('Langsmith')"><div style="font-weight:700;">Langsmith</div></div>
<div class="eval-platform-card" data-platform="Galileo" onclick="selectEvalObs('Galileo')"><div style="font-weight:700;">Galileo</div></div>
<div class="eval-platform-card" data-platform="Langfuse" onclick="selectEvalObs('Langfuse')"><div style="font-weight:700;">Langfuse</div></div>
</div>
<div id="evalObsFields" style="display:none;">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;"><div><label style="font-weight:600;display:block;margin-bottom:4px;">API Key</label><input type="password" id="evalObsApiKey" placeholder="Enter API key" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;" oninput="evalUpdateConfigBtn()"></div><div><label style="font-weight:600;display:block;margin-bottom:4px;">Project Name</label><input type="text" id="evalObsProject" placeholder="Enter project name" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;" oninput="evalUpdateConfigBtn()"></div></div>
</div>
</div></div><div class="wizard-actions"><button class="btn btn-secondary" onclick="goToEvalStep(1)">\u2190 Back</button><button class="btn btn-primary" id="evalStep2Next" disabled onclick="goToEvalStep(3)">Next \u2192</button></div></div>
<div class="wizard-body" id="evalStep3" style="display:none;"><div class="card"><div class="card-header" style="display:flex;justify-content:space-between;align-items:center;"><h3>Configure Metrics</h3><button class="btn" onclick="openCustomMetricModal()" style="background:rgba(255,255,255,0.2);border:2px solid rgba(255,255,255,0.6);color:white;font-weight:700;padding:8px 20px;">+ CUSTOM METRIC</button></div><div class="card-content">
<div style="display:grid;grid-template-columns:1fr 2fr;gap:12px;margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid #e2e8f0;">
<div><label style="font-weight:600;display:block;margin-bottom:4px;">Configuration Name *</label><input type="text" id="evalConfigName" placeholder="e.g., Logistics QA v2.1" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;" oninput="checkConfigNameFilled()"></div>
<div><label style="font-weight:600;display:block;margin-bottom:4px;">Configuration Description</label><input type="text" id="evalConfigDesc" placeholder="Brief description of this evaluation configuration..." style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;"></div>
</div>
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
<div style="display:flex;gap:4px;border:2px solid #e2e8f0;border-radius:14px;overflow:hidden;padding:3px;" id="evalMetricTabs">
<button class="emc-tab active" onclick="filterEvalMetrics('all',this)">All</button>
<button class="emc-tab" onclick="filterEvalMetrics('Model Quality',this)">Model Quality</button>
</div>
<div style="display:flex;align-items:center;gap:12px;"><label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-weight:600;font-size:0.9rem;color:#555;white-space:nowrap;"><input type="checkbox" id="evalSelectAll" onchange="toggleSelectAllMetrics(this.checked)" style="accent-color:#2E86AB;width:18px;height:18px;cursor:pointer;">Select All</label><input type="text" id="evalMetricSearch" placeholder="Search Metrics" oninput="filterEvalMetrics(null,null)" style="padding:10px 14px;border:1px solid #ccc;border-radius:8px;width:220px;font-size:0.9rem;"></div>
</div>
<div id="evalMetricCardsGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px;"></div>
<div id="evalMetricCount" style="margin-top:16px;font-weight:600;color:#555;"></div>
</div></div><div class="wizard-actions"><button class="btn btn-secondary" onclick="goToEvalStep(2)">\u2190 Back</button><button class="btn btn-primary" id="evalStep3Next" disabled onclick="goToEvalStep(4)">Next \u2192</button></div></div>
<div class="wizard-body" id="evalStep4" style="display:none;"><div class="card"><div class="card-header"><h3>Review &amp; Run</h3></div><div class="card-content">
<div id="evalConfigSummary" style="margin-bottom:24px;"></div>
<div id="evalRunSection"><button class="btn btn-primary" style="font-size:1.1rem;padding:14px 36px;" onclick="startEvaluation()">Save &amp; Run Evaluation</button></div>
<div id="evalInProgress" style="display:none;text-align:center;padding:40px;"><div style="display:inline-block;width:60px;height:60px;border:5px solid #e2e8f0;border-top-color:#2E86AB;border-radius:50%;animation:spin 1s linear infinite;"></div><h3 style="color:#2E86AB;margin-top:16px;">Evaluation in Progress</h3><p id="evalProgressMsg" style="color:#888;">Initializing...</p><div class="aug-progress" style="max-width:400px;margin:20px auto;"><div class="aug-progress-bar"><div class="aug-progress-fill" id="evalProgressFill" style="width:0%;"></div></div></div></div>
</div></div><div class="wizard-actions"><button class="btn btn-secondary" id="evalStep4Back" onclick="goToEvalStep(3)">\u2190 Back</button><div></div></div></div>
</div>
<div id="customMetricModal" class="modal"><div class="modal-content" style="max-width:800px;"><div class="modal-header" style="background:linear-gradient(135deg,#2E86AB,#A23B72);"><h3 class="modal-title">+ Custom Metric</h3><button class="modal-close" onclick="closeCustomMetricModal()">\u00d7</button></div><div class="modal-body" style="padding:0;flex-direction:column;max-height:70vh;overflow:hidden;">
<div style="display:flex;border-bottom:2px solid #e2e8f0;">
<button id="cmTab1" onclick="switchCMTab('custom')" style="flex:1;padding:14px;font-weight:700;border:none;cursor:pointer;background:#2E86AB;color:white;font-size:0.95rem;">Custom Metric</button>
<button id="cmTab2" onclick="switchCMTab('static')" style="flex:1;padding:14px;font-weight:700;border:none;cursor:pointer;background:white;color:#718096;font-size:0.95rem;">Static Metrics</button>
</div>
<div style="padding:24px;overflow-y:auto;max-height:60vh;">
<div id="cmCustomPanel">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;"><div><label style="font-weight:600;display:block;margin-bottom:4px;">Metric Name *</label><input type="text" id="cmName" placeholder="e.g., Custom Relevancy" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;"></div><div><label style="font-weight:600;display:block;margin-bottom:4px;">Category</label><select id="cmCategory" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;"><option value="Model Quality">Model Quality</option><option value="Custom">Custom</option></select></div></div>
<div style="margin-bottom:16px;"><label style="font-weight:600;display:block;margin-bottom:4px;">Description *</label><textarea id="cmDesc" rows="2" placeholder="What does this metric evaluate?" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;resize:vertical;"></textarea></div>
<div style="margin-bottom:16px;"><label style="font-weight:600;display:block;margin-bottom:4px;">Evaluation Prompt</label><textarea id="cmPrompt" rows="3" placeholder="Enter the LLM prompt for this metric evaluation. Use {{{{input}}}}, {{{{expected_output}}}}, {{{{response}}}} as placeholders..." style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;resize:vertical;font-family:monospace;font-size:0.85rem;"></textarea><div style="font-size:0.75rem;color:#888;margin-top:4px;">Available placeholders: <code>{{{{input}}}}</code>, <code>{{{{expected_output}}}}</code>, <code>{{{{response}}}}</code></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;"><div><label style="font-weight:600;display:block;margin-bottom:4px;">Default Threshold</label><input type="number" id="cmThreshold" value="0.5" min="0" max="1" step="0.01" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;"></div><div style="display:flex;align-items:flex-end;"><label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="cmInverse"> Inverse Metric</label></div></div>
<button class="btn btn-primary" onclick="addCustomEvalMetric()" style="width:100%;padding:12px;">+ Add Metric</button>
</div>
<div id="cmStaticPanel" style="display:none;">
<p style="color:#555;margin-bottom:16px;">Select static metrics to add. These are computed directly from text without LLM calls.</p>
<div id="cmStaticList"></div>
<button class="btn btn-primary" onclick="addSelectedStaticMetrics()" style="width:100%;padding:12px;margin-top:20px;">+ Add Selected Metrics</button>
</div>
</div></div></div></div>
<div id="spanPopover" style="display:none;position:fixed;z-index:2000;background:white;border:1px solid #ccc;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.15);padding:16px;width:320px;">
<h4 style="margin-bottom:10px;font-size:0.95rem;color:#333;">Metric Settings</h4>
<div style="margin-bottom:12px;">
<label style="font-weight:600;display:block;margin-bottom:4px;font-size:0.85rem;">Span Names</label>
<div style="display:flex;gap:8px;margin-bottom:6px;"><input type="text" id="spanInput" placeholder="Enter span name" style="flex:1;padding:8px;border:1px solid #ccc;border-radius:6px;font-size:0.85rem;"><button onclick="addSpanName()" class="btn btn-primary" style="padding:8px 12px;font-size:0.82rem;">Add</button></div>
<div id="spanList" style="max-height:80px;overflow-y:auto;"></div>
</div>
<div style="margin-bottom:12px;">
<label style="font-weight:600;display:block;margin-bottom:4px;font-size:0.85rem;">Expected Data Column</label>
<select id="spanExpectedCol" onchange="updateExpectedCol()" style="width:100%;padding:8px;border:1px solid #ccc;border-radius:6px;font-size:0.85rem;"><option value="">-- None --</option></select>
</div>
<div style="text-align:right;"><button onclick="closeSpanPopover()" class="btn btn-secondary" style="padding:6px 16px;font-size:0.82rem;">Done</button></div>
</div>
<script>
(function(){{
var EV_METRICS={metrics_json};
var EV_STATIC={static_json};
var EV_LLM={llm_json};
var evalFileData=null,evalSelectedLLM=null,evalSelectedModel=null,evalSelectedObs=null,evalCustomModelName='';
var evalLLMCreds={{}};var evalMetricStates={{}};var evalCurrentMetricForSpan=null;
var evalActiveTab='all';var evalExtraColumns=[];
EV_METRICS.forEach(function(m){{evalMetricStates[m.name]={{enabled:false,threshold:0.5,inverse:false,spans:[],expectedCol:''}};}});
window.goToEvalStep=function(s){{
if(s>1&&!evalFileData)s=1;
if(s>2){{var ok=evalSelectedLLM&&evalSelectedModel&&evalSelectedObs&&document.getElementById('evalObsApiKey').value.trim()&&document.getElementById('evalObsProject').value.trim();if(!ok)s=2;}}
if(s>3){{var any=Object.keys(evalMetricStates).some(function(k){{return evalMetricStates[k].enabled;}});var hasName=document.getElementById('evalConfigName')?.value.trim();if(!any||!hasName)s=3;}}
for(var i=1;i<=4;i++){{var el=document.getElementById('evalStep'+i);if(el)el.style.display=i===s?'block':'none';}}
document.querySelectorAll('#evalWizardSteps .wizard-step').forEach(function(el,i){{el.classList.remove('active','completed');if(i+1===s)el.classList.add('active');else if(i+1<s)el.classList.add('completed');}});
if(s===2)buildLLMCards();if(s===3)renderMetricCards();if(s===4)buildEvalSummary();
}};
window.evalHandleFileDrop=function(e){{if(e.dataTransfer.files.length>0)evalProcessFile(e.dataTransfer.files[0]);}};
window.evalHandleFileUpload=function(inp){{if(inp.files.length>0)evalProcessFile(inp.files[0]);}};
function evalProcessFile(f){{var st=document.getElementById('evalUploadStatus');var nm=f.name.toLowerCase();
if(!nm.endsWith('.csv')&&!nm.endsWith('.xlsx')&&!nm.endsWith('.xls')){{st.innerHTML='<span style="color:#dc3545;">\\u2717 Unsupported format</span>';return;}}
evalFileData={{name:f.name,size:(f.size/1024).toFixed(1)+' KB',rows:'\\u2014'}};
if(nm.endsWith('.csv')){{var reader=new FileReader();reader.onload=function(e){{var lines=e.target.result.split('\\n').filter(function(l){{return l.trim();}});evalFileData.rows=Math.max(0,lines.length-1);evalFileData.headers=lines[0]?lines[0].split(',').map(function(h){{return h.trim().replace(/"/g,'');}}):[]; evalFileData.dataRows=[];for(var li=1;li<lines.length;li++){{var cells=lines[li].split(',').map(function(c){{return c.trim().replace(/"/g,'');}});if(cells.some(function(c){{return c;}}))evalFileData.dataRows.push(cells);}} evalShowUploadOK();}};reader.readAsText(f);}}
else{{evalFileData.rows='(Excel)';evalFileData.dataRows=[];evalShowUploadOK();}}}}
function evalShowUploadOK(){{document.getElementById('evalUploadStatus').innerHTML='<span style="color:#28a745;font-weight:600;">\\u2713 '+evalFileData.name+' ('+evalFileData.size+', '+evalFileData.rows+' rows)</span>';document.getElementById('evalStep1Next').disabled=false;
var stdCols=['topic','sub-topic','subtopic','sub_topic','input','expected output','expected_output','expectedoutput'];
if(evalFileData.headers&&evalFileData.headers.length>0){{evalExtraColumns=evalFileData.headers.filter(function(h){{return stdCols.indexOf(h.toLowerCase().trim())===-1;}});
var p=document.getElementById('evalUploadPreview');p.style.display='block';var h='<table class="modern-table"><thead><tr>';evalFileData.headers.forEach(function(hd){{h+='<th>'+hd+'</th>';}});h+='</tr></thead><tbody>';var previewRows=evalFileData.dataRows||[];var lim=Math.min(previewRows.length,8);for(var ri=0;ri<lim;ri++){{h+='<tr>';previewRows[ri].forEach(function(cell){{h+='<td>'+String(cell||'').substring(0,120)+'</td>';}});h+='</tr>';}}h+='</tbody></table>';p.innerHTML=h;}}}}
function buildLLMCards(){{var c=document.getElementById('evalLLMCards');c.innerHTML='';Object.keys(EV_LLM).forEach(function(p){{var d=document.createElement('div');d.className='eval-platform-card'+(evalSelectedLLM===p?' selected':'');d.setAttribute('data-platform',p);d.innerHTML='<div style="font-weight:700;font-size:0.95rem;">'+p+'</div>';d.onclick=function(){{selectEvalLLM(p);}};c.appendChild(d);}});if(evalSelectedLLM)showLLMDetails(evalSelectedLLM);}}
window.selectEvalLLM=function(p){{evalSelectedLLM=p;evalSelectedModel=null;document.querySelectorAll('#evalLLMCards .eval-platform-card').forEach(function(c){{c.classList.toggle('selected',c.getAttribute('data-platform')===p);}});showLLMDetails(p);}};
function showLLMDetails(p){{var info=EV_LLM[p];if(!info)return;var ms=document.getElementById('evalLLMModelSelect');ms.style.display='block';var dd=document.getElementById('evalModelDropdown');dd.innerHTML='<option value="">-- Select Model --</option>';info.models.forEach(function(m){{var o=document.createElement('option');o.value=m;o.textContent=m;if(evalSelectedModel===m)o.selected=true;dd.appendChild(o);}});var co=document.createElement('option');co.value='__custom__';co.textContent='Other (specify custom model)';dd.appendChild(co);
var existCW=document.getElementById('evalCustomModelWrap');if(existCW)existCW.remove();var cw=document.createElement('div');cw.id='evalCustomModelWrap';cw.style.cssText='margin-top:8px;display:none;';cw.innerHTML='<label style="font-weight:600;display:block;margin-bottom:4px;font-size:0.85rem;">Custom Model Name</label><input type="text" id="evalCustomModelInput" placeholder="e.g., gpt-4o-2024-08-06" style="width:100%;max-width:300px;padding:10px;border:1px solid #ccc;border-radius:8px;" oninput="evalUpdateConfigBtn()">';ms.insertAdjacentElement('afterend',cw);
var fc=document.getElementById('evalLLMFields');fc.style.display='block';fc.innerHTML='';var grid=document.createElement('div');grid.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:12px;';info.fields.forEach(function(f){{var wrap=document.createElement('div');wrap.innerHTML='<label style="font-weight:600;display:block;margin-bottom:4px;">'+f.label+'</label><input type="'+(f.secret?'password':'text')+'" placeholder="'+f.placeholder+'" style="width:100%;padding:10px;border:1px solid #ccc;border-radius:8px;" data-cred-key="'+f.key+'" oninput="evalUpdateConfigBtn()" value="'+(evalLLMCreds[f.key]||'')+'">';grid.appendChild(wrap);}});fc.appendChild(grid);}}
document.getElementById('evalModelDropdown')?.addEventListener('change',function(){{evalSelectedModel=this.value;var cw=document.getElementById('evalCustomModelWrap');if(cw)cw.style.display=this.value==='__custom__'?'block':'none';evalUpdateConfigBtn();}});
window.selectEvalObs=function(p){{evalSelectedObs=p;document.querySelectorAll('#evalObsCards .eval-platform-card').forEach(function(c){{c.classList.toggle('selected',c.getAttribute('data-platform')===p);}});document.getElementById('evalObsFields').style.display='block';evalUpdateConfigBtn();}};
window.evalUpdateConfigBtn=function(){{document.querySelectorAll('#evalLLMFields [data-cred-key]').forEach(function(inp){{evalLLMCreds[inp.getAttribute('data-cred-key')]=inp.value.trim();}});var ci=document.getElementById('evalCustomModelInput');if(ci)evalCustomModelName=ci.value.trim();var modelOk=evalSelectedModel&&evalSelectedModel!=='__custom__';if(evalSelectedModel==='__custom__'&&evalCustomModelName)modelOk=true;var llmOk=evalSelectedLLM&&modelOk;var info=EV_LLM[evalSelectedLLM]||{{}};var fieldsOk=true;(info.fields||[]).forEach(function(f){{if(!evalLLMCreds[f.key])fieldsOk=false;}});var obsOk=evalSelectedObs&&(document.getElementById('evalObsApiKey')?.value.trim())&&(document.getElementById('evalObsProject')?.value.trim());document.getElementById('evalStep2Next').disabled=!(llmOk&&fieldsOk&&obsOk);}};
function renderMetricCards(){{var grid=document.getElementById('evalMetricCardsGrid');grid.innerHTML='';var search=(document.getElementById('evalMetricSearch')?.value||'').toLowerCase();var allMetrics=EV_METRICS.slice();Object.keys(evalMetricStates).forEach(function(k){{if(!allMetrics.some(function(m){{return m.name===k;}}))allMetrics.push({{name:k,cat:evalMetricStates[k].cat||'Custom',desc:evalMetricStates[k].desc||''}});}});var enabledCount=0;
allMetrics.forEach(function(m){{var st=evalMetricStates[m.name]||{{enabled:false,threshold:0.5,inverse:false,spans:[],expectedCol:''}};if(evalActiveTab!=='all'&&m.cat!==evalActiveTab)return;if(search&&m.name.toLowerCase().indexOf(search)===-1&&m.desc.toLowerCase().indexOf(search)===-1)return;if(st.enabled)enabledCount++;var badgeClass=m.cat==='Model Quality'?'emc-badge-mq':'emc-badge-custom';var sliderBg=st.inverse?'linear-gradient(90deg,#28a745 0%,#ffc107 50%,#dc3545 100%)':'linear-gradient(90deg,#dc3545 0%,#ffc107 50%,#28a745 100%)';
var card=document.createElement('div');card.className='emc-card'+(st.enabled?' enabled':'');card.setAttribute('data-metric',m.name);card.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><span class="emc-badge '+badgeClass+'">'+m.cat+'</span><div style="display:flex;align-items:center;gap:6px;"><label class="emc-toggle"><input type="checkbox" '+(st.enabled?'checked':'')+' onchange="toggleEvalMetric(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.checked)"><span class="slider"></span></label><button class="emc-dots" onclick="openSpanPopover(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this)" title="Settings">\\u22ee</button></div></div><h4 style="margin-bottom:6px;font-size:1rem;color:#333;">'+m.name+'</h4><p style="font-size:0.82rem;color:#888;margin-bottom:14px;line-height:1.4;">'+m.desc+'</p><div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;"><input type="checkbox" '+(st.inverse?'checked':'')+' onchange="toggleEvalInverse(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.checked)" style="accent-color:#A23B72;"><label style="font-size:0.85rem;color:#555;">Inverse</label></div><div style="display:flex;align-items:center;gap:10px;"><div style="flex:1;"><input type="range" class="emc-slider'+(st.inverse?' inverse-slider':'')+'" min="0" max="1" step="0.01" value="'+st.threshold+'" oninput="updateEvalThreshold(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.value)" style="background:'+sliderBg+';"></div><input type="number" min="0" max="1" step="0.01" value="'+st.threshold+'" onchange="updateEvalThreshold(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.value)" style="width:55px;padding:6px;border:1px solid #ccc;border-radius:6px;text-align:center;font-weight:700;font-size:0.95rem;"></div>';
grid.appendChild(card);}});
document.getElementById('evalMetricCount').textContent=enabledCount>0?enabledCount+' metric(s) enabled':'No metrics enabled';document.getElementById('evalMetricCount').style.color=enabledCount>0?'#28a745':'#dc3545';checkConfigNameFilled();}}
window.checkConfigNameFilled=function(){{var hasName=document.getElementById('evalConfigName')?.value.trim();var any=Object.keys(evalMetricStates).some(function(k){{return evalMetricStates[k].enabled;}});document.getElementById('evalStep3Next').disabled=!(any&&hasName);}};
window.filterEvalMetrics=function(cat,btn){{if(cat!==null){{evalActiveTab=cat;document.querySelectorAll('.emc-tab').forEach(function(b){{b.classList.remove('active');}});if(btn)btn.classList.add('active');}}renderMetricCards();}};
window.toggleEvalMetric=function(name,on){{if(!evalMetricStates[name])evalMetricStates[name]={{enabled:false,threshold:0.5,inverse:false,spans:[],expectedCol:''}};evalMetricStates[name].enabled=on;renderMetricCards();checkConfigNameFilled();}};
window.toggleSelectAllMetrics=function(on){{var allMetrics=EV_METRICS.slice();Object.keys(evalMetricStates).forEach(function(k){{if(!allMetrics.some(function(m){{return m.name===k;}}))allMetrics.push({{name:k,cat:evalMetricStates[k].cat||'Custom',desc:evalMetricStates[k].desc||''}});}});var search=(document.getElementById('evalMetricSearch')?.value||'').toLowerCase();allMetrics.forEach(function(m){{if(evalActiveTab!=='all'&&m.cat!==evalActiveTab)return;if(search&&m.name.toLowerCase().indexOf(search)===-1&&m.desc.toLowerCase().indexOf(search)===-1)return;if(!evalMetricStates[m.name])evalMetricStates[m.name]={{enabled:false,threshold:0.5,inverse:false,spans:[],expectedCol:''}};evalMetricStates[m.name].enabled=on;}});renderMetricCards();checkConfigNameFilled();}};
window.toggleEvalInverse=function(name,on){{if(!evalMetricStates[name])return;evalMetricStates[name].inverse=on;renderMetricCards();}};
window.updateEvalThreshold=function(name,val){{if(!evalMetricStates[name])return;evalMetricStates[name].threshold=parseFloat(val)||0;var card=document.querySelector('.emc-card[data-metric="'+name+'"]');if(card){{var slider=card.querySelector('input[type=range]');var num=card.querySelector('input[type=number]');if(slider)slider.value=val;if(num)num.value=val;}}}};
window.openSpanPopover=function(metricName,btn){{evalCurrentMetricForSpan=metricName;var pop=document.getElementById('spanPopover');var rect=btn.getBoundingClientRect();pop.style.left=Math.min(rect.left,window.innerWidth-340)+'px';pop.style.top=(rect.bottom+4)+'px';pop.style.display='block';document.getElementById('spanInput').value='';renderSpanList();var sel=document.getElementById('spanExpectedCol');sel.innerHTML='<option value="">-- None --</option>';evalExtraColumns.forEach(function(col){{var o=document.createElement('option');o.value=col;o.textContent=col;if(evalMetricStates[metricName]&&evalMetricStates[metricName].expectedCol===col)o.selected=true;sel.appendChild(o);}});}};
window.updateExpectedCol=function(){{if(!evalCurrentMetricForSpan)return;var sel=document.getElementById('spanExpectedCol');if(!evalMetricStates[evalCurrentMetricForSpan])return;evalMetricStates[evalCurrentMetricForSpan].expectedCol=sel.value;}};
window.closeSpanPopover=function(){{document.getElementById('spanPopover').style.display='none';evalCurrentMetricForSpan=null;}};
window.addSpanName=function(){{var inp=document.getElementById('spanInput');var v=inp.value.trim();if(!v||!evalCurrentMetricForSpan)return;if(!evalMetricStates[evalCurrentMetricForSpan])return;if(evalMetricStates[evalCurrentMetricForSpan].spans.indexOf(v)===-1)evalMetricStates[evalCurrentMetricForSpan].spans.push(v);inp.value='';renderSpanList();}};
function renderSpanList(){{var c=document.getElementById('spanList');if(!evalCurrentMetricForSpan){{c.innerHTML='';return;}}var spans=evalMetricStates[evalCurrentMetricForSpan]?.spans||[];c.innerHTML=spans.length===0?'<p style="color:#aaa;font-size:0.82rem;">No span names configured</p>':'';spans.forEach(function(s,i){{c.innerHTML+='<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 8px;background:#f8fafc;border-radius:6px;margin-bottom:4px;"><span style="font-size:0.85rem;">'+s+'</span><button onclick="removeSpanName('+i+')" style="background:none;border:none;color:#dc3545;cursor:pointer;font-weight:700;">\\u2715</button></div>';}});}}
window.removeSpanName=function(i){{if(!evalCurrentMetricForSpan)return;evalMetricStates[evalCurrentMetricForSpan].spans.splice(i,1);renderSpanList();}};
document.addEventListener('click',function(e){{var pop=document.getElementById('spanPopover');if(pop&&pop.style.display==='block'&&!pop.contains(e.target)&&!e.target.classList.contains('emc-dots'))pop.style.display='none';}});
window.openCustomMetricModal=function(){{document.getElementById('customMetricModal').style.display='block';switchCMTab('custom');renderStaticList();}};
window.closeCustomMetricModal=function(){{document.getElementById('customMetricModal').style.display='none';}};
window.switchCMTab=function(tab){{document.getElementById('cmTab1').style.background=tab==='custom'?'#2E86AB':'white';document.getElementById('cmTab1').style.color=tab==='custom'?'white':'#718096';document.getElementById('cmTab2').style.background=tab==='static'?'#2E86AB':'white';document.getElementById('cmTab2').style.color=tab==='static'?'white':'#718096';document.getElementById('cmCustomPanel').style.display=tab==='custom'?'block':'none';document.getElementById('cmStaticPanel').style.display=tab==='static'?'block':'none';}};
window.addCustomEvalMetric=function(){{var nm=document.getElementById('cmName').value.trim();var ds=document.getElementById('cmDesc').value.trim();var cat=document.getElementById('cmCategory').value;var th=parseFloat(document.getElementById('cmThreshold').value)||0.5;var inv=document.getElementById('cmInverse').checked;var prompt=document.getElementById('cmPrompt').value.trim();if(!nm||!ds){{alert('Name and Description are required.');return;}}evalMetricStates[nm]={{enabled:true,threshold:th,inverse:inv,spans:[],expectedCol:'',cat:cat,desc:ds,prompt:prompt}};document.getElementById('cmName').value='';document.getElementById('cmDesc').value='';document.getElementById('cmPrompt').value='';closeCustomMetricModal();renderMetricCards();checkConfigNameFilled();}};
function renderStaticList(){{var c=document.getElementById('cmStaticList');c.innerHTML='';EV_STATIC.forEach(function(m){{var already=!!evalMetricStates[m.name];var d=document.createElement('div');d.className='cm-static-item'+(already?' selected':'');d.innerHTML='<input type="checkbox" '+(already?'checked disabled':'')+' data-static-name="'+m.name+'"><div><div style="font-weight:600;font-size:0.9rem;">'+m.name+'</div><div style="font-size:0.8rem;color:#888;margin-top:2px;">'+m.desc+'</div></div>';if(!already)d.onclick=function(e){{if(e.target.tagName==='INPUT')return;var cb=d.querySelector('input');cb.checked=!cb.checked;d.classList.toggle('selected',cb.checked);}};c.appendChild(d);}});}}
window.addSelectedStaticMetrics=function(){{document.querySelectorAll('#cmStaticList input[data-static-name]:checked:not(:disabled)').forEach(function(cb){{var nm=cb.getAttribute('data-static-name');var m=EV_STATIC.find(function(s){{return s.name===nm;}});if(m)evalMetricStates[nm]={{enabled:true,threshold:0.5,inverse:false,spans:[],expectedCol:'',cat:'Static',desc:m.desc}};}});closeCustomMetricModal();renderMetricCards();}};
function buildEvalSummary(){{var enabled=[];Object.keys(evalMetricStates).forEach(function(k){{if(evalMetricStates[k].enabled)enabled.push({{name:k,threshold:evalMetricStates[k].threshold,inverse:evalMetricStates[k].inverse,spans:evalMetricStates[k].spans,expectedCol:evalMetricStates[k].expectedCol||''}});}});var cfgName=document.getElementById('evalConfigName')?.value.trim()||'\\u2014';var cfgDesc=document.getElementById('evalConfigDesc')?.value.trim()||'';var displayModel=evalSelectedModel==='__custom__'?evalCustomModelName:evalSelectedModel;
var h='<div style="background:#f8fafc;border-radius:12px;padding:24px;border:1px solid #e2e8f0;"><h4 style="color:#2E86AB;margin-bottom:16px;">Evaluation Configuration</h4>';
h+='<div class="eval-config-row"><span class="eval-config-label">Configuration Name</span><span class="eval-config-value" style="font-weight:700;color:#2E86AB;">'+cfgName+'</span></div>';
if(cfgDesc)h+='<div class="eval-config-row"><span class="eval-config-label">Description</span><span class="eval-config-value">'+cfgDesc+'</span></div>';
h+='<div class="eval-config-row"><span class="eval-config-label">Dataset</span><span class="eval-config-value">'+(evalFileData?evalFileData.name+' ('+evalFileData.rows+' rows)':'\\u2014')+'</span></div>';
h+='<div class="eval-config-row"><span class="eval-config-label">LLM Provider</span><span class="eval-config-value">'+(evalSelectedLLM&&displayModel?evalSelectedLLM+' / '+displayModel:'\\u2014')+'</span></div>';
h+='<div class="eval-config-row"><span class="eval-config-label">Observability</span><span class="eval-config-value">'+(evalSelectedObs||'\\u2014')+' \\u2014 '+(document.getElementById('evalObsProject')?.value||'\\u2014')+'</span></div>';
h+='<div class="eval-config-row"><span class="eval-config-label">Metrics ('+enabled.length+')</span><span class="eval-config-value">';
enabled.forEach(function(m){{h+='<span style="display:inline-block;background:#e3f2fd;color:#1565C0;padding:3px 10px;border-radius:12px;font-size:0.82rem;font-weight:600;margin:2px 4px;">'+m.name+' ('+m.threshold+')'+(m.inverse?' \\u2193':'')+'</span>';}});
h+='</span></div></div>';document.getElementById('evalConfigSummary').innerHTML=h;document.getElementById('evalRunSection').style.display='block';document.getElementById('evalInProgress').style.display='none';}}
window.startEvaluation=function(){{document.getElementById('evalRunSection').style.display='none';document.getElementById('evalInProgress').style.display='block';document.getElementById('evalStep4Back').disabled=true;var progress=0;var timer=setInterval(function(){{progress+=Math.random()*8+2;if(progress>92)progress=92;document.getElementById('evalProgressFill').style.width=progress+'%';}},800);}};
window.addEventListener('click',function(e){{if(e.target===document.getElementById('customMetricModal'))closeCustomMetricModal();}});
}})();
</script>"""
''')

    # ==================== Update templates/js_evaluations_wizard.py reference in tabs ====================
    w("tabs/mqa_evaluations_wizard.py", r'''"""Model Quality Assurance - Evaluations Wizard HTML generator. Fully self-contained."""


def generate_evaluations_wizard_html(all_metrics):
    from templates.js_evaluations_wizard import get_evaluations_wizard_html
    return get_evaluations_wizard_html(all_metrics)
''')

    print(f"\n{'='*60}")
    print("Part 7 COMPLETE: Evaluations Wizard - fully self-contained")
    print(f"{'='*60}")
    print("Next: Run build_part8.py for the master HTML assembly")
    print("After Part 8, NO original file will be needed at all!")

if __name__ == "__main__":
    build()
