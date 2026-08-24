"""
SIH 26155 Master Report — Content Part 1
Sections: Executive Summary through Vendor Configurations & Proposed Solution
Merged from ChatGPT and Perplexity research documents.
"""


def get_html():
    return _exec_summary() + _official_problem() + _why_matters() + _current_situation() + _competitors() + _compliance_standards() + _vendor_configs() + _proposed_solution()


# ── Executive Summary ──────────────────────────────────────────────

def _exec_summary():
    return '''
<section class="section" id="exec-summary">
<h1>Executive Summary</h1>

<p>Problem Statement 26155 — <strong>"AI-Driven Multi-Vendor Network Security Compliance Auditor"</strong> — is a cybersecurity challenge from the <strong>National Technical Research Organisation (NTRO)</strong> under the Blockchain &amp; Cybersecurity theme of Smart India Hackathon (SIH) 2026. The core ask: build a system that automatically audits network device configurations (Cisco, Juniper, Fortinet, Palo Alto, etc.) against security standards (CIS, NIST, DISA STIG), explains violations with evidence, and generates vendor-specific remediation — all without manual rule-by-rule checking.</p>

<div class="callout callout-key-insight">
<div class="callout-title">The Project in One Sentence</div>
<p>Build an AI-assisted security engine that can understand network configurations from different vendors, convert them into a common security representation, check them against cybersecurity standards, explain violations, learn how to interpret previously unseen configuration syntax, and generate safe remediation guidance.</p>
</div>

<p>The important words are: <strong>Multi-vendor + AI interpretation + normalization + compliance + adaptive learning + explainability + remediation.</strong></p>

<p>This is <strong>not</strong> simply a network scanner. It is <strong>not</strong> simply a vulnerability scanner. It is <strong>not</strong> simply a dashboard. It is <strong>not</strong> simply an LLM chatbot.</p>

<p>The central technical problem is:</p>

<blockquote>Different network vendors express essentially the same security settings in completely different configuration languages. How can one compliance engine understand all of them without requiring a separate hard-coded parser for every vendor and every OS version?</blockquote>

<p>The SIH problem statement explicitly identifies this syntactic diversity and asks for an AI-augmented vendor-agnostic compliance engine with normalization, deviation analysis, and an interactive training/adaptation loop.</p>

<p>This report provides everything your team needs to <strong>understand the problem deeply</strong>, <strong>design a technically defensible solution</strong>, and <strong>maximize your chances of winning SIH 2026</strong>.</p>

<h2>Report Scope</h2>
<p>This document consolidates research from multiple deep investigations into a single master reference covering:</p>
<ul>
<li>Complete problem analysis and stakeholder expectations</li>
<li>All relevant compliance frameworks (CIS, NIST, DISA STIG, ISO 27001)</li>
<li>Multi-vendor configuration syntax across Cisco, Juniper, Fortinet, Palo Alto, and Arista</li>
<li>Proposed NEXUS solution architecture with conceptual diagrams</li>
<li>AI/ML strategy — where AI helps and where deterministic rules are better</li>
<li>RAG system design for explainable compliance</li>
<li>Adaptive learning loop — the signature differentiator</li>
<li>Dataset strategy and evaluation methodology</li>
<li>36-hour hackathon execution plan with team roles</li>
<li>50+ anticipated judge questions with prepared answers</li>
<li>Complete reference list from authoritative sources</li>
</ul>
</section>
'''


# ── 1. Official Problem Statement ──────────────────────────────────

