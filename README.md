# HintForge — AI-Powered Cybersecurity Practice-Lab Coach

## Problem

Cybersecurity students practising web security challenges in OWASP Juice Shop often get stuck identifying vulnerable code and understanding how vulnerabilities work. When they ask general-purpose AI chatbots for help, they may receive fabricated vulnerabilities, incorrect file references, or complete solutions that reduce independent learning. HintForge addresses this problem by retrieving evidence from the actual OWASP Juice Shop source code and generating progressive, code-grounded hints. If the evidence is insufficient, the system responds with "I don't know" rather than inventing an answer.

## Who it is for

- Cybersecurity students and engineering students practising web application security challenges using OWASP Juice Shop.
- Cybersecurity faculty members conducting weekly web-security labs who need accurate hints and control over when students receive detailed vulnerability explanations or complete fixes.

## Signature feature

**Three-Level Evidence-Grounded Hint Ladder with Faculty Approval**

HintForge provides three progressive hint levels for each challenge:

- **Level 1 — File guidance:** Identifies the relevant source file.
- **Level 2 — Code guidance:** Points to the relevant function or code section and explains what to investigate.
- **Level 3 — Vulnerability guidance:** Identifies the specific unsafe code or line and explains the weakness.

Level 1 and Level 2 hints are delivered directly. Level 3 hints and complete fixes require faculty approval. Every hint must be supported by actual source-code evidence; when retrieval confidence is insufficient, HintForge abstains instead of guessing.

## Hardest problem (my interview story)

The hardest problem is ensuring that AI-generated hints are grounded in the real source code rather than relying on the language model's assumptions. A model might suggest a file that does not contain the vulnerability or describe a security flaw that does not exist in the repository. HintForge addresses this challenge through source-code retrieval, evidence verification, confidence-based abstention, and a fixed evaluation set of 60 questions. The goal is to achieve at least 90% faithfulness with zero invented vulnerabilities while preserving the progressive learning experience.

## Dataset

| **Source** | **Link** | **Documents** | **Pages** | **Licence / terms** |
|---|---|---|---|---|
| OWASP Juice Shop public GitHub repository | [github.com/juice-shop/juice-shop](https://github.com/juice-shop/juice-shop) | 650+ source files targeted, including TypeScript/Angular frontend files, Node.js routes, challenge definitions, and 160+ code-fix files | Not applicable — source-code repository, not a paginated document collection | MIT License; verify individual files and third-party components for applicable licence terms |

*Dataset counts are project targets from the project brief and should be verified against the actual downloaded repository before claiming completed ingestion.*

## 10 real questions

See [docs/QUESTIONS.md](https://github.com/selvaranipalanivelrajaan/HintForge/blob/main/docs/QUESTIONS.md).

The evaluation set should include realistic questions about vulnerable routes, authentication, JWT verification, challenge definitions, code-fix files, and questions for which the system should abstain because the source code does not provide sufficient evidence.

## Run it

Create and activate a virtual environment, then install the development dependencies.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload
```

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Check the health endpoint in another terminal:

```bash
curl http://localhost:8000/health
```

Ensure the required environment variables are configured in `.env` before starting the application.

## Live link

Coming in Week 2 — to be added after deployment.
