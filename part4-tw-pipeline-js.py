#!/usr/bin/env python3
"""
Part 4: Trustworthy JS files + Pipeline JS
Run: python build_part4.py
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
    print(f"Part 4: Building TW JS + Pipeline JS in ./{BASE}/templates/\n")

    # ==================== templates/js_tw_usecase.py ====================
    # This is the EXACT _generate_tw_usecase_js content
    w("templates/js_tw_usecase.py", r'''"""Trustworthy Usecase Assessment JavaScript - EXACT original code."""
import json


def get_tw_usecase_js():
    tw_metrics = [
        {"name":"SKU Priority Bias","cat":"Bias Evaluation","desc":"Detects if the system unfairly prioritizes certain SKUs over others based on non-relevant attributes."},
        {"name":"SKU Service Level Bias","cat":"Bias Evaluation","desc":"Checks whether service level agreements are applied inconsistently across different SKUs."},
        {"name":"Vendor Geographic Bias","cat":"Bias Evaluation","desc":"Detects if vendor selection or scoring is unfairly influenced by geographic location."},
        {"name":"Economic Value Bias","cat":"Bias Evaluation","desc":"Checks if higher-value items receive disproportionately better treatment in routing or prioritization."},
        {"name":"Geographic Reasoning Inconsistency Bias","cat":"Bias Evaluation","desc":"Identifies inconsistent reasoning when handling geographically similar scenarios."},
        {"name":"SKU Differential Treatment Bias","cat":"Bias Evaluation","desc":"Detects if similar SKUs receive significantly different handling without justification."},
        {"name":"Criminality","cat":"Trustworthy","desc":"Detects content that promotes, glorifies, or provides instructions for criminal activities."},
        {"name":"Insensitivity","cat":"Trustworthy","desc":"Identifies responses that are culturally, emotionally, or socially insensitive."},
        {"name":"Stereotype","cat":"Trustworthy","desc":"Detects stereotypical assumptions or generalizations based on protected attributes."},
        {"name":"Profanity","cat":"Trustworthy","desc":"Identifies the presence of profane, vulgar, or offensive language in outputs."},
        {"name":"PII Detection","cat":"Trustworthy","desc":"Checks if personally identifiable information is exposed or generated in responses."},
        {"name":"Unethical","cat":"Trustworthy","desc":"Detects outputs that suggest or encourage unethical behavior or decision-making."},
        {"name":"Decision Traceability","cat":"Explainability","desc":"Evaluates whether each decision can be traced back to specific inputs and reasoning steps."},
        {"name":"Explanation Consistency","cat":"Explainability","desc":"Checks if explanations remain consistent when similar queries are asked differently."},
        {"name":"Evidence Grounding","cat":"Explainability","desc":"Verifies that explanations are grounded in actual data and evidence from the context."},
        {"name":"Explanation Completeness","cat":"Explainability","desc":"Assesses whether all relevant factors are addressed in the explanation."},
        {"name":"Explanation Faithfulness","cat":"Explainability","desc":"Measures if the explanation accurately reflects the actual reasoning process used."},
        {"name":"Decision Factor Visibility","cat":"Explainability","desc":"Checks if the key factors influencing a decision are clearly visible and stated."},
        {"name":"Explanation Transparency","cat":"Explainability","desc":"Evaluates how transparent and understandable the explanation is for the end user."},
    ]
    return f"""<script>
(function(){{
var TW_METRICS={json.dumps(tw_metrics)};
var twMetricStates={{}};var twActiveTab='all';
TW_METRICS.forEach(function(m){{twMetricStates[m.name]={{enabled:false,threshold:0.5,inverse:false}};}});
window._twMetricStatesRef=twMetricStates;

window.suggestTWMetrics=function(){{
var desc=document.getElementById('twUcDesc')?.value.trim();var users=document.getElementById('twUcUsers')?.value.trim();
if(!desc){{alert('Please provide a usecase description.');return;}}
document.getElementById('twUsecaseForm').style.display='none';document.getElementById('twSuggestLoading').style.display='block';document.getElementById('twSuggestResults').style.display='none';
var msgs=['Reading usecase description...','Analyzing end user profiles...','Evaluating compliance requirements...','Mapping bias risk vectors...','Identifying explainability needs...','Generating metric recommendations...','Finalizing suggestions...'];
var progress=0,msgIdx=0;
var timer=setInterval(function(){{progress+=Math.random()*12+3;if(progress>95)progress=95;document.getElementById('twSuggestFill').style.width=progress+'%';
if(msgIdx<msgs.length-1&&Math.random()>0.45){{msgIdx++;document.getElementById('twSuggestMsg').textContent=msgs[msgIdx];}}}},600);
setTimeout(function(){{clearInterval(timer);document.getElementById('twSuggestFill').style.width='100%';document.getElementById('twSuggestMsg').textContent='Done!';
setTimeout(function(){{
TW_METRICS.forEach(function(m){{twMetricStates[m.name].enabled=true;}});
document.getElementById('twSuggestLoading').style.display='none';document.getElementById('twSuggestResults').style.display='block';
renderTWMetricCards();}},400);
}},4500);
}};

function renderTWMetricCards(){{
var grid=document.getElementById('twMetricCardsGrid');grid.innerHTML='';
var search=(document.getElementById('twMetricSearch')?.value||'').toLowerCase();
var enabledCount=0;
TW_METRICS.forEach(function(m){{
var st=twMetricStates[m.name]||{{enabled:false,threshold:0.5,inverse:false}};
if(twActiveTab!=='all'&&m.cat!==twActiveTab)return;
if(search&&m.name.toLowerCase().indexOf(search)===-1&&m.desc.toLowerCase().indexOf(search)===-1)return;
if(st.enabled)enabledCount++;
var badgeClass=m.cat==='Bias Evaluation'?'tw-badge-bias':(m.cat==='Trustworthy'?'tw-badge-trust':'tw-badge-explain');
var sliderBg=st.inverse?'linear-gradient(90deg,#28a745 0%,#ffc107 50%,#dc3545 100%)':'linear-gradient(90deg,#dc3545 0%,#ffc107 50%,#28a745 100%)';
var card=document.createElement('div');card.className='tw-card'+(st.enabled?' enabled':'');card.setAttribute('data-metric',m.name);
card.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><span class="tw-badge '+badgeClass+'">'+m.cat+'</span><label class="emc-toggle"><input type="checkbox" '+(st.enabled?'checked':'')+' onchange="toggleTWMetric(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.checked)"><span class="slider"></span></label></div>'
+'<h4 style="margin-bottom:6px;font-size:1rem;color:#333;">'+m.name+'</h4><p style="font-size:0.82rem;color:#888;margin-bottom:14px;line-height:1.4;">'+m.desc+'</p>'
+'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;"><input type="checkbox" id="twinv_'+m.name.replace(/\\s/g,'_')+'" '+(st.inverse?'checked':'')+' onchange="toggleTWInverse(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.checked)" style="accent-color:#A23B72;"><label for="twinv_'+m.name.replace(/\\s/g,'_')+'" style="font-size:0.85rem;color:#555;">Inverse</label></div>'
+'<div style="display:flex;align-items:center;gap:10px;"><div style="flex:1;"><input type="range" class="emc-slider'+(st.inverse?' inverse-slider':'')+'" min="0" max="1" step="0.01" value="'+st.threshold+'" oninput="updateTWThreshold(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.value)" style="background:'+sliderBg+';"><div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#aaa;margin-top:2px;"><span>0</span><span>1</span></div></div><input type="number" min="0" max="1" step="0.01" value="'+st.threshold+'" onchange="updateTWThreshold(\\''+m.name.replace(/'/g,"\\\\'")+'\\',this.value)" style="width:55px;padding:6px;border:1px solid #ccc;border-radius:6px;text-align:center;font-weight:700;font-size:0.95rem;"></div>';
grid.appendChild(card);}});
document.getElementById('twMetricCount').textContent=enabledCount>0?enabledCount+' metric(s) enabled':'No metrics enabled';
document.getElementById('twMetricCount').style.color=enabledCount>0?'#28a745':'#dc3545';
}}

window.filterTWMetrics=function(cat,btn){{if(cat!==null){{twActiveTab=cat;document.querySelectorAll('.tw-mc-tab').forEach(function(b){{b.classList.remove('active');}});if(btn)btn.classList.add('active');}}renderTWMetricCards();}};

window.downloadTWConfig=function(){{
var biasMetrics=[],explainMetrics=[],trustMetrics=[];
Object.keys(twMetricStates).forEach(function(k){{
if(!twMetricStates[k].enabled)return;
var m=TW_METRICS.find(function(x){{return x.name===k;}});
if(!m)return;
if(m.cat==='Bias Evaluation')biasMetrics.push(k);
else if(m.cat==='Explainability')explainMetrics.push(k);
else if(m.cat==='Trustworthy')trustMetrics.push(k);
}});
if(biasMetrics.length===0&&explainMetrics.length===0&&trustMetrics.length===0){{alert('No metrics enabled. Please enable at least one metric.');return;}}
var csv='Category,Metrics\\n';
csv+='"Bias Evaluation","'+biasMetrics.join(', ')+'"\\n';
csv+='"Explainability","'+explainMetrics.join(', ')+'"\\n';
csv+='"Trustworthy","'+trustMetrics.join(', ')+'"\\n';
var b=new Blob([csv],{{type:'text/csv'}}),u=URL.createObjectURL(b),a=document.createElement('a');
a.href=u;a.download='trustworthy_metrics_config.csv';a.click();URL.revokeObjectURL(u);
}};
window.toggleTWMetric=function(name,on){{if(twMetricStates[name])twMetricStates[name].enabled=on;renderTWMetricCards();}};
window.toggleTWInverse=function(name,on){{if(twMetricStates[name])twMetricStates[name].inverse=on;renderTWMetricCards();}};
window.updateTWThreshold=function(name,val){{if(!twMetricStates[name])return;twMetricStates[name].threshold=parseFloat(val)||0;
var card=document.querySelector('.tw-card[data-metric="'+name+'"]');if(card){{var sl=card.querySelector('input[type=range]');var nm=card.querySelector('input[type=number]');if(sl)sl.value=val;if(nm)nm.value=val;}}}};
}})();
</script>"""
''')

    # ==================== templates/js_tw_bias.py ====================
    # This is the EXACT _generate_tw_bias_eval_js content
    w("templates/js_tw_bias.py", r'''"""Trustworthy Bias Evaluation JavaScript - EXACT original code."""


def get_tw_bias_eval_js():
    return """<script>
