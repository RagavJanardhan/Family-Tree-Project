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
        if date_str == "Unknown" or date_str == "NULL":
            return None
        year, month, day = map(int, date_str.split("-"))
        return date(year, month, day)

    def calculate_age(self):
        if self.birthDate:
            end_date = self.deathDate if self.deathDate else date.today()
            age = relativedelta(end_date, self.birthDate)
            return {
                "years": age.years,
                "months": age.months,
                "days": age.days
            }
        return None

    def add_parent(self, parent):
        if parent not in self.relationships["parents"]:
            self.relationships["parents"].append(parent)
        if self not in parent.relationships["children"]:
            parent.relationships["children"].append(self)

    def add_sibling(self, sibling):
        if sibling not in self.relationships["siblings"]:
            self.relationships["siblings"].append(sibling)
        if self not in sibling.relationships["siblings"]:
            sibling.relationships["siblings"].append(self)

    def to_json(self):
        age = self.age
        return {
            "id": self.id,
            "data": {
                "first name": self.name.split()[0],  
                "last name": " ".join(self.name.split()[1:]),  
                "birthday": self.birthDate.strftime("%Y-%m-%d") if self.birthDate else "Unknown",  
                "avatar": "https://static8.depositphotos.com/1009634/988/v/950/depositphotos_9883921-stock-illustration-no-user-profile-picture.jpg",  
                "gender": self.gender if self.gender else ("M" if self.name[-1] != 'a' else "F"),  
                "age": f"{age['years']} years, {age['months']} months, {age['days']} days" if age else None  
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
        self.members = []

    def add_member(self, person):
        self.members.append(person)

    def get_sorted_members_by_age(self):
        return sorted(self.members, key=lambda p: p.birthDate)

def parse_family_tree(file_path):
    family_tree = FamilyTree()
    with open(file_path, "r") as file:
        lines = file.readlines()

    num_people = int(lines[0].strip())
    idx = 1
    people = {}

    while idx < len(lines):
        if not lines[idx].strip():
            idx += 1
            continue
        
        name = lines[idx].split(": ")[1].strip()
        birth_date = lines[idx + 1].split(": ")[1].strip()
        death_date = lines[idx + 2].split(": ")[1].strip()
        gender = lines[idx + 3].split(": ")[1].strip()
        parents = lines[idx + 4].split(": ")[1].strip().split(", ")
        spouse = lines[idx + 5].split(": ")[1].strip()
        children = lines[idx + 6].split(": ")[1].strip().split(", ") if lines[idx + 6].split(": ")[1].strip() != "None" else []

        death_date = None if death_date == "NULL" else death_date
        person = Person(name, birth_date, death_date, gender)
        
        person.temp_parents = parents
        person.temp_spouse = spouse if spouse != "NULL" else None
        person.temp_children = children

        family_tree.add_member(person)
        people[name] = person
        
        idx += 7

    for person in family_tree.members:
        # Resolve parents and ensure no duplicates
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

        # Resolve children and ensure no duplicates
        for child_name in getattr(person, "temp_children", []):
            child = people.get(child_name)
            if child:
                if child not in person.relationships["children"]:
                    person.relationships["children"].append(child)
                if person not in child.relationships["parents"]:
                    child.relationships["parents"].append(person)

        # Clean up temporary attributes
        del person.temp_parents
        del person.temp_spouse
        del person.temp_children

    return family_tree

def generate_family_tree_json(family_tree):
    return [person.to_json() for person in family_tree.members]

family_tree = parse_family_tree("data.txt")
family_tree_json = generate_family_tree_json(family_tree)

with open("family_tree.json", "w") as json_file:
    json.dump(family_tree_json, json_file, indent=2)

print("Family tree JSON generated successfully.")
