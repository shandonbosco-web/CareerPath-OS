# CareerPath OS — Operating System PBL Prototype

## Project description
A small career-guidance web prototype with an explainable keyword-based recommendation engine. It demonstrates selected OS-related application concepts: threaded request handling, a worker pool, a bounded semaphore, a lock-protected SQLite write path, and an educational CPU scheduling simulator.

**Important:** The recommender is rule-based, not a trained AI model. The scheduling simulator demonstrates FCFS, non-preemptive SJF and Round Robin; it does not replace or control the computer's actual OS scheduler.

## Requirements
- Python 3.9 or later
- pip

## Run
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Test
With the server running, open another terminal:
```bash
python concurrency_test.py
```
The script submits five API requests concurrently. Also inspect:
- `http://127.0.0.1:5000/api/health`
- `http://127.0.0.1:5000/api/history`
- `http://127.0.0.1:5000/scheduler`

Record the actual outputs and take screenshots before reporting test results.

## Architecture
- `app.py`: Flask routes, ThreadPoolExecutor, Queue, Lock, Semaphore and SQLite history.
- `recommender.py`: transparent keyword matching and top-three career suggestions.
- `scheduler.py`: FCFS, SJF and Round Robin scheduling calculations.
- `templates/index.html`, `static/style.css`: responsive interface.
- `concurrency_test.py`: parallel API test client.

## Limitations
- No authentication or personal-data security controls; use sample data only.
- No external career database, aptitude test or trained ML model.
- The in-memory Queue is a demonstration event queue, not a durable message broker.
- The Semaphore limits concurrent recommendation jobs; the Lock protects SQLite writes.
- OS scheduling concepts are modelled for learning and are not kernel-level implementations.
