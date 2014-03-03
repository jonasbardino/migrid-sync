#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# adminfreeze - back end to request freeze files in write-once fashion
# Copyright (C) 2003-2014  The MiG Project lead by Brian Vinter
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

"""Request freeze of one or more files into a write-once archive"""

import shared.returnvalues as returnvalues
from shared.functional import validate_input_and_cert
from shared.init import initialize_main_variables, find_entry


def signature():
    """Signature of the main function"""

    defaults = {}
    return ['html_form', defaults]


def main(client_id, user_arguments_dict):
    """Main function used by front end"""

    (configuration, logger, output_objects, op_name) = \
        initialize_main_variables(client_id, op_header=False)
    defaults = signature()[1]
    output_objects.append({'object_type': 'header', 'text'
                          : 'Make frozen archive'})
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

    title_entry = find_entry(output_objects, 'title')
    title_entry['text'] = 'Freeze Archive'

    # jquery support for dynamic addition of copy/upload fields

    title_entry['javascript'] = '''
<link rel="stylesheet" type="text/css" href="/images/css/jquery.managers.css" media="screen"/>
<link rel="stylesheet" type="text/css" href="/images/css/jquery.contextmenu.css" media="screen"/>
<link rel="stylesheet" type="text/css" href="/images/css/jquery-ui.css" media="screen"/>
<link rel="stylesheet" type="text/css" href="/images/css/jquery.xbreadcrumbs.css" media="screen"/>
<link rel="stylesheet" type="text/css" href="/images/css/jquery.fmbreadcrumbs.css" media="screen"/>


<script type="text/javascript" src="/images/js/jquery.js"></script>
<script type="text/javascript" src="/images/js/jquery.tablesorter.js"></script>
<script type="text/javascript" src="/images/js/jquery.tablesorter.pager.js"></script>
<script type="text/javascript" src="/images/js/jquery-ui.js"></script>
<script type="text/javascript" src="/images/js/jquery.form.js"></script>
<script type="text/javascript" src="/images/js/jquery.prettyprint.js"></script>
<script type="text/javascript" src="/images/js/jquery.filemanager.js"></script>
<script type="text/javascript" src="/images/js/jquery.contextmenu.js"></script>
<script type="text/javascript" src="/images/js/jquery.xbreadcrumbs.js"></script>

<script type="text/javascript" >

var copy_fields = 0;
var upload_fields = 0;
var open_chooser;

function add_copy(div_id) {
    var field_id = "freeze_copy_"+copy_fields;
    var field_name = "freeze_copy_"+copy_fields;
    var wrap_id = field_id+"_wrap";
    var browse_id = field_id+"_browse";
    copy_entry = "<span id=\'"+wrap_id+"\'>";
    copy_entry += "<input type=\'button\' value=\'Remove\' ";
    copy_entry += " onClick=\'remove_field(\"+wrap_id+\");\'/>";
    // add browse button to mimic upload field
    copy_entry += "<input type=\'button\' id=\'"+browse_id+"\' ";
    copy_entry += " value=\'Browse...\' />";
    copy_entry += "<input type=\'text\' id=\'"+field_id+"\' ";
    copy_entry += " name=\'" + field_name + "\' size=80 /><br / >";
    copy_entry += "</span>";

    $("#"+div_id).append(copy_entry);
    $("#"+field_id).click(function() {
        open_chooser("Add file(s)", function(file) {
                $("#"+field_id).val(file);
            });
    });
    $("#"+browse_id).click(function() {
         $("#"+field_id).click();
    });
    $("#"+field_id).click();
    copy_fields += 1;
}

function add_upload(div_id) {
    var field_id = "freeze_upload_"+upload_fields;
    var field_name = "freeze_upload_"+upload_fields;
    var wrap_id = field_id+"_wrap";
    upload_entry = "<span id=\'"+wrap_id+"\'>";
    upload_entry += "<input type=\'button\' value=\'Remove\' ";
    upload_entry += " onClick=\'remove_field(\"+wrap_id+\");\'/>";
    upload_entry += "<input type=\'file\' id=\'"+field_id+"\' ";
    upload_entry += " name=\'" + field_name + "\' size=50 /><br / >";
    upload_entry += "</span>";
    $("#"+div_id).append(upload_entry);
    $("#"+field_id).click();
    upload_fields += 1;
}

function remove_field(field_id) {
    $(field_id).remove();
}

// init file chooser dialogs with directory selction support
function init_dialogs() {
    open_chooser = mig_filechooser_init("fm_filechooser",
        function(file) {
            return;
        }, false, "/");
}

function post_init() {
    init_dialogs();
}

// function to load js helpers and then initialise the page parts
function init_page() {
    // load the helper scripts
    var script = document.createElement("script");
    script.setAttribute("type","text/javascript");
    script.setAttribute("src",
    "/images/js/jquery.migtools.js");
    document.getElementsByTagName("head")[0].appendChild(script);
    
    // and call continuation (browser dependent)
    if (script.readyState) { // IE style browser
        script.onreadystatechange = function() {
            if (this.readyState == "loaded" || this.readyState == "complete") {
                post_init();
            }
        };
    } else { // other browser, should support onload
        script.onload = post_init;
    }
}

$(document).ready(function() {
         // do sequenced initialisation (separate function)
         init_page();
     }
);
</script>
'''

    if not configuration.site_enable_freeze:
        output_objects.append({'object_type': 'text', 'text':
                           '''Freezing archives is not enabled on this site.
    Please contact the Grid admins if you think it should be.'''})
        return (output_objects, returnvalues.OK)

    output_objects.append(
        {'object_type': 'text', 'text'
         : '''Note that a frozen archive can not be changed after creation
and it can only be manually removed by the management, so please be careful
when filling in the details.'''
         })

    files_form = """
<!-- and now this... we do not want to see it, except in a dialog: -->
<div id='fm_filechooser' style='display:none'>
    <div class='fm_path_breadcrumbs'>
        <ul id='fm_xbreadcrumbs' class='xbreadcrumbs'>
        </ul>
    </div>
    <div class='fm_addressbar'>
        <input type='hidden' value='/' name='fm_current_path' readonly='readonly' />
    </div>
    <div class='fm_folders'>
        <ul class='jqueryFileTree'>
            <li class='directory expanded'>
                <a>...</a>
            </li>
        </ul>
    </div>
    <div class='fm_files'>
        <table id='fm_filelisting' style='font-size:13px;' cellspacing='0'>
            <thead>
                <tr>
                    <th>Name</th>
                    <th style='width: 80px;'>Size</th>
                    <th style='width: 50px;'>Type</th>
                    <th style='width: 120px;'>Date Modified</th>
                </tr>
            </thead>
            <tbody>
                <!-- this is a placeholder for contents: do not remove! -->
            </tbody>
         </table>
         
    </div>
    <div class='fm_statusbar'>&nbsp;</div>
    </div>
    <!-- very limited menus here - maybe we should add select all entry? -->
    <ul id='folder_context' class='contextMenu' style='display:none'>
        <li class='select'>
            <a href='#select'>Select</a>
        </li>
    </ul>
    <ul id='file_context' class='contextMenu' style='display:none'>
        <li class='select'>
            <a href='#select'>Select</a>
        </li>
    </ul>
    <div id='cmd_dialog' title='Command output' style='display: none;'></div>
    """
    output_objects.append({'object_type': 'html_form', 'text'
                          : files_form})
    html_form = """
<form enctype='multipart/form-data' method='post' action='createfreeze.py'>
<br /><b>Name:</b><br />
<input type='text' name='freeze_name' size=30 />
<br /><b>Description:</b><br />
<textarea cols='80' rows='20' wrap='off' name='freeze_description'></textarea>
<br />
<div id='freezefiles'>
<b>Freeze Archive Files:</b>
<input type='button' value='Add file/directory'
    onClick='add_copy(\"copyfiles\");'/>
<input type='button' value='Add upload'
    onClick='add_upload(\"uploadfiles\");'/>
<div id='copyfiles'>
<!-- Dynamically filled -->
</div>
<div id='uploadfiles'>
<!-- Dynamically filled -->
</div>
</div>
<input type='submit' value='Create Archive' />
</form>
"""
    output_objects.append({'object_type': 'html_form', 'text'
                          : html_form})

    return (output_objects, returnvalues.OK)


