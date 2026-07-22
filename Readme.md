# Lab 1: Grade Evaluator & Archiver

## Files
- `grade-evaluator.py` — reads a grades CSV, validates it, calculates GPA, and reports pass/fail + resubmission status.
- `organizer.sh` — archives the current `grades.csv` with a timestamp and resets the workspace.
- `grades.csv` — sample data used for testing.

## Requirements
- Python 3
- Bash (Linux/macOS terminal, or WSL/Git Bash on Windows)

## Running the Python application

```bash
python3 grade-evaluator.py
```

You'll be prompted to enter the CSV filename, e.g.:

```
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

The program will then print:
- Formative and Summative percentage scores
- The final weighted grade and GPA (out of 5.0)
- Whether the student PASSED or FAILED (requires ≥50% in both Formative and Summative)
- Which formative assignment(s) are eligible for resubmission (the failed formative assignment(s) with the highest weight — ties are all shown)

If the CSV is missing, empty, missing required columns, or contains invalid scores/weights, the program prints a clear error message instead of crashing.

### Expected CSV format

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

- `score` must be between 0 and 100.
- `weight` values must sum to exactly 100 overall, with Formative weights summing to exactly 60 and Summative weights summing to exactly 40.

## Running the shell script

Make sure the script is executable (only needed once):

```bash
chmod +x organizer.sh
```

Then run it from the same directory as `grades.csv`:

```bash
./organizer.sh
```

Each run will:
1. Create an `archive/` folder if it doesn't already exist.
2. Move the current `grades.csv` into `archive/` renamed with a timestamp (e.g. `grades_20260722-064510.csv`).
3. Create a fresh, empty `grades.csv` in the working directory.
4. Append a record of the run to `organizer.log`.

## Notes
- Run `organizer.sh` **after** you're done analyzing a batch of grades and want to reset the workspace for the next one.
- `organizer.log` accumulates a line per run, so you can see the full archiving history over time.
