# Dictionary basics

person = {
    "name": "Alice",
    "age": 25,
    "city": "London"
}

print(person)

# Accessing values
print(person["name"])

# Using get() method
print(person.get("name"))
print(person.get("email", "Not found"))

# Adding a new key-value pair
person["job"] = "Developer"
print(person)

# Updating a value
person["age"] = 26
print(person)
