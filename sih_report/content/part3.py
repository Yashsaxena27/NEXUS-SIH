"""
SIH 26155 Master Report — Content Part 3
Sections: 19. Dataset Strategy through 34. References (and Appendices)
"""

import os

def get_html():
    return _dataset_strategy() + _ground_truth() + _tech_stack() + _ui_ux() + _feasibility() + _innovation() + _scalability() + _what_not_to_build() + _implementation_plan() + _demo_strategy() + _presentation() + _qa() + _future() + _references() + _appendices()

# ── 19. Dataset Strategy ───────────────────────────────────────────

def _dataset_strategy():
    return '''
<section class="section" id="dataset-strategy">
<h1>19. Dataset Strategy</h1>

<p>A machine learning tool is only as good as its data. Because real-world enterprise network configurations are highly classified and not publicly available, generating a robust synthetic dataset is critical.</p>

<div class="figure">
<img src="../diagrams/diagram_dataset_flow.png" alt="Dataset Generation Flow" />
<div class="figure-caption">Figure 10: Synthetic Dataset Generation & Evaluation Pipeline</div>
</div>

<h2 id="dataset-layers">19.2 Dataset Layers</h2>
<p>We propose a 4-layer dataset strategy for training and evaluation:</p>
<ol>
<li><strong>Layer 1: Clean Baselines (Gold Standard).</strong> Perfectly compliant configurations derived directly from CIS Benchmarks.</li>
<li><strong>Layer 2: Real-World Messy.</strong> Configurations scraped from public GitHub repositories, sanitized, and anonymized.</li>
<li><strong>Layer 3: Synthetically Perturbed.</strong> Gold standard configs mutated via script (e.g., flipping <code>ssh</code> to <code>telnet</code>, modifying timeouts) to create labeled violations.</li>
<li><strong>Layer 4: Vendor Edge Cases.</strong> Configurations utilizing rare, legacy, or highly specific vendor OS features to test the normalizer's resilience.</li>
</ol>
</section>
'''

# ── 20. Ground Truth & Evaluation ──────────────────────────────────

def _ground_truth():
    return '''
<section class="section" id="ground-truth">
<h1>20. Ground Truth &amp; Evaluation</h1>

<h2 id="eval-metrics">20.2 Evaluation Metrics</h2>
<p>To prove to judges that NEXUS is enterprise-ready, we evaluate it strictly using standard ML metrics against the labeled synthetic dataset:</p>
<ul>
<li><strong>True Positives (TP):</strong> System correctly identifies a non-compliant setting.</li>
<li><strong>False Positives (FP):</strong> System flags a compliant setting as non-compliant (causes alert fatigue).</li>
<li><strong>True Negatives (TN):</strong> System correctly ignores a compliant setting.</li>
<li><strong>False Negatives (FN):</strong> System misses a non-compliant setting (causes security breach).</li>
</ul>

<div class="callout callout-key-insight">
<div class="callout-title">Optimization Goal</div>
<p>In cybersecurity, False Negatives are catastrophic. The system must be tuned for extremely high <strong>Recall</strong>, even at the slight expense of Precision.</p>
</div>
</section>
'''

# ── 21. Technology Stack ───────────────────────────────────────────

def _tech_stack():
    return '''
<section class="section" id="tech-stack">
<h1>21. Technology Stack</h1>

<h2 id="recommended-stack">21.2 Final Recommended Stack</h2>
<table>
<thead><tr><th>Component</th><th>Technology</th><th>Why?</th></tr></thead>
<tbody>
<tr><td><strong>Frontend</strong></td><td>Next.js (React) + Tailwind</td><td>Professional, fast, enterprise look</td></tr>
<tr><td><strong>Backend API</strong></td><td>FastAPI (Python)</td><td>High performance, async, ML-friendly</td></tr>
<tr><td><strong>Parser</strong></td><td>CiscoConfParse2</td><td>Handles nested blocks perfectly</td></tr>
<tr><td><strong>Rule Engine</strong></td><td>Custom YAML + JSONPath</td><td>Decouples code from policy</td></tr>
<tr><td><strong>Vector DB (RAG)</strong></td><td>ChromaDB</td><td>In-memory, local, no cloud dependency</td></tr>
<tr><td><strong>LLM Integration</strong></td><td>LangChain + Ollama/Gemini</td><td>Flexible abstraction over models</td></tr>
<tr><td><strong>Database</strong></td><td>SQLite (Hackathon) / Postgres</td><td>Simple setup for 36 hours</td></tr>
</tbody>
</table>
</section>
'''

# ── 22. UI/UX Concept ──────────────────────────────────────────────

def _ui_ux():
    return '''
<section class="section" id="ui-ux">
<h1>22. UI/UX Concept</h1>

<div class="figure">
<img src="../diagrams/diagram_end_to_end.png" alt="End-to-End Workflow" />
<div class="figure-caption">Figure 11: End-to-End User Experience Workflow</div>
</div>

<h2 id="dashboard-pages">22.2 Dashboard Pages</h2>
<ol>
<li><strong>Command Center (Overview):</strong> Total devices, overall risk score, top failing controls.</li>
<li><strong>Device Detail View:</strong> Side-by-side view (Raw Config | Normalized JSON | Rule Results).</li>
<li><strong>Violation Inspector:</strong> AI explanation box, citation links, and Diff viewer for remediation.</li>
<li><strong>Semantic Mapping Center (Adaptive Learning):</strong> Queue of unknown commands waiting for human semantic mapping.</li>
</ol>
</section>
'''

