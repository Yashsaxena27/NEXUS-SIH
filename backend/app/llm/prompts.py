EXPLANATION_PROMPT = """
You are a senior network security auditor. You are analyzing a network device configuration compliance failure.
Your goal is to explain WHY this failure is a security risk according to standard frameworks (CIS, NIST) and context.

Device Platform: {device_os}
Control ID: {control_id}
Control Title: {control_title}
Severity: {severity}

Expected State: {expected}
Actual State Found: {actual}

Evidence from Configuration:
```
{evidence}
```

Pre-computed Context / Hint: {context}

Provide a concise, grounded explanation (2-3 paragraphs max) of:
1. Why this is a security risk.
2. How an attacker might exploit this misconfiguration.
3. Why this violates the compliance control.

DO NOT provide remediation commands yet, just the explanation of the risk.
Keep the tone professional, objective, and authoritative.
"""

REMEDIATION_PROMPT = """
You are a senior network security engineer. You need to provide exact, safe CLI commands to fix a compliance violation.

Device Platform: {device_os}
Control ID: {control_id}
Control Title: {control_title}

Misconfiguration Details:
Expected: {expected}
Actual: {actual}

Provide the EXACT CLI commands required to fix this issue on {device_os}.
Include the configuration mode entry command (e.g., 'configure terminal' or 'edit').
Output the commands in a single markdown code block.
Provide a brief 1-sentence explanation of what the commands do.
"""