def _official_problem():
    return '''
<section class="section" id="official-problem">
<h1>1. Official Problem Statement (SIH26-26155)</h1>

<dl class="kv-grid">
<dt>Title</dt><dd>AI-Driven Multi-Vendor Network Security Compliance Auditor</dd>
<dt>Organization</dt><dd>National Technical Research Organisation (NTRO)</dd>
<dt>Theme</dt><dd>Blockchain &amp; Cybersecurity</dd>
<dt>Edition</dt><dd>Software</dd>
<dt>Problem ID</dt><dd>SIH26-26155</dd>
</dl>

<h2>Problem Description (from Official Source)</h2>
<blockquote>
Organizations managing multi-vendor network infrastructure (Cisco, Juniper, Fortinet, Palo Alto, etc.) face significant challenges in ensuring security compliance across devices. Manual configuration audits are time-consuming, error-prone, and cannot scale. There is a need for an AI-driven system that can automatically parse network configurations from different vendors, normalize them into a common security model, check against compliance standards (CIS Benchmarks, NIST, DISA STIGs), explain violations with evidence, and generate vendor-specific remediation steps.
</blockquote>

<h2>Existing Situation (as Stated)</h2>
<ul>
<li>Network security teams manually review configurations using spreadsheets and checklists</li>
<li>Each vendor has different CLI syntax and security controls</li>
<li>Compliance audits take days/weeks and are point-in-time only</li>
<li>Configuration drift between audits creates security gaps</li>
<li>Limited automation for multi-vendor environments</li>
</ul>

<h2>Expected Deliverables</h2>
<table>
<thead><tr><th>Deliverable</th><th>Specification</th></tr></thead>
<tbody>
<tr><td>Source Code</td><td>GitHub/Drive Link</td></tr>
<tr><td>README</td><td>Setup Instructions</td></tr>
<tr><td>Architecture Document</td><td>Max 2 Pages</td></tr>
<tr><td>Demo Video</td><td>Max 2 Minutes</td></tr>
<tr><td>Technical Presentation</td><td>Max 5 Slides</td></tr>
</tbody>
</table>

<h2>Target Users</h2>
<ul>
<li>Network security teams in government organizations</li>
<li>IT auditors and compliance officers</li>
<li>SOC analysts managing network infrastructure</li>
<li>Managed Security Service Providers (MSSPs)</li>
</ul>

<h2>Constraints</h2>
<ul>
<li>Must support multiple vendors (Cisco, Juniper, Fortinet, Palo Alto minimum)</li>
<li>Must map to recognized standards (CIS, NIST, DISA STIG)</li>
<li>Must provide explainable AI (not black-box decisions)</li>
<li>Must generate vendor-specific remediation</li>
<li>Should work offline/air-gapped (government deployment scenario)</li>
</ul>

<h2>Evaluation Criteria (Inferred from SIH Patterns)</h2>
<table>
<thead><tr><th>Criterion</th><th>Estimated Weight</th><th>How to Maximize</th></tr></thead>
<tbody>
<tr><td>Technical depth and architecture</td><td>20%</td><td>Parsing, normalization, compliance engine, RAG</td></tr>
<tr><td>Innovation (AI + deterministic compliance)</td><td>20%</td><td>Adaptive learning loop + vendor-neutral schema</td></tr>
<tr><td>Feasibility of 36-hour prototype</td><td>15%</td><td>Working demo with 4 vendors, 20 rules</td></tr>
<tr><td>Demo quality and wow factor</td><td>10%</td><td>Auto-detect vendor, AI citation, topology</td></tr>
<tr><td>Real-world applicability</td><td>15%</td><td>Government networks, NTRO use case</td></tr>
<tr><td>Security of the solution itself</td><td>10%</td><td>Secret redaction, sandboxed parsing</td></tr>
<tr><td>Multi-vendor normalization capability</td><td>10%</td><td>4 vendors → 1 common schema</td></tr>
</tbody>
</table>

<h2 id="problem-simple">1.1 In Simple Language</h2>

<div class="callout callout-simple">
<div class="callout-title">Simple Explanation</div>
<p>Your college team needs to build a "smart auditor" that:</p>
<ol>
<li>Takes network device configurations (like router/firewall settings)</li>
<li>Automatically checks if they follow security best practices</li>
<li>Tells you WHAT is wrong, WHY it's wrong, and HOW to fix it</li>
<li>Works for Cisco, Juniper, Fortinet, and Palo Alto devices</li>
<li>Explains everything in plain English (not just "FAIL")</li>
</ol>
</div>

<p>Think of it like a spell-checker for network security. Just as a spell-checker reads your document and highlights errors with explanations and fix suggestions, NEXUS reads network device configurations and highlights security problems with explanations and fix commands.</p>

<p>The key challenge: <strong>different network vendors use completely different "languages"</strong> (command syntax) to express the same security settings. Imagine if every word processor used a different language for the same document — you'd need a universal translator before you could check spelling.</p>

<h2 id="problem-technical">1.2 Technical Explanation</h2>

<div class="callout callout-technical">
<div class="callout-title">Technical Explanation</div>
<p>Build a multi-vendor configuration compliance engine that:</p>
<ol>
<li>Parses vendor-specific CLI configurations into structured data</li>
<li>Normalizes configurations into a vendor-agnostic security model</li>
<li>Applies deterministic compliance rules mapped to CIS/NIST/STIG controls</li>
<li>Uses RAG (Retrieval-Augmented Generation) to explain violations with citations</li>
<li>Generates vendor-specific remediation commands</li>
<li>Produces risk scores and audit reports</li>
<li>Provides an adaptive learning loop where administrators can teach the system to interpret previously unseen configuration syntax</li>
</ol>
</div>

<h2 id="what-ntro-wants">1.3 What NTRO Actually Wants</h2>
<p>Government and defense networks typically require solutions that work in classified, disconnected environments. They need:</p>

<table>
<thead><tr><th>They WANT</th><th>They DO NOT Want</th></tr></thead>
<tbody>
<tr><td>Automated compliance instead of manual checklists</td><td>A generic vulnerability scanner</td></tr>
<tr><td>Evidence-based audits for regulatory requirements</td><td>A chatbot that gives cybersecurity advice</td></tr>
<tr><td>Continuous monitoring instead of point-in-time checks</td><td>A tool that only works for one vendor</td></tr>
<tr><td>Explainable AI that auditors can trust</td><td>A black-box AI that can't explain its decisions</td></tr>
<tr><td>Air-gapped deployment capability (no cloud dependencies)</td><td>A cloud-only SaaS solution</td></tr>
</tbody>
</table>
</section>
'''


# ── 2. Why This Problem Matters ────────────────────────────────────

def _why_matters():
    return '''
<section class="section" id="why-matters">
<h1>2. Why This Problem Matters</h1>

<h2 id="real-world-impact">2.1 Real-World Impact</h2>

<p>Modern organizations use equipment from many vendors across their networks:</p>

<h3>Firewalls / SASE</h3>
<p>Palo Alto, Fortinet, Cisco, Check Point, Juniper, Sophos, SonicWall, WatchGuard, Barracuda, Zscaler, cloud-native firewalls, and many others.</p>

<h3>Routers / Switches</h3>
<p>Cisco, Aruba, Juniper, Arista, Extreme, Huawei, MikroTik, Ubiquiti, NVIDIA, etc.</p>

<p>The problem statement explicitly says the list is illustrative and the intended architecture should ideally support configurations regardless of vendor or market segment.</p>

<h3>The Core Challenge Visualized</h3>
<p>Suppose an organization's security policy says: <em>"Administrative access must use secure protocols."</em></p>
<p>A Cisco configuration, Juniper configuration, and Fortinet configuration will express the relevant settings in completely different syntax. Conceptually:</p>

<pre><code>SECURITY REQUIREMENT: "Secure administrative access"
            ↓
       Common concept
            ↓
 ┌──────────┼───────────┐
 ↓          ↓           ↓
Cisco     Juniper     Fortinet
syntax    syntax      syntax</code></pre>

<p>A traditional compliance engine generally needs vendor-specific knowledge — separate parsers, rules, and mappings for each vendor. As vendors and firmware versions increase, maintaining this becomes expensive and fragile.</p>

<div class="callout callout-key-insight">
<div class="callout-title">Business Value</div>
<p>The system can reduce: <strong>manual audit effort</strong> (instead of checking configurations individually), <strong>vendor-specific dependency</strong> (common security model), <strong>compliance drift</strong> (continuous scanning), <strong>audit preparation</strong> (automatic evidence/report generation), and <strong>human error</strong> (structured deterministic checks).</p>
</div>

<h3>Security Value</h3>
<p>Misconfiguration can create serious exposure. MITRE's Network Devices ATT&amp;CK matrix covers techniques targeting routers, switches, and load balancers. MITRE specifically documents how configuration repositories can expose sensitive network information. Configuration security isn't an artificial hackathon problem — it is a real security concern.</p>

<h2 id="real-world-examples">2.2 Real-World Compliance Examples</h2>

<h3>Example 1: Telnet vs SSH</h3>
<table>
<thead><tr><th>Attribute</th><th>Details</th></tr></thead>
<tbody>
<tr><td>CIS Control</td><td>Disable insecure management protocols</td></tr>
<tr><td>Manual Check</td><td>Search config for "telnet"</td></tr>
<tr><td>Problem</td><td>Telnet transmits credentials in plaintext</td></tr>
<tr><td>Risk</td><td>Attacker on network can capture admin passwords</td></tr>
</tbody>
</table>

<h3>Example 2: SNMP Community Strings</h3>
<table>
<thead><tr><th>Attribute</th><th>Details</th></tr></thead>
<tbody>
<tr><td>CIS Control</td><td>Change default SNMP community strings</td></tr>
<tr><td>Manual Check</td><td>Look for <code>snmp-server community public</code></td></tr>
<tr><td>Problem</td><td>"public" is well-known and allows network reconnaissance</td></tr>
<tr><td>Risk</td><td>Attacker can map entire network topology</td></tr>
</tbody>
</table>

<h3>Example 3: Session Timeout</h3>
<table>
<thead><tr><th>Attribute</th><th>Details</th></tr></thead>
<tbody>
<tr><td>DISA STIG</td><td>Management sessions must timeout after 10 minutes</td></tr>
<tr><td>Manual Check</td><td>Find <code>exec-timeout</code> or <code>idle-timeout</code> settings</td></tr>
<tr><td>Problem</td><td>Unattended sessions allow unauthorized access</td></tr>
<tr><td>Risk</td><td>Walk-up attack on console or SSH session</td></tr>
</tbody>
</table>

<h3>Example 4: Logging Configuration</h3>
<table>
<thead><tr><th>Attribute</th><th>Details</th></tr></thead>
<tbody>
<tr><td>NIST 800-53</td><td>Audit logs must be sent to centralized server</td></tr>
<tr><td>Manual Check</td><td>Verify <code>logging host</code> or syslog configuration</td></tr>
<tr><td>Problem</td><td>Local logs can be deleted by attacker</td></tr>
<tr><td>Risk</td><td>No forensic evidence after breach</td></tr>
</tbody>
</table>
</section>
'''


