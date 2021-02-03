# python3
# generate_test_messages.py

from datetime import datetime, timedelta


seconds_interval = 15
start_location = 0
destination = 0
item_id = ""
label_required = ""
intro_message = """
This program is designed to emulate scans along a conveyor.
\nIt has been scrubbed of details almost to the point of being useless, but I wanted so save off some of the logic.
\nThis is designed to be part of a suite of message generating/testing software. Depending on the parameters you give 
it, it might expect you to "send" some details to another tool, which would give you a message in response.
\nFor the sake of keeping this simple, if it asks you what was "returned" just put in whatever string you want 
("test" would be perfectly fine).
"""

print(intro_message)

while True:
    print("Enter a starting scanner between 1-50 (Normal) or 1000-1010 (Special cases).")
    try:
        start_location = int(input(">"))
    except ValueError:
        continue
    if not ((1 <= start_location <= 50)
            or (1000 <= start_location <= 1010)):
        print("%s is not a valid scanner." % start_location)
    else:
        break


def get_updated_datetime():
    """
    Adds 15 seconds to the seconds_interval variable
    (mimicking the conveyor travel time between scans)
    """

    global seconds_interval
    updated_datetime = datetime.now() + timedelta(seconds=seconds_interval)
    seconds_interval += 15
    return updated_datetime.strftime("%y%m%d%H%M%S")


def scan_item():
    """
    Message for when an item is scanned
    """

    print(r"[Initial Scan] Timestamp: %s, Start Location: %s, Item ID: %s"
          % (get_updated_datetime(), start_location, item_id))
    print()


def move_item(scanner, lane):
    """
    Message for when an item is moved
    """

    print(r"[Item Moved] Timestamp: %s, Scanner: %s, Item ID: %s, Action: %s"
          % (get_updated_datetime(), scanner, item_id, lane))


def get_item_id():
    """
    For scanners 1000-1010:
    After sending the initial scan message, you will receive a response
    You will receive an item_id as part of the response

    For scanners 1-50:
    This tests putting an existing item back into the main area
    """
    while True:
        global item_id
        try:
            if start_location >= 1000:
                print("Send these details to [OTHER TEST SIMULATION]")
                item_input = input(
                    "Which item appeared in the response message? (e.g. 'box001')\n>")
            else:
                item_input = input("Enter an item_id:\n>")
        except ValueError:
            print("Enter an item_id")
            continue
        item_id = item_input
        break


def get_destination():
    """
    Testing suite will tell you which destination to use

    Each scanner has 2 locations, so scanner 1 has zones 1 and 2
    scanner 2 has zones 3 and 4, etc

    Scanners 1000-1010 will need to route through all zones (1 -> destination)
    Others will only route from initial scanner to destination
    """
    start = 1 if start_location >= 1000 else (start_location * 2 - 1)
    while True:
        global destination
        print("Enter a destination zone between %s-100" % start)
        try:
            destination_input = int(input(">"))
            if not start <= destination_input <= 100:
                continue
            if destination_input < start_location <= 100:
                print("Destination cannot be before the start zone")
                continue
        except ValueError:
            continue
        destination = destination_input
        break


def get_label_required():
    """
    Whether or not this item needs a label applied to it
    """
    while True:
        global label_required
        try:
            label_input = input("Does this need a Hazardous Materials label? (y/n)\n>")
            if label_input.lower() != 'y' and label_input.lower() != 'n':
                print("Enter 'y' or 'n'")
                continue
        except ValueError:
            print("Enter 'y' or 'n'")
            continue
        label_required = 'label required' if label_input == 'y' else None
        break


def create_new_item():
    """
    Receive a new item ready to be assigned to an order
    """
    global item_id
    item_id = "new item"
    scan_item()


def assign_order_to_new_item():
    """
    Assign order details to the item
    """
    get_item_id()
    get_destination()
    get_label_required()


def continue_to_pick_zones():
    """
    Reset "start scanner" to  zone 1 scanner
    """
    global start_location
    start_location = 1


def start_at_pick_zones():
    """
    Starting the test in the pick zones
    """
    global item_id
    global destination
    get_item_id()
    get_destination()


# Scanners for assembling new items
if 1000 <= start_location <= 1010:
    create_new_item()
    assign_order_to_new_item()
    move_item(start_location, label_required)
    continue_to_pick_zones()

# Scanners for existing items
else:
    start_at_pick_zones()

# Navigate to the destination
for i in range(start_location, destination + 1):
    if i < destination / 2:
        move_item(i, '<Continue down the conveyor>')
    else:
        move_item(i, "<Diverted into lane: " + str(destination) + ">")
        break

# Prevent program from automatically closing
input("Press enter to quit...")
