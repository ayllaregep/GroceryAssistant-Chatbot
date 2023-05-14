import random
import myutils as extra

class GroceryAssistant:
    def __init__(self):
        self.greetings = ["Hello!", "Hi there!", "Hey!", "Welcome!"]

    def process_message(self, message, shopping_list, temp_data, current_state, session):
        response = ""
        new_state = current_state
        if new_state == "INIT":
            new_state = "IDLE"
            response = "Bot: I just woke up what do you want?"
        elif new_state == "ADDING_ITEMS":
            response, new_state = self.add_item(message, shopping_list, session)
        elif new_state == "DELETING_ITEMS":
            response, new_state = self.delete_item(message, shopping_list, session)
        elif new_state == "FIND_STORES":
            response, new_state = self.find_stores(message, session)
        elif new_state == "SHOULD_ADD":
            response, new_state = self.add_to_list(message, shopping_list, temp_data, session)
        elif new_state == "CHECK_ITEM":
            response, new_state = self.check_item(message, shopping_list)
        else:
            response, new_state = self.process_command(message, shopping_list, temp_data, session)

        session['current_state'] = new_state
        session.modified = True

        return response

    def process_command(self, message, shopping_list, temp_data, session):
        if message == "menu":
            return self.show_menu(), "IDLE"
        elif message == "1":
            return self.display_list(shopping_list), "IDLE"
        elif message == "2":
            return "Bot: Waiting for your items (type 'done' when you finished adding items)", "ADDING_ITEMS"
        elif message == "3":
            return "Bot: What items should I delete? (type 'done' when you finished deleting items)", "DELETING_ITEMS"
        elif message == "4":
            return "Bot: What range should the shop be?(km)", "FIND_STORES"
        elif message == "5":
            return self.suggest_recipe(shopping_list, session)
        elif message == "6":
            return self.count_items(shopping_list), "IDLE"
        elif message == "7":
            return "Bot: What item do you want to check?", "CHECK_ITEM"
        elif message == "8":
            return self.clear_list(shopping_list, session), "IDLE"
        elif message == "9":
            return self.export_list(shopping_list), "IDLE"
        else:
            return "Bot: Invalid command. Please enter a valid command from the menu.", "IDLE"

    def greet(self):
        return random.choice(self.greetings)

    def show_menu(self):
        menu = f'''
----------------MENU BOT-------------
1. Display shopping list
2. Add products to list
3. Delete products from list
4. Find nearby stores
5. Suggest a recipe
6. Count items in list
7. Check if an item exists in the list
8. Clear shopping list
9. Export list to JSON and download'''
        return menu

    def display_list(self, shopping_list):
        if not shopping_list:
            return "Bot: Your shopping list is empty."
        else:
            response = "Bot: Your shopping list:<br>"
            for item in shopping_list:
                response += f"- {item}<br>"
            return response

    def add_item(self, message, shopping_list, session):
        if message.lower() == 'done':
            return 'Bot: I finished adding your items',"IDLE"
        else:
            shopping_list.append(message.lower())
            session['shopping_list'] = shopping_list
            return f"'Bot: {message}' added to your shopping list.", "ADDING_ITEMS"

    def delete_item(self, message, shopping_list, session):
        if message.lower() == 'done':
            return 'Bot: I finished deleting your items',"IDLE"
        else:
            if message in shopping_list:
                shopping_list.remove(message.lower())
                session['shopping_list'] = shopping_list
                return f"'Bot: {message}' removed from your shopping list.", "DELETING_ITEMS"
            else:
                return f"'Bot: {message}' not found.", "DELETING_ITEMS"

    def find_stores(self, message, session):
        if 'user_location' not in session:
            return "Bot: User location is not available.", "IDLE"

        user_location = (session['user_location']['lat'], session['user_location']['lng'])
        search_radius = int(message) * 1000

        nearby_stores = extra.get_nearby_stores(user_location, search_radius)

        if not nearby_stores:
            return "Bot: No grocery stores found nearby.", "IDLE"

        response = "Bot: I found these nearby stores:<br>"
        for store_name, store_address in nearby_stores:
            response += f"{store_name}: {store_address}<br>"
        return response, "IDLE"

    def suggest_recipe(self, shopping_list, session):
        recipe_title, ingredients = extra.get_recipe_by_keyword(shopping_list)

        if not recipe_title or not ingredients:
            return "Bot: I couldn't find any recipe for you.", "IDLE"

        newTemp = []
        response = f"Bot: I found a recipe for you:<br>{recipe_title}<br>"
        for ingredient in ingredients:
            response += f"- {ingredient}<br>"
            newTemp.append(ingredient)
        session['temp_data'] = newTemp
        response += "Do you want them added to your list?(Yes/No)"
        return response, "SHOULD_ADD"

    def count_items(self, shopping_list):
        return f"Bot: Total items in the shopping list: {len(shopping_list)}"

    def check_item(self, message, shopping_list):
        if message in shopping_list:
            return f"'Bot: {message}' is already in your shopping list.", "IDLE"
        else:
            return f"'Bot: {message}' is not in your shopping list.", "IDLE"

    def clear_list(self, shopping_list, session):
        shopping_list = []
        session['shopping_list'] = shopping_list
        return "Bot: Your shopping list has been cleared."
    
    def add_to_list(self, message, shopping_list, temp_data, session):
        message = message.lower()
        if message == "no" or message == "nu":
            return "I didn't add anything to your list.", "IDLE"

        for ingredient in temp_data:
            if ingredient not in shopping_list:
                print(f"{ingredient} - should be added")
                shopping_list.append(ingredient)
                print(f"{shopping_list} - after add")
        session['shopping_list'] = shopping_list
        return "We added everything that wasn't on your list already.", "IDLE"


    def export_list(self, shopping_list):
        return shopping_list