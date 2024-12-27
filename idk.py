from datetime import date
from dateutil.relativedelta import relativedelta

# A node class created to store various attributes for each node (person) in the family tree
class Person:
    def __init__(self, name, birthDate, deathDate=None):
        self.name = name
        self.birthDate = self.parse_date(birthDate)
        self.deathDate = self.parse_date(deathDate) if deathDate else None
        self.relationships = {"parents": [], "children": [], "spouse": None, "siblings": []}
        self.age = self.calculate_age()  # Automatically calculate age

    @staticmethod
    def parse_date(date_str):
        """
        Parses a date string in 'YYYY MM DD' format and returns a date object.
        """
        year, month, day = map(int, date_str.split(" "))
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
    while idx < len(lines):
        if not lines[idx].strip():  # Skip empty lines
            idx += 1
            continue
        
        # Parse a single person's data
        name = lines[idx].split(": ")[1].strip()
        birth_date = lines[idx + 1].split(": ")[1].strip()
        death_date = lines[idx + 2].split(": ")[1].strip()
        parents = lines[idx + 3].split(": ")[1].strip().split(", ")
        num_children = int(lines[idx + 4].split(": ")[1].strip())

        # Create a Person object
        death_date = None if death_date == "ALIVE" else death_date
        person = Person(name, birth_date, death_date)
        
        # Temporarily store relationships (resolve them later if needed)
        person.temp_parents = parents  # Temporary attribute for unresolved parents
        person.num_children = num_children

        # Add to the family tree
        family_tree.add_member(person)
        idx += 5  # Move to the next person's data

    # Resolve relationships (if needed)
    for person in family_tree.members:
        for parent_name in getattr(person, "temp_parents", []):
            parent = next((p for p in family_tree.members if p.name == parent_name), None)
            if parent:
                person.add_parent(parent)
        del person.temp_parents  # Remove temporary attribute

    return family_tree

family_tree = parse_family_tree("data.txt")
for member in family_tree.members:
    print(f"{member.name}: Age = {member.age}, Parents = {[p.name for p in member.relationships['parents']]}")
