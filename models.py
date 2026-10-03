class Item:
    def __init__(self, name, item_type, value, rarity):
        self.name = name
        self.item_type = item_type
        self.value = int(value)
        self.rarity = rarity

    def describe(self):
        return (f"{self.name:<20} | {self.item_type:<7} | "
                f"{self.value:>5} gold | {self.rarity}")

    def __str__(self):
        return self.describe()


class Weapon(Item):
    def __init__(self, name, value, rarity):
        super().__init__(name, "Weapon", value, rarity)
        self.attack_power = self.value // 10

    def describe(self):
        return super().describe() + f" | ATK +{self.attack_power}"


class Potion(Item):
    def __init__(self, name, value, rarity):
        super().__init__(name, "Potion", value, rarity)
        self.heal_amount = self.value * 2

    def describe(self):
        return super().describe() + f" | HEAL +{self.heal_amount}"


class Armor(Item):
    def __init__(self, name, value, rarity):
        super().__init__(name, "Armor", value, rarity)
        self.defense_rating = self.value // 8

    def describe(self):
        return super().describe() + f" | DEF +{self.defense_rating}"


class Inventory:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def remove_item(self, name):
        for item in self._items:
            if item.name.lower() == name.strip().lower():
                self._items.remove(item)
                return True
        return False

    def search_by_name(self, keyword):
        keyword = keyword.strip().lower()
        return [i for i in self._items if keyword in i.name.lower()]

    def filter_by_type(self, item_type):
        return [i for i in self._items if i.item_type.lower() == item_type.strip().lower()]

    def filter_by_rarity(self, rarity):
        return [i for i in self._items if i.rarity.lower() == rarity.strip().lower()]

    def total_value(self):
        return sum(i.value for i in self._items)

    def unique_categories(self):
        return {i.item_type for i in self._items}

    def group_by_category(self):
        groups = {}
        for item in self._items:
            groups.setdefault(item.item_type, []).append(item)
        return groups

    def get_items(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)