# ── 3. Current Industry Situation ──────────────────────────────────

def _current_situation():
    return '''
<section class="section" id="current-situation">
<h1>3. Current Industry Situation</h1>

<h2 id="manual-process">3.1 Manual Audit Process (Current State)</h2>

<h3>Step 1: Configuration Collection</h3>
<ul>
<li>Engineers SSH into each device</li>
<li>Run <code>show running-config</code> (Cisco) or <code>show configuration</code> (Juniper)</li>
<li>Save configs to files or copy-paste into spreadsheets</li>
</ul>

<h3>Step 2: Security Review</h3>
<ul>
<li>Open CIS Benchmark PDF (100+ pages)</li>
<li>Manually check each control against config</li>
<li>Example: "Is Telnet disabled?" → Search config for <code>transport input telnet</code></li>
<li>Mark Pass/Fail in Excel</li>
</ul>

<h3>Step 3: Documentation</h3>
<ul>
<li>Screenshot configurations as evidence</li>
<li>Write explanations for each finding</li>
<li>Create PowerPoint reports for management</li>
</ul>

<h3>Step 4: Remediation</h3>
<ul>
<li>Manually write fix commands</li>
<li>Test in lab before production</li>
<li>Schedule maintenance window</li>
<li>Apply changes device-by-device</li>
</ul>

<h2 id="challenges-table">3.2 Why Manual Audits Fail</h2>

<table>
<thead><tr><th>Challenge</th><th>Impact</th><th>Evidence</th></tr></thead>
<tbody>
<tr><td><strong>Time-consuming</strong></td><td>A single firewall audit takes 4–8 hours manually</td><td>Industry reports</td></tr>
<tr><td><strong>Error-prone</strong></td><td>Human reviewers miss 15–30% of violations</td><td>Government audit studies</td></tr>
<tr><td><strong>Point-in-time</strong></td><td>Compliance degrades immediately after audit</td><td>Security best practices</td></tr>
<tr><td><strong>Vendor-specific</strong></td><td>Each vendor requires different expertise</td><td>Multi-vendor environments</td></tr>
<tr><td><strong>No evidence trail</strong></td><td>Hard to prove compliance to auditors</td><td>Regulatory requirements</td></tr>
<tr><td><strong>Configuration drift</strong></td><td>Changes between audits create security gaps</td><td>Continuous monitoring gap</td></tr>
</tbody>
</table>

<div class="callout callout-warning">
<div class="callout-title">The Drift Problem</div>
<p><strong>Day 1:</strong> Audit shows 100% compliance. <strong>Day 2:</strong> Engineer enables Telnet for troubleshooting. <strong>Day 30:</strong> Next audit — Telnet still enabled (violation!). Between audits, the organization is unknowingly non-compliant and exposed.</p>
</div>
</section>
'''


# ── 4. Existing Solutions & Competitor Analysis ────────────────────

