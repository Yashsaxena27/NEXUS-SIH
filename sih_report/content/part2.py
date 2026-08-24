"""
SIH 26155 Master Report — Content Part 2
Sections: 8. Architecture through 18. Security Architecture
"""

import os

def get_html():
    return _architecture() + _parsing() + _normalization() + _compliance_engine() + _ai_ml_role() + _rag_system() + _remediation() + _risk_scoring() + _adaptive_learning() + _drift() + _security_arch()

# ── 8. System Architecture ─────────────────────────────────────────

def _architecture():
    return '''
<section class="section" id="architecture">
<h1>8. System Architecture</h1>

<p>The NEXUS architecture is designed to cleanly separate vendor-specific ingestion from vendor-agnostic compliance evaluation. This decoupling is what makes multi-vendor support scalable.</p>

<div class="figure">
<img src="../diagrams/diagram_architecture.png" alt="NEXUS Conceptual Architecture" />
<div class="figure-caption">Figure 1: NEXUS 7-Layer Conceptual Architecture</div>
</div>

<h2 id="arch-overview">8.1 Architecture Overview</h2>
<p>The system comprises seven logical layers:</p>
<ol>
<li><strong>Data Ingestion &amp; UI Layer:</strong> Next.js frontend, accepts config files or API uploads.</li>
<li><strong>Vendor Auto-Detection:</strong> NLP/Heuristics to identify device OS without user input.</li>
<li><strong>Parsing Layer:</strong> Converts raw CLI text into vendor-specific structured data (AST/JSON).</li>
<li><strong>Normalization Layer:</strong> Translates vendor-specific JSON into the Common Security Schema.</li>
<li><strong>Compliance Engine (Deterministic):</strong> Evaluates the normalized schema against YAML rule sets.</li>
<li><strong>AI/RAG Layer:</strong> Generates natural language explanations, retrieves citations from standards, and formats remediation.</li>
<li><strong>Reporting &amp; Export:</strong> Generates PDF reports and risk dashboards.</li>
</ol>

<h2 id="mvp-arch">8.2 36-Hour MVP Architecture</h2>
<p>For the SIH hackathon, we must aggressively scope the architecture to what can be built in 36 hours:</p>
<ul>
<li><strong>Frontend:</strong> Next.js (React) for a professional, enterprise-grade interface.</li>
<li><strong>Backend:</strong> FastAPI (Python 3.10+).</li>
<li><strong>Database:</strong> SQLite or TinyDB (avoiding complex PostgreSQL setups).</li>
<li><strong>Vector Store:</strong> ChromaDB or FAISS (in-memory, no external services).</li>
<li><strong>LLM:</strong> Local Ollama (Llama 3 8B) or API fallback (Gemini/OpenAI) if permitted.</li>
</ul>

<h2 id="strong-arch">8.3 Strong SIH Submission Architecture</h2>
<p>To win, the architecture must demonstrate enterprise readiness even if the MVP is simplified:</p>
<ul>
<li><strong>Event-Driven:</strong> RabbitMQ or Redis queues for async config processing.</li>
<li><strong>Storage:</strong> PostgreSQL for state, MinIO/S3 for raw configs.</li>
<li><strong>Vector DB:</strong> Qdrant or Milvus for scalable RAG.</li>
</ul>

<h2 id="production-arch">8.4 Production-Grade Future Architecture</h2>
<p>For real-world NTRO deployment:</p>
<ul>
<li>Air-gapped deployment capability (no public cloud APIs).</li>
<li>Kubernetes cluster orchestration.</li>
<li>Local open-source LLMs (e.g., Mistral/Llama 3 via vLLM) on dedicated GPU nodes.</li>
<li>Integration with SIEM (Splunk/QRadar) via Syslog/Webhooks.</li>
</ul>
</section>
'''

# ── 9. Configuration Parsing Engine ────────────────────────────────

