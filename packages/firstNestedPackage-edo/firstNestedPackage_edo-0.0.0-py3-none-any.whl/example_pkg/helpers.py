# Title     : Helpers
# Objective : Functions for supporting all the modules and packages
# Created by: Janid
# Created on: 4/6/20


def greetings(str_1, str_2, str_3, person, str_4):
    """ Prints: Hello Worlds to "name" !!!

    Parameters
    ----------
    str_1   : str
    str_2   : str
    str_3   : str
    person  : str
    str_4   : str



    """
    if person:
        print("{} {} {} {} {}".format(str_1, str_2, str_3, person, str_4))
    else:
        print("{} {} {} nobuddy {}".format(str_1, str_2, str_3, str_4))


