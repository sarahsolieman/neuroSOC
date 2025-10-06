# Playbook: Authentication Anomalies
## Description
Brute-force and credential-stuffing attacks target login endpoints with repeated password attempts.

## Detection
- Multiple failed logins for the same user or IP within short windows.
- Successful login after many failures.

## Response
1. Block offending IPs or throttle login attempts.
2. Force password resets for affected accounts.
3. Review MFA enforcement and password policy.

## Recovery
Confirm no privilege escalation or lateral movement occurred post-login.
