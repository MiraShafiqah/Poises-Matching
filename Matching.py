import pandas as pd
import networkx as nx
from itertools import combinations
import random
import re

file_path = "student_data.csv"

def load_data(file_path):
    return pd.read_csv(file_path)


def create_knowledge_graph():
    G = nx.Graph()
    
    # Define the list of Majors before adding nodes to the graph
    Majors = ['Environmental Science', 'Geography', 'Physics', 'Astronomy', 'Chemistry', 'Materials Science', 'Biology', 'Psychology', 'Computer Science', 'Robotics', 'Electrical Engineering', 'Biochemistry', 'Civil Engineering', 'Urban Planning', 'International Relations', 'Sociology', 'Anthropology', 'Film Studies', 'Theater Arts', 'Nutrition', 'Forensic Science', 'Cybersecurity', 'Data Science', 'Statistics', 'Aerospace Engineering', 'Genetics', 'Microbiology', 'Zoology', 'Veterinary Science', 'Architecture', 'Music', 'Philosophy', 'Mathematics', 'Journalism', 'Communications', 'Gender Studies', 'Public Health', 'Web Development', 'Information System', 'Business Administration']
    
    # Add all majors as nodes
    G.add_nodes_from(Majors)
    
    # Define categories
    stem = ["Aerospace Engineering", "Applied Mathematics", "Artificial Intelligence", "Astronomy", "Astrophysics", "Biochemistry", "Biotechnology", "Chemical Engineering", "Chemistry", "Civil Engineering", "Computer Engineering", "Computer Science", "Cybersecurity", "Data Science", "Electrical Engineering", "Environmental Science", "Genetics", "Geology", "Industrial Engineering", "Materials Science", "Mathematics", "Mechanical Engineering", "Physics", "Robotics", "Software Engineering", "Statistics"]
    life_sciences = ["Agriculture", "Biochemistry", "Biology", "Biotechnology", "Environmental Science", "Food Science", "Genetics", "Medicine", "Microbiology", "Neuroscience", "Nursing", "Nutrition", "Public Health", "Veterinary Science", "Zoology"]
    social_sciences = ["Anthropology", "Criminal Justice", "Economics", "Education", "Gender Studies", "Geography", "Human Resources", "International Relations", "Linguistics", "Political Science", "Psychology", "Social Work", "Sociology", "Urban Planning"]
    humanities = ["Art History", "Classical Studies", "Communications", "English Literature", "History", "Journalism", "Philosophy", "Religious Studies"]
    business = ["Accounting", "Business Administration", "Finance", "Hospitality Management", "Marketing"]
    arts = ["Architecture", "Fashion Design", "Film Studies", "Fine Arts", "Graphic Design", "Music", "Theater Arts"]

    # Connect majors within categories (stronger connections)
    categories = [stem, life_sciences, social_sciences, humanities, business, arts]
    for category in categories:
        for major1, major2 in combinations(category, 2):
            G.add_edge(major1, major2, weight=0.7)

    # Connect related majors across categories (medium connections)
    interdisciplinary_connections = [
        ("Computer Science", "Artificial Intelligence", 0.9),
        ("Computer Science", "Data Science", 0.9),
        ("Mathematics", "Physics", 0.8),
        ("Mathematics", "Statistics", 0.8),
        ("Biology", "Biochemistry", 0.8),
        ("Biology", "Environmental Science", 0.7),
        ("Psychology", "Neuroscience", 0.7),
        ("Economics", "Mathematics", 0.6),
        ("Linguistics", "Computer Science", 0.5),
        ("Business Administration", "Economics", 0.6),
        ("Marketing", "Psychology", 0.5),
        ("Environmental Science", "Geography", 0.6),
        ("Physics", "Astronomy", 0.8),
        ("Chemistry", "Materials Science", 0.7),
        ("Biology", "Psychology", 0.5),
        ("Computer Science", "Robotics", 0.7),
        ("Electrical Engineering", "Robotics", 0.7),
        ("Medicine", "Biochemistry", 0.7),
        ("Civil Engineering", "Urban Planning", 0.6),
        ("Political Science", "International Relations", 0.7),
        ("Sociology", "Anthropology", 0.6),
        ("Film Studies", "Theater Arts", 0.6),
        ("Nutrition", "Biology", 0.6),
        ("Forensic Science", "Chemistry", 0.6),
        ("Forensic Science", "Biology", 0.6),
        ("Cybersecurity", "Computer Science", 0.7),
        ("Data Science", "Statistics", 0.8),
        ("Aerospace Engineering", "Physics", 0.7),
        ("Genetics", "Biology", 0.8),
        ("Microbiology", "Biology", 0.8),
        ("Zoology", "Biology", 0.8),
        ("Veterinary Science", "Biology", 0.7),
        ("Architecture", "Civil Engineering", 0.5),
        ("Music", "Physics", 0.3),
        ("Philosophy", "Mathematics", 0.4),
        ("Journalism", "Communications", 0.7),
        ("Gender Studies", "Sociology", 0.6),
        ("Public Health", "Biology", 0.6),
        ("Public Health", "Sociology", 0.5),
        ("Web Development", "Computer Science", 0.7),
        ("Information System", "Computer Science", 0.7),
        ("Information System", "Business Administration", 0.6)
    ]

    for major1, major2, weight in interdisciplinary_connections:
        G.add_edge(major1, major2, weight=weight)

    return G