def _competitors():
    return '''
<section class="section" id="existing-solutions">
<h1>4. Existing Solutions &amp; Competitor Analysis</h1>

<h2 id="competitor-products">4.1 Existing Products</h2>

<table>
<thead><tr><th>Product</th><th>What It Does</th><th>Strengths</th><th>Weaknesses</th><th>Gap NEXUS Fills</th></tr></thead>
<tbody>
<tr><td><strong>Tenable</strong></td><td>Vulnerability management</td><td>Broad coverage, cloud</td><td>Not config-focused, no multi-vendor normalization</td><td>We focus on configuration compliance</td></tr>
<tr><td><strong>Qualys</strong></td><td>Vulnerability + compliance</td><td>Integrated platform</td><td>Cloud-only, expensive</td><td>We work offline, free for SIH</td></tr>
<tr><td><strong>Cisco Defense Orchestrator</strong></td><td>Cisco config management</td><td>Deep Cisco integration</td><td>Cisco-only</td><td>We support multi-vendor</td></tr>
<tr><td><strong>SolarWinds NCM</strong></td><td>Network config management</td><td>Config backup, compliance</td><td>Limited AI, no RAG</td><td>We have AI explanations</td></tr>
<tr><td><strong>ManageEngine NCM</strong></td><td>Config management</td><td>Affordable</td><td>Basic compliance checks</td><td>We have AI + RAG</td></tr>
<tr><td><strong>Tufin</strong></td><td>Firewall management</td><td>Multi-vendor firewall</td><td>Firewall-only</td><td>We cover routers, switches, firewalls</td></tr>
<tr><td><strong>AlgoSec</strong></td><td>Firewall analytics</td><td>Policy analysis</td><td>Complex, expensive</td><td>We are simpler, AI-powered</td></tr>
<tr><td><strong>FireMon</strong></td><td>Firewall management</td><td>Policy optimization</td><td>Firewall-only</td><td>We are broader</td></tr>
<tr><td><strong>RedSeal</strong></td><td>Network security + STIG</td><td>STIG compliance, risk scoring</td><td>Expensive, enterprise</td><td>We are free, AI-powered</td></tr>
<tr><td><strong>Tripwire</strong></td><td>Config compliance</td><td>File integrity, compliance</td><td>Legacy, no AI</td><td>We have modern AI</td></tr>
<tr><td><strong>OpenSCAP</strong></td><td>SCAP compliance</td><td>Free, open-source</td><td>Linux-focused, not network</td><td>We focus on network devices</td></tr>
<tr><td><strong>Chef InSpec</strong></td><td>Compliance as code</td><td>DevOps integration</td><td>Requires coding</td><td>We are no-code rules</td></tr>
<tr><td><strong>Batfish</strong></td><td>Network config analysis</td><td>Powerful, open-source</td><td>Complex, no AI</td><td>We add AI + RAG</td></tr>
</tbody>
</table>

<h2 id="competitor-matrix">4.2 Feature Comparison Matrix</h2>

<table class="feature-matrix">
<thead><tr><th>Feature</th><th>Tenable</th><th>Qualys</th><th>RedSeal</th><th>Batfish</th><th>NEXUS (Ours)</th></tr></thead>
<tbody>
<tr><td>Multi-vendor config</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td></tr>
<tr><td>CIS Benchmark</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td></tr>
<tr><td>NIST 800-53</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td><td class="partial">⚠️</td><td class="yes">✅</td></tr>
<tr><td>DISA STIG</td><td class="partial">⚠️</td><td class="partial">⚠️</td><td class="yes">✅</td><td class="partial">⚠️</td><td class="yes">✅</td></tr>
<tr><td>AI explanation</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td></tr>
<tr><td>RAG citations</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td></tr>
<tr><td>Vendor-specific remediation</td><td class="partial">⚠️</td><td class="partial">⚠️</td><td class="yes">✅</td><td class="no">❌</td><td class="yes">✅</td></tr>
<tr><td>Network topology</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td><td class="partial">⚠️</td><td class="yes">✅</td></tr>
<tr><td>"Ask your network" chatbot</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td></tr>
<tr><td>Adaptive learning</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td></tr>
<tr><td>Offline/air-gapped</td><td class="partial">⚠️</td><td class="no">❌</td><td class="yes">✅</td><td class="yes">✅</td><td class="yes">✅</td></tr>
<tr><td>Free/open-source</td><td class="no">❌</td><td class="no">❌</td><td class="no">❌</td><td class="yes">✅</td><td class="yes">✅</td></tr>
</tbody>
</table>

<h2 id="gaps">4.3 Gaps in Existing Solutions</h2>

<div class="callout callout-key-insight">
<div class="callout-title">Our Differentiation</div>
<ul>
<li><strong>AI + RAG</strong> — Explainable, cited compliance explanations (most traditional tools lack this specific integration)</li>
<li><strong>Multi-vendor normalization</strong> — Unified rules across vendors via common schema</li>
<li><strong>Adaptive learning</strong> — System learns new vendor syntax from human feedback</li>
<li><strong>Chatbot interface</strong> — Natural language compliance queries</li>
<li><strong>Free for SIH</strong> — No cost barrier for evaluation</li>
</ul>
</div>
</section>
'''


# ── 5. Compliance Standards Deep-Dive ──────────────────────────────

