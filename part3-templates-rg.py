#!/usr/bin/env python3
"""
Part 3: CSS styles, JS templates, HTML modal, report_generator.py
Run: python build_part3.py
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
    print(f"Part 3: Building templates + report_generator in ./{BASE}/\n")

    # ==================== templates/css_styles.py ====================
    # This is the EXACT _get_modern_css method content, extracted as a function
    w("templates/css_styles.py", r'''"""Complete CSS stylesheet generator for the report."""


def get_modern_css(config):
    theme = config['theme']
    sc = config['status_colors']
    return f"""* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: {theme['font_family']}; line-height: 1.6; color: #333; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; margin: 0; padding: 20px; }}
.container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
#rcaOutputContent.empty-json {{ display:flex; font-weight:600; color:#666; text-align:center; width:100%; }}
.empty-json {{ color:#888; font-style:italic; }}
.report-header {{ background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%); color: white; padding: 40px; text-align: center; position: relative; overflow: hidden; }}
.report-header::before {{ content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px); animation: shimmer 20s linear infinite; }}
@keyframes shimmer {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(100%); }} }}
.report-title {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); position: relative; z-index: 1; }}
.report-subtitle {{ font-size: 1.4rem; font-weight: 300; margin-bottom: 15px; opacity: 0.9; position: relative; z-index: 1; }}
.report-description {{ font-size: 1rem; max-width: 800px; margin: 0 auto; opacity: 0.85; line-height: 1.6; position: relative; z-index: 1; }}
.report-timestamp {{ position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 8px 15px; border-radius: 20px; font-size: 0.9rem; z-index: 2; }}
.tab-navigation {{ background: {theme['light_bg']}; border-bottom: none; display: flex; justify-content: center; padding: 12px 16px; position: sticky; top: 0; z-index: 100; gap: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.tab-button {{ background: white; border: 2px solid #e2e8f0; padding: 10px 24px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; position: relative; color: #666; border-radius: 50px; }}
.tab-button:hover {{ background: rgba(46, 134, 171, 0.08); border-color: {theme['primary_color']}; color: {theme['primary_color']}; }}
.tab-button.active {{ background: {theme['primary_color']}; color: white; border-color: {theme['primary_color']}; box-shadow: 0 2px 10px rgba(46,134,171,0.35); }}
.tab-button.active::after {{ content: none; }}
.tab-content {{ display: none; padding: 16px 30px; animation: fadeIn 0.3s ease-in; width: 100%; }}
.tab-content.active {{ display: block; height: auto; overflow: visible; }}
.sub-tab-content {{ display: none; padding: 20px 0; animation: fadeIn 0.3s ease-in; }}
.sub-tab-content.active {{ display: block; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.card {{ background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 25px; overflow: hidden; transition: all 0.3s ease; border: 1px solid {theme['border_color']}; }}
.card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
.card-header {{ background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%); color: white; padding: 20px; font-weight: 600; font-size: 1.2rem; position: relative; }}
.card-content {{ padding: 20px; }}
.charts-grid {{ display: block; width: 100%; }}
.chart-card {{ background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: visible; transition: all 0.3s ease; margin-bottom: 25px; }}
.chart-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
.chart-card.full-width {{ grid-column: 1 / -1; }}
.multi-select {{ position: relative; width: 300px; border: 1px solid #ccc; border-radius: 6px; padding: 6px; }}
.multi-select input {{ border: none; outline: none; width: 100%; cursor: pointer; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 4px; }}
.chip {{ background: #e0e0e0; padding: 4px 8px; border-radius: 12px; font-size: 12px; display: flex; align-items: center; }}
.chip span {{ margin-left: 6px; cursor: pointer; }}
.dropdown {{ position: absolute; background: white; border: 1px solid #ccc; width: 100%; max-height: 150px; overflow-y: auto; display: none; z-index: 10; }}
.dropdown div {{ padding: 6px; cursor: pointer; }}
.dropdown div:hover {{ background: #f0f0f0; }}
.chart-scroll {{ width:100%; overflow-x: auto; overflow-y: hidden; }}
.chart-scroll > div {{ min-width: max-content; }}
.table-container {{ background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow-x: auto; overflow-y: auto; max-width: 100%; max-height: 600px; position: relative; margin-bottom: 25px; }}
.modern-table {{ width: 100%; border-collapse: collapse; font-size: 0.95rem; }}
.modern-table th {{ background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%); color: white; padding: 15px 12px; text-align: left; font-weight: 600; border: none; position: sticky; top: 0; z-index: 10; }}
.modern-table td {{ padding: 12px; border-bottom: 1px solid {theme['border_color']}; vertical-align: top; }}
.modern-table tr:hover {{ background: rgba(46, 134, 171, 0.04); }}
.modern-table tr:nth-child(even) {{ background: rgba(0,0,0,0.02); }}
.modern-table tr:nth-child(even):hover {{ background: rgba(46, 134, 171, 0.04); }}
.details-table {{ width: max-content; min-width: 100%; border-collapse: collapse; font-size: 0.95rem; table-layout: auto; }}
.details-table thead th {{ background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%); color: white; padding: 15px 12px; text-align: left; font-weight: 600; border: none; position: sticky; top: 0; z-index: 10; }}
.details-table td {{ padding: 12px; border-bottom: 1px solid {theme['border_color']}; vertical-align: top; white-space: normal; word-break: break-word; max-width: 600px; }}
.details-table tr:hover {{ background: rgba(46, 134, 171, 0.04); }}
.details-table tr:nth-child(even) {{ background: rgba(0,0,0,0.02); }}
.details-table tr:nth-child(even):hover {{ background: rgba(46, 134, 171, 0.04); }}
.resizer {{ position: absolute; right: 0; top: 0; width: 6px; height: 100%; cursor: col-resize; user-select: none; }}
.metric-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
.metric-table th, .metric-table td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
.metric-table th {{ background-color: #7393B3; font-weight: 600; text-transform: capitalize; }}
.metric-table thead th {{ position: sticky; top: 0; z-index: 20; background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; }}
.traceback-card {{ background: #f8fafc; border-radius: 12px; padding: 16px 18px; margin: 14px 0; border: 1px solid #e5eaf2; }}
.tb-badge {{ display:inline-flex; align-items:center; gap:4px; padding:2px 8px; border-radius:10px; font-size:12px; font-weight:600; }}
.tb-pass {{ background:#ecfdf5; color:#059669; border:1px solid #a7f3d0; }}
.tb-fail {{ background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }}
.status-cell {{ padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; text-align: center; min-width: 80px; display: inline-block; cursor: pointer; transition: all 0.2s ease; }}
.status-cell:hover {{ transform: scale(1.05); box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
.status-warning {{ background: #e6c65c; color: #4a3a00; }}
.status-passed {{ background: {sc['passed']}; color: white; }}
.status-failed {{ background: {sc['failed']}; color: white; }}
.status-skipped {{ background: {sc['skipped']}; color: white; }}
.diff-added {{ background:#00bcd4; color:white; padding:2px 4px; border-radius:3px; }}
.metric-score {{ font-weight: 600; font-size: 1rem; }}
.below-threshold {{ background: {sc['failed']}; color: white; font-weight: 600; font-size: inherit; padding: 3px 10px; border-radius: 8px; display: inline-block; }}
.equal-threshold {{ background: {theme['warning_color']}; color: white; font-weight: 600; font-size: inherit; padding: 3px 10px; border-radius: 8px; display: inline-block; }}
.pagination-container {{ background: {theme['light_bg']}; border-top: 1px solid {theme['border_color']}; padding: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }}
.pagination-controls {{ display: flex; align-items: center; gap: 10px; }}
.page-btn {{ padding: 10px 15px; border: 1px solid {theme['border_color']}; background: white; cursor: pointer; border-radius: 6px; font-size: 14px; transition: all 0.2s ease; min-width: 40px; text-align: center; }}
.page-btn:hover:not(:disabled) {{ background: {theme['primary_color']}; color: white; border-color: {theme['primary_color']}; }}
.page-btn.active {{ background: {theme['primary_color']}; color: white; border-color: {theme['primary_color']}; }}
.page-btn:disabled {{ background: {theme['light_bg']}; color: #999; cursor: not-allowed; }}
.page-info {{ font-size: 0.9rem; color: #666; font-weight: 500; }}
.rows-selector {{ padding: 8px 12px; border: 1px solid {theme['border_color']}; border-radius: 6px; background: white; font-size: 14px; }}
.modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); }}
.modal-content {{ background: white; margin: 2% auto; border-radius: 15px; display: flex; flex-direction: column; width: 95%; max-width: 1400px; max-height: 90vh; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: modalSlideIn 0.3s ease-out; }}
@keyframes modalSlideIn {{ from {{ opacity: 0; transform: translateY(-50px) scale(0.9); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
.modal-header {{ background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%); color: white; padding: 25px; position: relative; }}
.modal-title {{ font-size: 1.5rem; font-weight: 600; margin: 0; }}
.modal-subtitle {{ font-size: 1rem; opacity: 0.9; margin: 5px 0 0; }}
.modal-close {{ position: absolute; top: 20px; right: 25px; background: rgba(255,255,255,0.2); border: none; color: white; font-size: 24px; font-weight: bold; cursor: pointer; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; }}
.modal-close:hover {{ background: rgba(255,255,255,0.3); transform: scale(1.1); }}
.modal-body {{ display: flex; flex: 1; overflow: hidden; }}
.modal-left {{ flex: 1; width: 100%; padding: 25px; overflow-y: auto; border-right: none; }}
#scoreReasonBlock {{ display:flex; flex-direction:row; gap:24px; align-items:stretch; }}
#scoreReasonBlock .score-box {{ flex:0 0 320px; max-width:320px; }}
#scoreReasonBlock .evaluation-box {{ flex:1; min-width:0; }}
#scoreReasonBlock .modal-section {{ width:auto; }}
.modal-section {{ background: white; border-radius: 8px; padding: 0 20px 20px 20px; margin-bottom: 20px; border-left: 4px solid {theme['accent_color']}; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
.modal-section h4 {{ color: {theme['primary_color']}; margin-bottom: 8px; font-size: 1.1rem; font-weight: 600; }}
.modal-section p {{ line-height: 1.6; color: #555; }}
.collapsible-section {{ background: white; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); overflow: hidden; }}
.collapsible-header {{ background: linear-gradient(135deg, {theme['light_bg']} 0%, rgba(46,134,171,0.1) 100%); padding: 15px 20px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid {theme['accent_color']}; transition: all 0.2s ease; }}
.collapsible-header:hover {{ background: linear-gradient(135deg, rgba(46,134,171,0.1) 0%, rgba(46,134,171,0.2) 100%); }}
.collapsible-content {{ padding: 0 20px 20px 20px; max-height: 200px; overflow-y: auto; transition: all 0.3s ease; border-left: 4px solid {theme['accent_color']}; }}
.collapsible-content.collapsed {{ max-height: 0; padding: 0 20px; overflow: hidden; }}
#tracebackContent:not(.collapsed), #metricFieldsContent:not(.collapsed) {{ max-height: 420px; overflow-y: auto; position: relative; }}
#rcaContainer {{ max-height: 420px; overflow-y: auto; position: relative; }}
#rcaContainer table thead th {{ position: sticky; top: 0; z-index: 5; background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; }}
.toggle-icon {{ font-size: 1.2rem; transition: transform 0.3s ease; color: {theme['primary_color']}; transform: rotate(180deg); }}
.toggle-icon.expanded {{ transform: rotate(0deg); }}
#scorePieChart {{ margin: 0 auto; display: flex; justify-content: center; align-items: center; max-width: 100%; max-height: 200px; overflow: hidden; }}
#metricSheetFields {{ padding: 0; margin: 0; }}
.trajectory-wrapper {{ display:flex; gap:20px; margin-bottom:20px; }}
.trajectory-wrapper .modal-section {{ flex:1; }}
.wizard-steps {{ display:flex; justify-content:center; gap:0; margin-bottom:32px; position:relative; }}
.wizard-step {{ display:flex; align-items:center; gap:10px; cursor:pointer; padding:14px 24px; position:relative; z-index:1; }}
.wizard-step-num {{ width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem; border:2px solid #cbd5e1; color:#94a3b8; background:white; transition:all 0.3s; }}
.wizard-step.active .wizard-step-num {{ background:{theme['primary_color']}; color:white; border-color:{theme['primary_color']}; box-shadow:0 2px 8px rgba(46,134,171,0.3); }}
.wizard-step.completed .wizard-step-num {{ background:#28a745; color:white; border-color:#28a745; }}
.wizard-step-label {{ font-size:0.9rem; font-weight:600; color:#94a3b8; transition:color 0.3s; }}
.wizard-step.active .wizard-step-label {{ color:{theme['primary_color']}; }}
.wizard-step.completed .wizard-step-label {{ color:#28a745; }}
.wizard-connector {{ width:60px; height:2px; background:#cbd5e1; align-self:center; }}
.wizard-connector.completed {{ background:#28a745; }}
.wizard-body {{ min-height:300px; }}
.wizard-actions {{ display:flex; justify-content:space-between; margin-top:24px; padding-top:16px; border-top:1px solid #e2e8f0; }}
.btn {{ padding:10px 24px; border-radius:8px; font-weight:600; font-size:0.95rem; cursor:pointer; border:none; transition:all 0.2s; }}
.btn-primary {{ background:{theme['primary_color']}; color:white; }}
.btn-primary:hover {{ opacity:0.9; box-shadow:0 2px 8px rgba(46,134,171,0.3); }}
.btn-primary:disabled {{ background:#94a3b8; cursor:not-allowed; box-shadow:none; }}
.btn-secondary {{ background:white; color:#555; border:1px solid #ccc; }}
.btn-secondary:hover {{ background:#f8f9fa; }}
.btn-success {{ background:#28a745; color:white; }}
.btn-success:hover {{ opacity:0.9; }}
.upload-zone {{ border:2px dashed #cbd5e1; border-radius:12px; padding:40px; text-align:center; cursor:pointer; transition:all 0.3s; background:#fafbfc; }}
.upload-zone:hover {{ border-color:{theme['primary_color']}; background:rgba(46,134,171,0.04); }}
.upload-zone.dragover {{ border-color:{theme['primary_color']}; background:rgba(46,134,171,0.08); }}
.preview-table {{ max-height:300px; overflow:auto; margin-top:16px; }}
.aug-multi-select {{ position:relative; width:100%; border:1px solid #ccc; border-radius:6px; padding:8px; min-height:42px; background:white; cursor:pointer; }}
.aug-multi-select .chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
.aug-multi-select .dropdown {{ position:absolute; left:0; right:0; top:100%; background:white; border:1px solid #ccc; border-top:none; max-height:200px; overflow-y:auto; display:none; z-index:20; border-radius:0 0 6px 6px; }}
.aug-multi-select .dropdown div {{ padding:8px 12px; cursor:pointer; font-size:0.9rem; }}
.aug-multi-select .dropdown div:hover {{ background:#f0f4ff; }}
.coverage-row {{ display:flex; gap:12px; align-items:center; margin-bottom:10px; }}
.coverage-row input {{ padding:8px 10px; border:1px solid #ccc; border-radius:6px; font-size:0.9rem; }}
.coverage-total {{ font-size:1rem; font-weight:700; margin-top:8px; }}
.coverage-total.valid {{ color:#28a745; }}
.coverage-total.invalid {{ color:#dc3545; }}
.spinner {{ display:inline-block; width:18px; height:18px; border:3px solid rgba(255,255,255,0.4); border-top-color:white; border-radius:50%; animation:spin 0.7s linear infinite; vertical-align:middle; margin-right:8px; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.aug-progress {{ margin-top:16px; }}
.aug-progress-bar {{ height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden; }}
.aug-progress-fill {{ height:100%; background:linear-gradient(90deg,{theme['primary_color']},{theme['secondary_color']}); transition:width 0.4s; }}
.aug-progress-text {{ font-size:0.85rem; color:#555; margin-top:6px; }}
@media (max-width: 768px) {{ .container {{ margin: 10px; border-radius: 10px; }} .report-title {{ font-size: 2rem; }} .tab-content {{ padding: 20px; }} .modal-content {{ width: 98%; max-height: 95vh; }} .wizard-steps {{ flex-wrap:wrap; }} }}
.loading {{ display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(46,134,171,0.3); border-radius: 50%; border-top-color: {theme['primary_color']}; animation: spin 1s ease-in-out infinite; }}
.text-center {{ text-align: center; }} .text-right {{ text-align: right; }}
.text-primary {{ color: {theme['primary_color']}; }} .text-secondary {{ color: {theme['secondary_color']}; }}
.text-success {{ color: {sc['passed']}; }} .text-danger {{ color: {sc['failed']}; }}
.p-0 {{ padding: 0; }} .p-1 {{ padding: 0.5rem; }} .p-2 {{ padding: 1rem; }} .p-3 {{ padding: 1.5rem; }}
.mb-0 {{ margin-bottom: 0; }} .mb-1 {{ margin-bottom: 0.5rem; }} .mb-2 {{ margin-bottom: 1rem; }} .mb-3 {{ margin-bottom: 1.5rem; }}
.eval-platform-card {{ border:2px solid #e2e8f0; border-radius:12px; padding:24px 16px; text-align:center; cursor:pointer; transition:all 0.25s; background:white; }}
.eval-platform-card:hover {{ border-color:#2E86AB; background:rgba(46,134,171,0.04); transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,0.08); }}
.eval-platform-card.selected {{ border-color:#2E86AB; background:rgba(46,134,171,0.08); box-shadow:0 0 0 3px rgba(46,134,171,0.2); }}
.eval-llm-provider {{ border:2px solid #e2e8f0; border-radius:12px; padding:18px; transition:all 0.2s; background:white; }}
.eval-llm-model {{ display:flex; align-items:center; gap:8px; padding:8px 12px; border-radius:8px; cursor:pointer; transition:all 0.15s; margin-bottom:4px; }}
.eval-llm-model:hover {{ background:rgba(46,134,171,0.06); }}
.eval-llm-model.selected {{ background:rgba(46,134,171,0.12); font-weight:600; }}
.eval-llm-model .radio-dot {{ width:18px; height:18px; border-radius:50%; border:2px solid #cbd5e1; display:flex; align-items:center; justify-content:center; flex-shrink:0; }}
.eval-llm-model.selected .radio-dot {{ border-color:#2E86AB; }}
.eval-llm-model.selected .radio-dot::after {{ content:''; width:10px; height:10px; border-radius:50%; background:#2E86AB; }}
.eval-metric-chip {{ padding:10px 18px; border:2px solid #e2e8f0; border-radius:10px; cursor:pointer; transition:all 0.2s; font-weight:500; font-size:0.9rem; user-select:none; }}
.eval-metric-chip:hover {{ border-color:#2E86AB; background:rgba(46,134,171,0.04); }}
.eval-metric-chip.selected {{ border-color:#2E86AB; background:#2E86AB; color:white; }}
.eval-config-row {{ display:flex; justify-content:space-between; padding:14px 0; border-bottom:1px solid #f0f0f0; }}
.eval-config-row:last-child {{ border-bottom:none; }}
.eval-config-label {{ font-weight:600; color:#555; min-width:180px; }}
.eval-config-value {{ color:#333; text-align:right; max-width:60%; word-break:break-word; }}
.tw-mc-tab {{padding:10px 18px;font-weight:600;font-size:0.85rem;border:none;cursor:pointer;background:white;color:#718096;transition:all 0.2s;border-radius:10px;}}
.tw-mc-tab.active {{background:#2E86AB;color:white;border-radius:10px;}}
.tw-mc-tab:hover:not(.active) {{background:rgba(46,134,171,0.08);border-radius:10px;}}
.tw-card {{border:2px solid #e2e8f0;border-radius:12px;padding:18px;background:white;transition:all 0.25s;position:relative;}}
.tw-card:hover {{border-color:#cbd5e1;box-shadow:0 4px 12px rgba(0,0,0,0.06);}}
.tw-card.enabled {{border-color:#2E86AB;background:rgba(46,134,171,0.02);}}
.tw-badge {{display:inline-block;padding:3px 10px;border-radius:12px;font-size:0.72rem;font-weight:700;}}
.tw-badge-bias {{background:#fff3e0;color:#e65100;}}
.tw-badge-trust {{background:#e8eaf6;color:#5c6bc0;}}
.tw-badge-explain {{background:#e0f2f1;color:#00897b;}}
.traceback-subcard {{ margin-left: 14px; border-left: 3px solid #e2e8f0; padding-left: 12px; margin-top: 10px; }}
.traceback-param-row {{ display: flex; justify-content: space-between; align-items: baseline; font-size: 13px; padding: 3px 0; }}
.traceback-param-name {{ color: #1f2937; font-weight: 700; }}
.traceback-param-value {{ color: #6b7280; font-weight: 500; }}
.traceback-param-value.na {{ color: #9ca3af; font-style: italic; }}
.constant-collapsible {{ margin-bottom:15px; }}
.constant-header {{ background:#f1f4f8; padding:10px 14px; border-radius:6px; cursor:pointer; font-weight:600; border:1px solid #e3e6ea; }}
.constant-content {{ border:1px solid #e3e6ea; border-top:none; padding:12px; display:none; border-radius:0 0 6px 6px; max-height:350px; overflow:auto; white-space:pre-wrap; }}
.fewshot-row {{ border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:10px; background:#fafbfc; }}
.fewshot-row textarea {{ font-family:inherit; }}
.aug-tech-tab {{padding:8px 14px;font-weight:600;font-size:0.82rem;border:none;cursor:pointer;background:white;color:#718096;transition:all 0.2s;border-radius:10px;}}
.aug-tech-tab.active {{background:#2E86AB;color:white;border-radius:10px;}}
.aug-tech-tab:hover:not(.active) {{background:rgba(46,134,171,0.08);border-radius:10px;}}
.aug-tech-item {{display:flex;align-items:center;gap:8px;padding:10px 12px;border:2px solid #e2e8f0;border-radius:10px;cursor:pointer;transition:all 0.2s;background:white;font-size:0.85rem;font-weight:500;color:#555;user-select:none;}}
.aug-tech-item:hover {{border-color:#cbd5e1;background:rgba(46,134,171,0.03);}}
.aug-tech-item.selected {{border-color:#2E86AB;background:rgba(46,134,171,0.08);color:#2E86AB;font-weight:600;}}
.aug-tech-item input[type=checkbox] {{accent-color:#2E86AB;width:16px;height:16px;cursor:pointer;flex-shrink:0;}}
.aug-chip {{display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border:1.5px solid #2E86AB;border-radius:50px;background:transparent;color:#2E86AB;font-size:0.82rem;font-weight:600;cursor:default;transition:all 0.2s;}}
.aug-chip:hover {{background:rgba(46,134,171,0.06);}}
.emc-tab {{padding:10px 18px;font-weight:600;font-size:0.85rem;border:none;cursor:pointer;background:white;color:#718096;transition:all 0.2s;border-radius:10px;}}
.emc-tab.active {{background:#2E86AB;color:white;border-radius:10px;}}
.emc-tab:hover:not(.active) {{background:rgba(46,134,171,0.08);border-radius:10px;}}
.emc-card {{border:2px solid #e2e8f0;border-radius:12px;padding:18px;background:white;transition:all 0.25s;position:relative;}}
.emc-card:hover {{border-color:#cbd5e1;box-shadow:0 4px 12px rgba(0,0,0,0.06);}}
.emc-card.enabled {{border-color:#2E86AB;background:rgba(46,134,171,0.02);}}
.emc-badge {{display:inline-block;padding:3px 10px;border-radius:12px;font-size:0.72rem;font-weight:700;}}
.emc-badge-da {{background:#e0f2f1;color:#00897b;}}
.emc-badge-mq {{background:#e8eaf6;color:#5c6bc0;}}
.emc-badge-custom {{background:#fff3e0;color:#f57c00;}}
.emc-toggle {{position:relative;width:44px;height:24px;cursor:pointer;}}
.emc-toggle input {{opacity:0;width:0;height:0;}}
.emc-toggle .slider {{position:absolute;top:0;left:0;right:0;bottom:0;background:#ccc;border-radius:24px;transition:0.3s;}}
.emc-toggle .slider:before {{content:'';position:absolute;height:18px;width:18px;left:3px;bottom:3px;background:white;border-radius:50%;transition:0.3s;}}
.emc-toggle input:checked + .slider {{background:#2E86AB;}}
.emc-toggle input:checked + .slider:before {{transform:translateX(20px);}}
.emc-dots {{background:none;border:none;font-size:1.2rem;cursor:pointer;color:#999;padding:4px 8px;border-radius:4px;}}
.emc-dots:hover {{background:#f0f0f0;color:#333;}}
.emc-slider {{-webkit-appearance:none;width:100%;height:6px;border-radius:3px;outline:none;transition:0.2s;}}
.emc-slider::-webkit-slider-thumb {{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;cursor:pointer;border:2px solid #2E86AB;background:#2E86AB;}}
.emc-slider.inverse-slider {{}}
.emc-slider.inverse-slider::-webkit-slider-thumb {{border-color:#A23B72;background:#A23B72;}}
.cm-static-item {{display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;margin-bottom:8px;cursor:pointer;transition:all 0.15s;}}
.cm-static-item:hover {{background:rgba(46,134,171,0.04);border-color:#cbd5e1;}}
.cm-static-item.selected {{background:rgba(46,134,171,0.08);border-color:#2E86AB;}}
.cm-static-item input[type=checkbox] {{margin-top:3px;accent-color:#2E86AB;}}
"""
''')

    # ==================== templates/js_disaggregated.py ====================
    w("templates/js_disaggregated.py", r'''"""Disaggregated view JavaScript."""


def get_disagg_js():
    return """<script>var selectedSubs=[];document.addEventListener('DOMContentLoaded',function(){var ts=document.getElementById("topicSelect");var dd=document.getElementById("subTopicDropdown");if(!ts)return;ts.innerHTML="<option value=''>Select Topic</option>";Array.from(new Set(DISAGG_DATA.map(function(d){return d.topic;}))).forEach(function(t){var o=document.createElement("option");o.value=t;o.textContent=t;ts.appendChild(o);});ts.onchange=function(){selectedSubs=[];renderChips();dd.innerHTML="";var topic=ts.value;if(!topic)return;Array.from(new Set(DISAGG_DATA.filter(function(d){return d.topic===topic;}).map(function(d){return d.sub_topic;}))).forEach(function(st){var d2=document.createElement("div");d2.textContent=st;d2.onclick=function(){addSubTopic(st);};dd.appendChild(d2);});};var si=document.getElementById("subTopicInput");if(si)si.onclick=function(){dd.style.display="block";};document.addEventListener("click",function(e){if(!e.target.closest(".multi-select"))dd.style.display="none";});});function addSubTopic(s){if(selectedSubs.indexOf(s)===-1){selectedSubs.push(s);renderChips();}}function removeSub(s){selectedSubs=selectedSubs.filter(function(x){return x!==s;});renderChips();}function renderChips(){var cb=document.getElementById("selectedSubTopics");if(!cb)return;cb.innerHTML="";selectedSubs.forEach(function(s){var ch=document.createElement("div");ch.className="chip";var lb=document.createElement("span");lb.textContent=s;var cl=document.createElement("span");cl.textContent=" x";cl.style.cursor="pointer";cl.addEventListener("click",function(){removeSub(s);});ch.appendChild(lb);ch.appendChild(cl);cb.appendChild(ch);});updateChart();}function updateChart(){var te=document.getElementById("topicSelect");var topic=te?te.value:"";if(!topic||selectedSubs.length===0)return;var rows=DISAGG_DATA.filter(function(d){return d.topic===topic&&selectedSubs.indexOf(d.sub_topic)!==-1;});var metrics={};rows.forEach(function(r){Object.keys(r.metrics).forEach(function(m){var v=r.metrics[m];if(!metrics[m])metrics[m]={passed:0,failed:0};metrics[m].passed+=v.passed;metrics[m].failed+=v.failed;});});var labels=Object.keys(metrics);if(!labels.length)return;var mc=Math.max.apply(null,labels.map(function(m){return Math.max(metrics[m].passed,metrics[m].failed);}))||1;Plotly.newPlot("disaggChart",[{x:labels,y:labels.map(function(m){return metrics[m].passed;}),name:"Passed",type:"bar",marker:{color:"#2ca02c"}},{x:labels,y:labels.map(function(m){return metrics[m].failed;}),name:"Failed",type:"bar",marker:{color:"#d62728"}}],{barmode:"group",title:topic+" - "+selectedSubs.join(", "),yaxis:{title:"Count",range:[0,mc],tickmode:"linear",dtick:1}});}</script>"""
''')

    # ==================== templates/js_upload_runs.py ====================
    w("templates/js_upload_runs.py", r'''"""Upload runs comparison JavaScript."""


def get_upload_runs_js():
    return """<script>function uploadRuns(){var pf=document.getElementById("prevRun").files[0];var cf=document.getElementById("currRun").files[0];if(!pf||!cf){alert("Please upload both files");return;}var fd=new FormData();fd.append("previous_run",pf);fd.append("current_run",cf);fetch("/compare-runs",{method:"POST",body:fd}).then(function(r){return r.text();}).then(function(h){var c=document.getElementById("runComparisonResult");if(!c)return;c.innerHTML=h;Array.from(c.querySelectorAll("script")).forEach(function(os){var ns=document.createElement("script");if(os.src){ns.src=os.src;ns.async=false;}else{ns.textContent=os.innerHTML;}document.body.appendChild(ns);document.body.removeChild(ns);});}).catch(function(){document.getElementById("runComparisonResult").innerHTML="<b>Error comparing runs</b>";});}</script>"""
''')

    # ==================== templates/html_modal.py ====================
    w("templates/html_modal.py", r'''"""Detail modal HTML generator."""


def get_modern_modal():
    return """<div id="detailModal" class="modal"><div class="modal-content"><div class="modal-header"><div><h3 class="modal-title" id="modalTitle">Metric Details</h3><p class="modal-subtitle" id="modalSubtitle">Threshold: N/A</p></div><button class="modal-close" onclick="closeModal()">\u00d7</button></div><div class="modal-body"><div class="modal-left"><div id="scoreReasonBlock"><div class="modal-section score-box"><h4>Score Analysis</h4><div id="scorePieChart"></div></div><div class="modal-section evaluation-box"><h4>Evaluation Reason</h4><p id="modalReason">N/A</p></div></div><div class="modal-section"><h4>Question</h4><p id="modalQuestion">N/A</p></div><div id="rcaContainer">N/A</div><div id="secondaryContainer">N/A</div><div class="collapsible-section"><div class="collapsible-header" onclick="toggleCollapsible('response')"><h4>Response</h4><span class="toggle-icon" id="responseIcon">\u25bc</span></div><div class="collapsible-content collapsed" id="responseContent"><p id="modalResponse">N/A</p></div></div><div id="metricContainer"><div class="collapsible-section"><div class="collapsible-header" onclick="toggleCollapsible('traceback')"><h4>Traceback</h4><span class="toggle-icon" id="tracebackIcon">\u25bc</span></div><div class="collapsible-content collapsed" id="tracebackContent"><div id="tracebackFields">N/A</div></div></div><div class="collapsible-section"><div class="collapsible-header" onclick="toggleCollapsible('metricFields')"><h4>Metric Fields</h4><span class="toggle-icon" id="metricFieldsIcon">\u25bc</span></div><div class="collapsible-content collapsed" id="metricFieldsContent"><div id="metricSheetFields">N/A</div></div></div></div></div></div></div></div><div id="rcaOutputModal" class="modal"><div class="modal-content" style="max-width:900px;"><div class="modal-header"><h3>Actual Problematic Output</h3><button class="modal-close" onclick="closeRcaOutput()">\u00d7</button></div><div class="modal-body"><pre id="rcaOutputContent" style="white-space:pre-wrap;max-height:70vh;overflow:auto;"></pre></div></div></div>"""
''')

    # ==================== report_generator.py ====================
    # This is the MAIN orchestrator class - it imports from tabs and templates
    # and delegates to them. The _generate_modern_html method is in templates/html_report.py (Part 4)
    w("report_generator.py", r'''"""
Main ReportGenerator class - orchestrates all tabs and template generation.
This imports from tabs/ and templates/ to build the final HTML report.
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
from utils import (
    find_column, safe_numeric_conversion, normalize_text, text_equal,
    clean_text, normalize_query_match
)
from tabs.metrics_summary import generate_metrics_summary_table
from tabs.data_assurance import (
    create_test_coverage_sunburst, generate_augmented_data_table,
    get_coverage_edit_data
)
from tabs.model_quality_assurance import (
    generate_interactive_details_table,
    create_metrics_bar_chart, create_overall_pie_chart,
    create_score_comparison_chart, create_disaggregated_table,
    load_recovery_loop_global
)
from tabs.secondary_llm import generate_secondary_llm_table


class ReportGenerator:
    def __init__(self, config=None):
        logger.info('Initializing ReportGenerator')
        self.config = config or get_default_config()
        self.report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metric_details_excel_path = Path(__file__).resolve().parent / "final_eval_results01.xlsx"

    def _get_chart_layout(self, theme):
        return {
            'font': {'family': theme['font_family'], 'size': 12},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'height': self.config['chart_height'],
            'margin': dict(l=60, r=60, t=80, b=100),
            'xaxis': {'showgrid': True, 'gridcolor': theme['border_color'], 'tickangle': -45, 'tickfont': {'size': 10}},
            'yaxis': {'showgrid': True, 'gridcolor': theme['border_color'], 'tickfont': {'size': 10}},
        }

    def _calculate_status(self, df, metrics, thresholds):
        try:
            df_copy = df.copy()
            for metric in metrics:
                if metric not in df_copy.columns:
                    continue
                status_col = f"{metric}_status"
                reason_col = f"{metric}-reason"
                threshold = thresholds.get(metric)
                if threshold is None:
                    df_copy[status_col] = "Unknown"
                    continue
                if reason_col in df_copy.columns:
                    df_copy[status_col] = df_copy.apply(
                        lambda row, m=metric, rc=reason_col, th=threshold: self._determine_status_with_reason(row, m, rc, th), axis=1)
                else:
                    df_copy[status_col] = df_copy[metric].apply(
                        lambda x, m=metric, th=threshold: self._determine_status_simple(x, m, th))
            return df_copy
        except Exception as e:
            logger.error(f"Error calculating status: {e}")
            return df

    def _determine_status_with_reason(self, row, metric, reason_col, threshold):
        reason = str(row.get(reason_col, "")).strip().upper()
        if reason == "NA":
            return "Skipped"
        score = safe_numeric_conversion(row[metric])
        if pd.isna(score):
            return "Failed"
        if metric in self.config['reverse_metrics']:
            return "Passed" if score <= threshold else "Failed"
        return "Passed" if score >= threshold else "Failed"

    def _determine_status_simple(self, value, metric, threshold):
        score = safe_numeric_conversion(value)
        if pd.isna(score):
            return "Failed"
        if metric in self.config['reverse_metrics']:
            return "Passed" if score <= threshold else "Failed"
        return "Passed" if score >= threshold else "Failed"

    def _prepare_modal_data(self, df, metrics, thresholds):
        try:
            modal_data = {}
            metric_sheets = {}
            try:
                if self.metric_details_excel_path.exists():
                    xls = pd.ExcelFile(self.metric_details_excel_path)
                    for sheet in xls.sheet_names:
                        try:
                            metric_sheets[sheet] = pd.read_excel(xls, sheet_name=sheet)
                        except:
                            continue
            except Exception as e:
                logger.warning(f"Unable to read metric details excel: {e}")

            normalized_sheet_map = {str(s).strip().lower(): s for s in metric_sheets.keys()}

            for idx, row in df.iterrows():
                modal_data[idx] = {
                    'query': clean_text(row.get('Query', 'N/A')),
                    'response': clean_text(row.get('Response', 'N/A')),
                    'timestamp': self.report_timestamp,
                    'metrics': {},
                }
                modal_data[idx]["metric_fields"] = {}

                for metric in metrics:
                    norm_metric = str(metric).strip().lower()
                    if norm_metric in normalized_sheet_map:
                        sheet_name = normalized_sheet_map[norm_metric]
                        metric_df = metric_sheets.get(sheet_name)
                        if isinstance(metric_df, pd.DataFrame):
                            query_col = find_column(metric_df, ['Query', 'query', 'Question'])
                            found_entry = {}
                            if query_col and query_col in metric_df.columns:
                                metric_df[query_col] = metric_df[query_col].ffill()
                                details_query = normalize_text(row.get('Query', ''))
                                mask = metric_df[query_col].apply(lambda x: normalize_text(x) == details_query)
                                matched = metric_df[mask]
                                if not matched.empty:
                                    found_entry = matched.iloc[0].replace({pd.NA: None}).to_dict() if len(matched) == 1 else [r.replace({pd.NA: None}).to_dict() for _, r in matched.iterrows()]
                                else:
                                    mask2 = metric_df[query_col].apply(lambda x: text_equal(x, details_query))
                                    matched2 = metric_df[mask2]
                                    if not matched2.empty:
                                        found_entry = matched2.iloc[0].replace({pd.NA: None}).to_dict() if len(matched2) == 1 else [r.replace({pd.NA: None}).to_dict() for _, r in matched2.iterrows()]
                            modal_data[idx]["metric_fields"][str(metric).strip()] = found_entry
                        else:
                            modal_data[idx]["metric_fields"][metric] = {}
                    else:
                        modal_data[idx]["metric_fields"][metric] = {}

                self._add_metrics_data(modal_data[idx], row, metrics, thresholds)
            return modal_data
        except Exception as e:
            logger.error(f"Error preparing modal data: {e}")
            return {}

    def _add_metrics_data(self, modal_item, row, metrics, thresholds):
        for metric in metrics:
            ms = str(metric).strip()
            mn = normalize_text(ms)
            md = {
                'score': clean_text(row.get(metric, 'N/A')),
                'threshold': str(thresholds.get(metric, 'N/A')),
                'status': clean_text(row.get(f"{metric}_status", 'Unknown')),
                'additional_fields': {},
            }
            for col in row.index:
                cn = normalize_text(str(col).strip())
                if cn == mn or cn.endswith("status"):
                    continue
                if cn.startswith(mn):
                    fn = cn.replace(mn, "").strip(" _-")
                    fv = clean_text(row.get(col, ''))
                    if fv != 'N/A':
                        md['additional_fields'][fn] = fv
            modal_item['metrics'][ms] = md

    def _create_modern_charts(self, summary_df, overall_df, metrics_df, metrics_col, score_col, threshold_col):
        try:
            charts = {}
            layout_fn = self._get_chart_layout
            charts['metrics'] = create_metrics_bar_chart(summary_df, self.config, layout_fn)
            charts['overall'] = create_overall_pie_chart(overall_df, self.config, layout_fn)
            charts['comparison'] = create_score_comparison_chart(metrics_df, metrics_col, score_col, threshold_col, self.config, layout_fn)
            base_dir = Path(__file__).resolve().parent
            charts['coverage'] = create_test_coverage_sunburst(excel_path=base_dir / "Metrics_template02.xlsx", sheet_name='Test data coverage')
            charts['augmentation'] = generate_augmented_data_table(excel_path=base_dir / "agent_query_augmentations.xlsx", sheet_name='Sheet1')
            charts['disaggregated'] = create_disaggregated_table(base_dir / "Metrics_template02.xlsx")
            return charts
        except Exception as e:
            logger.error(f"Error creating charts: {e}")
            return {}

    def generate_report(self, metrics_df, details_df, summary_df, overall_df):
        try:
            logger.info("Starting report generation")
            if any(df.empty for df in [metrics_df, details_df, summary_df, overall_df]):
                return self._generate_error_report("One or more input DataFrames are empty")

            mc = find_column(metrics_df, ['Metrics', 'Metric', 'metric'])
            tc = find_column(metrics_df, ['Threshold_Value', 'Threshold', 'threshold'])
            sc = find_column(metrics_df, ['aggregate_score', 'score', 'Score'])

            if not all([mc, tc, sc]):
                return self._generate_error_report("Required columns not found")

            all_metrics = [m for m in metrics_df[mc].dropna().astype(str).tolist() if m.strip().lower() != 'knowledge retention']
            thresholds = {k: v for k, v in zip(metrics_df[mc], metrics_df[tc]) if str(k).strip().lower() != 'knowledge retention'}

            details_df = self._calculate_status(details_df, all_metrics, thresholds)
            charts = self._create_modern_charts(summary_df, overall_df, metrics_df, mc, sc, tc)
            modal_data = self._prepare_modal_data(details_df, all_metrics, thresholds)

            # Import the main HTML assembly function
            from templates.html_report import generate_modern_html
            return generate_modern_html(
                config=self.config,
                report_timestamp=self.report_timestamp,
                metrics_df=metrics_df,
                details_df=details_df,
                all_metrics=all_metrics,
                charts=charts,
                modal_data=modal_data,
                metric_details_excel_path=self.metric_details_excel_path,
            )
        except Exception as e:
            return self._generate_error_report(f"Error: {e}")

    def _generate_error_report(self, msg):
        return f"<!DOCTYPE html><html><body style='font-family:Arial;padding:40px;text-align:center;'><h1>Report Generation Error</h1><div style='color:#dc3545;margin:20px;'>{msg}</div></body></html>"
''')

    print(f"\n{'='*60}")
    print("Part 3 COMPLETE: CSS, JS templates, modal, report_generator.py")
    print(f"{'='*60}")
    print("Next: Run build_part4.py for:")
    print("  - templates/js_tw_usecase.py")
    print("  - templates/js_tw_bias.py")
    print("  - templates/js_tw_explain_trust.py")
    print("  - templates/js_pipeline.py (biggest JS)")
    print("  - templates/html_report.py (main HTML assembly)")

if __name__ == "__main__":
    build()
