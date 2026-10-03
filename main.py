import csv
from models import Item, Weapon, Potion, Armor, Inventory

DATA_FILE = "data/items.csv"
VALID_RARITIES = {"common", "rare", "epic", "legendary"}


def create_item(name, item_type, value, rarity):
    if item_type == "Weapon":
        return Weapon(name, value, rarity)
    if item_type == "Potion":
        return Potion(name, value, rarity)
    if item_type == "Armor":
        return Armor(name, value, rarity)
    return Item(name, item_type, value, rarity)


def parse_row(row):
    if len(row) != 4:
        raise ValueError(f"expected 4 fields, got {len(row)}")
    name, item_type, value, rarity = [field.strip() for field in row]
    if not name or not item_type:
        raise ValueError("empty name or type")
    value = int(value)
    if value < 0:
        raise ValueError("negative value")
    if rarity.lower() not in VALID_RARITIES:
        raise ValueError(f"unknown rarity '{rarity}'")
    return create_item(name, item_type.capitalize(), value, rarity.capitalize())


def load_items(path):
    inventory = Inventory()
    skipped = 0
    file = None
    try:
        file = open(path, newline="", encoding="utf-8")
        reader = csv.reader(file)
        next(reader, None)
        for line_no, row in enumerate(reader, start=2):
            try:
                inventory.add_item(parse_row(row))
            except (ValueError, IndexError) as err:
                skipped += 1
                print(f"[WARNING] Line {line_no} skipped ({err}): {row}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
    finally:
        if file:
            file.close()
        print(f"Loading complete: {len(inventory)} valid items, {skipped} corrupt rows skipped.")
    return inventory


def show(items, empty_msg="No items found."):
    if not items:
        print(empty_msg)
    for item in items:
        print(" ", item)


def show_menu():
    print("\n===== RPG INVENTORY ENGINE =====")
    print("1. View all items")
    print("2. Search item by name")
    print("3. Filter by type")
    print("4. Filter by rarity")
    print("5. Total gold value")
    print("6. Unique categories")
    print("7. Items grouped by category")
    print("8. Add item")
    print("9. Remove item")
    print("0. Exit")


def add_item_flow(inventory):
    name = input("Item name: ").strip()
    item_type = input("Type (Weapon/Potion/Armor/Magic): ").strip()
    rarity = input("Rarity (Common/Rare/Epic/Legendary): ").strip()
    try:
        value = input("Gold value: ")
        item = parse_row([name, item_type, value, rarity])
        inventory.add_item(item)
        print(f"Added: {item}")
    except ValueError as err:
        print(f"Could not add item: {err}")


def main():
    inventory = load_items(DATA_FILE)
    if len(inventory) == 0:
        return

    while True:
        show_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            break

        if choice == "1":
            show(inventory.get_items())
        elif choice == "2":
            show(inventory.search_by_name(input("Name keyword: ")))
        elif choice == "3":
            show(inventory.filter_by_type(input("Type: ")))
        elif choice == "4":
            show(inventory.filter_by_rarity(input("Rarity: ")))
        elif choice == "5":
            print(f"Total gold value: {inventory.total_value()}")
        elif choice == "6":
            print("Categories:", ", ".join(sorted(inventory.unique_categories())))
        elif choice == "7":
            for category, items in inventory.group_by_category().items():
                print(f"\n[{category}] ({len(items)})")
                show(items)
        elif choice == "8":
            add_item_flow(inventory)
        elif choice == "9":
            name = input("Item name to remove: ")
            print("Removed." if inventory.remove_item(name) else "Item not found.")
        elif choice == "0":
            break
        else:
            print("Invalid option. Choose 0-9.")
    print("Game saved. Farewell, adventurer!")


if __name__ == "__main__":
    main()