(function(){
var twBiasData=[];var twBiasGroups=[];var twBiasEvalData=[];var twBiasConfigMetrics=[];

window.showTWBiasSubTab=function(tab){
['twBiasUpload','twBiasResults','twBiasAnalytics'].forEach(function(id){var el=document.getElementById(id);if(el)el.style.display=id===tab?'block':'none';});
var gs=document.getElementById('twBiasGroupingSection');if(gs)gs.style.display=tab==='twBiasUpload'?'block':'none';
var activeBtn=null;
if(tab==='twBiasUpload')activeBtn=document.getElementById('twBias-btn-upload');
else if(tab==='twBiasResults')activeBtn=document.getElementById('twBias-btn-results');
else if(tab==='twBiasAnalytics')activeBtn=document.getElementById('twBias-btn-analytics');
['twBias-btn-upload','twBias-btn-results','twBias-btn-analytics'].forEach(function(bid){var btn=document.getElementById(bid);if(btn){btn.style.borderBottomColor='transparent';btn.style.color='#718096';}});
if(activeBtn){activeBtn.style.borderBottomColor='#e65100';activeBtn.style.color='#e65100';}
if(tab==='twBiasAnalytics')renderTWBiasAnalytics();
};

window.twBiasHandleDrop=function(e){if(e.dataTransfer.files.length>0)twBiasProcessFile(e.dataTransfer.files[0]);};
window.twBiasHandleUpload=function(inp){if(inp.files.length>0)twBiasProcessFile(inp.files[0]);};
window.twBiasHandleConfigDrop=function(e){if(e.dataTransfer.files.length>0)twBiasProcessConfig(e.dataTransfer.files[0]);};
window.twBiasHandleConfigUpload=function(inp){if(inp.files.length>0)twBiasProcessConfig(inp.files[0]);};

window.twBiasStartGrouping=function(){
if(twBiasData.length===0){alert('Please upload a dataset first.');return;}
document.getElementById('twBiasGroupingSection').style.display='block';
twBiasRunGrouping();
};

function twBiasProcessConfig(file){
var st=document.getElementById('twBiasConfigStatus');
var reader=new FileReader();
reader.onload=function(e){
var lines=e.target.result.split('\n').filter(function(l){return l.trim();});
twBiasConfigMetrics=[];
lines.forEach(function(line,idx){
if(idx===0&&line.toLowerCase().indexOf('category')!==-1)return;
var parts=line.split(',');if(parts.length>=2){
var cat=parts[0].replace(/"/g,'').trim();
var metrics=parts.slice(1).join(',').replace(/"/g,'').trim();
if(cat==='Bias Evaluation'&&metrics){
twBiasConfigMetrics=metrics.split(',').map(function(m){return m.trim();}).filter(function(m){return m;});
}}
});
if(twBiasConfigMetrics.length>0){
st.innerHTML='<span style="color:#28a745;font-weight:600;">\u2713 '+twBiasConfigMetrics.length+' bias metrics loaded</span>';
}else{
st.innerHTML='<span style="color:#F18F01;font-weight:600;">\u26a0 No bias metrics found in config. Using defaults.</span>';
}
};
reader.readAsText(file);
};

function twBiasProcessFile(file){
    var st=document.getElementById('twBiasUploadStatus');
    var nm=file.name.toLowerCase();
    if(!nm.endsWith('.csv')&&!nm.endsWith('.xlsx')&&!nm.endsWith('.xls')){
        st.innerHTML='<span style="color:#dc3545;">Unsupported format</span>';return;
    }
    st.innerHTML='<span class="spinner"></span> Uploading...';
    var fd=new FormData();fd.append('file',file);
    fetch('/api/upload-bias-data',{method:'POST',body:fd})
    .then(function(r){return r.json();})
    .then(function(d){
        if(d.success){
            twBiasData=d.rows;
            twBiasData._result_col=d.result_col;
            twBiasData._columns=d.columns;
            st.innerHTML='<span style="color:#28a745;font-weight:600;">\u2713 '+d.total+' rows uploaded successfully.</span>';
            var pv=document.getElementById('twBiasPreview');
            pv.style.display='block';
            pv.innerHTML='<div style="padding:12px 16px;background:#fff3e0;border:1px solid #ffe0b2;border-radius:8px;color:#e65100;font-weight:600;">\u2713 '+d.total+' rows uploaded successfully.</div>';
            document.getElementById('twBiasGroupBtn').disabled=false;document.getElementById('twBiasEvalBtnUpload').disabled=false;
        }else{
            st.innerHTML='<span style="color:#dc3545;">\u2717 '+(d.error||'Failed')+'</span>';
        }
    }).catch(function(e){st.innerHTML='<span style="color:#dc3545;">\u2717 '+e+'</span>';});
}

function twBiasRunGrouping(){
    var loading=document.getElementById('twBiasGroupLoading');
    var results=document.getElementById('twBiasGroupResults');
    loading.style.display='block';results.innerHTML='';
    var criteria=(document.getElementById('twBiasGroupCriteria')?.value||'').trim();
    document.getElementById('twBiasGroupMsg').textContent='Sending queries to LLM for semantic analysis...';
    var cols=twBiasData._columns||[];
    var tcCol=cols.find(function(c){var n=c.trim().toLowerCase();return n==='tc id'||n==='tc_id'||n==='tcid'||n==='id';});
    var inputCol=cols.find(function(c){var n=c.trim().toLowerCase();return n==='input query'||n==='input'||n==='query'||n==='question';});
    if(!tcCol)tcCol=cols[0]||'TC ID';
    if(!inputCol)inputCol=cols[1]||'Input Query';
    var inputsPayload=twBiasData.map(function(row){
        return{tc_id:row[tcCol]||'',input:row[inputCol]||''};
    });
    fetch('/api/bias-grouping',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({inputs:inputsPayload,criteria:criteria})
    })
    .then(function(r){return r.json();})
    .then(function(d){
        loading.style.display='none';
        if(!d.success){
            var errHtml='<div style="border:2px solid #dc3545;border-radius:10px;padding:20px;background:#fff5f5;">';
            errHtml+='<div style="font-weight:700;color:#dc3545;font-size:1rem;margin-bottom:10px;">\u2717 Azure OpenAI Error</div>';
            errHtml+='<div style="background:#1e1e1e;color:#f8f8f2;padding:14px;border-radius:8px;font-family:monospace;font-size:0.82rem;white-space:pre-wrap;word-break:break-word;">';
            errHtml+=twEsc(d.error||'Unknown error');
            errHtml+='</div>';
            if(d.raw_response){
                errHtml+='<div style="margin-top:12px;"><strong style="color:#555;font-size:0.82rem;">Raw LLM Response:</strong>';
                errHtml+='<div style="background:#f5f5f5;padding:10px;border-radius:6px;font-family:monospace;font-size:0.78rem;white-space:pre-wrap;margin-top:4px;">'+twEsc(d.raw_response)+'</div></div>';
            }
            errHtml+='</div>';
            results.innerHTML=errHtml;
            return;
        }
        var colorPalette=['#e65100','#1565C0','#2e7d32','#7b1fa2','#00838f','#ad1457','#4527a0','#00695c','#558b2f','#6d4c41'];
        twBiasGroups=[];
        d.groups.forEach(function(g,gi){
            var color=colorPalette[gi%colorPalette.length];
            var indices=[];
            g.tc_ids.forEach(function(tc){
                var idx=twBiasData.findIndex(function(r){return r.tc_id===tc;});
                if(idx!==-1)indices.push(idx);
            });
            twBiasGroups.push({id:'G'+(gi+1),tcIds:g.tc_ids,indices:indices,bias:g.group_name,reasoning:g.reasoning,color:color,count:g.count});
        });
        var individuals=d.individuals||[];
        var h='';
        if(twBiasGroups.length>0){
            h+='<h4 style="color:#333;margin-bottom:16px;">Identified Bias Groups ('+twBiasGroups.length+')</h4>';
            h+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-bottom:24px;">';
            twBiasGroups.forEach(function(g){
                h+='<div style="border:2px solid '+g.color+';border-radius:12px;padding:16px;background:white;">';
                h+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">';
                h+='<span style="font-weight:700;font-size:1.0rem;color:'+g.color+';">'+g.id+': '+twEsc(g.bias)+'</span>';
                h+='<span style="background:'+g.color+';color:white;padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">'+g.count+' queries</span>';
                h+='</div>';
                if(g.reasoning){h+='<div style="font-size:0.8rem;color:#555;margin-bottom:10px;padding:8px;background:#f9f9f9;border-radius:6px;border-left:3px solid '+g.color+';"><strong>Why:</strong> '+twEsc(g.reasoning)+'</div>';}
                h+='<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;">';
                g.tcIds.forEach(function(tc){h+='<span style="background:#f0f0f0;padding:4px 10px;border-radius:6px;font-size:0.82rem;font-weight:600;color:#333;">'+twEsc(tc)+'</span>';});
                h+='</div>';
                var samples=g.indices.slice(0,2);
                samples.forEach(function(idx){
                    var sampleText=twBiasData[idx][inputCol]||twBiasData[idx].input||'';
                    h+='<div style="background:#fafbfc;padding:8px 10px;border-radius:6px;margin-bottom:4px;font-size:0.8rem;color:#555;border-left:3px solid '+g.color+';">';
                    h+=twEsc(sampleText).substring(0,150);
                    h+='</div>';
                });
                if(g.indices.length>2)h+='<div style="font-size:0.78rem;color:#888;margin-top:4px;">...and '+(g.indices.length-2)+' more</div>';
                h+='</div>';
            });
            h+='</div>';
        }
        if(individuals.length>0){
            h+='<h4 style="color:#333;margin-bottom:12px;">\ud83d\udccc Individual Queries ('+individuals.length+')</h4>';
            h+='<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">';
            individuals.forEach(function(ind){
                h+='<div style="border:1px solid #e2e8f0;border-radius:8px;padding:10px 14px;background:#fafbfc;max-width:340px;">';
                h+='<span style="font-weight:700;color:#555;font-size:0.85rem;">'+twEsc(ind.tc_id)+'</span>';
                h+='<div style="font-size:0.78rem;color:#888;margin-top:4px;">'+twEsc(ind.input).substring(0,100)+'</div>';
                h+='</div>';
            });
            h+='</div>';
        }
        h+='<div style="background:#f0f4ff;border:1px solid #c5cae9;border-radius:8px;padding:14px;margin-top:8px;">';
        h+='<span style="font-weight:600;color:#333;">Summary:</span> ';
        h+='<span style="color:#555;">'+twBiasGroups.length+' bias group(s) identified across '+twBiasData.length+' queries. '+individuals.length+' individual query/queries.</span>';
        if(criteria){h+='<br><span style="font-size:0.82rem;color:#7b1fa2;margin-top:4px;display:inline-block;">Grouping criteria applied: "'+twEsc(criteria)+'"</span>';}
        h+='</div>';
        results.innerHTML=h;
    })
    .catch(function(e){
        loading.style.display='none';
        results.innerHTML='<div style="color:#dc3545;padding:16px;font-weight:600;">\u2717 Request failed: '+twEsc(String(e))+'</div>';
    });
}

window.twBiasRunEval=function(){
    if(!twBiasData||twBiasData.length===0){alert('Please upload a dataset first.');return;}
    showTWBiasSubTab('twBiasResults');
    var loading=document.getElementById('twBiasEvalLoading');
    var results=document.getElementById('twBiasEvalResults');
    loading.style.display='block';
    results.innerHTML='';
    var msgs=['Loading bias evaluation data...','Reading Bias Category column...','Computing pass/fail counts...','Preparing metrics summary...','Rendering results...'];
    var msgIdx=0;var progress=0;
    var timer=setInterval(function(){
        progress+=Math.random()*18+8;
        if(progress>92)progress=92;
        document.getElementById('twBiasEvalFill').style.width=progress+'%';
        if(msgIdx<msgs.length-1&&Math.random()>0.4){msgIdx++;document.getElementById('twBiasEvalMsg').textContent=msgs[msgIdx];}
    },500);
    setTimeout(function(){
        clearInterval(timer);
        document.getElementById('twBiasEvalFill').style.width='100%';
        document.getElementById('twBiasEvalMsg').textContent='Done!';
        loading.style.display='none';
        var resultCol=twBiasData._result_col||'Result';
        var columns=twBiasData._columns||[];
        var rows=twBiasData;
        var biasAuditCols=columns.filter(function(c){return c.trim().toLowerCase().indexOf('bias audit')!==-1;});
        twBiasEvalData=rows.map(function(r){
            var res=(r[resultCol]||'').trim().toLowerCase();
            var auditResults={};
            biasAuditCols.forEach(function(col){
                var val=(r[col]||'').trim().toLowerCase();
                auditResults[col]=val.indexOf('pass')===0?'Pass':'Fail';
            });
            return{result: res.indexOf('pass')===0?'Pass':'Fail',audit_results: auditResults,raw: r};
        });
        twBiasEvalData._biasAuditCols=biasAuditCols;
        var passCount=twBiasEvalData.filter(function(r){return r.result==='Pass';}).length;
        var failCount=twBiasEvalData.length-passCount;
        var h='<div style="display:flex;gap:16px;margin-bottom:20px;flex-wrap:wrap;">';
        h+='<div style="padding:14px 24px;background:#e8f5e9;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#28a745;">'+passCount+'</div><div style="font-size:0.82rem;color:#2e7d32;font-weight:600;">Overall Passed</div></div>';
        h+='<div style="padding:14px 24px;background:#ffebee;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#dc3545;">'+failCount+'</div><div style="font-size:0.82rem;color:#c62828;font-weight:600;">Overall Failed</div></div>';
        h+='<div style="padding:14px 24px;background:#fff3e0;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#e65100;">'+(passCount/(twBiasEvalData.length||1)*100).toFixed(1)+'%</div><div style="font-size:0.82rem;color:#e65100;font-weight:600;">Overall Pass Rate</div></div>';
        h+='</div>';
        h+='<div class="table-container" style="max-height:500px;">';
        h+='<table class="modern-table"><thead><tr>';
        columns.forEach(function(c){
            var cl=c.trim().toLowerCase();
            var isStatus=cl.indexOf('bias audit')!==-1||cl.indexOf('bias result')!==-1||cl==='result';
            var al=isStatus?' style="text-align:center;"':'';
            h+='<th'+al+'>'+twEsc(c)+'</th>';
        });
        h+='</tr></thead><tbody>';
        rows.forEach(function(r){
            h+='<tr>';
            columns.forEach(function(c){
                var val=r[c]||'';
                var cl=c.trim().toLowerCase();
                var isOverallResult=c===resultCol||cl.indexOf('bias result')!==-1;
                var isAuditCol=cl.indexOf('bias audit')!==-1;
                if(isOverallResult){
                    var isPass=val.trim().toLowerCase().indexOf('pass')===0;
                    var sc=isPass?'#28a745':'#dc3545';
                    var lb=isPass?'Pass':'Fail';
                    h+='<td style="text-align:center;"><span style="padding:4px 12px;border-radius:12px;font-size:0.8rem;font-weight:700;color:white;background:'+sc+';">'+lb+'</span></td>';
                }else if(isAuditCol){
                    var trimmed=val.trim();
                    var isPass=trimmed.toLowerCase().indexOf('pass')===0;
                    var sc=isPass?'#28a745':'#dc3545';
                    var lb=isPass?'Pass':'Fail';
                    var reason='';
                    var dashIdx=-1;
                    var separators=[' \u2014 ',' - ',' \u2013 ','\u2014','\u2013','-'];
                    var sepLen=1;
                    for(var si=0;si<separators.length;si++){
                        var idx=trimmed.indexOf(separators[si]);
                        if(idx!==-1){dashIdx=idx;sepLen=separators[si].length;break;}
                    }
                    if(dashIdx!==-1)reason=trimmed.substring(dashIdx+sepLen).trim();
                    h+='<td><span style="padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;color:white;background:'+sc+';margin-right:8px;">'+lb+'</span>';
                    if(reason)h+='<span style="font-size:0.82rem;color:#555;">'+twEsc(reason)+'</span>';
                    h+='</td>';
                }else{
                    h+='<td>'+twEsc(val).substring(0,150)+'</td>';
                }
            });
            h+='</tr>';
        });
        h+='</tbody></table></div>';
        results.innerHTML=h;
    }, 30000);
};

window.twBiasDownloadResults=function(){
if(twBiasEvalData.length===0){alert('No evaluation results yet.');return;}
var csv='TC ID,Input,Expected Output,Bias Category,Score,Result,Explanation\\n';
twBiasEvalData.forEach(function(r){
csv+='"'+twCe(r.tc_id)+'","'+twCe(r.input)+'","'+twCe(r.expected_output)+'","'+twCe(r.bias_category)+'","'+r.score.toFixed(2)+'","'+twCe(r.result)+'","'+twCe(r.explanation)+'"\\n';
});
var b=new Blob([csv],{type:'text/csv'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='bias_evaluation_results.csv';a.click();URL.revokeObjectURL(u);
};

function renderTWBiasAnalytics(){
    if(twBiasEvalData.length===0){
        document.getElementById('twBiasAnalyticsEmpty').style.display='block';
        document.getElementById('twBiasAnalyticsContent').style.display='none';
        return;
    }
    document.getElementById('twBiasAnalyticsEmpty').style.display='none';
    document.getElementById('twBiasAnalyticsContent').style.display='block';
    var biasAuditCols=twBiasEvalData._biasAuditCols||[];
    var auditMap={};
    biasAuditCols.forEach(function(col){
        var shortName=col.replace(/\\s*bias\\s*audit\\s*/i,'').trim();
        if(!shortName)shortName=col;
        auditMap[shortName]={pass:0,fail:0,col:col};
        twBiasEvalData.forEach(function(r){
            if(r.audit_results&&r.audit_results[col]==='Pass')auditMap[shortName].pass++;
            else auditMap[shortName].fail++;
        });
    });
    var overallPass=twBiasEvalData.filter(function(r){return r.result==='Pass';}).length;
    var overallFail=twBiasEvalData.length-overallPass;
    auditMap['Overall']={pass:overallPass,fail:overallFail};
    var labels=Object.keys(auditMap);
    var passVals=labels.map(function(l){return auditMap[l].pass;});
    var failVals=labels.map(function(l){return auditMap[l].fail;});
    Plotly.newPlot('twBiasPassFailChart',[
        {x:labels,y:passVals,name:'Pass',type:'bar',marker:{color:'#28a745'}},
        {x:labels,y:failVals,name:'Fail',type:'bar',marker:{color:'#dc3545'}}
    ],{barmode:'group',margin:{t:30,b:120,l:50,r:20},xaxis:{tickangle:-30,title:'Bias Audit Type'},yaxis:{title:'Count'},legend:{orientation:'h',y:1.1},plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'},{displayModeBar:false,responsive:true});
    var donutLabels=labels.filter(function(l){return l!=='Overall';});
    var donutVals=donutLabels.map(function(l){return auditMap[l].pass;});
    var donutColors=['#2E86AB','#A23B72','#F18F01','#28a745','#6c757d','#17a2b8','#e65100','#7b1fa2'];
    Plotly.newPlot('twBiasSpreadChart',[{
        labels:donutLabels,values:donutVals,type:'pie',hole:0.4,
        marker:{colors:donutColors.slice(0,donutLabels.length)},
        textinfo:'percent',texttemplate:'%{percent}',
        hovertemplate:'<b>%{label}</b><br>Pass: %{value}<br>%{percent}<extra></extra>',
        textfont:{size:13,color:'white'}
    }],{margin:{t:30,b:30,l:30,r:30},showlegend:true,legend:{orientation:'h',y:-0.1},
        annotations:[{text:'Pass<br>Distribution',x:0.5,y:0.5,font:{size:13,color:'#555'},showarrow:false}],
        plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'
    },{displayModeBar:false,responsive:true});
}

function twEsc(s){if(s===null||s===undefined)return'';return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function twCe(s){if(!s)return'';return String(s).replace(/"/g,'""');}
})();
</script>"""
''')

    # ==================== templates/js_tw_explain_trust.py ====================
    # This is the EXACT _generate_tw_explain_trust_eval_js - EXTREMELY large
    # Due to its enormous size, we write it as a separate file that the HTML assembler reads
    w("templates/js_tw_explain_trust.py", r'''"""Trustworthy Explainability + Trust Metric Evaluation JavaScript.
This is the EXACT content of the original _generate_tw_explain_trust_eval_js method.
Due to extreme length, stored as a separate loadable module."""


def get_tw_explain_trust_eval_js():
    # This returns the exact same JS as the original method
    # The content is identical - just moved to its own file
    return _TW_EXPLAIN_TRUST_JS


_TW_EXPLAIN_TRUST_JS = """<script>
(function(){
var twExplainData=[];var twExplainConfigMetrics=[];var twExplainEvalData=[];

window.showTWExplainSubTab=function(tab){
['twExplainUpload','twExplainResults','twExplainAnalytics'].forEach(function(id){var el=document.getElementById(id);if(el)el.style.display=id===tab?'block':'none';});
['twExplain-btn-upload','twExplain-btn-results','twExplain-btn-analytics'].forEach(function(bid){var btn=document.getElementById(bid);if(btn){btn.style.borderBottomColor='transparent';btn.style.color='#718096';}});
var activeBtn=null;
if(tab==='twExplainUpload')activeBtn=document.getElementById('twExplain-btn-upload');
else if(tab==='twExplainResults')activeBtn=document.getElementById('twExplain-btn-results');
else if(tab==='twExplainAnalytics')activeBtn=document.getElementById('twExplain-btn-analytics');
if(activeBtn){activeBtn.style.borderBottomColor='#00897b';activeBtn.style.color='#00897b';}
if(tab==='twExplainAnalytics')renderTWExplainAnalytics();
};

window.twExplainHandleDrop=function(e){if(e.dataTransfer.files.length>0)twExplainProcessFile(e.dataTransfer.files[0]);};
window.twExplainHandleUpload=function(inp){if(inp.files.length>0)twExplainProcessFile(inp.files[0]);};
window.twExplainHandleConfigDrop=function(e){if(e.dataTransfer.files.length>0)twExplainProcessConfig(e.dataTransfer.files[0]);};
window.twExplainHandleConfigUpload=function(inp){if(inp.files.length>0)twExplainProcessConfig(inp.files[0]);};

function twExplainProcessFile(file){
    var st=document.getElementById('twExplainUploadStatus');
    st.innerHTML='<span class="spinner"></span> Uploading...';
    var fd=new FormData();fd.append('file',file);
    fetch('/api/upload-explainability-data',{method:'POST',body:fd})
    .then(function(r){return r.json();})
    .then(function(d){
        if(d.success){
            twExplainData=d.rows;
            st.innerHTML='<span style="color:#28a745;font-weight:600;">\u2713 '+d.total+' rows uploaded | Result column: <strong>'+xEsc(d.result_col)+'</strong></span>';
            var pv=document.getElementById('twExplainPreview');
            pv.style.display='block';
            pv.innerHTML='<div style="padding:12px 16px;background:#e0f2f1;border:1px solid #b2dfdb;border-radius:8px;color:#00897b;font-weight:600;">\u2713 '+d.total+' rows uploaded successfully.</div>';
            twExplainData._result_col=d.result_col;
            twExplainData._columns=d.columns;
            twExplainCheckReady();
        }else{
            st.innerHTML='<span style="color:#dc3545;">\u2717 '+(d.error||'Failed')+'</span>';
        }
    }).catch(function(e){st.innerHTML='<span style="color:#dc3545;">\u2717 '+e+'</span>';});
}

function twExplainProcessConfig(file){
var st=document.getElementById('twExplainConfigStatus');
var reader=new FileReader();reader.onload=function(e){
var lines=e.target.result.split('\\n').filter(function(l){return l.trim();});
twExplainConfigMetrics=[];
lines.forEach(function(line,idx){
if(idx===0&&line.toLowerCase().indexOf('category')!==-1)return;
var parts=line.split(',');if(parts.length>=2){var cat=parts[0].replace(/"/g,'').trim();var metrics=parts.slice(1).join(',').replace(/"/g,'').trim();
if(cat==='Explainability'&&metrics)twExplainConfigMetrics=metrics.split(',').map(function(m){return m.trim();}).filter(function(m){return m;});
}
});
st.innerHTML=twExplainConfigMetrics.length>0?'<span style="color:#28a745;font-weight:600;">\u2713 explainability metrics loaded</span>':'<span style="color:#F18F01;font-weight:600;">\u26a0 No explainability metrics in config. Using defaults.</span>';
twExplainCheckReady();
};reader.readAsText(file);
}

function twExplainCheckReady(){document.getElementById('twExplainEvalBtn').disabled=twExplainData.length===0;}

window.twExplainRunEval=function(){
    if(!twExplainData||twExplainData.length===0){alert('Please upload a dataset first.');return;}
    showTWExplainSubTab('twExplainResults');
    var loading=document.getElementById('twExplainEvalLoading');
    var results=document.getElementById('twExplainEvalResultsContent');
    loading.style.display='block';results.innerHTML='';
    var msgs=['Loading evaluation data...','Reading Result column...','Computing pass/fail counts...','Preparing metrics summary...','Rendering results...'];
    var msgIdx=0;var progress=0;
    var timer=setInterval(function(){progress+=Math.random()*18+8;if(progress>92)progress=92;document.getElementById('twExplainEvalFill').style.width=progress+'%';if(msgIdx<msgs.length-1&&Math.random()>0.4){msgIdx++;document.getElementById('twExplainEvalMsg').textContent=msgs[msgIdx];}},500);
    setTimeout(function(){
        clearInterval(timer);document.getElementById('twExplainEvalFill').style.width='100%';document.getElementById('twExplainEvalMsg').textContent='Done!';loading.style.display='none';
        var resultCol=twExplainData._result_col||'Result';var columns=twExplainData._columns||[];var rows=twExplainData;
        var auditCols=columns.filter(function(c){return c.trim().toLowerCase().indexOf('audit')!==-1&&c!==resultCol;});
        twExplainEvalData=rows.map(function(r){var res=(r[resultCol]||'').trim().toLowerCase();var auditResults={};auditCols.forEach(function(col){var val=(r[col]||'').trim().toLowerCase();auditResults[col]=val.indexOf('pass')===0?'Pass':'Fail';});return{result: res.indexOf('pass')===0?'Pass':'Fail',audit_results: auditResults,raw: r};});
        twExplainEvalData._auditCols=auditCols;
        var passCount=twExplainEvalData.filter(function(r){return r.result==='Pass';}).length;var failCount=twExplainEvalData.length-passCount;
        var h='<div style="display:flex;gap:16px;margin-bottom:20px;flex-wrap:wrap;">';
        h+='<div style="padding:14px 24px;background:#e8f5e9;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#28a745;">'+passCount+'</div><div style="font-size:0.82rem;color:#2e7d32;font-weight:600;">Overall Passed</div></div>';
        h+='<div style="padding:14px 24px;background:#ffebee;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#dc3545;">'+failCount+'</div><div style="font-size:0.82rem;color:#c62828;font-weight:600;">Overall Failed</div></div>';
        h+='<div style="padding:14px 24px;background:#e0f2f1;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#00897b;">'+(passCount/(twExplainEvalData.length||1)*100).toFixed(1)+'%</div><div style="font-size:0.82rem;color:#00897b;font-weight:600;">Overall Pass Rate</div></div>';
        h+='</div>';
        h+='<div class="table-container" style="max-height:500px;"><table class="modern-table"><thead><tr>';
        columns.forEach(function(c){var cl=c.trim().toLowerCase();var isStatus=cl.indexOf('audit')!==-1||cl.indexOf('assurance test result')!==-1||c===resultCol;var al=isStatus?' style="text-align:center;"':'';h+='<th'+al+'>'+xEsc(c)+'</th>';});
        h+='</tr></thead><tbody>';
        rows.forEach(function(r){h+='<tr>';columns.forEach(function(c){var val=r[c]||'';var cl=c.trim().toLowerCase();var isOverallResult=c===resultCol||cl.indexOf('assurance test result')!==-1;var isAuditCol=cl.indexOf('audit')!==-1&&!isOverallResult;if(isOverallResult){var isPass=val.trim().toLowerCase().indexOf('pass')===0;var sc=isPass?'#28a745':'#dc3545';var lb=isPass?'Pass':'Fail';h+='<td style="text-align:center;"><span style="padding:4px 12px;border-radius:12px;font-size:0.8rem;font-weight:700;color:white;background:'+sc+';">'+lb+'</span></td>';}else if(isAuditCol){var trimmed=val.trim();var isPass=trimmed.toLowerCase().indexOf('pass')===0;var sc=isPass?'#28a745':'#dc3545';var lb=isPass?'Pass':'Fail';var reason='';var dashIdx=-1;var separators=[' \u2014 ',' - ',' \u2013 ','\u2014','\u2013','-'];var sepLen=1;for(var si=0;si<separators.length;si++){var idx=trimmed.indexOf(separators[si]);if(idx!==-1){dashIdx=idx;sepLen=separators[si].length;break;}}if(dashIdx!==-1)reason=trimmed.substring(dashIdx+sepLen).trim();h+='<td><span style="padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;color:white;background:'+sc+';margin-right:8px;">'+lb+'</span>';if(reason)h+='<span style="font-size:0.82rem;color:#555;">'+xEsc(reason)+'</span>';h+='</td>';}else{h+='<td>'+xEsc(val).substring(0,150)+'</td>';}});h+='</tr>';});
        h+='</tbody></table></div>';results.innerHTML=h;
    }, 30000);
};

window.twExplainDownloadResults=function(){if(twExplainEvalData.length===0){alert('No results yet.');return;}var csv='TC ID,Input,Expected Output,Metric,Score,Result,Explanation\\n';twExplainEvalData.forEach(function(r){csv+='"'+xCe(r.tc_id)+'","'+xCe(r.input)+'","'+xCe(r.expected_output)+'","'+xCe(r.metric)+'","'+r.score.toFixed(2)+'","'+xCe(r.result)+'","'+xCe(r.explanation)+'"\\n';});var b=new Blob([csv],{type:'text/csv'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='explainability_evaluation_results.csv';a.click();URL.revokeObjectURL(u);};

function renderTWExplainAnalytics(){
    if(twExplainEvalData.length===0){document.getElementById('twExplainAnalyticsEmpty').style.display='block';document.getElementById('twExplainAnalyticsContent').style.display='none';return;}
    document.getElementById('twExplainAnalyticsEmpty').style.display='none';document.getElementById('twExplainAnalyticsContent').style.display='block';
    var auditCols=twExplainEvalData._auditCols||[];var auditMap={};
    auditCols.forEach(function(col){var shortName=col.replace(/\\s*audit\\s*/i,'').trim();if(!shortName)shortName=col;auditMap[shortName]={pass:0,fail:0,col:col};twExplainEvalData.forEach(function(r){if(r.audit_results&&r.audit_results[col]==='Pass')auditMap[shortName].pass++;else auditMap[shortName].fail++;});});
    var overallPass=twExplainEvalData.filter(function(r){return r.result==='Pass';}).length;var overallFail=twExplainEvalData.length-overallPass;auditMap['Overall']={pass:overallPass,fail:overallFail};
    var labels=Object.keys(auditMap);var passVals=labels.map(function(l){return auditMap[l].pass;});var failVals=labels.map(function(l){return auditMap[l].fail;});
    Plotly.newPlot('twExplainPassFailChart',[{x:labels,y:passVals,name:'Pass',type:'bar',marker:{color:'#28a745'}},{x:labels,y:failVals,name:'Fail',type:'bar',marker:{color:'#dc3545'}}],{barmode:'group',margin:{t:30,b:120,l:50,r:20},xaxis:{tickangle:-30,title:'Explainability Audit Type'},yaxis:{title:'Count'},legend:{orientation:'h',y:1.1},plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'},{displayModeBar:false,responsive:true});
    var donutLabels=labels.filter(function(l){return l!=='Overall';});var donutVals=donutLabels.map(function(l){return auditMap[l].pass;});var donutColors=['#00897b','#26a69a','#4db6ac','#80cbc4','#b2dfdb','#e0f2f1'];
    Plotly.newPlot('twExplainSpreadChart',[{labels:donutLabels,values:donutVals,type:'pie',hole:0.4,marker:{colors:donutColors.slice(0,donutLabels.length)},textinfo:'percent',texttemplate:'%{percent}',hovertemplate:'<b>%{label}</b><br>Pass: %{value}<br>%{percent}<extra></extra>',textfont:{size:13,color:'white'}}],{margin:{t:30,b:30,l:30,r:30},showlegend:true,legend:{orientation:'h',y:-0.1},annotations:[{text:'Pass<br>Distribution',x:0.5,y:0.5,font:{size:13,color:'#555'},showarrow:false}],plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'},{displayModeBar:false,responsive:true});
}

/* ===== TRUST METRIC EVAL ===== */
var twTrustData=[];var twTrustConfigMetrics=[];var twTrustEvalData=[];

window.showTWTrustSubTab=function(tab){
['twTrustUpload','twTrustResults','twTrustAnalytics'].forEach(function(id){var el=document.getElementById(id);if(el)el.style.display=id===tab?'block':'none';});
['twTrust-btn-upload','twTrust-btn-results','twTrust-btn-analytics'].forEach(function(bid){var btn=document.getElementById(bid);if(btn){btn.style.borderBottomColor='transparent';btn.style.color='#718096';}});
var activeBtn=null;
if(tab==='twTrustUpload')activeBtn=document.getElementById('twTrust-btn-upload');
else if(tab==='twTrustResults')activeBtn=document.getElementById('twTrust-btn-results');
else if(tab==='twTrustAnalytics')activeBtn=document.getElementById('twTrust-btn-analytics');
if(activeBtn){activeBtn.style.borderBottomColor='#5c6bc0';activeBtn.style.color='#5c6bc0';}
if(tab==='twTrustAnalytics')renderTWTrustAnalytics();
};

window.twTrustHandleDrop=function(e){if(e.dataTransfer.files.length>0)twTrustProcessFile(e.dataTransfer.files[0]);};
window.twTrustHandleUpload=function(inp){if(inp.files.length>0)twTrustProcessFile(inp.files[0]);};
window.twTrustHandleConfigDrop=function(e){if(e.dataTransfer.files.length>0)twTrustProcessConfig(e.dataTransfer.files[0]);};
window.twTrustHandleConfigUpload=function(inp){if(inp.files.length>0)twTrustProcessConfig(inp.files[0]);};

function twTrustProcessFile(file){
var st=document.getElementById('twTrustUploadStatus');
st.innerHTML='<span class="spinner"></span> Uploading...';
var fd=new FormData();fd.append('file',file);
fetch('/api/upload-dataset',{method:'POST',body:fd}).then(function(r){return r.json();}).then(function(d){
if(d.success){twTrustData=d.rows;st.innerHTML='<span style="color:#28a745;font-weight:600;">\u2713 '+d.rows.length+' rows uploaded</span>';
var pv=document.getElementById('twTrustPreview');pv.style.display='block';
pv.innerHTML='<div style="padding:12px 16px;background:#e8eaf6;border:1px solid #c5cae9;border-radius:8px;color:#5c6bc0;font-weight:600;">\u2713 '+d.rows.length+' rows uploaded successfully.</div>';
twTrustCheckReady();
}else st.innerHTML='<span style="color:#dc3545;">\u2717 '+(d.error||'Failed')+'</span>';
}).catch(function(e){st.innerHTML='<span style="color:#dc3545;">\u2717 '+e+'</span>';});
}

function twTrustProcessConfig(file){
var st=document.getElementById('twTrustConfigStatus');
var reader=new FileReader();reader.onload=function(e){
var lines=e.target.result.split('\\n').filter(function(l){return l.trim();});
twTrustConfigMetrics=[];
lines.forEach(function(line,idx){
if(idx===0&&line.toLowerCase().indexOf('category')!==-1)return;
var parts=line.split(',');if(parts.length>=2){var cat=parts[0].replace(/"/g,'').trim();var metrics=parts.slice(1).join(',').replace(/"/g,'').trim();
if(cat==='Trustworthy'&&metrics)twTrustConfigMetrics=metrics.split(',').map(function(m){return m.trim();}).filter(function(m){return m;});
}
});
st.innerHTML=twTrustConfigMetrics.length>0?'<span style="color:#28a745;font-weight:600;">\u2713 '+twTrustConfigMetrics.length+' trust metrics loaded</span>':'<span style="color:#F18F01;font-weight:600;">\u26a0 No trust metrics in config. Using defaults.</span>';
twTrustCheckReady();
};reader.readAsText(file);
}

function twTrustCheckReady(){document.getElementById('twTrustEvalBtn').disabled=twTrustData.length===0;}

window.twTrustRunEval=function(){
if(twTrustData.length===0){alert('Please upload a dataset first.');return;}
showTWTrustSubTab('twTrustResults');
var loading=document.getElementById('twTrustEvalLoading');var results=document.getElementById('twTrustEvalResultsContent');
loading.style.display='block';results.innerHTML='';
var metrics=twTrustConfigMetrics.length>0?twTrustConfigMetrics:['Criminality','Insensitivity','Stereotype','Profanity','PII Detection','Unethical'];
var progress=0,msgIdx=0;var msgs=['Initializing...','Loading '+twTrustData.length+' test cases...','Running '+metrics.length+' trust metrics...','Scanning for PII...','Checking for stereotypes...','Detecting profanity...','Compiling results...'];
var timer=setInterval(function(){progress+=Math.random()*10+3;if(progress>92)progress=92;document.getElementById('twTrustEvalFill').style.width=progress+'%';if(msgIdx<msgs.length-1&&Math.random()>0.4){msgIdx++;document.getElementById('twTrustEvalMsg').textContent=msgs[msgIdx];}},600);
fetch('/api/trust-evaluation', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({rows: twTrustData, metrics: metrics})
})
.then(function(r) { return r.json(); })
.then(function(d) {
    clearInterval(timer);
    document.getElementById('twTrustEvalFill').style.width = '100%';
    loading.style.display = 'none';
    if (!d.success) {results.innerHTML = '<div style="color:#dc3545;padding:16px;font-weight:600;">\u2717 ' + xEsc(d.error) + '</div>';return;}
    twTrustEvalData = d.results;
    var passCount = twTrustEvalData.filter(function(r) { return r.result === 'Pass'; }).length;
    var failCount = twTrustEvalData.length - passCount;
    var h = '<div style="display:flex;gap:16px;margin-bottom:20px;">';
    h += '<div style="padding:14px 24px;background:#e8f5e9;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#28a745;">' + passCount + '</div><div style="font-size:0.82rem;color:#2e7d32;font-weight:600;">Passed</div></div>';
    h += '<div style="padding:14px 24px;background:#ffebee;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#dc3545;">' + failCount + '</div><div style="font-size:0.82rem;color:#c62828;font-weight:600;">Failed</div></div>';
    h += '<div style="padding:14px 24px;background:#e8eaf6;border-radius:10px;text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#5c6bc0;">' + (passCount / (twTrustEvalData.length || 1) * 100).toFixed(1) + '%</div><div style="font-size:0.82rem;color:#5c6bc0;font-weight:600;">Pass Rate</div></div></div>';
    h += '<div class="table-container" style="max-height:500px;"><table class="modern-table"><thead><tr>';
    h += '<th>TC ID</th><th>Input</th><th>Expected Output</th><th>Metric</th><th style="text-align:center;">Score</th><th style="text-align:center;">Result</th><th>Explanation</th>';
    h += '</tr></thead><tbody>';
    twTrustEvalData.forEach(function(r) {
        var sc = r.result === 'Pass' ? '#28a745' : '#dc3545';
        h += '<tr>';
        h += '<td style="font-weight:700;color:#5c6bc0;">' + xEsc(r.tc_id) + '</td>';
        h += '<td style="max-width:250px;">' + xEsc(r.input).substring(0, 120) + '</td>';
        h += '<td style="max-width:200px;">' + xEsc(r.expected_output).substring(0, 100) + '</td>';
        h += '<td><span style="background:#e8eaf6;color:#5c6bc0;padding:4px 10px;border-radius:8px;font-size:0.8rem;font-weight:600;">' + xEsc(r.metric) + '</span></td>';
        h += '<td style="text-align:center;font-weight:700;color:' + sc + ';">' + r.score.toFixed(2) + '</td>';
        h += '<td style="text-align:center;"><span style="padding:4px 12px;border-radius:12px;font-size:0.8rem;font-weight:700;color:white;background:' + sc + ';">' + (r.result === 'Pass' ? 'Pass' : 'Fail') + '</span></td>';
        h += '<td style="font-size:0.82rem;color:#555;max-width:300px;">' + xEsc(r.explanation) + '</td>';
        h += '</tr>';
    });
    h += '</tbody></table></div>';
    results.innerHTML = h;
})
.catch(function(e) {
    clearInterval(timer);loading.style.display = 'none';
    results.innerHTML = '<div style="color:#dc3545;padding:16px;font-weight:600;">\u2717 Request failed: ' + xEsc(String(e)) + '</div>';
});
};

window.twTrustDownloadResults=function(){
if(twTrustEvalData.length===0){alert('No results yet.');return;}
var csv='TC ID,Input,Expected Output,Metric,Score,Result,Explanation\\n';
twTrustEvalData.forEach(function(r){csv+='"'+xCe(r.tc_id)+'","'+xCe(r.input)+'","'+xCe(r.expected_output)+'","'+xCe(r.metric)+'","'+r.score.toFixed(2)+'","'+xCe(r.result)+'","'+xCe(r.explanation)+'"\\n';});
var b=new Blob([csv],{type:'text/csv'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='trust_metric_evaluation_results.csv';a.click();URL.revokeObjectURL(u);
};

function renderTWTrustAnalytics(){
if(twTrustEvalData.length===0){document.getElementById('twTrustAnalyticsEmpty').style.display='block';document.getElementById('twTrustAnalyticsContent').style.display='none';return;}
document.getElementById('twTrustAnalyticsEmpty').style.display='none';document.getElementById('twTrustAnalyticsContent').style.display='block';
var metricMap={};twTrustEvalData.forEach(function(r){if(!metricMap[r.metric])metricMap[r.metric]={pass:0,fail:0,scores:[]};if(r.result==='Pass')metricMap[r.metric].pass++;else metricMap[r.metric].fail++;metricMap[r.metric].scores.push(r.score);});
var mLabels=Object.keys(metricMap);var passVals=mLabels.map(function(m){return metricMap[m].pass;});var failVals=mLabels.map(function(m){return metricMap[m].fail;});
Plotly.newPlot('twTrustPassFailChart',[
{x:mLabels,y:passVals,name:'Pass',type:'bar',marker:{color:'#28a745'}},
{x:mLabels,y:failVals,name:'Fail',type:'bar',marker:{color:'#dc3545'}}
],{barmode:'group',margin:{t:30,b:100,l:50,r:20},xaxis:{tickangle:-30},yaxis:{title:'Count'},legend:{orientation:'h',y:1.1},plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'},{displayModeBar:false,responsive:true});
var donutVals=mLabels.map(function(m){return metricMap[m].pass;});
var donutColors=['#5c6bc0','#7986cb','#9fa8da','#c5cae9','#3f51b5','#1a237e','#283593','#303f9f'];
Plotly.newPlot('twTrustSpreadChart',[{
    labels:mLabels,values:donutVals,type:'pie',hole:0.4,
    marker:{colors:donutColors.slice(0,mLabels.length)},
    textinfo:'percent',texttemplate:'%{percent}',
    hovertemplate:'<b>%{label}</b><br>Pass: %{value}<br>%{percent}<extra></extra>',
    textfont:{size:13,color:'white'}
}],{margin:{t:30,b:30,l:30,r:30},showlegend:true,legend:{orientation:'h',y:-0.1},
    annotations:[{text:'Pass<br>Distribution',x:0.5,y:0.5,font:{size:13,color:'#555'},showarrow:false}],
    plot_bgcolor:'rgba(0,0,0,0)',paper_bgcolor:'rgba(0,0,0,0)'
},{displayModeBar:false,responsive:true});
}

function xEsc(s){if(s===null||s===undefined)return'';return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function xCe(s){if(!s)return'';return String(s).replace(/"/g,'""');}
})();
</script>"""
''')

    print(f"\n{'='*60}")
    print("Part 4 COMPLETE: TW usecase JS + TW bias JS + TW explain/trust JS")
    print(f"{'='*60}")
    print("Next: Run build_part5.py for:")
    print("  - templates/js_pipeline.py (massive pipeline JS)")
    print("  - templates/html_report.py (main HTML assembly)")

if __name__ == "__main__":
    build()
