EXPLANATION_PROMPT = """
You are a senior network security auditor and engineer. You are analyzing a network device configuration compliance failure.
Your goal is to explain WHY this failure is a security risk according to standard frameworks (CIS, NIST) and context, and provide a concrete remediation path.

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

You MUST structure your response EXACTLY into the following four sections using Markdown headers:

### 1. Evidence
(What was actually observed based on the evidence provided above.)

### 2. Interpretation
(Why this violates the control, and how an attacker might exploit this misconfiguration.)

### 3. Recommendation
(Vendor-specific CLI commands to fix the issue on {device_os}. Use a single Markdown code block.)

### 4. Verification
(How to verify the fix locally, e.g., 'show run | include ssh'.)

Keep the tone professional, objective, and authoritative. Do not hallucinate commands if you are unsure.
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
