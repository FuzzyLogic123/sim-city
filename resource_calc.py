from datetime import datetime, timedelta
from math import ceil
import os
import subprocess

recipes = {
    "metal": {
        "time": 60,
        "store": "factory"
    },
    "wood": {
        "time": 3 * 60,
        "store": "factory"
    },
    "plastic": {
        "time": 9*60,
        "store": "factory"
    },
    "textiles": {
        "time": 3*60*60,
        "store": "factory"
    },
    "sugar_and_spices": {
        "time": 4*60*60,
        "store": "factory"
    },
    "glass": {
        "time": 5*60*60,
        "store": "factory"
    },
    "seeds": {
        "time": 20*60,
        "store": "factory"
    },
    "animal_feed": {
        "time": 6*60*60,
        "store": "factory"
    },
    "minerals": {
        "time": 30*60,
        "store": "factory"
    },
    "chemicals": {
        "time": 2*60*60,
        "store": "factory"
    },
    "nails": {
        "time": 4*60 + 30,
        "store": "building_supplies_store",
        "materials": {
            "metal": 2
        }
    },
    "planks": {
        "time": 27*60,
        "store": "building_supplies_store",
        "materials": {
            "wood": 2
        },
    },
    "bricks": {
        "time": 18*60,
        "store": "building_supplies_store",
        "materials": {
            "minerals": 2,
        },
    },
    "cement": {
        "time": 45*60,
        "store": "building_supplies_store",
        "materials": {
            "minerals": 2,
            "chemicals": 1
        },
    },
    "glue": {
        "time": 54 * 60,
        "store": "building_supplies_store",
        "materials": {
            "plastic": 1,
            "chemicals": 2
        }
    },
    "paint": {
        "time": 54 * 60,
        "store": "building_supplies_store",
        "materials": {
            "metal": 2,
            "chemicals": 2,
            "minerals": 1
        }
    },
    "chairs": {
        "time": 20 * 60,
        "store": "furniture_store",
        "materials": {
            "wood": 2,
            "nails": 1,
            "hammer": 1
        }
    },
    "tables": {
        "time": 30 * 60,
        "store": "furniture_store",
        "materials": {
            "planks": 1,
            "nails": 2,
            "hammer": 1
        }
    },
    "home_textiles": {
        "time": 1*60*60 + 15*60,
        "store": "furniture_store",
        "materials": {
            "textiles": 2,
            "measuring_tape": 1
        }
    },
    "vegetables": {
        "time": 18 * 60,
        "store": "farmer's_market",
        "materials": {
            "seeds": 2
        }
    },
    "flour_bag": {
        "time": 27 * 60,
        "store": "farmer's_market",
        "materials": {
            "seeds": 2,
            "textiles": 2
        }
    },
    "fruit_and_berries": {
        "time": 1 * 60 * 60 + 21 * 60,
        "store": "farmer's_market",
        "materials": {
            "seeds": 2,
            "tree_saplings": 1
        }
    },
    "cream": {
        "time": 1 * 60 * 60 + 7 * 60,
        "store": "farmer's_market",
        "materials": {
            "animal_feed": 1
        }
    },
    "corn": {
        "time": 54 * 60,
        "store": "farmer's_market",
        "materials": {
            "minerals": 1,
            "seeds": 4
        }
    },
    "cap": {
        "time": 1 * 60 * 60,
        "store": "fashion_store",
        "materials": {
            "textiles": 2,
            "measuring_tape": 1
        }
    },
    "shoes": {
        "time": 1 * 60 * 60 + 15 * 60,
        "store": "fashion_store",
        "materials": {
            "textiles": 2,
            "plastic": 1,
            "glue": 1
        }
    },
    "watch": {
        "time": 1 * 60 * 60 + 30 * 60,
        "store": "fashion_store",
        "materials": {
            "plastic": 2,
            "glass": 1,
            "chemicals": 1
        }
    },
    "grass": {
        "time": 30 * 60,
        "store": "gardening_supplies",
        "materials": {
            "seeds": 1,
            "shovel": 1
        }
    },
    "tree_saplings": {
        "time": 1 * 60 * 60 + 30 * 60,
        "store": "gardening_supplies",
        "materials": {
            "seeds": 2,
            "shovel": 1
        }
    },
    "garden_furniture": {
        "time": 2 * 60 * 60 + 15 * 60,
        "store": "gardening_supplies",
        "materials": {
            "planks": 2,
            "plastic": 2,
            "textiles": 2
        }
    },
    "donuts": {
        "time": 45 * 60,
        "store": "donut_shop",
        "materials": {
            "sugar_and_spices": 1,
            "flour_bag": 1
        }
    },
    "green_smoothie": {
        "time": 30 * 60,
        "store": "donut_shop",
        "materials": {
            "fruit_and_berries": 1,
            "vegetables": 1
        }
    },
    "bread_roll": {
        "time": 1 * 60 * 60,
        "store": "donut_shop",
        "materials": {
            "flour_bag": 2,
            "cream": 1
        }
    },
    "hammer": {
        "time": 12 * 60 + 36,
        "store": "hardware_store",
        "materials": {
            "metal": 1,
            "wood": 1
        }
    },
    "measuring_tape": {
        "time": 18 * 60,
        "store": "hardware_store",
        "materials": {
            "metal": 1,
            "plastic": 1
        }
    },
    "shovel": {
        "time": 27 * 60,
        "store": "hardware_store",
        "materials": {
            "metal": 1,
            "wood": 1,
            "plastic": 1
        }
    },
    "cooking_utencils": {
        "time": 40 * 60 + 30,
        "store": "hardware_store",
        "materials": {
            "metal": 2,
            "plastic": 2,
            "wood": 2
        }
    },
    "ladder": {
        "time": 54 * 60,
        "store": "hardware_store",
        "materials": {
            "planks": 2,
            "metal": 2
        }
    },
    "ice_cream_sandwich": {
        "time": 14 * 60,
        "store": "fast_food_restaurant",
        "materials": {
            "cream": 1,
            "bread_roll": 1
        }
    },
}

