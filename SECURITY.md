# Security Policy

## Supported Versions

Security updates are applied to actively maintained SpecFact CLI release lines.
For exact support windows, use the latest release notes and upgrade guidance.

## Reporting a Vulnerability

We take the security of SpecFact CLI seriously. If you believe you've found a security vulnerability, please follow these guidelines for responsible disclosure:

### How to Report

Please **DO NOT** report security vulnerabilities through public GitHub issues.

Instead, please report them via email to:

- `hello@noldai.com`

Please include the following information in your report:

1. Description of the vulnerability
2. Steps to reproduce the issue
3. Potential impact of the vulnerability
4. Any suggested mitigations (if available)

### What to Expect

After you report a vulnerability:

- You'll receive acknowledgment of your report within 48 hours.
- We'll provide an initial assessment of the report within 5 business days.
- We aim to validate and respond to reports as quickly as possible, typically within 10 business days.
- We'll keep you informed about our progress addressing the issue.

### Disclosure Policy

- Please give us a reasonable time to address the issue before any public disclosure.
- We will coordinate with you to ensure that a fix is available before any disclosure.
- We will acknowledge your contribution in our release notes (unless you prefer to remain anonymous).

## Security Best Practices

When using SpecFact CLI in your environment:

- Keep your installation updated with the latest releases.
- Use least-privilege credentials for GitHub/ADO integrations.
- Store tokens securely and avoid committing secrets to source control.
- Run CLI commands in CI with restricted permissions and audited logs.
- Review generated artifacts before syncing to external backlog systems.

Thank you for helping keep SpecFact CLI and our users secure!