def _parsing():
    return '''
<section class="section" id="parsing">
<h1>9. Configuration Parsing Engine</h1>

<p>Before any intelligence can be applied, raw text must become structured data.</p>

<h2 id="parser-comparison">9.1 Parser Comparison</h2>
<table>
<thead><tr><th>Tool</th><th>Approach</th><th>Pros</th><th>Cons</th></tr></thead>
<tbody>
<tr><td><strong>Regex</strong></td><td>Text matching</td><td>Fast, zero dependencies</td><td>Brittle, fails on nested blocks</td></tr>
<tr><td><strong>Batfish</strong></td><td>Java AST</td><td>Incredibly powerful</td><td>Huge dependency, hard to extend</td></tr>
<tr><td><strong>TextFSM / NTC</strong></td><td>Templates</td><td>Industry standard</td><td>Need templates for everything</td></tr>
<tr><td><strong>Netmiko</strong></td><td>Scraping</td><td>Great for SSH extraction</td><td>Doesn't parse meaning, just gets text</td></tr>
<tr><td><strong>CiscoConfParse2</strong></td><td>Python Object Tree</td><td>Understands parent/child config relationships natively</td><td>Mostly Cisco/Arista focused (though adaptable)</td></tr>
</tbody>
</table>

<h2 id="ciscoconfparse">9.2 CiscoConfParse2 — Recommended Parser</h2>
<p>For the hackathon, building custom AST parsers is too slow. <strong>CiscoConfParse2</strong> is the ideal choice. Despite the name, it can parse any bracketed or indented configuration format (Cisco, Juniper, Palo Alto, F5).</p>

<div class="callout callout-technical">
<div class="callout-title">Why CiscoConfParse2?</div>
<p>It natively understands that <code>ip ssh version 2</code> is a global command, but <code>transport input ssh</code> belongs to the parent <code>line vty 0 4</code>. This context is critical for security checks.</p>
</div>

<h2 id="parser-examples">9.3 Parser Code Examples</h2>
<pre><code>from ciscoconfparse2 import CiscoConfParse

# Load Cisco config
parse = CiscoConfParse("router_config.txt")

# Find all VTY lines
vty_lines = parse.find_objects(r"^line vty")

for line in vty_lines:
    # Check if transport input ssh is configured under this specific line
    has_ssh = line.re_search_children(r"transport input ssh")
    if not has_ssh:
        print(f"Violation on {line.text}: SSH not explicitly required")
</code></pre>
</section>
'''

# ── 10. Configuration Normalization ────────────────────────────────

def _normalization():
    return '''
<section class="section" id="normalization">
<h1>10. Configuration Normalization Engine</h1>

<div class="figure">
<img src="../diagrams/diagram_multivendor_flow.png" alt="Multi-Vendor Flow" />
<div class="figure-caption">Figure 2: Multi-Vendor Configuration Ingestion Flow</div>
</div>

<h2 id="why-normalize">10.1 Why Normalization Is Critical</h2>
<p>Without normalization, you must write a "Disable Telnet" rule four times (Cisco, Juniper, Fortinet, Palo Alto). With normalization, you write it <strong>once</strong>.</p>

<div class="figure">
<img src="../diagrams/diagram_normalization.png" alt="Vendor Normalization" />
<div class="figure-caption">Figure 3: Vendor Normalization Concept</div>
</div>

<h2 id="openconfig">10.2 OpenConfig / YANG Approach</h2>
<p>OpenConfig provides vendor-neutral YANG data models for network devices. While robust, mapping legacy CLI to OpenConfig is a massive engineering effort—too large for a 36-hour hackathon.</p>

<h2 id="custom-schema">10.3 Lightweight Custom Schema (Recommended)</h2>
<p>We propose a lightweight, security-focused JSON schema that captures <em>only</em> what matters for compliance:</p>
<ul>
<li><code>mgmt.ssh.enabled</code> (boolean)</li>
<li><code>mgmt.telnet.enabled</code> (boolean)</li>
<li><code>mgmt.session_timeout_seconds</code> (integer)</li>
<li><code>auth.aaa_enabled</code> (boolean)</li>
<li><code>logging.syslog_servers</code> (list of strings)</li>
</ul>

<h2 id="norm-code">10.4 Normalization Logic (Python)</h2>
<pre><code>class CiscoNormalizer:
    def normalize(self, parsed_config):
        normalized = BaseSecuritySchema()
        
        # Check SSH
        ssh_cmd = parsed_config.find_objects(r"^ip ssh version")
        if ssh_cmd and "2" in ssh_cmd[0].text:
            normalized.mgmt.ssh.version = 2
            
        # Check Telnet (Is there a 'transport input' without ssh?)
        # ... logic ...
        
        return normalized
</code></pre>
</section>
'''

# ── 11. Compliance Engine ──────────────────────────────────────────