store_slots = {
    "factory": 40,
    "building_supplies_store": 4,
    "furniture_store": 3,
    "farmer's_market": 4,
    "fashion_store": 2,
    "gardening_supplies": 3,
    "donut_shop": 3,
    "hardware_store": 4,
    "fast_food_restaurant": 2
}

resources_dict = {}


def update_dict(resource, resources_dict):
    if resource and resource in resources_dict:
        resources_dict[resource] += 1
    else:
        resources_dict[resource] = 1


def get_resources(resource):
    update_dict(resource, resources_dict)
    if not recipes[resource].get("materials"):
        return resource
    materials_needed = recipes[resource]["materials"]
    for material in materials_needed:
        material_count = materials_needed[material]
        for _ in range(material_count):
            get_resources(material)


def check_for_required_resources(resource, resources_sorted, inventory):
    resources_sorted = [e for e in resources_sorted if type(e) is list]
    if not recipes[resource].get('materials'):
        return True
    for element in recipes[resource]['materials']:
        # check the amount of each element that we have by iterating over resources_sorted
        # if the number of a certain material that is required is less than the resources currently made, return false. This includes if 0 have been made.
        if not inventory.get(element) or recipes[resource]["materials"][element] > inventory[element]:
            return False
    return True


def sec_to_hours(seconds):
    hours = (seconds//3600)
    minutes = ((seconds % 3600)//60)
    seconds = str((seconds % 3600) % 60)
    return f'{hours} hours {minutes} mins {seconds} seconds' if hours > 0 else f'{minutes} mins {seconds} seconds'


def update_inventory(resource, count, inventory, new_inventory):
    if not inventory.get(resource):
        new_inventory[resource] = count
    else:
        new_inventory[resource] += count
    if recipes[resource]["store"] != 'factory':
        for used_resource in recipes[resource]["materials"]:
            if inventory.get(used_resource):
                inventory[used_resource] -= recipes[resource]["materials"][used_resource] * count


def print_to_user(resources_sorted):
    print_statement = ''
    wait_time_list = [
        wait_time for wait_time in resources_sorted if type(wait_time) is int]
    total_wait_time = sum(
        wait_time_list)
    print_statement += f'\nThe total wait time is {sec_to_hours(total_wait_time)}\n'
    print_statement += f'This could optimally be finished at {(datetime.now() + timedelta( minutes=( ceil(total_wait_time / 60)) ) ).strftime("%I:%M %p")}\n'
    print_statement += f'This will require {len(wait_time_list)} visits\n\n'
    next_check_in = datetime.now()
    for resource in resources_sorted:
        if type(resource) is int:
            next_check_in += timedelta(minutes=(ceil(resource / 60)))
            print_statement += f'\nwait {sec_to_hours(resource)}...\n'
            print_statement += f'Check back in at {next_check_in.strftime("%I:%M %p")}\n\n'
        else:
            print_statement += f'{resource[1]} {resource[0]}\n'
    print(print_statement)
    return print_statement


resources_needed_input = input('What resources do you need?\n').split(' ')
# resources_needed_input = 'shovel:1 planks:2 bricks:1 measuring_tape:1 textiles:1 plastic:1 nails:2 metal:2 home_textiles:1 measuring_tape:1 metal:1 green_smoothie:1 minerals:1 nails:1 cooking_utencils:1 seeds:1\n'

for resource in resources_needed_input:
    for _ in range(int(resource.split(':')[1])):
        get_resources(resource.split(':')[0])

resources_sorted = []
inventory = {}
while resources_dict:
    new_inventory = inventory.copy()
    store_slots_copy = store_slots.copy()
    candidates = []
    resources_list = list(resources_dict.items())
    resources_list.sort(
        reverse=True, key=lambda resource_tuple: recipes[resource_tuple[0]]["time"])
    for resource in resources_list:
        resource = resource[0]
        store = recipes[resource]["store"]
        if check_for_required_resources(resource, resources_sorted, inventory):
            # indexes count per store for the store that the resource belongs to
            if store_slots_copy[store] >= resources_dict[resource]:
                update_inventory(
                    resource, resources_dict[resource], inventory, new_inventory)
                store_slots_copy[store] -= resources_dict[resource]
                candidates.append([resource, resources_dict[resource]])
                resources_dict.pop(resource)
            # if the number of items listed is greater than the number of slots available do what you can and then skip that item
            elif store_slots_copy[store] > 0:
                update_inventory(
                    resource, store_slots_copy[store], inventory, new_inventory)
                candidates.append([resource, store_slots_copy[store]])
                resources_dict[resource] -= store_slots_copy[store]
                store_slots_copy[store] = 0
    candidates.sort(
        reverse=True, key=lambda resource: recipes[resource[0]]["time"])
    resources_sorted += candidates
    # appends the wait time, this is the item that will take the longest to make
    time_per_store = {}
    for candidate in candidates:
        if recipes[candidate[0]]["store"] == "factory":
            if not time_per_store.get("factory") or time_per_store["factory"] < recipes[candidate[0]]["time"]:
                time_per_store["factory"] = recipes[candidate[0]]["time"]
        else:
            if not time_per_store.get(recipes[candidate[0]]["store"]):
                time_per_store[recipes[candidate[0]]["store"]
                            ] = recipes[candidate[0]]["time"] * candidate[1]
            else:
                time_per_store[recipes[candidate[0]]["store"]
                            ] += recipes[candidate[0]]["time"] * candidate[1]
    # appending the max value from the dictionary
    resources_sorted.append(max(time_per_store.values()))
    # adding the new inventory to the old inventory
    inventory = {key: inventory.get(key, 0) + new_inventory.get(key, 0)
                 for key in set(inventory) | set(new_inventory)}

final_solution = print_to_user(resources_sorted)
subprocess.run("pbcopy", universal_newlines=True, input=final_solution)

os.system('open /System/Applications/Notes.app')