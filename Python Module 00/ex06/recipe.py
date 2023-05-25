cookbook = {
    "Sandwich": {
        "ingredients": ["ham", "bread", "cheese", "tomatoes"],
        "meal": "lunch",
        "prep_time": 10
    },
    "Cake": {
        "ingredients": ["flour", "sugar", "eggs"],
        "meal": "dessert",
        "prep_time": 60
    },
    "Salad": {
        "ingredients": ["avocado", "arugula", "tomatoes", "spinach"],
        "meal": "lunch",
        "prep_time": 15
    }
}

def print_recipe_names():
    print("Recipe names:")
    for recipe_name in cookbook.keys():
        print("- " + recipe_name)

def print_recipe_details(recipe_name):
    if recipe_name in cookbook:
        print("Recipe for " + recipe_name + ":")
        print("Ingredients list: " + str(cookbook[recipe_name]["ingredients"]))
        print("To be eaten for " + cookbook[recipe_name]["meal"] + ".")
        print("Takes " + str(cookbook[recipe_name]["prep_time"]) + " minutes of preparation.")
    else:
        print("Recipe not found.")

def delete_recipe(recipe_name):
    if recipe_name in cookbook:
        del cookbook[recipe_name]
        print("Recipe " + recipe_name + " deleted.")
    else:
        print("Recipe not added. Please provide at least one ingredient.")

def add_recipe():
    recipe_name = input("Enter a name: ")
    ingredients = input("Enter ingredients (separated by commas): ").split(",")
    meal = input("Enter a meal type: ")
    prep_time = int(input("Enter a preparation time (in minutes): "))
    recipe = {
        "ingredients": ingredients,
        "meal": meal,
        "prep_time": prep_time
    }
    cookbook[recipe_name] = recipe
    print("Recipe " + recipe_name + " added.")

def print_cookbook():
    print("Cookbook:")
    for recipe_name, recipe in cookbook.items():
        print("Recipe: " + recipe_name)
        print("Ingredients list: " + str(recipe["ingredients"]))
        print("To be eaten for " + recipe["meal"] + ".")
        print("Takes " + str(recipe["prep_time"]) + " minutes of preparation.")

def cookbook_program():
    print("Welcome to the Python Cookbook!")
    while True:
        print("List of available options:")
        print("1: Add a recipe")
        print("2: Delete a recipe")
        print("3: Print a recipe")
        print("4: Print the cookbook")
        print("5: Quit")
        choice = input("Please select an option: ")
        if choice == "1":
            add_recipe()
        elif choice == "2":
            recipe_name = input("Please enter a recipe name to delete: ")
            delete_recipe(recipe_name)
        elif choice == "3":
            recipe_name = input("Please enter a recipe name to print: ")
            print_recipe_details(recipe_name)
        elif choice == "4":
            print_cookbook()
        elif choice == "5":
            print("Cookbook closed. Goodbye!")
            break
        else:
            print("Sorry, this option does not exist.")

cookbook_program()