# ── 23. Feasibility & Technical Challenges ─────────────────────────

def _feasibility():
    return '''
<section class="section" id="feasibility">
<h1>23. Feasibility &amp; Technical Challenges</h1>

<h2 id="failure-modes">23.2 Failure Modes &amp; Risk Matrix</h2>
<table>
<thead><tr><th>Risk</th><th>Impact</th><th>Mitigation Strategy</th></tr></thead>
<tbody>
<tr><td>LLM Hallucinates Rule Result</td><td><span class="badge badge-critical">HIGH</span></td><td>Never use LLM for evaluation. Use deterministic YAML engine.</td></tr>
<tr><td>Parsing Fails on New Vendor</td><td><span class="badge badge-high">HIGH</span></td><td>Graceful fallback to "Unknown Command" and route to Adaptive Learning.</td></tr>
<tr><td>API Rate Limits</td><td><span class="badge badge-medium">MEDIUM</span></td><td>Cache explanations. Mock LLM responses if internet fails at SIH.</td></tr>
<tr><td>Time Runs Out (36 hours)</td><td><span class="badge badge-high">HIGH</span></td><td>Hardcode complex logic for the demo; focus on UI and core pipeline.</td></tr>
</tbody>
</table>
</section>
'''

# ── 24. Innovation & Novelty ───────────────────────────────────────

def _innovation():
    return '''
<section class="section" id="innovation">
<h1>24. Innovation &amp; Novelty</h1>

<h2 id="differentiators">24.1 Key Differentiators</h2>
<p>If judges ask, "How is this different from a Python regex script?", the answers are:</p>
<ol>
<li><strong>Semantic Normalization:</strong> We evaluate intent, not syntax.</li>
<li><strong>Explainability:</strong> We don't just say "Failed." We cite the NIST paragraph proving why.</li>
<li><strong>Adaptability:</strong> Regex is static. Our system learns new commands interactively.</li>
</ol>
</section>
'''

# ── 25. Scalability ────────────────────────────────────────────────

def _scalability():
    return '''
<section class="section" id="scalability">
<h1>25. Scalability &amp; Deployment</h1>

<h2 id="air-gapped">25.2 Air-Gapped Deployment</h2>
<p>NTRO requires solutions that work in classified, disconnected environments. NEXUS is designed to be fully containerized (Docker) with a local LLM (Ollama) and local Vector DB, requiring exactly <strong>zero bytes</strong> of outbound internet traffic.</p>
</section>
'''

# ── 26. What NOT to Build ──────────────────────────────────────────

def _what_not_to_build():
    return '''
<section class="section" id="what-not-to-build">
<h1>26. What NOT to Build</h1>

<div class="callout callout-warning">
<div class="callout-title">Hackathon Scope Cuts</div>
<p>Do NOT try to build SSH connection logic to pull configs live from routers. Network mocking is extremely error-prone during a demo. Accept file uploads (<code>.txt</code>, <code>.cfg</code>) via the UI instead. Tell the judges this abstracts transport (SSH/API/TFTP) from the core parsing logic.</p>
</div>
</section>
'''

# ── 27. Implementation Plan ────────────────────────────────────────

def _implementation_plan():
    return '''
<section class="section" id="implementation-plan">
<h1>27. 36-Hour Hackathon Implementation Plan</h1>

<h2 id="team-roles">27.3 Team Role Distribution (6 Members)</h2>
<ul>
<li><strong>Member 1 (UI/UX):</strong> Next.js dashboard, visualizations, diff viewer.</li>
<li><strong>Member 2 (Backend APIs):</strong> FastAPI, file upload, routing, database models.</li>
<li><strong>Member 3 (Core Engine):</strong> CiscoConfParse2 logic, Normalization layer.</li>
<li><strong>Member 4 (Security/Rules):</strong> YAML rule creation, CIS benchmark mapping.</li>
<li><strong>Member 5 (AI/RAG):</strong> LangChain, Vector DB, Prompt engineering.</li>
<li><strong>Member 6 (Pitch/Demo):</strong> Video creation, slide deck, demo flow optimization.</li>
</ul>
</section>
'''

# ── 28. Demo Strategy ──────────────────────────────────────────────

def _demo_strategy():
    return '''
<section class="section" id="demo-strategy">
<h1>28. Demo Strategy</h1>

<h2 id="wow-moments">28.2 Top 5 Wow Moments</h2>
<ol>
<li><strong>The Upload:</strong> Drag in a Cisco file and a Fortinet file. The UI instantly identifies the OS without being told.</li>
<li><strong>The Common Language:</strong> Show the raw CLI, then click "Normalize". The screen transitions to clean, identical JSON for both vendors.</li>
<li><strong>The Citation:</strong> Click a failure. The AI explains it and provides a clickable link/citation to the actual NIST documentation.</li>
<li><strong>The Fix:</strong> Click "Generate Remediation". The system provides the exact, copy-pasteable CLI command.</li>
<li><strong>The Learning Loop:</strong> Upload an "Unknown" vendor config. The system asks for help. The user confirms the meaning. Re-run the audit, and it passes automatically.</li>
</ol>
</section>
'''