def _compliance_engine():
    return '''
<section class="section" id="compliance-engine">
<h1>11. Compliance Engine</h1>

<p>The compliance engine evaluates the normalized JSON schema against deterministic rules. <strong>It does not use AI to make Pass/Fail decisions.</strong></p>

<div class="figure">
<img src="../diagrams/diagram_compliance_flow.png" alt="Compliance Evaluation Flow" />
<div class="figure-caption">Figure 4: Compliance Evaluation Flow</div>
</div>

<h2 id="rule-engine">11.1 Rule Engine Design</h2>
<p>We use a YAML-based rule definition. This keeps code and policy separate, allowing security engineers to write rules without knowing Python.</p>

<h2 id="yaml-rules">11.2 YAML Rule Format</h2>
<pre><code>rule_id: CIS-1.1
title: "Ensure Telnet is Disabled"
description: "Telnet transmits data in plaintext. SSH must be used."
severity: CRITICAL
framework_mappings:
  cis_cisco: "1.1"
  nist_800_53: ["AC-17", "CM-7"]
  disa_stig: "NET0020"
condition:
  # Evaluated against normalized schema using JSONPath or PySensors
  path: "mgmt.telnet.enabled"
  operator: "equals"
  value: false
remediation_templates:
  cisco: "no transport input telnet\\ntransport input ssh"
  juniper: "delete system services telnet"
</code></pre>

<h2 id="engine-implementation">11.3 Engine Implementation (Python)</h2>
<pre><code>import yaml
import jsonpath_ng

def evaluate_rule(rule_yaml, normalized_json):
    path_expr = jsonpath_ng.parse(rule_yaml['condition']['path'])
    match = path_expr.find(normalized_json)
    
    if not match:
        return "UNKNOWN" # Data point missing
        
    actual_value = match[0].value
    expected = rule_yaml['condition']['value']
    operator = rule_yaml['condition']['operator']
    
    if operator == "equals":
        passed = (actual_value == expected)
    elif operator == "greater_than":
        passed = (actual_value > expected)
        
    return "PASS" if passed else "FAIL"
</code></pre>

<h2 id="oscal">11.5 NIST OSCAL Integration</h2>
<p>To demonstrate enterprise maturity, the engine can map its YAML rules to NIST OSCAL (Open Security Controls Assessment Language) component definitions. This allows exporting audit results in a standardized XML/JSON format that government GRC tools (like Archer or eMASS) can ingest directly.</p>
</section>
'''

# ── 12. AI/ML Role ─────────────────────────────────────────────────

def _ai_ml_role():
    return '''
<section class="section" id="ai-ml-role">
<h1>12. AI/ML Role — Where AI Helps and Where It Doesn't</h1>

<p>The biggest trap in this hackathon is attempting to use an LLM to read a config file and ask "Is this secure?" LLMs hallucinate, miss subtle configuration inheritance, and cannot provide deterministic audit trails.</p>

<div class="figure">
<img src="../diagrams/diagram_ai_deterministic.png" alt="AI vs Deterministic" />
<div class="figure-caption">Figure 5: Separation of Deterministic Rules and AI Inference</div>
</div>

<h2 id="ai-suitable">12.1 AI Suitability Matrix</h2>
<table>
<thead><tr><th>Task</th><th>Use AI/LLM?</th><th>Why?</th></tr></thead>
<tbody>
<tr><td><strong>Pass/Fail Decision</strong></td><td><span class="badge badge-fail">NO</span></td><td>Must be 100% deterministic and auditable. AI hallucinates.</td></tr>
<tr><td><strong>Rule Evaluation</strong></td><td><span class="badge badge-fail">NO</span></td><td>Math/logic operations are better in Python.</td></tr>
<tr><td><strong>Syntax Parsing</strong></td><td><span class="badge badge-fail">NO</span></td><td>Regex/AST parsers are infinitely faster and more accurate.</td></tr>
<tr><td><strong>Unknown Syntax Inference</strong></td><td><span class="badge badge-pass">YES</span></td><td>LLMs excel at inferring the meaning of new/custom commands.</td></tr>
<tr><td><strong>Violation Explanation</strong></td><td><span class="badge badge-pass">YES</span></td><td>Translates "Rule 4.1 Failed" into human-readable impact.</td></tr>
<tr><td><strong>Remediation Generation</strong></td><td><span class="badge badge-pass">YES</span></td><td>Can tailor fix commands to the specific context of the device.</td></tr>
<tr><td><strong>Q&A / Chatbot</strong></td><td><span class="badge badge-pass">YES</span></td><td>"Why does this router have a high risk score?"</td></tr>
</tbody>
</table>

<h2 id="ai-explanation">12.3 AI Explanation Generation</h2>
<p>When a rule fails, the LLM is invoked to explain the risk. It is provided with:</p>
<ol>
<li>The failing rule title.</li>
<li>The exact snippet of the configuration that failed.</li>
<li>RAG context from CIS/NIST standards detailing the risk.</li>
</ol>
<p><strong>Prompt Template:</strong> <em>"You are a network security auditor. The following configuration snippet failed the {rule_title} check. Using the provided NIST context, explain the business risk of this misconfiguration in 2 paragraphs."</em></p>
</section>
'''