def _compliance_standards():
    return '''
<section class="section" id="compliance-standards">
<h1>5. Compliance Standards Deep-Dive</h1>

<h2 id="cis-benchmarks">5.1 CIS Benchmarks</h2>

<h3>What It Is</h3>
<p>Center for Internet Security (CIS) Benchmarks are vendor-specific security configuration guides with Level 1 (basic) and Level 2 (hardened) controls. CIS provides concrete secure configuration recommendations and has network-device benchmarks covering vendors including Cisco, Fortinet, Juniper, and Palo Alto Networks.</p>

<h3>Why It Matters</h3>
<ul>
<li>Industry-accepted baseline for network hardening</li>
<li>Automated checks available for most controls</li>
<li>Mapped to NIST, ISO, and regulatory requirements</li>
<li>Ideal for prototype because you can translate concrete recommendations into machine-checkable controls</li>
</ul>

<h3>Relevant Controls (Network Devices)</h3>
<table>
<thead><tr><th>Control ID</th><th>Description</th><th>Automated Check</th><th>Example Violation</th></tr></thead>
<tbody>
<tr><td>1.1</td><td>Disable Telnet</td><td><span class="badge badge-pass">YES</span></td><td><code>transport input telnet</code></td></tr>
<tr><td>1.2</td><td>Enable SSH v2</td><td><span class="badge badge-pass">YES</span></td><td><code>ip ssh version 1</code></td></tr>
<tr><td>1.3</td><td>Set session timeout</td><td><span class="badge badge-pass">YES</span></td><td>No <code>exec-timeout</code> configured</td></tr>
<tr><td>1.4</td><td>Configure login banner</td><td><span class="badge badge-pass">YES</span></td><td>Missing <code>banner login</code></td></tr>
<tr><td>2.1</td><td>Change SNMP community</td><td><span class="badge badge-pass">YES</span></td><td><code>snmp-server community public</code></td></tr>
<tr><td>3.1</td><td>Enable logging to syslog</td><td><span class="badge badge-pass">YES</span></td><td>No <code>logging host</code></td></tr>
<tr><td>3.2</td><td>Set NTP servers</td><td><span class="badge badge-pass">YES</span></td><td>No <code>ntp server</code></td></tr>
<tr><td>4.1</td><td>Disable unused services</td><td><span class="badge badge-pass">YES</span></td><td><code>ip http server</code> enabled</td></tr>
<tr><td>5.1</td><td>Configure AAA</td><td><span class="badge badge-medium">PARTIAL</span></td><td>No <code>aaa authentication</code></td></tr>
</tbody>
</table>

<h3>Machine-Checkable Translation Example</h3>
<pre><code>control_id: CIS-1.1
title: Disable Telnet for Remote Management
check:
  cisco: "NOT transport input telnet"
  juniper: "NOT set system services telnet"
  fortinet: "NOT config system global -> set admin-sport 23"
severity: CRITICAL
remediation: "Disable Telnet and enable SSH only"</code></pre>

<h2 id="nist-800-53">5.2 NIST SP 800-53</h2>

<h3>What It Is</h3>
<p>NIST Special Publication 800-53 provides security and privacy controls for federal information systems (1,000+ controls across 20 families). Required for US federal systems and adopted by many Indian government agencies.</p>

<h3>Why It Matters</h3>
<ul>
<li>Focuses on outcomes rather than specific configurations</li>
<li>Mapped to risk management framework (RMF)</li>
<li>NIST provides machine-readable SP 800-53 controls and related assessment resources</li>
</ul>

<div class="callout callout-info">
<div class="callout-title">Key Insight</div>
<p>NIST 800-53 contains many procedural controls (training, policies) that cannot be automated. Only ~50 technical controls can be checked via configuration analysis. Focus on those for the prototype.</p>
</div>

<h3>Relevant Controls (Network Infrastructure)</h3>
<table>
<thead><tr><th>Control</th><th>Family</th><th>Description</th><th>Automated Check</th></tr></thead>
<tbody>
<tr><td>AC-2</td><td>Access Control</td><td>Account Management</td><td><span class="badge badge-medium">PARTIAL</span> (AAA config)</td></tr>
<tr><td>AC-17</td><td>Access Control</td><td>Remote Access</td><td><span class="badge badge-pass">YES</span> (SSH/Telnet)</td></tr>
<tr><td>AU-2</td><td>Audit</td><td>Auditable Events</td><td><span class="badge badge-pass">YES</span> (logging config)</td></tr>
<tr><td>AU-4</td><td>Audit</td><td>Audit Storage Capacity</td><td><span class="badge badge-medium">PARTIAL</span> (buffer size)</td></tr>
<tr><td>CM-6</td><td>Configuration Mgmt</td><td>Configuration Settings</td><td><span class="badge badge-pass">YES</span> (hardening)</td></tr>
<tr><td>IA-2</td><td>Identification</td><td>User Authentication</td><td><span class="badge badge-pass">YES</span> (AAA)</td></tr>
<tr><td>SC-8</td><td>System Comm.</td><td>Transmission Confidentiality</td><td><span class="badge badge-pass">YES</span> (SSH/TLS)</td></tr>
<tr><td>SI-4</td><td>System Info.</td><td>Information Monitoring</td><td><span class="badge badge-pass">YES</span> (syslog/SNMP)</td></tr>
</tbody>
</table>

<h3>NIST's Secret Weapon: OSCAL</h3>
<p>NIST's <strong>Open Security Controls Assessment Language (OSCAL)</strong> provides machine-readable representations of security controls, implementations, and assessments in formats such as XML, JSON, and YAML. NIST currently provides SP 800-53 control catalogs in machine-readable formats.</p>
<p>This means we can design our compliance engine around a structured control model rather than storing everything as random text — giving the architecture much more credibility.</p>

<h2 id="nist-csf">5.3 NIST Cybersecurity Framework (CSF)</h2>

<h3>What It Is</h3>
<p>A risk-based framework with 5 functions: <strong>Identify, Protect, Detect, Respond, Recover</strong>.</p>

<h3>Relevance to This Problem</h3>
<table>
<thead><tr><th>Function</th><th>Relevance</th><th>Configuration Check</th></tr></thead>
<tbody>
<tr><td><strong>Protect (PR)</strong></td><td>Configuration hardening</td><td>CIS Benchmarks</td></tr>
<tr><td><strong>Detect (DE)</strong></td><td>Logging and monitoring</td><td>Syslog, SNMP</td></tr>
<tr><td><strong>Identify (ID)</strong></td><td>Asset inventory</td><td>Device configs</td></tr>
</tbody>
</table>

<h2 id="disa-stigs">5.4 DISA STIGs</h2>

<h3>What It Is</h3>
<p>Defense Information Systems Agency Security Technical Implementation Guides — mandatory security configurations for US DoD systems. The most detailed and prescriptive security standard.</p>

<h3>Severity Classification</h3>
<table>
<thead><tr><th>Category</th><th>Severity</th><th>Description</th></tr></thead>
<tbody>
<tr><td><span class="badge badge-critical">CAT I</span></td><td>Critical</td><td>Directly exploitable vulnerabilities</td></tr>
<tr><td><span class="badge badge-high">CAT II</span></td><td>High</td><td>Security configuration weaknesses</td></tr>
<tr><td><span class="badge badge-medium">CAT III</span></td><td>Medium</td><td>Best practice deviations</td></tr>
</tbody>
</table>

<h3>Relevant STIGs</h3>
<table>
<thead><tr><th>STIG</th><th>Device Type</th><th>Controls</th></tr></thead>
<tbody>
<tr><td>Network Infrastructure Router L3 Switch</td><td>Cisco/Juniper Routers</td><td>100+ checks</td></tr>
<tr><td>Network L2 Switch</td><td>Switches</td><td>80+ checks</td></tr>
<tr><td>Firewall Security Requirements Guide</td><td>Firewalls</td><td>35+ checks</td></tr>
<tr><td>WLAN Access Points</td><td>Wireless</td><td>50+ checks</td></tr>
</tbody>
</table>

<h3>Example STIG Check</h3>
<pre><code>Finding ID: NET0020 (CAT II)
Title: Administrative Access Authentication
Check: Review network device configuration to determine
       if administrative access requires authentication.
Violation: No password or AAA configured for console/VTY lines
Risk: Unauthorized device access</code></pre>

<h2 id="iso-27001">5.5 ISO/IEC 27001</h2>

<h3>What It Is</h3>
<p>International standard for Information Security Management Systems (ISMS). Globally recognized certification with Annex A containing 114 security controls.</p>

<h3>Relevant Annex A Controls</h3>
<table>
<thead><tr><th>Control</th><th>Description</th><th>Network Config Relevance</th></tr></thead>
<tbody>
<tr><td>A.9.1.2</td><td>Access to Networks</td><td>Network access control (ACLs, 802.1X)</td></tr>
<tr><td>A.9.4.1</td><td>Information Access Restriction</td><td>AAA, privilege levels</td></tr>
<tr><td>A.12.4.1</td><td>Event Logging</td><td>Syslog configuration</td></tr>
<tr><td>A.13.1.1</td><td>Network Controls</td><td>Firewall rules, segmentation</td></tr>
<tr><td>A.13.1.3</td><td>Segregation in Networks</td><td>VLANs, VRFs</td></tr>
</tbody>
</table>

<h2 id="rfcs">5.6 Relevant RFCs</h2>

<table>
<thead><tr><th>RFC</th><th>Topic</th><th>Relevance</th></tr></thead>
<tbody>
<tr><td>RFC 4251–4256</td><td>SSH Protocol</td><td>Secure remote access</td></tr>
<tr><td>RFC 3411–3418</td><td>SNMP v3</td><td>Secure network management</td></tr>
<tr><td>RFC 5905</td><td>NTP v4</td><td>Time synchronization</td></tr>
<tr><td>RFC 5424</td><td>Syslog Protocol</td><td>Centralized logging</td></tr>
<tr><td>RFC 2475</td><td>DiffServ</td><td>QoS configuration</td></tr>
</tbody>
</table>

<h2 id="vendor-guides">5.7 Vendor Security Hardening Guides</h2>

<table>
<thead><tr><th>Vendor</th><th>Document</th><th>Key Topics</th></tr></thead>
<tbody>
<tr><td>Cisco</td><td>IOS Security Configuration Guide</td><td>AAA, SSH, ACLs, logging</td></tr>
<tr><td>Juniper</td><td>Security Configuration Guide</td><td>Services, authentication, logging</td></tr>
<tr><td>Fortinet</td><td>FortiOS Hardening Guide</td><td>Admin access, policies, logging</td></tr>
<tr><td>Palo Alto</td><td>PAN-OS Hardening Guide</td><td>Management, policies, reporting</td></tr>
</tbody>
</table>

<h2 id="compliance-mapping">5.8 Cross-Framework Compliance Mapping</h2>

<table>
<thead><tr><th>Standard</th><th>Control</th><th>Network Configuration</th><th>Automated</th><th>Severity</th><th>Remediation</th></tr></thead>
<tbody>
<tr><td>CIS 1.1</td><td>Disable Telnet</td><td><code>transport input telnet</code></td><td>Regex</td><td><span class="badge badge-critical">CRITICAL</span></td><td><code>transport input ssh</code></td></tr>
<tr><td>CIS 1.2</td><td>SSH v2 Only</td><td><code>ip ssh version 1</code></td><td>Config parse</td><td><span class="badge badge-high">HIGH</span></td><td><code>ip ssh version 2</code></td></tr>
<tr><td>CIS 2.1</td><td>SNMP Community</td><td><code>snmp-server community public</code></td><td>String match</td><td><span class="badge badge-critical">CRITICAL</span></td><td>Change to random string</td></tr>
<tr><td>NIST AC-17</td><td>Remote Access</td><td>Telnet/SSH config</td><td>Protocol check</td><td><span class="badge badge-high">HIGH</span></td><td>Disable Telnet</td></tr>
<tr><td>NIST AU-2</td><td>Audit Events</td><td><code>logging host</code></td><td>Syslog check</td><td><span class="badge badge-medium">MEDIUM</span></td><td>Configure syslog server</td></tr>
<tr><td>DISA NET0020</td><td>Admin Auth</td><td>login on lines</td><td>AAA check</td><td><span class="badge badge-critical">CRITICAL</span></td><td>Enable AAA</td></tr>
<tr><td>DISA NET0050</td><td>Session Timeout</td><td><code>exec-timeout</code></td><td>Timeout check</td><td><span class="badge badge-medium">MEDIUM</span></td><td>Set 10 min timeout</td></tr>
<tr><td>ISO A.12.4.1</td><td>Event Logging</td><td>Syslog/SNMP</td><td>Logging check</td><td><span class="badge badge-medium">MEDIUM</span></td><td>Enable centralized logging</td></tr>
</tbody>
</table>
</section>
'''