# ── 29. Presentation & 30. Q&A ─────────────────────────────────────

def _presentation():
    return '''
<section class="section" id="presentation">
<h1>29. SIH Presentation Strategy</h1>
<p>Keep slides minimal. Focus on the architecture diagram, the core problem (manual audits don't scale), and the adaptive learning differentiator. Spend 70% of the time showing the working software.</p>
</section>
'''

def _qa():
    return '''
<section class="section" id="judge-qa">
<h1>30. Judge Questions &amp; Answers</h1>

<div class="qa-item">
<div class="qa-question">Q: Why not just use Regex?</div>
<div class="qa-answer">Regex fails on hierarchical configurations. If I regex for "transport input ssh", I don't know if that's applied to the console, the VTY line, or a completely isolated test block. Our AST parser understands context.</div>
</div>

<div class="qa-item">
<div class="qa-question">Q: How do you prevent the AI from giving bad security advice?</div>
<div class="qa-answer">We don't use AI for decisions. The YAML rules dictate pass/fail. The AI is strictly constrained via RAG to only explain the violation using official CIS/NIST text.</div>
</div>

<div class="qa-item">
<div class="qa-question">Q: What happens when Cisco changes its syntax in the next update?</div>
<div class="qa-answer">That's what our Adaptive Learning Loop solves. The system flags the unknown syntax, the AI suggests a mapping, the admin confirms it once, and the system remembers it permanently without a code update.</div>
</div>

<div class="qa-item">
<div class="qa-question">Q: How do you handle multi-vendor schemas without OpenConfig?</div>
<div class="qa-answer">OpenConfig is excellent but highly complex to map for legacy commands in a 36-hour hackathon. We designed a lightweight, security-specific JSON schema that captures only the compliance-relevant settings (e.g., mgmt.ssh.enabled) rather than the entire device state.</div>
</div>

<div class="qa-item">
<div class="qa-question">Q: Can this operate in a classified, air-gapped environment like NTRO?</div>
<div class="qa-answer">Yes. We designed the architecture to run fully offline. We use a local LLM (like Llama 3 via Ollama) and a local Vector DB (ChromaDB), ensuring zero bytes of outbound internet traffic.</div>
</div>

<div class="qa-item">
<div class="qa-question">Q: Are the remediation commands applied automatically?</div>
<div class="qa-answer">No. Network engineers do not trust autonomous AI with write access. NEXUS generates a downloadable Ansible playbook or CLI snippet for human review and approval.</div>
</div>
</section>
'''

# ── 31-34: Testing, Future, Verdict, References ────────────────────

def _future():
    return '''
<section class="section" id="future-roadmap">
<h1>32. Future Roadmap</h1>
<ul>
<li>Automated GitOps integration (scan configs in GitHub PRs before deployment).</li>
<li>Support for Cloud-Native configurations (AWS Security Groups, Azure NSGs).</li>
<li>Integration with ServiceNow for automated ticketing of violations.</li>
</ul>
</section>

<section class="section" id="final-verdict">
<h1>33. Final Verdict</h1>
<p>NEXUS represents a highly feasible, highly innovative solution to SIH 26155. By combining deterministic parsing with AI-driven explainability and adaptive learning, it bridges the gap between traditional rigid tools and untrustworthy pure-LLM approaches.</p>
</section>
'''

def _references():
    return '''
<section class="section" id="references">
<h1>34. References</h1>
<ul class="reference-list">
<li>National Institute of Standards and Technology (NIST). (2020). Security and Privacy Controls for Information Systems and Organizations. SP 800-53 Rev. 5.</li>
<li>Center for Internet Security (CIS). (2023). CIS Cisco IOS 15 Benchmark v4.1.0.</li>
<li>Defense Information Systems Agency (DISA). (2023). Network Infrastructure Policy STIG.</li>
<li>Cisco Systems. (2022). Cisco IOS Security Configuration Guide.</li>
<li>Palo Alto Networks. (2023). PAN-OS Administrator's Guide: Security Best Practices.</li>
<li>Pennington, D. (2023). CiscoConfParse2 Documentation. GitHub.</li>
<li>Gao, Y., et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv preprint arXiv:2312.10997.</li>
</ul>
</section>
'''

def _appendices():
    return '''
<section class="section page-break" id="appendix-a">
<h1>Appendix A: Configuration Examples</h1>
<p><em>Refer to Section 6 for detailed configuration snippets across all supported vendors.</em></p>
</section>

<section class="section page-break" id="appendix-b">
<h1>Appendix B: Compliance Rule YAML</h1>
<p><em>Refer to Section 11.2 for the complete YAML schema definition.</em></p>
</section>
'''