# ── 13. RAG System ─────────────────────────────────────────────────

def _rag_system():
    return '''
<section class="section" id="rag-system">
<h1>13. RAG System (Retrieval-Augmented Generation)</h1>

<p>To prevent the AI from hallucinating security advice, we use RAG to ground its explanations in authoritative documentation.</p>

<div class="figure">
<img src="../diagrams/diagram_rag_architecture.png" alt="RAG Architecture" />
<div class="figure-caption">Figure 6: RAG Architecture for Compliance Citations</div>
</div>

<h2 id="rag-sources">13.1 Knowledge Sources</h2>
<p>The vector database is populated pre-hackathon with chunked, embedded text from:</p>
<ul>
<li>CIS Benchmarks (PDFs converted to text)</li>
<li>NIST SP 800-53 rev 5 (JSON/XML)</li>
<li>DISA STIG descriptions</li>
<li>Vendor hardening guides</li>
</ul>

<h2 id="vector-db">13.3 Vector Database Comparison</h2>
<p>For a 36-hour build, <strong>ChromaDB</strong> or <strong>FAISS</strong> running locally is recommended over managed services like Pinecone, ensuring the system can run offline (a critical government requirement).</p>

<h2 id="hallucination">13.4 Hallucination Prevention</h2>
<p>We enforce strict grounding prompts:</p>
<pre><code>Answer the user's question about the security violation using ONLY the provided context blocks below. 
If the context does not contain the answer, reply "I cannot answer this based on the provided compliance standards."
Do NOT invent commands or cite frameworks not present in the context.

Context:
{retrieved_documents}</code></pre>
</section>
'''

# ── 14. Remediation Engine ─────────────────────────────────────────

def _remediation():
    return '''
<section class="section" id="remediation-engine">
<h1>14. Remediation Engine</h1>

<p>Detecting a problem is only half the battle. NEXUS must provide the exact CLI commands to fix it.</p>

<div class="figure">
<img src="../diagrams/diagram_remediation.png" alt="Remediation Workflow" />
<div class="figure-caption">Figure 7: Secure Remediation Workflow</div>
</div>

<h2 id="remediation-workflow">14.1 Remediation Workflow</h2>
<ol>
<li><strong>Base Template:</strong> The YAML rule provides a static remediation template (e.g., <code>transport input ssh</code>).</li>
<li><strong>Context Injection:</strong> Python injects device-specific context (e.g., applying it to <code>line vty 0 4</code> vs <code>line vty 0 15</code> depending on what the device actually has).</li>
<li><strong>Diff Generation:</strong> The UI displays a clear before/after diff of the proposed changes.</li>
</ol>

<h2 id="remediation-safety">14.2 Safety Mechanisms</h2>
<div class="callout callout-warning">
<div class="callout-title">Read-Only Operations</div>
<p>For the SIH prototype, the system should <strong>NOT</strong> attempt to SSH back into the device to apply changes automatically. Network engineers do not trust autonomous AI making changes. The system should generate a downloadable <code>.txt</code> or Ansible playbook containing the fix commands for human review.</p>
</div>
</section>
'''

# ── 15. Risk Scoring ───────────────────────────────────────────────

def _risk_scoring():
    return '''
<section class="section" id="risk-scoring">
<h1>15. Risk Scoring</h1>

<p>Not all compliance violations are equal. Missing a login banner is a finding; leaving Telnet exposed to the internet is an emergency.</p>

<div class="figure">
<img src="../diagrams/diagram_risk_scoring.png" alt="Risk Scoring Flow" />
<div class="figure-caption">Figure 8: CVSS-Inspired Risk Scoring Model</div>
</div>

<h2 id="scoring-model">15.1 Scoring Model</h2>
<p>We implement a risk scoring algorithm inspired by CVSS, tailored for configuration compliance:</p>

<div class="kv-grid">
<dt>Base Score</dt><dd>Derived from the Rule Severity (Critical=10, High=7, Medium=4, Low=1)</dd>
<dt>Asset Criticality</dt><dd>Multiplier based on device role (Core Router = 1.0, Edge Firewall = 1.0, Access Switch = 0.5)</dd>
<dt>Exposure Factor</dt><dd>Is the vulnerable interface public-facing? (Yes = 1.0, Internal = 0.6, OOB Mgmt = 0.3)</dd>
</div>

<h2 id="risk-formula">15.2 Risk Score Formula</h2>
<pre><code>Device_Risk_Score = Σ (Violation_Severity × Asset_Criticality × Exposure_Factor)
Normalized_Score = MIN(100, (Device_Risk_Score / Max_Possible_Score) * 100)
Compliance_Percentage = 100 - Normalized_Score</code></pre>

<div class="two-col">
<div class="score-display score-critical">
<div class="score-number">42%</div>
<div>Compliance Score (FAIL)</div>
</div>
<div class="score-display score-good">
<div class="score-number">98%</div>
<div>Compliance Score (PASS)</div>
</div>
</div>
</section>
'''