# ── 6. Vendor-Specific Configurations ──────────────────────────────

def _vendor_configs():
    return '''
<section class="section" id="vendor-configs">
<h1>6. Vendor-Specific Network Configurations</h1>

<h2 id="cisco-config">6.1 Cisco IOS / IOS-XE</h2>

<p><strong>Configuration Format:</strong> Hierarchical CLI (parent-child structure)</p>

<h3>Security-Relevant Commands</h3>
<pre><code><span class="comment">! Management Access</span>
<span class="keyword">line vty</span> 0 4
 <span class="keyword">transport input</span> ssh
 <span class="keyword">transport output</span> ssh
 <span class="keyword">login authentication</span> ADMIN
 <span class="keyword">exec-timeout</span> <span class="number">10</span> <span class="number">0</span>
!
<span class="keyword">ip ssh version</span> <span class="number">2</span>
<span class="keyword">ip ssh server algorithm kex</span> dh-group14-sha256
!
<span class="comment">! AAA Configuration</span>
<span class="keyword">aaa new-model</span>
<span class="keyword">aaa authentication login</span> ADMIN group tacacs+ local
<span class="keyword">aaa authorization exec</span> ADMIN group tacacs+ local
!
<span class="comment">! SNMP</span>
<span class="keyword">snmp-server community</span> MyC0mmun1ty RO <span class="number">10</span>
<span class="keyword">snmp-server host</span> <span class="number">10.1.1.100</span> version 2c MyC0mmun1ty
!
<span class="comment">! Logging</span>
<span class="keyword">logging host</span> <span class="number">10.1.1.100</span>
<span class="keyword">logging trap</span> informational
!
<span class="comment">! NTP</span>
<span class="keyword">ntp server</span> <span class="number">10.1.1.50</span>
<span class="keyword">ntp authenticate</span>
!
<span class="comment">! Services</span>
<span class="keyword">no ip http server</span>
<span class="keyword">no ip telnet source-interface</span></code></pre>

<h2 id="juniper-config">6.2 Juniper Junos</h2>

<p><strong>Configuration Format:</strong> Hierarchical set commands or structured config</p>

<h3>Security-Relevant Commands</h3>
<pre><code><span class="keyword">system</span> {
    <span class="keyword">services</span> {
        <span class="keyword">ssh</span> {
            <span class="keyword">protocol-version</span> v2;
        }
        <span class="comment"># telnet disabled by default</span>
    }
    <span class="keyword">login</span> {
        <span class="keyword">class</span> admin-class {
            <span class="keyword">idle-timeout</span> <span class="number">10</span>;
        }
        <span class="keyword">user</span> admin {
            <span class="keyword">authentication</span> {
                <span class="keyword">encrypted-password</span> <span class="string">"$9$..."</span>;
            }
        }
    }
    <span class="keyword">syslog</span> {
        <span class="keyword">host</span> <span class="number">10.1.1.100</span> {
            any informational;
        }
    }
    <span class="keyword">ntp</span> {
        <span class="keyword">server</span> <span class="number">10.1.1.50</span>;
    }
}
<span class="keyword">snmp</span> {
    <span class="keyword">community</span> MyC0mmun1ty {
        <span class="keyword">authorization</span> read-only;
        <span class="keyword">clients</span> {
            <span class="number">10.1.1.0/24</span>;
        }
    }
}</code></pre>

<h2 id="fortinet-config">6.3 Fortinet FortiOS</h2>

<p><strong>Configuration Format:</strong> Nested config blocks</p>

<h3>Security-Relevant Commands</h3>
<pre><code><span class="keyword">config system global</span>
    <span class="keyword">set</span> admin-sport <span class="number">443</span>
    <span class="keyword">set</span> admin-https-ssl-versions tlsv1-2
    <span class="keyword">set</span> admin-login-max <span class="number">5</span>
    <span class="keyword">set</span> admin-lockout-timer <span class="number">30</span>
<span class="keyword">end</span>

<span class="keyword">config system admin</span>
    <span class="keyword">edit</span> <span class="string">"admin"</span>
        <span class="keyword">set</span> accprofile <span class="string">"prof_admin"</span>
        <span class="keyword">set</span> two-factor fortitoken
        <span class="keyword">set</span> idle-timeout <span class="number">600</span>
    <span class="keyword">next</span>
<span class="keyword">end</span>

<span class="keyword">config log syslog setting</span>
    <span class="keyword">set</span> status enable
    <span class="keyword">set</span> server <span class="number">10.1.1.100</span>
    <span class="keyword">set</span> port <span class="number">514</span>
<span class="keyword">end</span>

<span class="keyword">config system ntp</span>
    <span class="keyword">edit</span> <span class="number">1</span>
        <span class="keyword">set</span> server <span class="number">10.1.1.50</span>
    <span class="keyword">next</span>
<span class="keyword">end</span></code></pre>

<h2 id="paloalto-config">6.4 Palo Alto PAN-OS</h2>

<p><strong>Configuration Format:</strong> XML or hierarchical CLI</p>

<h3>Security-Relevant Commands</h3>
<pre><code><span class="keyword">set deviceconfig system</span> login-banner <span class="string">"Authorized Access Only"</span>
<span class="keyword">set deviceconfig system service</span> ssh on
<span class="keyword">set deviceconfig system service</span> telnet off
<span class="keyword">set deviceconfig system service</span> https on
<span class="keyword">set deviceconfig system</span> idle-timeout <span class="number">10</span>
<span class="keyword">set deviceconfig system</span> authentication-profile <span class="string">"AD-Auth"</span>
<span class="keyword">set deviceconfig server-profile syslog</span> <span class="string">"Syslog-Server"</span>
<span class="keyword">set deviceconfig server-profile ntp</span> <span class="string">"NTP-Server"</span>
<span class="keyword">set deviceconfig setting config</span> rematch yes</code></pre>

<h2 id="arista-config">6.5 Arista EOS</h2>

<p><strong>Configuration Format:</strong> Cisco-like CLI</p>

<h3>Security-Relevant Commands</h3>
<pre><code><span class="keyword">service ssh</span>
<span class="keyword">no service telnet</span>
!
<span class="keyword">aaa authentication login</span> default group tacacs+ local
<span class="keyword">aaa authorization exec</span> default group tacacs+ local
!
<span class="keyword">snmp-server community</span> MyC0mmun1ty ro
<span class="keyword">snmp-server host</span> <span class="number">10.1.1.100</span> version 2c MyC0mmun1ty
!
<span class="keyword">logging host</span> <span class="number">10.1.1.100</span>
!
<span class="keyword">ntp server</span> <span class="number">10.1.1.50</span></code></pre>

<h2 id="normalization-strategy">6.6 Configuration Normalization Strategy</h2>

<p><strong>Goal:</strong> Map vendor-specific syntax to a common security model.</p>

<table>
<thead><tr><th>Security Concept</th><th>Cisco</th><th>Juniper</th><th>Fortinet</th><th>Palo Alto</th><th>Normalized</th></tr></thead>
<tbody>
<tr><td>SSH Enabled</td><td><code>transport input ssh</code></td><td><code>set system services ssh</code></td><td><code>set admin-sport 443</code></td><td><code>service ssh on</code></td><td><code>mgmt.ssh.enabled = true</code></td></tr>
<tr><td>Telnet Disabled</td><td><code>no transport input telnet</code></td><td>(default disabled)</td><td>(not present)</td><td><code>service telnet off</code></td><td><code>mgmt.telnet.enabled = false</code></td></tr>
<tr><td>SSH Version 2</td><td><code>ip ssh version 2</code></td><td><code>protocol-version v2</code></td><td><code>admin-https-ssl-versions tlsv1-2</code></td><td>(implicit)</td><td><code>mgmt.ssh.version = 2</code></td></tr>
<tr><td>Session Timeout</td><td><code>exec-timeout 10 0</code></td><td><code>idle-timeout 10</code></td><td><code>idle-timeout 600</code></td><td><code>idle-timeout 10</code></td><td><code>mgmt.session.timeout = 600</code></td></tr>
<tr><td>SNMP Community</td><td><code>snmp-server community X</code></td><td><code>snmp community X</code></td><td><code>config system snmp community</code></td><td>(not applicable)</td><td><code>mgmt.snmp.community = "X"</code></td></tr>
<tr><td>Syslog Server</td><td><code>logging host X</code></td><td><code>set system syslog host X</code></td><td><code>config log syslog setting</code></td><td><code>server-profile syslog</code></td><td><code>logging.syslog.server = "X"</code></td></tr>
<tr><td>NTP Server</td><td><code>ntp server X</code></td><td><code>set system ntp server X</code></td><td><code>config system ntp</code></td><td><code>server-profile ntp</code></td><td><code>time.ntp.server = "X"</code></td></tr>
</tbody>
</table>

<div class="callout callout-technical">
<div class="callout-title">Recommendation</div>
<p>Create a lightweight JSON schema for normalization (not full OpenConfig/YANG — too complex for 36-hour prototype). Use a custom schema covering only security-relevant controls that's fast to build and easy to extend later.</p>
</div>

<h3>Example Normalized Configuration (JSON)</h3>
<pre><code>{
  <span class="string">"device"</span>: {
    <span class="string">"vendor"</span>: <span class="string">"cisco"</span>,
    <span class="string">"model"</span>: <span class="string">"ISR4451"</span>,
    <span class="string">"os"</span>: <span class="string">"IOS-XE"</span>,
    <span class="string">"version"</span>: <span class="string">"17.3.4"</span>
  },
  <span class="string">"management"</span>: {
    <span class="string">"ssh"</span>: {
      <span class="string">"enabled"</span>: <span class="keyword">true</span>,
      <span class="string">"version"</span>: <span class="number">2</span>,
      <span class="string">"algorithms"</span>: [<span class="string">"aes256-ctr"</span>, <span class="string">"hmac-sha2-256"</span>]
    },
    <span class="string">"telnet"</span>: { <span class="string">"enabled"</span>: <span class="keyword">false</span> },
    <span class="string">"session_timeout"</span>: <span class="number">600</span>,
    <span class="string">"login_banner"</span>: <span class="string">"Authorized Access Only"</span>
  },
  <span class="string">"authentication"</span>: {
    <span class="string">"aaa_enabled"</span>: <span class="keyword">true</span>,
    <span class="string">"method"</span>: <span class="string">"tacacs+"</span>,
    <span class="string">"local_fallback"</span>: <span class="keyword">true</span>
  },
  <span class="string">"logging"</span>: {
    <span class="string">"syslog"</span>: {
      <span class="string">"enabled"</span>: <span class="keyword">true</span>,
      <span class="string">"server"</span>: <span class="string">"10.1.1.100"</span>,
      <span class="string">"level"</span>: <span class="string">"informational"</span>
    }
  },
  <span class="string">"time"</span>: {
    <span class="string">"ntp"</span>: {
      <span class="string">"enabled"</span>: <span class="keyword">true</span>,
      <span class="string">"servers"</span>: [<span class="string">"10.1.1.50"</span>]
    }
  }
}</code></pre>
</section>
'''