def extract_timezone_offset(timezone_str):
    match = re.search(r'([-+]\d+)', timezone_str)
    if match:
        return int(match.group())
    return None

def calculate_compatibility(student1, student2, G):
    score = 0
    
    # Major compatibility
    for major1 in student1['Majors']:
        for major2 in student2['Majors']:
            if nx.has_path(G, major1, major2):
                score += 1 / nx.shortest_path_length(G, major1, major2)
    
    # Primary Interest overlap
    p_interests = set(student1['Primary']) & set(student2['Primary'])
    score += len(p_interests) * 0.5
    
    # Secondary Interest overlap
    s_interest = set(student1['Secondary']) & set(student2['Secondary'])
    score += len(s_interest)
    
    # Timezone compatibility
    time_diff = abs(extract_timezone_offset(student1['Timezone']) - extract_timezone_offset(student2['Timezone']))

    if 1 <= time_diff <= 3:
        score += 1  # Slight bonus for close but different time zones
    elif 6 <= time_diff <= 9:
        score += 2  # Larger bonus for time zones that are further apart but still practical for meetings
    elif time_diff > 9:
        score -= (time_diff - 9) * 0.2  # Slight penalty for time differences beyond 9 hours
    # No adjustment for time differences of 0, 4, or 5 hours
    
    return score

def form_groups(students, G, group_size=5):
    groups = []
    remaining_students = students.copy()
    
    while len(remaining_students) >= group_size:
        group = [remaining_students.pop(0)]
        while len(group) < group_size:
            compatibility_scores = [
                (student, sum(calculate_compatibility(student, member, G) for member in group))
                for student in remaining_students
            ]
            best_match = max(compatibility_scores, key=lambda x: x[1])[0]
            group.append(best_match)
            remaining_students.remove(best_match)
        groups.append(group)
    
    # Handle remaining students
    if remaining_students:
        for student in remaining_students:
            best_group = max(groups, key=lambda g: sum(calculate_compatibility(student, member, G) for member in g) / len(g))
            best_group.append(student)
    
    return groups

def preprocess_data(data):
    # Convert Majors to a list if it's not already
    data['Majors'] = data['Majors'].apply(lambda x: [x.strip()] if isinstance(x, str) else x)
    
    # Handle Primary and Secondary Interests
    data['Primary'] = data['Primary'].apply(lambda x: [x.strip()] if isinstance(x, str) else x)
    data['Secondary'] = data['Secondary'].apply(lambda x: [x.strip()] if isinstance(x, str) else x)
    
    return data

if __name__ == "__main__":
    # Load data
    data = load_data('student_data.csv')
    data = preprocess_data(data)
    
    # Create knowledge graph
    G = create_knowledge_graph()
    
    # Form groups
    groups = form_groups(data.to_dict('records'), G)
    
    # Output groups
    for i, group in enumerate(groups, 1):
        print(f"Group {i}:")
        for member in group:
            print(f"  Name: {member['Name']}")
            print(f"  Email: {member['Email']}")
            print(f"  Majors: {', '.join(member['Majors'])}")
            print(f"  Timezone: {member['Timezone']}")
            print(f"  Interests: {', '.join(member['Interests'])}")
            print(f"  Topics: {', '.join(member['Topics'])}")
            print()
        print()
        