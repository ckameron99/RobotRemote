def turn(list_of_instructions):
    """ Function which is called whenever turn is mentioned in the speech command which analyses text and
    sends the command to the robot or instructions to the user whenever speech isnt transcribed correctly or
    incorrect information is given
    :param list_of_instructions: A list of strings containing all the text analysed by Deepspeech
    :return command: A command for the robot to follow or instruction to the user
    """

    directions = {"left": -1, "right": 1, "around": 1}
    degrees = {"five": 5, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40,
               "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "around": 180}

    direction = sum(directions.get(word, 0) for word in list_of_instructions)
    degree = sum(degrees.get(word, 0) for word in list_of_instructions)
    if abs(direction) != 1:
        return "display", "Invalid Command: No clear direction presented"
    if degree == 0:
        return "display", "Invalid Command: No clear bearing presented"
    else:
        bearing = direction * degree
        return "command", ["turn", bearing]


def move(list_of_instructions):
    directions = {"back": -1, "forward": 1}
    amount = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
              "eight": 8, "nine": 9, "ten": 10, "twenty": 20}

    direction = sum(directions.get(word, 0) for word in list_of_instructions)
    distance = sum(amount.get(word, 0) for word in list_of_instructions)
    if abs(direction) != 1:
        return "display", "Invalid Command: No clear direction presented"
    if distance == 0:
        return "display", "Invalid Command: No Distance Specified"
    else:
        translate = direction * distance
        return "command", ["move", translate]
