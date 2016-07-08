#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main module.
"""

import json
import os
import vk
import timeout


def main():
    """Parse user info and start the bot."""

    app_id = 5448459
    user_info = "user_info.txt"

    if not can_read_file(user_info):
        return

    login, password = parse_user_info(user_info)
    if (login, password) == (None, None):
        return

    scope = 'Wall'
    lottery_group_names = ['*розыгр*', '*халяв*']

    try:
        api = get_vk_api(app_id, login, password, scope)
    except vk.exceptions.VkAuthError:
        pass


def search_groups(api, names):
    '''Search lottery groups.'''

    res = []

    for name in names:
        res += [gr.get('gid', '-1') for gr in api.groups.search(q=name)[1:]
                if not gr.get('is_closed', 0)]

    return res


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


def can_read_file(file_name):
    """Return True if file exists and read permission is set, either False"""

    if not os.path.isfile(file_name) or not os.access(file_name, os.R_OK):
        return False

    return True


def get_vk_api(app_id, user_login, user_password, scope):
    """Return vk api."""

    while True:
        try:
            print("Try to connect to the vk.")
            return connect_to_vk(app_id, user_login, user_password, scope)
        except timeout.TimeoutError:
            continue


@timeout.timeout(20)
def connect_to_vk(app_id, user_login, user_password, scope):
    """Return the vk api."""

    session = vk.AuthSession(app_id, user_login, user_password, scope)
    return vk.API(session)

if __name__ == '__main__':
    main()
