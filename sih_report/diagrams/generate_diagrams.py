import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Colors
NAVY = '#0f3460'
DARK_BLUE = '#16213e'
RED = '#e94560'
WHITE = '#ffffff'
LIGHT_GRAY = '#f5f5f5'
GREEN = '#4caf50'
ORANGE = '#f57c00'
LIGHT_BLUE = '#42a5f5'
PURPLE = '#7b1fa2'
BLACK = '#000000'

OUTPUT_DIR = r"c:\Users\saxen\Documents\antigravity\beautiful-mendel\sih_report\diagrams"

def draw_box(ax, x, y, width, height, text, color=NAVY, text_color=WHITE, fontsize=12, alpha=1.0):
    box = patches.FancyBboxPatch((x, y), width, height,
                                 boxstyle="round,pad=0.1,rounding_size=0.1",
                                 facecolor=color, edgecolor=BLACK, linewidth=1, alpha=alpha)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', 
            color=text_color, fontsize=fontsize, fontweight='bold', wrap=True)
    return x + width/2, y + height/2, x, y, width, height

def draw_arrow(ax, x1, y1, x2, y2, color=BLACK):
    arrow = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                    arrowstyle='-|>', mutation_scale=20,
                                    color=color, linewidth=2)
    ax.add_patch(arrow)

