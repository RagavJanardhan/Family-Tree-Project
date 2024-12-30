import uuid
import json
from datetime import date
from dateutil.relativedelta import relativedelta

# A node class created to store various attributes for each node (person) in the family tree
class Person:
    def __init__(self, name, birthDate, deathDate=None, gender=None):
        self.name = name
        self.birthDate = self.parse_date(birthDate)
        self.deathDate = self.parse_date(deathDate) if deathDate and deathDate != "NULL" else None
        self.gender = gender
        self.relationships = {"parents": [], "children": [], "spouse": None, "siblings": []}
        self.age = self.calculate_age()  # Automatically calculate age
        self.id = str(uuid.uuid4())  # Generate a unique ID for each person

    @staticmethod
    def parse_date(date_str):
        """
        Parses a date string in 'YYYY-MM-DD' format and returns a date object.
        """
        if date_str == "Unknown" or date_str == "NULL":
            return None
        year, month, day = map(int, date_str.split("-"))
        return date(year, month, day)

    def calculate_age(self):
        """
        Calculates the person's age based on their birthDate and deathDate (if available).
        If the person is alive, calculate age using the current date.
        """
        if self.birthDate:
            end_date = self.deathDate if self.deathDate else date.today()
            return relativedelta(end_date, self.birthDate).years
        return None  # Return None if birthDate is not set

    def add_parent(self, parent):
        self.relationships["parents"].append(parent)
        parent.relationships["children"].append(self)

    def add_sibling(self, sibling):
        self.relationships["siblings"].append(sibling)
        sibling.relationships["siblings"].append(self)

    def to_json(self):
        """Returns the JSON representation of the person."""
        return {
            "id": self.id,
            "data": {
                "first name": self.name.split()[0],  # First name
                "last name": " ".join(self.name.split()[1:]),  # Last name
                "birthday": self.birthDate.strftime("%Y") if self.birthDate else None,  # Year of birth
                "avatar": "https://static8.depositphotos.com/1009634/988/v/950/depositphotos_9883921-stock-illustration-no-user-profile-picture.jpg",  # Placeholder avatar
                "gender": self.gender if self.gender else ("M" if self.name[-1] != 'a' else "F")  # Use provided gender, default based on name
            },
            "rels": {
                "spouses": [self.relationships["spouse"].id] if self.relationships["spouse"] else [],
                "father": self.relationships["parents"][0].id if self.relationships["parents"] else None,
                "mother": self.relationships["parents"][1].id if len(self.relationships["parents"]) > 1 else None,
                "children": [child.id for child in self.relationships["children"]]
            }
        }

class FamilyTree:
    def __init__(self):
        self.members = []  # List to store all family members

    def add_member(self, person):
        self.members.append(person)
        
    def get_sorted_members_by_age(self):
        return sorted(self.members, key=lambda p: p.birthDate)  # Oldest to youngest
        
def parse_family_tree(file_path):
    family_tree = FamilyTree()
    with open(file_path, "r") as file:
        lines = file.readlines()

    num_people = int(lines[0].strip())  # First line gives the number of people
    idx = 1
    people = {}  # Temporary storage to resolve relationships by name

    while idx < len(lines):
        if not lines[idx].strip():  # Skip empty lines
            idx += 1
            continue
        
        # Parse a single person's data
        name = lines[idx].split(": ")[1].strip()
        birth_date = lines[idx + 1].split(": ")[1].strip()
        death_date = lines[idx + 2].split(": ")[1].strip()
        gender = lines[idx + 3].split(": ")[1].strip()  # Read gender
        parents = lines[idx + 4].split(": ")[1].strip().split(", ")
        spouse = lines[idx + 5].split(": ")[1].strip()
        children = lines[idx + 6].split(": ")[1].strip().split(", ") if lines[idx + 6].split(": ")[1].strip() != "None" else []

        # Create a Person object
        death_date = None if death_date == "NULL" else death_date
        person = Person(name, birth_date, death_date, gender)
        
        # Temporarily store relationships (resolve them later if needed)
        person.temp_parents = parents  # Temporary attribute for unresolved parents
        person.temp_spouse = spouse if spouse != "NULL" else None  # Temporary attribute for spouse
        person.temp_children = children  # Temporary attribute for unresolved children

        # Add to the family tree and people dictionary
        family_tree.add_member(person)
        people[name] = person  # Add to people dictionary by name
        
        idx += 7  # Move to the next person's data

    # Resolve relationships (if needed)
    for person in family_tree.members:
        # Resolve parents
        for parent_name in getattr(person, "temp_parents", []):
            parent = people.get(parent_name)
            if parent:
                person.add_parent(parent)
        # Resolve spouse
        spouse_name = getattr(person, "temp_spouse", None)
        if spouse_name:
            spouse = people.get(spouse_name)
            if spouse:
                person.relationships["spouse"] = spouse
                spouse.relationships["spouse"] = person
        # Resolve children
        for child_name in getattr(person, "temp_children", []):
            child = people.get(child_name)
            if child:
                person.relationships["children"].append(child)
                child.relationships["parents"].append(person)

        # Clean up temporary attributes
        del person.temp_parents
        del person.temp_spouse
        del person.temp_children

    return family_tree

def generate_family_tree_json(family_tree):
    # Generate JSON data for the entire family tree
    return [person.to_json() for person in family_tree.members]

# Parse the family tree from the data file
family_tree = parse_family_tree("data.txt")

# Generate JSON data
family_tree_json = generate_family_tree_json(family_tree)

# Save the JSON data to a file
with open("family_tree.json", "w") as json_file:
    json.dump(family_tree_json, json_file, indent=2)

print("Family tree JSON generated successfully.")