# ── 7. Proposed NEXUS Solution ─────────────────────────────────────

def _proposed_solution():
    return '''
<section class="section" id="proposed-solution">
<h1>7. Proposed NEXUS Solution</h1>

<h2 id="core-idea">7.1 Core Idea — Vendor-Neutral Security Interpretation Layer</h2>

<p>Instead of building separate parsers and rules for each vendor, NEXUS creates a <strong>vendor-neutral security interpretation layer</strong>:</p>

<div class="arch-box">Cisco ────────┐
Juniper ──────┤
Fortinet ─────┤       AI Configuration        Vendor-Neutral        Compliance
Palo Alto ────┤  ──▶  Interpreter          ──▶  Security Schema  ──▶  Engine
Arista ───────┤                                                        ↓
Unknown ──────┘                                                   CIS / NIST / STIG
                                                                       ↓
                                                                  Findings + Risk
                                                                       ↓
                                                                Explanation + Fix</div>

<div class="callout callout-simple">
<div class="callout-title">Simple Explanation</div>
<p>Think of it like Google Translate for network security. Every vendor speaks a different "language," but our system translates them all into one common language first, then checks security rules against that common language.</p>
</div>

<div class="callout callout-technical">
<div class="callout-title">Technical Explanation</div>
<p>NEXUS implements a vendor-agnostic configuration normalization pipeline that transforms heterogeneous CLI syntax into a canonical JSON security model, enabling framework-independent compliance evaluation through deterministic rule matching with AI-augmented explanation via RAG-grounded LLM inference.</p>
</div>

<h2 id="what-makes-different">7.2 What Makes NEXUS Different</h2>

<h3>Traditional Tool</h3>
<pre><code>Known vendor → Known command → Hard-coded rule → Pass/Fail</code></pre>

<h3>NEXUS</h3>
<pre><code>Configuration
      ↓
Identify vendor
      ↓
Parse / interpret
      ↓
Extract security meaning
      ↓
Map to common schema
      ↓
Evaluate controls
      ↓
Explain finding
      ↓
Generate remediation</code></pre>

<p>And most importantly — the <strong>adaptive learning loop</strong>:</p>
<pre><code>UNKNOWN COMMAND
       ↓
AI interpretation
       ↓
Human confirmation
       ↓
Knowledge update
       ↓
Future configurations → Previously understood automatically</code></pre>

<div class="callout callout-key-insight">
<div class="callout-title">Strongest Differentiator</div>
<p>The adaptive learning loop is the feature that should be the centerpiece of the SIH demo. Traditional tools say "Unsupported ❌" for unknown vendors. NEXUS says: "I think this means X — can you confirm?" After confirmation, it remembers forever.</p>
</div>

<h2 id="core-features">7.3 Core Features</h2>

<table>
<thead><tr><th>#</th><th>Feature</th><th>Description</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>Multi-Vendor Parsing</strong></td><td>Parse Cisco, Juniper, Fortinet, Palo Alto configs into structured data</td></tr>
<tr><td>2</td><td><strong>Vendor-Neutral Normalization</strong></td><td>Map all vendors to common JSON security schema</td></tr>
<tr><td>3</td><td><strong>Deterministic Compliance Engine</strong></td><td>YAML rules evaluated against normalized config — 100% auditable</td></tr>
<tr><td>4</td><td><strong>RAG-Grounded Explanations</strong></td><td>AI explains WHY with citations to CIS/NIST/STIG — not hallucinated</td></tr>
<tr><td>5</td><td><strong>Vendor-Specific Remediation</strong></td><td>Generate fix commands in the correct vendor CLI syntax</td></tr>
<tr><td>6</td><td><strong>Risk Scoring</strong></td><td>Device and network-level compliance scores weighted by severity</td></tr>
<tr><td>7</td><td><strong>Evidence-Based Audit Reports</strong></td><td>PDF reports with config snippets, citations, and remediation</td></tr>
<tr><td>8</td><td><strong>Adaptive Learning</strong></td><td>Learn new vendor syntax from administrator feedback</td></tr>
</tbody>
</table>

<h2 id="advanced-features">7.4 Advanced Features &amp; Prioritization</h2>

<table>
<thead><tr><th>Feature</th><th>WOW</th><th>Technical</th><th>Difficulty</th><th>SIH Value</th><th>Priority</th></tr></thead>
<tbody>
<tr><td>Multi-vendor normalization</td><td>8</td><td>10</td><td>7</td><td>10</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>AI configuration explanation</td><td>9</td><td>7</td><td>5</td><td>9</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>AI remediation generation</td><td>8</td><td>8</td><td>6</td><td>8</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>Compliance RAG</td><td>7</td><td>9</td><td>6</td><td>8</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>Natural-language auditing</td><td>9</td><td>7</td><td>6</td><td>9</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>Risk scoring</td><td>6</td><td>7</td><td>3</td><td>7</td><td><span class="badge badge-critical">MUST</span></td></tr>
<tr><td>Network topology</td><td>8</td><td>6</td><td>6</td><td>7</td><td><span class="badge badge-high">SHOULD</span></td></tr>
<tr><td>"Ask your network" chatbot</td><td>10</td><td>6</td><td>7</td><td>8</td><td><span class="badge badge-high">SHOULD</span></td></tr>
<tr><td>Configuration drift detection</td><td>6</td><td>8</td><td>7</td><td>6</td><td><span class="badge badge-medium">NICE</span></td></tr>
<tr><td>What-if analysis</td><td>7</td><td>8</td><td>9</td><td>6</td><td><span class="badge badge-low">CUT</span></td></tr>
<tr><td>SIEM integration</td><td>5</td><td>8</td><td>8</td><td>5</td><td><span class="badge badge-low">CUT</span></td></tr>
<tr><td>CI/CD compliance checks</td><td>6</td><td>8</td><td>8</td><td>6</td><td><span class="badge badge-low">CUT</span></td></tr>
</tbody>
</table>
</section>
'''
