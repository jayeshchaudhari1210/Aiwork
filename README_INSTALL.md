# AIWork installation and local verification

AIWork is alpha software. Use a virtual environment and Python 3.11 for the setup verified on 28 October 2026. Metadata requires Python >=3.10; Python 3.11 is the verified target.

## Install

```bash
git clone https://github.com/jayeshchaudhari1210/Aiwork.git
cd Aiwork
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -c "from aiwork import Task, Flow, Orchestrator; print('AIWork imports successfully')"
```

On Windows with Python 3.11 installed, create the environment with `py -3.11 -m venv .venv`, then activate `.venv\Scripts\Activate.ps1` in PowerShell. That Windows procedure was not executed during the Linux verification.

## Verified deterministic/mock examples

Run from the repository root with the environment active:

```bash
python examples/quickstart.py
python examples/agents/document_processor/run.py
python examples/agents/customer_support/run.py
python -m pytest -o addopts= -q
```

All three examples exited successfully and all 78 tests passed (7 warnings) on Python 3.11.16. OCR, provider replies and adapters are demonstrations, not evidence of real model/service operation. See [README limitations](README.md#known-limitations).

## Optional extras are not implemented service integrations

`python -m pip install -e ".[dev]"` installs the development extras; its broad test-version range differs from the requirements file's patched pytest 9.x range. The verification above used requirements.txt.

`python -m pip install -e ".[intel]"` installs OpenVINO as an optional dependency. It does **not** replace the placeholder adapter or turn the simulated benchmark into a hardware measurement.

`python -m pip install -e ".[integrations]"` installs optional Kafka/Redis clients. Broker communication and Redis persistence remain prototype/stub work. Neither optional extra was needed or installed for the verified examples.

## Local API

```bash
python -m aiwork.api --host 127.0.0.1 --port 5000
```

The application exposes `/health`, `/workflow`, `/workflow/<id>` and `/workflow/<id>/task/<name>`. It uses generic handlers and in-memory state. Keep the demo local; deploying a production service needs separate implementation work.

## Troubleshooting

- Import failures: check the active environment and rerun `python -m pip install -e .` from this checkout.
- API annotation failures on old Python: use the verified Python 3.11 environment.
- Port conflicts: choose another port, for example `--port 5050`.
- GUI/provider/service credentials are not needed for the deterministic examples; no paid model calls were performed.
