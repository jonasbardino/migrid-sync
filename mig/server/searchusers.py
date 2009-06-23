#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# searchusers - [insert a few words of module description on this line]
# Copyright (C) 2003-2009  The MiG Project lead by Brian Vinter
#
# This file is part of MiG.
#
# MiG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# -- END_HEADER ---
#

"""Find all users with given data base field(s)"""

import sys
import getopt

from shared.useradm import init_user_adm, search_users, default_search


def usage(name='searchusers.py'):
    """Usage help"""
    print """Usage:
%(name)s [SEARCH_OPTIONS]
Where SEARCH_OPTIONS may be one or more of:
   -c COUNTRY          Search for country
   -d DB_PATH          Use DB_PATH as user data base file path
   -e EMAIL            Search for email
   -f FULLNAME         Search for full name
   -n                  Show only name
   -h                  Show this help
   -o ORGANIZATION     Search for organization
   -s STATE            Search for state

Each search value can be a string or a pattern with * and ? as wildcards.
"""\
         % {'name': name}


# ## Main ###
if "__main__" == __name__:
    (args, app_dir, db_path) = init_user_adm()
    conf_path = None
    user_dict = {}
    opt_args = 'c:C:d:E:F:hnO:S:'
    search_filter = default_search()
    name_only = False
    try:
        (opts, args) = getopt.getopt(args, opt_args)
    except getopt.GetoptError, err:
        print 'Error: ', err.msg
        usage()
        sys.exit(1)

    for (opt, val) in opts:
        if opt == '-c':
            conf_path = val
        elif opt == '-d':
            db_path = val
        elif opt == '-h':
            usage()
            sys.exit(0)
        elif opt == '-n':
            name_only = True
        elif opt == '-C':
            search_filter['country'] = val
        elif opt == '-E':
            search_filter['email'] = val
        elif opt == '-F':
            search_filter['full_name'] = val
        elif opt == '-O':
            search_filter['organization'] = val
        elif opt == '-S':
            search_filter['state'] = val
        else:
            print 'Error: %s not supported!' % opt
            usage()
            sys.exit(0)

    hits = search_users(search_filter, conf_path, db_path)
    for (uid, user_dict) in hits:
        if name_only:
            print '%s' % (user_dict['full_name'])
        else:
            print '%s : %s' % (uid, user_dict)
