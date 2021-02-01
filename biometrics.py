# 291632, Ella Rinnemaa, ella.rinnemaa@tuni.fi

###############################################################################
# read_biometric_registry(filename)                                                     
# =========================================
# Function reads the biometric information from the file whose name is in
# the parameter filename. The read information will be parsed and saved in 
# the data structure that is in the variable called result. The coder has
# to define the data structure by him/herself.
# After successfully reading the file and saving its contents in the data
# structure, the function returns the result. If there's an error, None is
# returned.
#         
# PLEASE NOTE:
# (a) Implement all parts of the code that say TODO.
# (b) The data structure returned by the function must be something that
#     that nests lists and/or dicts. That is the whole point of this project:
#     to use nested data structures.
###############################################################################
import math


def read_biometric_registry(filename):
    result = {}

    handled_passports = []

    try:
        with open(filename, "r") as file_object:
            for row in file_object:
                fields = row.rstrip().split(";")

                if len(fields) != 8:
                    print("Error: there is a wrong number of fields "
                          "in the file:")
                    print("'", row, "'", sep="")
                    return None

                name = fields[0] + ", " + fields[1]
                passport = fields[2]

                if passport in handled_passports:
                    print("Error: passport number", passport,
                          "found multiple times.")
                    return None
                else:
                    handled_passports.append(passport)

                biometrics = []

                for i in range(3, 8):
                    try:
                        id_value = float(fields[i])
                    except ValueError:
                        print("Error: there's a non-numeric value on the row:")
                        print("'", row, "'", sep="")
                        return None

                    if 0 <= id_value <= 3.0:
                        biometrics.append(id_value)
                    else:
                        print(
                            "Error: there is an erroneous value in the file:")
                        print("'", row, "'", sep="")
                        return None

                # Data structure that contains the read information:
                result[name] = {}
                result[name][passport] = biometrics

        return result

    except FileNotFoundError:
        print("Error: file", filename, "could not be opened.")
        return None


###############################################################################
# TODO
###############################################################################
def execute_match(registry):

    global compare_coordinates, main_coordinates, compare_name, matches, a

    new_registry = registry.copy()

    matches_in_registry = {}

    key_list = list(new_registry.keys())

    all_matches = []

    for k in key_list:

        matches = []

        for document in new_registry[k]:
            main_coordinates = new_registry[k][document]
        del new_registry[k]

        for compare_name in new_registry:
            for compare_id in new_registry[compare_name]:
                compare_coordinates = \
                    new_registry[compare_name][compare_id]

            distance = euclidean_distance(compare_coordinates,
                                          main_coordinates)

            if distance < 0.1 and compare_name not in all_matches:
                matches.append(compare_name)
                all_matches.append(compare_name)
                if len(matches) != 0:
                    matches_in_registry[k] = matches

    if len(matches_in_registry) == 0:
        print("No matching persons were found.")
        return True
    else:
        print_matches(matches_in_registry, registry)
        return True


def print_matches(match_dict, registry):

    for name in match_dict:
        print("Probably the same person:")
        print(name, "".join(registry[name]), sep=";", end=";")

        for values in registry[name]:
            coordinates = registry[name][values]
            for i in coordinates[0:4]:
                print("{:.2f}".format(i), end=";")
            print("{:.2f}".format(coordinates[4]))

        matches = match_dict[name]

        for same_person in matches:
            print(same_person, "".join(registry[same_person]), sep=";", end=";")

            for values in registry[same_person]:
                coordinates = registry[same_person][values]
                for i in coordinates[0:4]:
                    print("{:.2f}".format(i), end=";")
                print(coordinates[4])
        print()

    return
###############################################################################
# TODO
###############################################################################
def execute_search(registry):
    global points

    suspects = []

    input_incorrect = True

    while input_incorrect:

        points = input("enter 5 measurement points separated by semicolon: ") \
            .split(";")

        if len(points) != 5:
            print("Error: wrong number of measurements. Try again.")

            input_incorrect = True

        else:
            input_incorrect = False

        while not input_incorrect:

            try:
                for point in points:
                    input_point = float(point)
            except ValueError:
                print("Error: enter floats only. Try again.")
                input_incorrect = True
            else:
                break

    for name in registry:
        for id_document in registry[name]:
            coordinates = registry[name][id_document]

            distance = euclidean_distance(points, coordinates)

            if distance < 0.1:
                suspects.append(name)

    if len(suspects) == 0:
        print("No suspects were found.")
        print()
        return True

    else:
        print_suspects(suspects, registry)
        return True


def print_suspects(suspects, registry):
    print("Suspects found:")

    for name in suspects:

        print(name, "".join(registry[name]), sep=";", end=";")

        for values in registry[name]:
            coordinates = registry[name][values]
            for i in coordinates[0:4]:
                print("{:.2f}".format(i), end=";")
            print("{:.2f}".format(coordinates[4]))
    print()

    return


def euclidean_distance(list1, list2):
    difference_between_points = 0.0

    i = 0

    while i <= 4:
        difference_between_points += ((float(list1[i]) -
                                       float(list2[i])) ** 2)
        i += 1
    distance = math.sqrt(difference_between_points)

    return distance


###############################################################################
# command_line_user_interface
# Very simple user interface. It might be good to add some helper functions.
#                                                                             
###############################################################################
def command_line_user_interface(registry):
    while True:
        command = input("command [search/match/<enter>] ")
        if command == "":
            return
        elif command == "match":
            execute_match(registry)
        elif command == "search":
            execute_search(registry)
        else:
            print("Error: unknown command '", command,
                  "': try again.", sep="")


###############################################################################
# main()                                                                      #
# ======                                                                      #
# Main program for the project. You're not supposed to edit this.
#
###############################################################################
def main():
    registry_file = input("Enter the name of the registry file: ")

    biometric_registry = read_biometric_registry(registry_file)
    if biometric_registry is not None:
        command_line_user_interface(biometric_registry)


main()