# ── 16. Adaptive Learning ──────────────────────────────────────────

def _adaptive_learning():
    return '''
<section class="section" id="adaptive-learning">
<h1>16. Adaptive Learning — Signature Feature</h1>

<div class="callout callout-key-insight">
<div class="callout-title">The "Aha!" Moment for Judges</div>
<p>This is the feature that wins the hackathon. It solves the biggest problem with hard-coded parsers: what happens when a vendor releases a new OS version with slightly different syntax?</p>
</div>

<div class="figure">
<img src="../diagrams/diagram_adaptive_learning.png" alt="Adaptive Learning" />
<div class="figure-caption">Figure 9: Human-in-the-Loop Semantic Adaptation</div>
</div>

<h2 id="adaptive-concept">16.1 The Adaptive Learning Concept</h2>
<p>When the normalizer encounters a command it doesn't recognize (e.g., a new vendor <code>configure sys access ssh</code>):</p>
<ol>
<li>It flags it as <strong>"Unknown Semantics"</strong>.</li>
<li>It uses the LLM to hypothesize the meaning: <em>"This looks like SSH enablement."</em></li>
<li>It presents this hypothesis to the human administrator in a "Semantic Mapping" UI.</li>
<li>The human clicks <strong>"Confirm"</strong> or <strong>"Edit"</strong>.</li>
<li>The system writes a new mapping rule to its local knowledge base.</li>
<li><strong>Next time, it parses it deterministically without LLM overhead.</strong></li>
</ol>

<p>This creates a system that gets smarter and broader the more it is used, seamlessly expanding to new vendors without code updates.</p>
</section>
'''

# ── 17. Configuration Drift ────────────────────────────────────────

def _drift():
    return '''
<section class="section" id="config-drift">
<h1>17. Configuration Drift Detection</h1>

<h2 id="drift-problem">17.1 The Drift Problem</h2>
<p>Compliance is continuous, not point-in-time. A network is secure on Friday and vulnerable on Monday due to a weekend troubleshooting change.</p>

<h2 id="drift-implementation">17.2 Implementation</h2>
<p>NEXUS maintains a baseline of the last known "compliant" state. When a new config is uploaded (or fetched via API):</p>
<ol>
<li>Calculate SHA-256 hash of the normalized JSON (ignoring transient data like uptime).</li>
<li>If hash differs from baseline, run a logical diff.</li>
<li>Highlight exactly which security control drifted.</li>
<li>Trigger a "Drift Alert" in the UI.</li>
</ol>
</section>
'''

# ── 18. Security Architecture ──────────────────────────────────────

def _security_arch():
    return '''
<section class="section" id="security-arch">
<h1>18. Security Architecture</h1>

<p>A security tool must itself be secure. Judges will scrutinize how you handle sensitive configuration data.</p>

<h2 id="secret-redaction">18.2 Secret Redaction</h2>
<p>Network configs contain highly sensitive data: enable passwords, SNMP strings, pre-shared keys (PSKs), and BGP passwords.</p>
<p><strong>Implementation:</strong> Before a configuration ever hits the LLM (or even the database), a regex-based sanitization pass must run to redact secrets.</p>
<pre><code># Sanitization Example
snmp-server community MySecretString RW
# Becomes:
snmp-server community [REDACTED_SNMP_RW] RW</code></pre>

<h2 id="llm-privacy">18.3 LLM Privacy Architecture</h2>
<p>For government/defense scenarios (NTRO), uploading network topology and configurations to OpenAI is a severe data breach. The architecture document must clearly state:</p>
<ul>
<li><strong>Option A:</strong> Local LLM execution (Llama 3, Mistral) via Ollama/vLLM. Data never leaves the air-gapped network.</li>
<li><strong>Option B:</strong> If cloud LLMs are used for the hackathon demo, state explicitly that it is a placeholder for a local/VPC-hosted model in production.</li>
</ul>
</section>
'''
