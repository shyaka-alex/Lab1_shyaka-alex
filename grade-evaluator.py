import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Handle a completely empty file (no header row at all)
            if reader.fieldnames is None:
                print(f"Error: '{filename}' is empty. No data to process.")
                sys.exit(1)

            required_columns = {'assignment', 'group', 'score', 'weight'}
            missing_columns = required_columns - set(reader.fieldnames)
            if missing_columns:
                print(f"Error: CSV is missing required column(s): {', '.join(missing_columns)}")
                sys.exit(1)

            for line_num, row in enumerate(reader, start=2):
                try:
                    assignment_name = row['assignment'].strip()
                    group = row['group'].strip()

                    if not assignment_name or not group:
                        print(f"Warning: Skipping row {line_num} - missing assignment name or group.")
                        continue

                    # Convert numeric fields to floats for calculations
                    assignments.append({
                        'assignment': assignment_name,
                        'group': group,
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except (ValueError, AttributeError, KeyError):
                    print(f"Warning: Skipping row {line_num} - invalid or missing data: {row}")
                    continue

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Validates the data, calculates GPA, determines pass/fail status,
    and identifies resubmission-eligible assignments.
    """
    print("\n--- Processing Grades ---")

    
    if not data:
        print("Error: No valid assignment records found. Cannot evaluate grades.")
        return

    errors = []
    total_weight = 0.0
    formative_weight = 0.0
    summative_weight = 0.0

    
    for a in data:
        if not (0 <= a['score'] <= 100):
            errors.append(
                f"Invalid score for '{a['assignment']}': {a['score']} (must be between 0 and 100)."
            )

        if a['group'] not in ('Formative', 'Summative'):
            errors.append(
                f"Unknown group '{a['group']}' for assignment '{a['assignment']}' "
                f"(expected 'Formative' or 'Summative')."
            )

        total_weight += a['weight']
        if a['group'] == 'Formative':
            formative_weight += a['weight']
        elif a['group'] == 'Summative':
            summative_weight += a['weight']

    
    if abs(total_weight - 100) > 0.01:
        errors.append(f"Total weight is {total_weight:.2f}, but it must equal exactly 100.")
    if abs(formative_weight - 60) > 0.01:
        errors.append(f"Formative weight is {formative_weight:.2f}, but it must equal exactly 60.")
    if abs(summative_weight - 40) > 0.01:
        errors.append(f"Summative weight is {summative_weight:.2f}, but it must equal exactly 40.")

    if errors:
        print("Validation failed. Please fix the following issue(s) in your CSV:")
        for e in errors:
            print(f"  - {e}")
        return

    final_grade = sum(a['score'] * a['weight'] for a in data) / 100
    gpa = (final_grade / 100) * 5.0

    
    formative_pct = sum(a['score'] * a['weight'] for a in data if a['group'] == 'Formative') / formative_weight
    summative_pct = sum(a['score'] * a['weight'] for a in data if a['group'] == 'Summative') / summative_weight

    
    passed = formative_pct >= 50 and summative_pct >= 50

    print(f"Formative Score: {formative_pct:.2f}%")
    print(f"Summative Score: {summative_pct:.2f}%")
    print(f"Final Weighted Grade: {final_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}/5.0")
    print(f"Final Status: {'PASSED' if passed else 'FAILED'}")

    
    failed_formatives = [a for a in data if a['group'] == 'Formative' and a['score'] < 50]

    if failed_formatives:
        highest_weight = max(a['weight'] for a in failed_formatives)
        resubmission_targets = [a['assignment'] for a in failed_formatives if a['weight'] == highest_weight]

        print(f"\nResubmission required (highest weight among failed formatives: {highest_weight:.0f}):")
        for name in resubmission_targets:
            print(f"  - {name}")
    else:
        print("\nNo formative resubmission needed.")


if __name__ == "__main__":
    
    course_data = load_csv_data()

    
    evaluate_grades(course_data)