def setup_fig(figsize=(14, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    return fig, ax

def save_fig(fig, filename):
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Generated: {filename}")

def diagram_1():
    fig, ax = setup_fig((14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    
    # Left
    draw_box(ax, 1, 1, 4, 4, "MANUAL AUDIT\n\n- Time-consuming\n- Error-prone\n- Point-in-time\n- Vendor-specific\n- No evidence", color=RED)
    
    # Right
    draw_box(ax, 9, 1, 4, 4, "NEXUS SOLUTION\n\n- Automated\n- Accurate\n- Continuous\n- Multi-vendor\n- Evidence-based", color=GREEN)
    
    # Arrow
    draw_arrow(ax, 5.2, 3, 8.8, 3, color=NAVY)
    
    ax.set_title("Problem \u2192 Solution Flow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_problem_solution.png')

def diagram_2():
    fig, ax = setup_fig((12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 18)
    
    steps = [
        ("Reporting", "Generate PDFs, dashboards"),
        ("Remediation Engine", "Generate config fixes"),
        ("AI Explanation Layer", "Explain violations using LLM"),
        ("RAG System", "Retrieve docs & evidence"),
        ("Compliance Engine", "Evaluate rules against schema"),
        ("Normalization Engine", "Convert to vendor-neutral schema"),
        ("Parsing Engine", "Parse raw configs"),
        ("API Layer", "Handles requests & integrations"),
        ("User Interface", "Web dashboard")
    ]
    
    y = 0.5
    for i, (title, sub) in enumerate(steps):
        text = f"{title}\n\n{sub}"
        draw_box(ax, 3, y, 6, 1.2, text, color=NAVY)
        if i < len(steps) - 1:
            draw_arrow(ax, 6, y + 1.2, 6, y + 1.7)
        y += 1.8

    ax.set_title("NEXUS Conceptual Architecture", fontsize=16, fontweight='bold', color=NAVY, y=0.95)
    save_fig(fig, 'diagram_architecture.png')

def diagram_3():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    vendors = ["Cisco IOS", "Juniper Junos", "Fortinet FortiOS", "Palo Alto PAN-OS"]
    y_pos = [6.5, 4.8, 3.1, 1.4]
    
    for i, v in enumerate(vendors):
        draw_box(ax, 0.5, y_pos[i], 3, 1, v, color=LIGHT_BLUE, text_color=BLACK)
        draw_arrow(ax, 3.6, y_pos[i] + 0.5, 5.8, 4)
        
    draw_box(ax, 6, 3, 3, 2, "AI Configuration\nInterpreter", color=DARK_BLUE)
    draw_arrow(ax, 9.1, 4, 10.4, 4)
    
    draw_box(ax, 10.5, 4.5, 3, 1.5, "Vendor-Neutral\nSecurity Schema (JSON)", color=NAVY)
    draw_arrow(ax, 12, 4.4, 12, 3.6)
    
    draw_box(ax, 10.5, 2, 3, 1.5, "Compliance Engine", color=NAVY)
    
    draw_arrow(ax, 12, 1.9, 10.5, 0.8)
    draw_arrow(ax, 12, 1.9, 12, 0.8)
    draw_arrow(ax, 12, 1.9, 13.5, 0.8)
    
    draw_box(ax, 9.5, 0, 1.5, 0.7, "CIS", color=GREEN)
    draw_box(ax, 11.25, 0, 1.5, 0.7, "NIST", color=GREEN)
    draw_box(ax, 13, 0, 1.5, 0.7, "STIG", color=GREEN)
    
    ax.set_title("Multi-Vendor Configuration Flow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_multivendor_flow.png')

def diagram_4():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    draw_box(ax, 1, 5, 3, 2, "Cisco IOS\n\ntransport input ssh\nip ssh version 2\nexec-timeout 10 0", color=LIGHT_BLUE, text_color=BLACK, fontsize=10)
    draw_box(ax, 5.5, 5, 3, 2, "Juniper Junos\n\nset system services ssh\nprotocol-version v2\nidle-timeout 10", color=LIGHT_BLUE, text_color=BLACK, fontsize=10)
    draw_box(ax, 10, 5, 3, 2, "Fortinet FortiOS\n\nset admin-sport 443\nadmin-https-ssl-versions tlsv1-2\nidle-timeout 600", color=LIGHT_BLUE, text_color=BLACK, fontsize=10)
    
    draw_arrow(ax, 2.5, 4.9, 7, 3.1)
    draw_arrow(ax, 7, 4.9, 7, 3.1)
    draw_arrow(ax, 11.5, 4.9, 7, 3.1)
    
    draw_box(ax, 4, 1, 6, 2, "Common Security Model\n\nssh.enabled=true\nssh.version=2\nsession_timeout=600", color=NAVY)
    
    ax.set_title("Vendor Normalization Concept", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_normalization.png')

def diagram_5():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    draw_box(ax, 1, 6, 2.5, 1, "Normalized Config", color=NAVY)
    draw_box(ax, 1, 4, 2.5, 1, "Load YAML Rules", color=NAVY)
    draw_box(ax, 1, 2, 2.5, 1, "Evaluate Each Rule", color=NAVY)
    
    draw_arrow(ax, 2.25, 5.9, 2.25, 5.1)
    draw_arrow(ax, 2.25, 3.9, 2.25, 3.1)
    draw_arrow(ax, 3.6, 2.5, 4.4, 2.5)
    
    draw_box(ax, 4.5, 2, 2.5, 1, "Pass/Fail Decision", color=NAVY)
    
    # Branches
    draw_arrow(ax, 7.1, 2.8, 8, 4)
    draw_arrow(ax, 7.1, 2.2, 8, 1)
    
    draw_box(ax, 8, 3.5, 2.5, 1, "Compliant", color=GREEN)
    draw_box(ax, 8, 0.5, 2.5, 1, "Violation Detected", color=RED)
    
    draw_arrow(ax, 10.6, 1, 11.4, 1)
    draw_box(ax, 11.5, 0.5, 2, 1.5, "Explanation +\nRemediation", color=PURPLE)
    
    draw_arrow(ax, 5.75, 3.1, 5.75, 4.9)
    draw_box(ax, 4.5, 5, 2.5, 1, "Evidence Collection", color=NAVY)
    
    draw_arrow(ax, 7.1, 5.5, 8.4, 5.5)
    draw_box(ax, 8.5, 5, 2.5, 1, "Risk Score Calculation", color=NAVY)
    
    draw_arrow(ax, 11.1, 5.5, 11.9, 5.5)
    draw_box(ax, 12, 5, 1.8, 1, "Findings Report", color=NAVY)
    
    ax.set_title("Compliance Evaluation Flow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_compliance_flow.png')

def diagram_6():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    draw_box(ax, 1, 2, 5, 5, "DETERMINISTIC\n\n- Compliance Decision\n- Rule Matching\n- Risk Scoring\n- Configuration Parsing", color=LIGHT_BLUE, text_color=BLACK, fontsize=14)
    draw_box(ax, 8, 2, 5, 5, "AI-POWERED\n\n- Violation Explanation\n- Remediation Generation\n- RAG Retrieval\n- Natural Language Q&A\n- Unknown Config Interpretation", color=PURPLE, fontsize=14)
    
    draw_box(ax, 1, 0.5, 12, 1, "AI interprets \u2192 Deterministic engine verifies", color=NAVY, fontsize=14)
    
    ax.set_title("AI + Deterministic Rules Relationship", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_ai_deterministic.png')

def diagram_7():
    fig, ax = setup_fig((14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    
    draw_box(ax, 1, 8.5, 12, 1, "Document Sources\n(CIS PDFs, NIST SP 800-53, DISA STIGs, Vendor Docs)", color=DARK_BLUE)
    draw_arrow(ax, 7, 8.4, 7, 7.6)
    
    draw_box(ax, 4, 6.5, 6, 1, "Document Ingestion (PDF \u2192 Text \u2192 Chunk \u2192 Metadata)", color=NAVY)
    draw_arrow(ax, 7, 6.4, 7, 5.6)
    
    draw_box(ax, 4.5, 4.5, 5, 1, "Embedding Model", color=PURPLE)
    draw_arrow(ax, 7, 4.4, 7, 3.6)
    
    draw_box(ax, 4.5, 2.5, 5, 1, "Vector Database (Qdrant/Chroma)", color=NAVY)
    
    # Query branch
    draw_box(ax, 0.5, 0.5, 2.5, 1, "Violation Query", color=RED)
    draw_arrow(ax, 3.1, 1, 3.9, 1)
    draw_box(ax, 4, 0.5, 2, 1, "Query Embed", color=PURPLE)
    draw_arrow(ax, 6.1, 1, 6.9, 1)
    draw_box(ax, 7, 0.5, 2, 1, "Vector Search", color=NAVY)
    draw_arrow(ax, 7.5, 2.4, 7.5, 1.6) # From DB
    
    draw_arrow(ax, 9.1, 1, 9.9, 1)
    draw_box(ax, 10, 0.5, 3.5, 2.5, "Top K Chunks \u2192 Reranking\n\u2193\nLLM + Context\n\u2193\nExplanation with Citations", color=GREEN)
    
    ax.set_title("RAG Architecture", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_rag_architecture.png')

def diagram_8():
    fig, ax = setup_fig((12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    
    steps = [
        (6, 8.5, "Unknown Configuration", NAVY),
        (9, 6.5, "AI Interpretation\n(with confidence %)", PURPLE),
        (9, 3.5, "Human Review\n(Accept/Edit/Reject)", ORANGE),
        (6, 1.5, "Knowledge Store Update", NAVY),
        (3, 3.5, "Parser/Heuristic\nEnhancement", LIGHT_BLUE),
        (3, 6.5, "Future Configs\nUnderstood Automatically", GREEN)
    ]
    
    for x, y, text, color in steps:
        tc = BLACK if color == LIGHT_BLUE else WHITE
        draw_box(ax, x-1.5, y-0.75, 3, 1.5, text, color=color, text_color=tc)
        
    draw_arrow(ax, 7.6, 8.5, 9, 7.4)
    draw_arrow(ax, 10.5, 5.6, 10.5, 4.4)
    draw_arrow(ax, 9, 2.6, 7.6, 1.5)
    draw_arrow(ax, 4.4, 1.5, 3, 2.6)
    draw_arrow(ax, 1.5, 4.4, 1.5, 5.6)
    draw_arrow(ax, 3, 7.4, 4.4, 8.5)
    
    ax.text(6, 5, "Human-in-the-Loop\nSemantic Adaptation", ha='center', va='center', fontsize=14, fontweight='bold', color=DARK_BLUE)
    
    ax.set_title("Adaptive Learning Loop", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_adaptive_learning.png')

def diagram_9():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    ax.text(7, 7, "Risk = Severity \u00D7 Asset Criticality \u00D7 Exploitability", ha='center', fontsize=16, fontweight='bold', color=NAVY)
    
    draw_box(ax, 1, 4.5, 3.5, 1.5, "Severity\nCritical=10, High=7.5\nMedium=5, Low=2.5", color=NAVY)
    draw_box(ax, 1, 2.5, 3.5, 1.5, "Asset Criticality\nCore=10, Distribution=7\nAccess=5", color=NAVY)
    draw_box(ax, 1, 0.5, 3.5, 1.5, "Exploitability\nInternet=10, DMZ=7\nInternal=5", color=NAVY)
    
    draw_arrow(ax, 4.6, 5.25, 6, 3.5)
    draw_arrow(ax, 4.6, 3.25, 6, 3.5)
    draw_arrow(ax, 4.6, 1.25, 6, 3.5)
    
    draw_box(ax, 6, 2.75, 1.5, 1.5, "\u00D7", color=DARK_BLUE, fontsize=24)
    draw_arrow(ax, 7.6, 3.5, 9, 3.5)
    
    draw_box(ax, 9, 2.5, 4, 2, "Risk Score (0-1000)\n\n0-200 Low (Green)\n200-500 Medium (Yellow)\n500-750 High (Orange)\n750-1000 Critical (Red)", color=LIGHT_GRAY, text_color=BLACK)
    
    ax.set_title("Risk Scoring Flow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_risk_scoring.png')

def diagram_10():
    fig, ax = setup_fig((12, 12))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    
    steps = [
        ("Verify Resolution", GREEN),
        ("Re-Audit", NAVY),
        ("Apply (Optional, with rollback)", LIGHT_BLUE),
        ("Dry-Run Validation", NAVY),
        ("Human Approval Required", ORANGE),
        ("Generate Config Diff (Before/After)", PURPLE),
        ("LLM Enhancement (add context, explain risk)", PURPLE),
        ("Retrieve Remediation Template (from YAML)", NAVY),
        ("Violation Detected", RED)
    ]
    
    y = 0.5
    for i, (text, color) in enumerate(steps):
        tc = BLACK if color in [LIGHT_BLUE] else WHITE
        draw_box(ax, 3, y, 6, 1.0, text, color=color, text_color=tc)
        if i < len(steps) - 1:
            draw_arrow(ax, 6, y + 1.1, 6, y + 1.6)
        y += 1.7

    ax.set_title("Remediation Workflow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_remediation.png')

def diagram_11():
    fig, ax = setup_fig((14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    
    draw_box(ax, 0.5, 5, 2.5, 2, "Data Sources\nVendor Docs,\nPublic Examples,\nCIS/STIG Samples", color=NAVY)
    
    draw_arrow(ax, 3.1, 6, 4, 6)
    draw_box(ax, 4, 5.5, 2.5, 1, "Template-Based\nGeneration", color=NAVY)
    
    draw_arrow(ax, 6.6, 6, 7.5, 6)
    draw_box(ax, 7.5, 5.5, 2.5, 1, "Controlled\nViolation Injection", color=NAVY)
    
    draw_arrow(ax, 10.1, 6, 11, 6)
    draw_box(ax, 11, 5, 2.5, 2, "Labeled Dataset\n(Config + Expected Results)", color=GREEN)
    
    draw_arrow(ax, 12.25, 4.9, 12.25, 3.6)
    draw_box(ax, 10.5, 2.5, 3.5, 1, "Split\n(70% Dev, 15% Val, 15% Test)", color=NAVY)
    
    draw_arrow(ax, 10.4, 3, 9.6, 3)
    draw_box(ax, 7, 2.5, 2.5, 1, "Evaluation\n(Accuracy, Precision, Recall, F1)", color=PURPLE)
    
    draw_arrow(ax, 8.75, 4.5, 8.75, 3.6)
    draw_box(ax, 7.5, 4.5, 2.5, 0.8, "Ground Truth Comparison", color=ORANGE)
    
    ax.set_title("Dataset Generation & Evaluation Flow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_dataset_flow.png')

def diagram_12():
    fig, ax = setup_fig((16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    
    boxes = [
        (0.5, 7, "User Uploads Config", NAVY),
        (3, 7, "Vendor Auto-Detection", NAVY),
        (6, 7, "Configuration Parsing", NAVY),
        (9, 7, "Normalization to\nCommon Schema", NAVY),
        (12, 7, "Compliance Scan\n(CIS/NIST/STIG)", NAVY),
        (12, 4.5, "Risk Score Calculation", NAVY),
        (9, 4.5, "RAG Retrieval", PURPLE),
        (6, 4.5, "AI Explanation", PURPLE),
        (3, 4.5, "Remediation Generation", PURPLE),
        (0.5, 4.5, "Dashboard Display", NAVY),
        (0.5, 2, "PDF Report Export", NAVY)
    ]
    
    for x, y, text, color in boxes:
        draw_box(ax, x, y, 2.2, 1.2, text, color=color, fontsize=10)
        
    draw_arrow(ax, 2.8, 7.6, 2.9, 7.6) # 0 to 1
    draw_arrow(ax, 5.3, 7.6, 5.9, 7.6) # 1 to 2
    draw_arrow(ax, 8.3, 7.6, 8.9, 7.6) # 2 to 3
    draw_arrow(ax, 11.3, 7.6, 11.9, 7.6) # 3 to 4
    
    draw_arrow(ax, 13.1, 6.9, 13.1, 5.8) # 4 to 5
    
    draw_arrow(ax, 11.9, 5.1, 11.3, 5.1) # 5 to 6
    draw_arrow(ax, 8.9, 5.1, 8.3, 5.1) # 6 to 7
    draw_arrow(ax, 5.9, 5.1, 5.3, 5.1) # 7 to 8
    draw_arrow(ax, 2.9, 5.1, 2.8, 5.1) # 8 to 9
    
    draw_arrow(ax, 1.6, 4.4, 1.6, 3.3) # 9 to 10
    
    # Parallel branch for unknown config
    draw_box(ax, 6, 2, 2.2, 1.2, "Unknown Config", RED, fontsize=10)
    draw_box(ax, 9, 2, 2.2, 1.2, "Adaptive Learning", ORANGE, fontsize=10)
    draw_box(ax, 12, 2, 2.2, 1.2, "Knowledge Update", GREEN, fontsize=10)
    
    draw_arrow(ax, 7.1, 6.9, 7.1, 3.3) # Parse to Unknown
    draw_arrow(ax, 8.3, 2.6, 8.9, 2.6) # Unk to Adapt
    draw_arrow(ax, 11.3, 2.6, 11.9, 2.6) # Adapt to Knowl
    draw_arrow(ax, 13.1, 3.3, 13.1, 6.9) # Knowl to Compliance
    
    ax.set_title("Complete End-to-End Workflow", fontsize=16, fontweight='bold', color=NAVY)
    save_fig(fig, 'diagram_end_to_end.png')

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    diagram_1()
    diagram_2()
    diagram_3()
    diagram_4()
    diagram_5()
    diagram_6()
    diagram_7()
    diagram_8()
    diagram_9()
    diagram_10()
    diagram_11()
    diagram_12()
    print("All diagrams generated successfully.")

if __name__ == '__main__':
    main()
