#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# resedit - Resource editor back end
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

# Martin Rehr martin@rehr.dk August 2005

"""Display resource editor"""

import socket

import shared.resconfkeywords as resconfkeywords
import shared.returnvalues as returnvalues
from shared.init import initialize_main_variables
from shared.functional import validate_input_and_cert
from shared.refunctions import list_runtime_environments
from shared.resource import init_conf, empty_resource_config 
from shared.vgrid import res_allowed_vgrids, default_vgrid


def signature():
    """Signature of the main function"""

    defaults = {'hosturl': [''], 'hostidentifier':['']}
    return ['html_form', defaults]


def field_size(value, default=30):
    """Find best input field size for value"""
    value_len = len("%s" % value)
    if value_len < 40:
        size = default
    elif value_len > 120:
        size = 120
    else:
        size = value_len
    return size

def available_choices(configuration, client_id, resource_id, field, spec):
    """Find the available choices for the selectable field.
    Tries to lookup all valid choices from configuration if field is
    specified to be a string variable.
    """
    if 'boolean' == spec['Type']:
        choices = [True, False]
    elif 'string' == spec['Type']:
        try:
            choices = getattr(configuration, '%ss' % field.lower())
        except AttributeError, exc:
            print exc
            choices = []
    else:
        choices = []
    default = spec['Value']
    if default in choices:
        choices = [default] + [i for i in choices if not default == i]
    return choices

def main(client_id, user_arguments_dict):
    """Main function used by front end"""

    (configuration, logger, output_objects, op_name) = \
        initialize_main_variables(op_header=False, op_title=False)
    defaults = signature()[1]
    (validate_status, accepted) = validate_input_and_cert(
        user_arguments_dict,
        defaults,
        output_objects,
        client_id,
        configuration,
        allow_rejects=False,
        )
    if not validate_status:
        return (accepted, returnvalues.CLIENT_ERROR)

    hosturl = accepted['hosturl'][-1]
    hostidentifier = accepted['hostidentifier'][-1]
    resource_id = '%s.%s' % (hosturl, hostidentifier)
    extra_selects = 3
    allowed_vgrids = res_allowed_vgrids(configuration, resource_id)
    allowed_vgrids.sort()
    (re_status, allowed_run_envs) = list_runtime_environments(configuration)
    allowed_run_envs.sort()
    area_cols = 80
    area_rows = 5
    
    status = returnvalues.OK

    logger.info('Starting Resource edit GUI.')

    output_objects.append({'object_type': 'title', 'text': 'Resource Editor'
                          })
    output_objects.append({'object_type': 'header', 'text': 'Resource Editor'
                          })
    output_objects.append({'object_type': 'sectionheader', 'text'
                          : 'MiG Resource Editor'})
    output_objects.append({'object_type': 'text', 'text'
                           : '''
Please fill in or edit the fields below to fit your MiG resource reservation. Most fields
will work with their default values. So if you are still in doubt after reading the help
description, you can likely just leave the field alone.'''
                          })

    if hosturl and hostidentifier:
        conf = init_conf(configuration, hosturl, hostidentifier)
        if not conf:
            status = returnvalues.CLIENT_ERROR
            output_objects.append({'object_type': 'error_text', 'text'
                           : '''No such resource! (%s.%s)''' % (hosturl, hostidentifier)})
            return (output_objects, status)
    else:
        conf = empty_resource_config(configuration)

    res_fields = resconfkeywords.get_resource_specs(configuration)
    exe_fields = resconfkeywords.get_exenode_specs(configuration)
    store_fields = resconfkeywords.get_storenode_specs(configuration)

    output_objects.append({'object_type': 'html_form', 'text': """
<form method='post' action='reseditaction.py''>
"""
                           })

    # Resource overall fields

    output_objects.append({'object_type': 'sectionheader', 'text'
                           : "Main Resource Settings"})
    output_objects.append({'object_type': 'text', 'text'
                           : """This section configures general options for the resource."""
                           })

    (title, field) = ('Host FQDN', 'HOSTURL')
    if hosturl:
        hostip = conf.get('HOSTIP', socket.gethostbyname(hosturl))
        output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
<input type='hidden' name='%s' value='%s'>
<input type='hidden' name='HOSTIP' value='%s'>
%s
<br>
<br>""" % (title, field, field, conf[field], hostip,
           conf[field])
                               })
    else:
        output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
<input type='text' name='%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field, field_size(conf[field]),
           conf[field])
                               })

    (title, field) = ('Host identifier', 'HOSTIDENTIFIER')
    if hostidentifier:
        output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
<input type='hidden' name='%s' value='%s'>
%s
<br>
<br>""" % (title, field, field, conf[field], conf[field])
                               })                               

    (field, title) = 'frontendhome', 'Frontend Home Path'
    output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#%s'>help</a><br>
