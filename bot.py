#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main module.
"""

import json
import os

def main():
    """Parse user info and start the bot."""

    user_info = "user_info.txt"

    if not check_user_info_file(user_info):
        return

    login, password = parse_user_info(user_info)
    if (login, password) == (None, None):
        return

def parse_user_info(user_info_file):
    """
    Return (user_login, user_password)
    Return (None, None) if user info file format is wrong
    """

    try:
        with open(user_info_file) as f:
            user = json.load(f)

            if not isinstance(user, list) or len(user) != 2:
                return (None, None)

            return (user[0], user[1])

    except ValueError:
        print("Incorrect user info file format.")
        return (None, None)

def check_user_info_file(file_name):
    """Return True if file exists and read permission is set, either False"""

    if not os.path.isfile(file_name):
        print("File", file_name, "doesn't exist.")
        return False

    if not os.access(file_name, os.R_OK):
        print("Haven't permission to read", file_name)
        return False

    return True


if __name__ == '__main__':
    main()
