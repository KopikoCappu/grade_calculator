import os
import matplotlib.pyplot as plt

def read_students(filepath):
    students = {}
    with open(filepath, 'r') as f:
        for line in f:
            student_id = line[:3]
            name = line[3:].strip()
            students[name] = student_id
    return students

def read_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as f:
        while True:
            name = f.readline().strip()
            if not name:
                break
            assignment_id = f.readline().strip()
            points = float(f.readline().strip())
            assignments[name] = {'id': assignment_id, 'points': points}
    return assignments


def read_submissions(directory):
    submissions = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                for line in f:
                    student_id, assignment_id, percentage = line.strip().split('|')

                    submissions.append({
                        'student_id': student_id,
                        'assignment_id': assignment_id,
                        'percentage': float(percentage)
                    })

    return submissions


def calculate_student_grade(students, assignments, submissions, student_name):
    if student_name not in students:
        return None

    student_id = students[student_name]

    student_submissions = [
        sub for sub in submissions
        if sub['student_id'] == student_id
    ]

    total_points_earned = sum(
        (sub['percentage'] / 100) * assignments[assignment_name]['points']
        for assignment_name in assignments.keys()
        for sub in student_submissions
        if assignments[assignment_name]['id'] == sub['assignment_id']
    )

    grade_percentage = (total_points_earned / 1000) * 100
    return round(grade_percentage)


def assignment_statistics(assignments, submissions, assignment_name):
    if assignment_name not in assignments:
        return None

    assignment_id = assignments[assignment_name]['id']

    assignment_submissions = [
        sub['percentage']
        for sub in submissions
        if sub['assignment_id'] == assignment_id
    ]

    if not assignment_submissions:
        return None

    return {
        'min': min(assignment_submissions),
        'avg': sum(assignment_submissions) / len(assignment_submissions),
        'max': max(assignment_submissions)
    }


def plot_assignment_scores(assignments, submissions, assignment_name):
    if assignment_name not in assignments:
        return None

    assignment_id = assignments[assignment_name]['id']

    assignment_submissions = [
        sub['percentage']
        for sub in submissions
        if sub['assignment_id'] == assignment_id
    ]

    plt.figure(figsize=(10, 6))
    plt.hist(assignment_submissions, bins=[0, 25, 50, 75, 100], edgecolor='black')
    plt.title(f'Score Distribution for {assignment_name}')
    plt.xlabel('Percentage Score')
    plt.ylabel('Number of Students')
    plt.show()


def main():
    students = read_students('data/students.txt')
    assignments = read_assignments('data/assignments.txt')
    submissions = read_submissions('data/submissions')

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")

    selection = input("Enter your selection: ")

    if selection == '1':
        student_name = input("What is the student's name: ")
        grade = calculate_student_grade(students, assignments, submissions, student_name)
        if grade is not None:
            print(f"{grade}%")
        else:
            print("Student not found")

    elif selection == '2':
        assignment_name = input("What is the assignment name: ")
        stats = assignment_statistics(assignments, submissions, assignment_name)
        if stats:
            print(f"Min: {round(stats['min'])}%")
            print(f"Avg: {round(stats['avg'])}%")
            print(f"Max: {round(stats['max'])}%")
        else:
            print("Assignment not found")

    elif selection == '3':
        assignment_name = input("What is the assignment name: ")
        plot_assignment_scores(assignments, submissions, assignment_name)


if __name__ == "__main__":
    main()