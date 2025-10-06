# Playbook: Privilege Escalation
## Description
Attackers often elevate privileges after gaining initial access.

## Detection
- Creation of new admin users.
- Use of PowerShell with encoded commands.

## Response
1. Review event logs for new user creation.
2. Reset admin credentials.
3. Monitor for lateral movement.

## Recovery
Ensure endpoint hardening and least-privilege policies are enforced.