<input type='text' name='%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf[field]), conf[field])
                               })

    for (field, spec) in res_fields:
        title = spec['Title']
        if 'invisible' == spec['Editor']:
            continue
        elif 'input' == spec['Editor']:
            output_objects.append({'object_type': 'html_form', 'text'
                                   : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
<input type='text' name='%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field, field_size(conf[field]),
           conf[field])
                                   })
        elif 'select' == spec['Editor']:
            choices = available_choices(configuration, client_id,
                                        resource_id, field, spec)
            res_value = conf[field]
            value_select = ''
            value_select += "<select name='%s'>\n" % field
            for name in choices:
                selected = ''
                if res_value == name:
                    selected = 'selected'
                value_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
            value_select += """</select><br>\n"""    
            output_objects.append({'object_type': 'html_form', 'text'
                                   : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
%s
<br>""" % (title, field, value_select)
                                   })

    # Not all resource fields here map directly to keywords/specs input field
    
    (title, field) = ('Runtime Environments', 'RUNTIMEENVIRONMENT')
    re_list = conf[field]
    show = re_list + [('', []) for i in range(extra_selects)]
    re_select = "<input type='hidden' name='runtime_env_fields' value='%s'>\n" % len(show)
    i = 0
    for active in show:
        re_select += "<select name='runtimeenvironment%d'>\n" % i
        for name in allowed_run_envs + ['']:
            selected = ''
            if active[0] == name:
                selected = 'selected'
            re_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
        re_select += """</select><br>\n"""
        values = '\n'.join(['%s=%s' % pair for pair in active[1]])
        re_select += "<textarea cols='%d' rows='%d' name='re_values%d'>%s</textarea><br>\n" % \
                     (area_cols, area_rows, i, values)
        i += 1

    output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#res-%s'>help</a><br>
Please enter any required environment variable settings on the form NAME=VALUE in the box below
each selected runtimeenvironment.<br>
%s
<br>""" % (title, field, re_select)
                           })


    # Execution node fields

    output_objects.append({'object_type': 'sectionheader', 'text'
                           : "Execution nodes"})
    output_objects.append({'object_type': 'text', 'text'
                           : """This section configures execution nodes on the resource."""
                           })
    (field, title) = 'executionnodes', 'Execution Node(s)'
    output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#exe-%s'>help</a><br>
<input type='text' name='exe-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_exes'][field]), conf['all_exes'][field])
                               })

    (field, title) = 'executionhome', 'Execution Home Path'
    output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#exe-%s'>help</a><br>
<input type='text' name='exe-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_exes'][field]), conf['all_exes'][field])
                               })

    for (field, spec) in exe_fields:
        title = spec['Title']
        if 'invisible' == spec['Editor']:
            continue
        elif 'input' == spec['Editor']:
            output_objects.append({'object_type': 'html_form', 'text'
                                   : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#exe-%s'>help</a><br>
<input type='text' name='exe-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_exes'][field]), conf['all_exes'][field])
                                   })
        elif 'select' == spec['Editor']:
            choices = available_choices(configuration, client_id,
                                        resource_id, field, spec)
            exe_value = conf['all_exes'][field]
            value_select = ''
            value_select += "<select name='exe-%s'>\n" % field
            for name in choices:
                selected = ''
                if exe_value == name:
                    selected = 'selected'
                value_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
            value_select += """</select><br>\n"""    
            output_objects.append({'object_type': 'html_form', 'text'
                                   : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#exe-%s'>help</a><br>
%s
<br>""" % (title, field, value_select)
                                   })

    (title, field) = ('VGrid Participation', 'vgrid')
    exe_vgrids = conf['all_exes']['vgrid']
    show = exe_vgrids + ['' for i in range(extra_selects)]
    vgrid_select = ''
    for active in show:
        vgrid_select += "<select name='exe-%s'>\n" % field
        for name in allowed_vgrids + ['']:
            selected = ''
            if active == name:
                selected = 'selected'
            vgrid_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
        vgrid_select += """</select><br>\n"""    
    output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#exe-%s'>help</a><br>
%s
<br>""" % (title, field, vgrid_select)
                           })
    
    # Storage node fields

    output_objects.append({'object_type': 'sectionheader', 'text'
                           : "Storage nodes"})
    output_objects.append({'object_type': 'text', 'text'
                           : """This section configures storage nodes on the resource."""
                           })
    
    (field, title) = 'storagenodes', 'Storage Node(s)'
    output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#store-%s'>help</a><br>
<input type='text' name='store-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_stores'][field]), conf['all_stores'][field])
                               })

    (field, title) = 'storagehome', 'Storage Home Path'
    output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#store-%s'>help</a><br>
<input type='text' name='store-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_stores'][field]), conf['all_stores'][field])
                               })

    for (field, spec) in store_fields:
        title = spec['Title']
        if 'invisible' == spec['Editor']:
            continue
        elif 'input' == spec['Editor']:
            output_objects.append({'object_type': 'html_form', 'text'
                           : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#store-%s'>help</a><br>
<input type='text' name='store-%s' size='%d' value='%s'>
<br>
<br>""" % (title, field, field,
           field_size(conf['all_stores'][field]), conf['all_stores'][field])
                                   })
        elif 'select' == spec['Editor']:
            choices = available_choices(configuration, client_id,
                                        resource_id, field, spec)
            store_value = conf['all_stores'][field]
            value_select = ''
            value_select += "<select name='store-%s'>\n" % field
            for name in choices:
                selected = ''
                if store_value == name:
                    selected = 'selected'
                value_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
            value_select += """</select><br>\n"""    
            output_objects.append({'object_type': 'html_form', 'text'
                                   : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#store-%s'>help</a><br>
%s
<br>""" % (title, field, value_select)
                                   })
    (title, field) = ('VGrid Participation', 'vgrid')
    store_vgrids = conf['all_stores']['vgrid']
    show = store_vgrids + ['' for i in range(extra_selects)]
    vgrid_select = ''
    for active in show:
        vgrid_select += "<select name='store-%s'>\n" % field
        for name in allowed_vgrids + ['']:
            selected = ''
            if active == name:
                selected = 'selected'
            vgrid_select += """<option %s value='%s'>%s</option>\n""" % (selected, name, name)
        vgrid_select += """</select><br>\n"""    
    output_objects.append({'object_type': 'html_form', 'text'
                               : """<br>
<b>%s:</b>&nbsp;<a href='resedithelp.py#store-%s'>help</a><br>
%s
<br>""" % (title, field, vgrid_select)
                           })


    output_objects.append({'object_type': 'html_form', 'text': """
<input type='submit' value='Save'>
</form>
"""
                           })

    return (output_objects, status)
