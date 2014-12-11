#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# --- BEGIN_HEADER ---
#
# configuration - configuration wrapper
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

"""Configuration class"""

import base64
import pwd
import os
import socket
import sys
import time
from ConfigParser import ConfigParser

from shared.logger import Logger
from shared.html import menu_items, vgrid_items

def fix_missing(config_file, verbose=True):
    """Add missing configuration options - used by checkconf script"""

    config = ConfigParser()
    config.read([config_file])

    fqdn = socket.getfqdn()
    user = os.environ['USER']
    global_section = {
        'enable_server_dist': False,
        'auto_add_cert_user': False,
        'auto_add_oid_user': False,
        'auto_add_resource': False,
        'server_fqdn': fqdn,
        'admin_email': '%s@%s' % (user, fqdn),
        'admin_list': '',
        'mrsl_files_dir': '~/state/mrsl_files/',
        're_files_dir': '~/state/re_files/',
        're_pending_dir': '~/state/re_pending/',
        'log_dir': '~/state/log/',
        're_home': '~/state/re_home/',
        'grid_stdin': '~/mig/server/server.stdin',
        'im_notify_stdin': '~/mig/server/notify.stdin',
        'gridstat_files_dir': '~/state/gridstat_files/',
        'mig_server_home': '~/mig/server/',
        'mig_code_base': '~/mig/',
        'resource_home': '~/state/resource_home/',
        'resource_pending': '~/state/resource_pending/',
        'user_pending': '~/state/user_pending/',
        'vgrid_home': '~/state/vgrid_home/',
        'vgrid_files_home': '~/state/vgrid_files_home/',
        'vgrid_public_base': '~/state/vgrid_public_base/',
        'vgrid_private_base': '~/state/vgrid_private_base/',
        'user_home': '~/state/user_home/',
        'user_settings': '~/state/user_settings/',
        'user_cache': '~/state/user_cache/',
        'server_home': '~/state/server_home/',
        'webserver_home': '~/state/webserver_home/',
        'sessid_to_mrsl_link_home': '~/state/sessid_to_mrsl_link_home/',
        'mig_system_files': '~/state/mig_system_files/',
        'wwwpublic': '~/state/wwwpublic/',
        'vm_home': '~/state/vm_home',
        'server_cert': '~/certs/cert.pem',
        'server_key': '~/certs/key.pem',
        'ca_cert': '~/certs/ca.pem',
        'sss_home': '~/state/sss_home/',
        'sandbox_home': '~/state/sandbox_home',
        'freeze_home': '~/state/freeze_home',
        'openid_store': '~/state/openid_store/',
        'public_key_file': '',
        'javabin_home': '~/mig/java-bin',
        'rate_limit_db': '~/mig/mig_system_files/daemon-rate-limit.db',
        'site_vgrid_links': 'files web tracker workflows monitor',
        'site_vgrid_creators': 'distinguished_name:.*',
        'hg_path': '/usr/bin/hg',
        'hgweb_scripts': '/usr/share/doc/mercurial-common/examples/',
        'trac_admin_path': '/usr/bin/trac-admin',
        'trac_ini_path': '~/mig/server/trac.ini',
        'trac_id_field': 'email',
        'migserver_http_url': 'http://%%(server_fqdn)s',
        'backup_http_urls': '',
        'migserver_https_url': 'https://%%(server_fqdn)s',
        'backup_https_urls': '',
        'myfiles_py_location': 'https://%%(server_fqdn)s/cgi-bin/ls.py',
        'mig_server_id': '%s.0' % fqdn,
        'empty_job_name': 'no_suitable_job-',
        'smtp_server': fqdn,
        'smtp_sender': 'MiG Server <%s@%s>' % (user, fqdn),
        'user_sftp_address': fqdn,
        'user_sftp_port': 2222,
        'user_sftp_key': '~/certs/combined.pem',
        'user_sftp_key_pub': '~/certs/server.pub',
        'user_sftp_auth': ['publickey'],
        'user_sftp_alias': '',
        'user_sftp_log': 'sftp.log',
        'user_davs_address': fqdn,
        'user_davs_port': 4443,
        'user_davs_key': '~/certs/combined.pem',
        'user_davs_auth': ['password'],
        'user_davs_alias': '',
        'user_davs_log': 'davs.log',
        'user_ftps_address': fqdn,
        'user_ftps_ctrl_port': 8021,
        'user_ftps_pasv_ports': range(8100, 8400),
        'user_ftps_key': '~/certs/combined.pem',
        'user_ftps_auth': ['password'],
        'user_ftps_alias': '',
        'user_ftps_log': 'ftps.log',
        'user_openid_address': fqdn,
        'user_openid_port': 8443,
        'user_openid_key': '~/certs/combined.pem',
        'user_openid_auth': ['password'],
        'user_openid_alias': '',
        'user_openid_log': 'openid.log',
        'user_openid_providers': [],
        'user_events_log': 'events.log',
        'logfile': 'server.log',
        'loglevel': 'info',
        'sleep_period_for_empty_jobs': '80',
        'cputime_for_empty_jobs': '120',
        'min_seconds_between_live_update_requests': '120',
        'architectures': 'X86 AMD64 IA64 SPARC SPARC64 ITANIUM SUN4U SPARC-T1',
        'scriptlanguages': 'sh python java',
        'jobtypes': 'batch interactive bulk all',
        'lrmstypes': 'Native Native-execution-leader Batch Batch-execution-leader',
        }
    scheduler_section = {'algorithm': 'FairFit',
                         'expire_after': '99999999999',
                         'job_retries': '4'}
    monitor_section = {'sleep_secs': '60',
                       'sleep_update_totals': '600',
                       'slackperiod': '600'}
    settings_section = {'language': 'English', 'submitui': ['fields',
                        'textarea', 'files']}
    feasibility_section = {'resource_seen_within_hours': '24',
                          'skip_validation': '',
                          'job_cond_green': 'ARCHITECTURE PLATFORM \
                          RUNTIMEENVIRONMENT VERIFYFILES VGRID SANDBOX',
                          'job_cond_yellow': 'DISK MEMORY CPUTIME',
                          'job_cond_orange': 'CPUCOUNT NODECOUNT',
                          'job_cond_red': 'EXECUTABLES INPUTFILES REGISTERED \
                          SEEN_WITHIN_X',
                          'enable_suggest': 'False',
                          'suggest_threshold': 'GREEN',
                          }

    defaults = {
        'GLOBAL': global_section,
        'SCHEDULER': scheduler_section,
        'MONITOR': monitor_section,
        'SETTINGS': settings_section,
        'FEASIBILITY': feasibility_section,
        }
    for section in defaults.keys():
        if not section in config.sections():
            config.add_section(section)

    modified = False
    for (section, settings) in defaults.items():
        for (option, value) in settings.items():
            if not config.has_option(section, option):
                if verbose:
                    print 'setting %s->%s to %s' % (section, option,
                            value)
                config.set(section, option, value)
                modified = True
    if modified:
        backup_path = '%s.%d' % (config_file, time.time())
        print 'Backing up existing configuration to %s as update removes all comments'\
             % backup_path
        fd = open(config_file, 'r')
        backup_fd = open(backup_path, 'w')
        backup_fd.writelines(fd.readlines())
        backup_fd.close()
        fd.close()
        fd = open(config_file, 'w')
        config.write(fd)
        fd.close()


class Configuration:
    """Server configuration in parsed form"""
    
    mig_server_id = None
    mrsl_files_dir = ''
    re_files_dir = ''
    re_pending_dir = ''
    log_dir = ''
    re_home = ''
    grid_stdin = ''
    im_notify_stdin = ''
    gridstat_files_dir = ''
    mig_server_home = ''
    mig_code_base = ''
    server_fqdn = ''
    admin_email = ''
    admin_list = ''
    resource_home = ''
    vgrid_home = ''
    vgrid_public_base = ''
    vgrid_private_base = ''
    vgrid_files_home = ''
    resource_pending = ''
    user_pending = ''
    webserver_home = ''
    user_home = ''
    user_settings = ''
    user_cache = ''
    sss_home = ''
    sandbox_home = ''
    freeze_home = ''
    javabin_home = ''
    openid_store = ''
    rate_limit_db = ''
    site_vgrid_links = []
    site_vgrid_creators = [('distinguished_name', '.*')]
    hg_path = ''
    hgweb_scripts = ''
    trac_admin_path = ''
    trac_ini_path = ''
    trac_id_field = ''
    smtp_server = ''
    smtp_sender = ''
    user_sftp_address = ''
    user_sftp_port = 2222
    user_sftp_key = ''
    user_sftp_key_pub = ''
    user_sftp_auth = ['publickey']
    user_sftp_alias = ''
    user_sftp_log = 'sftp.log'
    user_davs_address = ''
    user_davs_port = 4443
    user_davs_key = ''
    user_davs_auth = ['password']
    user_davs_alias = ''
    user_davs_log = 'davs.log'
    user_ftps_address = ''
    user_ftps_ctrl_port = 8021
    user_ftps_pasv_ports = range(8100, 8500)
    user_ftps_key = ''
    user_ftps_auth = ['password']
    user_ftps_alias = ''
    user_ftps_log = 'ftps.log'
    user_openid_address = ''
    user_openid_port = 8443
    user_openid_key = ''
    user_openid_auth = ['password']
    user_openid_alias = ''
    user_openid_log = 'openid.log'
    user_openid_providers = []
    user_events_log = 'events.log'
    server_home = ''
    vms_builder_home = ''
    sessid_to_mrsl_link_home = ''
    mig_system_files = ''
    empty_job_name = ''
    migserver_http_url = ''
    backup_http_urls = ''
    migserver_https_url = ''
    migserver_https_cert_url = ''
    migserver_https_oid_url = ''
    migserver_https_sid_url = ''
    # Default entry point for users: i.e. prefer cert or oid url for links
    migserver_https_default_url = ''
    backup_https_urls = ''
    migserver_https_default_url = ''
    sleep_period_for_empty_jobs = ''
    min_seconds_between_live_update_requests = 0
    cputime_for_empty_jobs = 0
    myfiles_py_location = ''
    public_key_file = ''
    wwwpublic = ''
    vm_home = ''
    vm_proxy_host = ''
    vm_proxy_port = vm_agent_port = 8112
    vm_client_port = 8111
    vm_applet_port = 8114
    enable_server_dist = False
    sleep_secs = 0
    sleep_update_totals = 0
    slackperiod = 0
    architectures = []
    scriptlanguages = []
    jobtypes = []
    lrmstypes = []
    storage_protocols = ['sftp']
    server_cert = ''
    server_key = ''
    passphrase_file = ''
    ca_file = ''
    ca_dir = ''
    sched_alg = 'FirstFit'
    expire_after = 86400
    job_retries = 4
    logfile = ''
    loglevel = ''
    logger_obj = None
    logger = None
    peers = None

    # feasibility

    resource_seen_within_hours = 24
    skip_validation = []
    job_cond_green = ['ARCHITECTURE', 'PLATFORM', 'RUNTIMEENVIRONMENT',
                      'VERIFYFILES', 'VGRID', 'SANDBOX']
    job_cond_yellow = ['DISK', 'MEMORY', 'CPUTIME']
    job_cond_orange = ['CPUCOUNT', 'NODECOUNT']
    job_cond_red = ['EXECUTABLES', 'INPUTFILES', 'REGISTERED', 'SEEN_WITHIN_X']
    enable_suggest = False
    suggest_threshold = 'GREEN'

    # Max number of jobs to migrate in each migration batch

    migrate_limit = 3

    # seconds before peer data expires

    expire_peer = 600
    language = ['English']
    submitui = ['fields', 'textarea', 'files']

    # directory for usage records, initially None (means: do not generate)

    usage_record_dir = None

    auto_add_cert_user = False
    auto_add_oid_user = False
    auto_add_resource = False

    # ARC resource configuration (list)
    # wired-in shorthands in arcwrapper: 
    # fyrgrid, benedict. Otherwise, ldap://bla.bla:2135/...
    
    arc_clusters = [] 
    
    config_file = None

    # constructor

    def __init__(self, config_file, verbose=True):
        self.config_file = config_file
        self.reload_config(verbose)

    def reload_config(self, verbose):
        """Re-read and parse configuration file"""

        try:
            self.logger.info('reloading configuration and reopening log'
                             )
        except:
            pass

        if not os.path.isfile(self.config_file):
            print 'Could not find your configuration file (', \
                self.config_file, ').'
            print 'Are you missing a symlink from server/MiGserver.conf pointing to server/MiGserver-{server}.conf?'
            raise IOError

        config = ConfigParser()
        config.read([self.config_file])

        # print "expanding config paths"

        # Expand all paths once and for all to allow '~' in config paths
        # NB! expanduser does not properly honor seteuid - must force it to

        os.environ['HOME'] = pwd.getpwuid(os.geteuid())[5]

        for (key, val) in config.items('GLOBAL'):
            expanded_val = os.path.expanduser(val)
            config.set('GLOBAL', key, expanded_val)

        try:
            self.log_dir = config.get('GLOBAL', 'log_dir')
            self.logfile = config.get('GLOBAL', 'logfile')
            self.loglevel = config.get('GLOBAL', 'loglevel')
        except:

            # Fall back to file in current dir

            self.log_dir = '.'
            self.logfile = 'mig.log'
            self.loglevel = 'info'
            
        self.log_path = os.path.join(self.log_dir, self.logfile)
        
        if verbose:
            print 'logging to:', self.log_path, '; level:', self.loglevel

        # reopen or initialize logger

        if self.logger_obj:

            # hangup reopens log file

            self.logger_obj.hangup()
        else:
            self.logger_obj = Logger(self.log_path, self.loglevel)

        logger = self.logger_obj.logger
        self.logger = logger

        # print "logger initialized (level " + logger_obj.loglevel() + ")"
        # logger.debug("logger initialized")

        try:
            self.mig_server_id = config.get('GLOBAL', 'mig_server_id')
            self.mrsl_files_dir = config.get('GLOBAL', 'mrsl_files_dir')
            self.re_files_dir = config.get('GLOBAL', 're_files_dir')
            self.re_pending_dir = config.get('GLOBAL', 're_pending_dir')
            self.re_home = config.get('GLOBAL', 're_home')
            self.grid_stdin = config.get('GLOBAL', 'grid_stdin')
            self.im_notify_stdin = config.get('GLOBAL',
                    'im_notify_stdin')
            self.gridstat_files_dir = config.get('GLOBAL',
                    'gridstat_files_dir')
            self.mig_server_home = config.get('GLOBAL',
                    'mig_server_home')

            # logger.info("grid_stdin = " + self.grid_stdin)

            self.server_fqdn = config.get('GLOBAL', 'server_fqdn')
            self.resource_home = config.get('GLOBAL', 'resource_home')
            self.vgrid_home = config.get('GLOBAL', 'vgrid_home')
            self.vgrid_private_base = config.get('GLOBAL',
                    'vgrid_private_base')
            self.vgrid_public_base = config.get('GLOBAL',
                    'vgrid_public_base')
            self.vgrid_files_home = config.get('GLOBAL',
                    'vgrid_files_home')
            self.resource_pending = config.get('GLOBAL',
                    'resource_pending')
            self.user_pending = config.get('GLOBAL', 'user_pending')
            self.webserver_home = config.get('GLOBAL', 'webserver_home')
            self.user_home = config.get('GLOBAL', 'user_home')
            self.user_settings = config.get('GLOBAL', 'user_settings')
            self.user_cache = config.get('GLOBAL', 'user_cache')
            self.server_home = config.get('GLOBAL', 'server_home')
            self.sss_home = config.get('GLOBAL', 'sss_home')
            self.sandbox_home = config.get('GLOBAL', 'sandbox_home')
            self.javabin_home = config.get('GLOBAL', 'javabin_home')
            self.smtp_server = config.get('GLOBAL', 'smtp_server')
            self.wwwpublic = config.get('GLOBAL', 'wwwpublic')
            self.vm_home = config.get('GLOBAL', 'vm_home')
            self.architectures = config.get('GLOBAL', 'architectures').split()
            self.scriptlanguages = config.get('GLOBAL',
                                              'scriptlanguages').split()
            self.jobtypes = config.get('GLOBAL', 'jobtypes').split()
            self.lrmstypes = config.get('GLOBAL', 'lrmstypes').split()
            self.sessid_to_mrsl_link_home = config.get('GLOBAL',
                    'sessid_to_mrsl_link_home')
            self.mig_system_files = config.get('GLOBAL',
                    'mig_system_files')
            self.empty_job_name = config.get('GLOBAL', 'empty_job_name')
            self.migserver_http_url = config.get('GLOBAL',
                    'migserver_http_url')
            self.backup_http_urls = config.get('GLOBAL',
                    'backup_http_urls')
            self.migserver_https_url = config.get('GLOBAL',
                    'migserver_https_url')
            self.backup_https_urls = config.get('GLOBAL',
                    'backup_https_urls')
            self.failover_http_urls = [self.migserver_http_url]\
                 + self.backup_http_urls.split()
            self.failover_https_urls = [self.migserver_https_url]\
                 + self.backup_https_urls.split()
            self.sleep_period_for_empty_jobs = config.get('GLOBAL',
                    'sleep_period_for_empty_jobs')
            self.min_seconds_between_live_update_requests = \
                config.get('GLOBAL',
                           'min_seconds_between_live_update_requests')
            self.cputime_for_empty_jobs = config.get('GLOBAL',
                    'cputime_for_empty_jobs')
            self.myfiles_py_location = config.get('GLOBAL',
                    'myfiles_py_location')
            self.sleep_secs = config.get('MONITOR', 'sleep_secs')
            self.sleep_update_totals = config.get('MONITOR',
                    'sleep_update_totals')
            self.slackperiod = config.get('MONITOR', 'slackperiod')
            self.language = config.get('SETTINGS', 'language').split()
            self.submitui = config.get('SETTINGS', 'submitui').split()

        except Exception, err:

            # logger.info("done reading settings from config")

            try:
                self.logger.error('Error in reloading configuration: %s'
                                   % err)
            except:
                pass
            raise Exception('Failed to parse configuration: %s' % err)

        if config.has_option('GLOBAL', 'admin_list'):
            # Parse semi-colon separated list of admins with optional spaces
            admins = config.get('GLOBAL', 'admin_list')
            self.admin_list = [admin.strip() for admin in admins.split(',')]
        else:
            self.admin_list = []
        if config.has_option('GLOBAL', 'admin_email'):
            self.admin_email = config.get('GLOBAL', 'admin_email')
        else:
            self.admin_email = []
        if config.has_option('GLOBAL', 'migserver_https_cert_url'):
            self.migserver_https_cert_url = config.get('GLOBAL',
                                                       'migserver_https_cert_url')
        else:
            self.migserver_https_cert_url = self.migserver_https_url
        if config.has_option('GLOBAL', 'migserver_https_oid_url'):
            self.migserver_https_oid_url = config.get('GLOBAL',
                                                       'migserver_https_oid_url')
        else:
            self.migserver_https_oid_url = self.migserver_https_url
        if config.has_option('GLOBAL', 'migserver_https_sid_url'):
            self.migserver_https_sid_url = config.get('GLOBAL',
                                                       'migserver_https_sid_url')
        else:
            self.migserver_https_sid_url = self.migserver_https_url
        if config.has_option('GLOBAL', 'migserver_https_default_url'):
            self.migserver_https_default_url = config.get('GLOBAL',
                                                       'migserver_https_default_url')
        else:
            self.migserver_https_default_url = self.migserver_https_cert_url
        if config.has_option('GLOBAL', 'rate_limit_db'):
            self.rate_limit_db = config.get('GLOBAL', 'rate_limit_db')
        else:
            self.rate_limit_db = os.path.join(self.mig_system_files,
                                              'daemon-rate-limit.db')
        if config.has_option('GLOBAL', 'freeze_home'):
            self.freeze_home = config.get('GLOBAL', 'freeze_home')
        else:
            self.freeze_home = ''
        if config.has_option('GLOBAL', 'openid_store'):
            self.openid_store = config.get('GLOBAL', 'openid_store')
        if config.has_option('GLOBAL', 'user_sftp_address'):
            self.user_sftp_address = config.get('GLOBAL', 
                                                'user_sftp_address')
        if config.has_option('GLOBAL', 'user_sftp_port'):
            self.user_sftp_port = config.getint('GLOBAL', 
                                                'user_sftp_port')
        if config.has_option('GLOBAL', 'user_sftp_key'):
            self.user_sftp_key = config.get('GLOBAL', 
                                            'user_sftp_key')
        if config.has_option('GLOBAL', 'user_sftp_key_pub'):
            self.user_sftp_key_pub = config.get('GLOBAL', 
                                            'user_sftp_key_pub')
        if config.has_option('GLOBAL', 'user_sftp_auth'):
            self.user_sftp_auth = config.get('GLOBAL', 
                                             'user_sftp_auth').split()
        if config.has_option('GLOBAL', 'user_sftp_alias'):
            self.user_sftp_alias = config.get('GLOBAL', 
                                              'user_sftp_alias')
        if config.has_option('GLOBAL', 'user_sftp_log'):
            self.user_sftp_log = config.get('GLOBAL', 'user_sftp_log')
        if config.has_option('GLOBAL', 'user_davs_address'):
            self.user_davs_address = config.get('GLOBAL', 
                                                'user_davs_address')
        if config.has_option('GLOBAL', 'user_davs_port'):
            self.user_davs_port = config.getint('GLOBAL', 
                                                'user_davs_port')
        if config.has_option('GLOBAL', 'user_davs_key'):
            self.user_davs_key = config.get('GLOBAL', 
                                            'user_davs_key')
        if config.has_option('GLOBAL', 'user_davs_auth'):
            self.user_davs_auth = config.get('GLOBAL', 
                                             'user_davs_auth').split()
        if config.has_option('GLOBAL', 'user_davs_alias'):
            self.user_davs_alias = config.get('GLOBAL', 
                                              'user_davs_alias')
        if config.has_option('GLOBAL', 'user_davs_log'):
            self.user_davs_log = config.get('GLOBAL', 'user_davs_log')
        if config.has_option('GLOBAL', 'user_ftps_address'):
            self.user_ftps_address = config.get('GLOBAL', 
                                                'user_ftps_address')
        if config.has_option('GLOBAL', 'user_ftps_ctrl_port'):
            self.user_ftps_ctrl_port = config.getint('GLOBAL', 
                                                     'user_ftps_ctrl_port')
        if config.has_option('GLOBAL', 'user_ftps_pasv_ports'):
            text_range = config.get('GLOBAL', 'user_ftps_pasv_ports')
            first, last = text_range.split(':')[:2]
            self.user_ftps_pasv_ports = range(int(first), int(last))
        if config.has_option('GLOBAL', 'user_ftps_key'):
            self.user_ftps_key = config.get('GLOBAL', 
                                            'user_ftps_key')
        if config.has_option('GLOBAL', 'user_ftps_auth'):
            self.user_ftps_auth = config.get('GLOBAL', 
                                             'user_ftps_auth').split()
        if config.has_option('GLOBAL', 'user_ftps_alias'):
            self.user_ftps_alias = config.get('GLOBAL', 
                                              'user_ftps_alias')
        if config.has_option('GLOBAL', 'user_ftps_log'):
            self.user_ftps_log = config.get('GLOBAL', 'user_ftps_log')
        if config.has_option('GLOBAL', 'user_openid_address'):
            self.user_openid_address = config.get('GLOBAL', 
                                                 'user_openid_address')
        if config.has_option('GLOBAL', 'user_openid_port'):
            self.user_openid_port = config.getint('GLOBAL', 
                                                 'user_openid_port')
        if config.has_option('GLOBAL', 'user_openid_key'):
            self.user_openid_key = config.get('GLOBAL', 
                                                 'user_openid_key')
        if config.has_option('GLOBAL', 'user_openid_auth'):
            self.user_openid_auth = config.get('GLOBAL', 
                                                 'user_openid_auth').split()
        if config.has_option('GLOBAL', 'user_openid_alias'):
            self.user_openid_alias = config.get('GLOBAL', 
                                                 'user_openid_alias')
        if config.has_option('GLOBAL', 'user_openid_log'):
            self.user_openid_log = config.get('GLOBAL', 'user_openid_log')
        if config.has_option('GLOBAL', 'user_openid_providers'):
            self.user_openid_providers = config.get('GLOBAL', 
                                                   'user_openid_providers').split()
        if config.has_option('GLOBAL', 'user_events_log'):
            self.user_events_log = config.get('GLOBAL', 'user_events_log')
        if config.has_option('GLOBAL', 'mig_code_base'):
            self.mig_code_base = config.get('GLOBAL', 'mig_code_base')
        else:
            self.mig_code_base = os.path.dirname(self.mig_server_home.rstrip(os.sep))
        if config.has_option('GLOBAL', 'vms_builder_home'):
            self.vms_builder_home = config.get('GLOBAL', 'vms_builder_home')
        else:
            self.vms_builder_home = os.path.join(self.server_home, 'vms_builder')
        if config.has_option('GLOBAL', 'public_key_file'):
            self.public_key_file = config.get('GLOBAL', 'public_key_file')
        if config.has_option('GLOBAL', 'smtp_sender'):
            self.smtp_sender = config.get('GLOBAL', 'smtp_sender')
        else:
            self.smtp_sender = 'MiG Server <%s@%s>'\
                 % (os.environ.get('USER', 'mig'), self.server_fqdn)
        if config.has_option('GLOBAL', 'notify_protocols'):
            self.notify_protocols = config.get('GLOBAL', 'notify_protocols').split()
        else:
            self.notify_protocols = []
        if config.has_option('GLOBAL', 'storage_protocols'):
            self.storage_protocols = config.get('GLOBAL', 'storage_protocols').split()
        if config.has_option('GLOBAL', 'vm_proxy_host'):
            self.vm_proxy_host = config.get('GLOBAL', 'vm_proxy_host')
        else:
            self.vm_proxy_host = self.server_fqdn
        if config.has_option('GLOBAL', 'vm_proxy_port'):
            self.vm_proxy_port = config.getint('GLOBAL', 'vm_proxy_port')
        if config.has_option('GLOBAL', 'vm_client_port'):
            self.vm_client_port = config.getint('GLOBAL', 'vm_client_port')
        if config.has_option('GLOBAL', 'vm_applet_port'):
            self.vm_applet_port = config.getint('GLOBAL', 'vm_applet_port')

        # vm_agent_port is just an alias for vm_proxy_port

        self.vm_agent_port = self.vm_proxy_port

        # logger.debug('starting scheduler options')

        if config.has_option('SCHEDULER', 'algorithm'):
            self.sched_alg = config.get('SCHEDULER', 'algorithm')
        else:
            self.sched_alg = 'FirstFit'
        if config.has_option('SCHEDULER', 'expire_after'):
            self.expire_after = config.getint('SCHEDULER',
                    'expire_after')

        if config.has_option('SCHEDULER', 'job_retries'):
            self.job_retries = config.getint('SCHEDULER', 'job_retries')

        if config.has_option('FEASIBILITY', 'resource_seen_within_hours'):
            self.resource_seen_within_hours = config.getint(
                'FEASIBILITY', 'resource_seen_within_hours')
        if config.has_option('FEASIBILITY', 'skip_validation'):
            self.skip_validation = config.get('FEASIBILITY',
                                              'skip_validation').split()
        if config.has_option('FEASIBILITY', 'enable_suggest'):
            self.enable_suggest = config.getboolean('FEASIBILITY',
                                                    'enable_suggest')
        if config.has_option('FEASIBILITY', 'suggest_threshold'):
            self.suggest_threshold = config.get('FEASIBILITY', 
                                                'suggest_threshold')
        if config.has_option('FEASIBILITY', 'job_cond_green'):
            self.job_cond_green = config.get('FEASIBILITY', 
                                                   'job_cond_green').split()
        if config.has_option('FEASIBILITY', 'job_cond_yellow'):
            self.job_cond_yellow = config.get('FEASIBILITY', 
                                                   'job_cond_yellow').split()
        if config.has_option('FEASIBILITY', 'job_cond_orange'):
            self.job_cond_orange = config.get('FEASIBILITY', 
                                                   'job_cond_orange').split()
        if config.has_option('FEASIBILITY', 'job_cond_red'):
            self.job_cond_red = config.get('FEASIBILITY', 
                                                   'job_cond_red').split()
        if config.has_option('SCM', 'hg_path'):
            self.hg_path = config.get('SCM', 'hg_path')
        else:
            self.hg_path = ''
        if config.has_option('SCM', 'hgweb_scripts'):
            self.hgweb_scripts = config.get('SCM', 'hgweb_scripts')
        elif config.has_option('SCM', 'hgweb_path'):
            # Legacy name (including actual cgi script no longer used)
            self.hgweb_scripts = os.path.dirname(config.get('SCM',
                                                            'hgweb_path'))
        else:
            self.hgweb_scripts = ''
        if config.has_option('TRACKER', 'trac_admin_path'):
            self.trac_admin_path = config.get('TRACKER', 'trac_admin_path')
        else:
            self.trac_admin_path = ''
        if config.has_option('TRACKER', 'trac_ini_path'):
            self.trac_ini_path = config.get('TRACKER', 'trac_ini_path')
        else:
            self.trac_ini_path = ''
        if config.has_option('TRACKER', 'trac_id_field'):
            self.trac_id_field = config.get('TRACKER', 'trac_id_field')
        else:
            self.trac_id_field = 'email'
        if config.has_option('RESOURCES', 'default_mount_re'):
            self.res_default_mount_re = config.get('RESOURCES', 'default_mount_re')
        else:
            self.res_default_mount_re = 'SSHFS-2.X-1'
        if config.has_option('VMACHINES', 'default_os'):
            self.vm_default_os = config.get('VMACHINES', 'default_os')
        else:
            self.vm_default_os = 'ubuntu-12.04'
        if config.has_option('VMACHINES', 'default_flavor'):
            self.vm_default_flavor = config.get('VMACHINES', 'default_flavor')
        else:
            self.vm_default_flavor = 'basic'
        if config.has_option('VMACHINES', 'default_hypervisor'):
            self.vm_default_hypervisor = config.get('VMACHINES',
                                                    'default_hypervisor')
        else:
            self.vm_default_hypervisor = 'vbox4x'
        if config.has_option('VMACHINES', 'default_disk_format'):
            self.vm_default_disk_format = config.get('VMACHINES',
                                                     'default_disk_format')
        else:
            self.vm_default_disk_format = 'vmdk'
        if config.has_option('VMACHINES', 'default_hypervisor_re'):
            self.vm_default_hypervisor_re = config.get(
                'VMACHINES', 'default_hypervisor_re')
        else:
            self.vm_default_hypervisor_re = 'VIRTUALBOX-4.X-1'
        if config.has_option('VMACHINES', 'default_sys_re'):
            self.vm_default_sys_re = config.get('VMACHINES', 'default_sys_re')
        else:
            self.vm_default_sys_re = 'VBOX4.X-IMAGES-2012-1'
        if config.has_option('VMACHINES', 'default_sys_base'):
            self.vm_default_sys_base = config.get('VMACHINES',
                                                  'default_sys_base')
        else:
            self.vm_default_sys_base = '$VBOXIMGDIR'
        if config.has_option('VMACHINES', 'default_user_conf'):
            self.vm_default_user_conf = config.get('VMACHINES',
                                                   'default_user_conf')
        else:
            self.vm_default_user_conf = '$VBOXUSERCONF'
        if config.has_option('VMACHINES', 'extra_os'):
            self.vm_extra_os = config.get('VMACHINES',
                                          'extra_os').split()
        else:
            self.vm_extra_os = []
        if config.has_option('VMACHINES', 'extra_flavors'):
            self.vm_extra_flavors = config.get('VMACHINES',
                                               'extra_flavors').split()
        else:
            self.vm_extra_flavors = []
        if config.has_option('VMACHINES', 'extra_hypervisor_re'):
            self.vm_extra_hypervisor_re = config.get(
                'VMACHINES', 'extra_hypervisor_re').split()
        else:
            self.vm_extra_hypervisor_re = []
        if config.has_option('VMACHINES', 'extra_sys_re'):
            self.vm_extra_sys_re = config.get('VMACHINES',
                                              'extra_sys_re').split()
        else:
            self.vm_extra_sys_re = []

        if config.has_option('SITE', 'images'):
            self.site_images = config.get('SITE', 'images')
        else:
            self.site_images = "/images"
        if config.has_option('SITE', 'styles'):
            self.site_styles = config.get('SITE', 'styles')
        else:
            self.site_styles = self.site_images
        if config.has_option('SITE', 'user_redirect'):
            self.site_user_redirect = config.get('SITE', 'user_redirect')
        else:
            self.site_user_redirect = '/cert_redirect'
        if config.has_option('SITE', 'title'):
            self.site_title = config.get('SITE', 'title')
        else:
            self.site_title = "Minimum intrusion Grid"
        if config.has_option('SITE', 'short_title'):
            self.short_title = config.get('SITE', 'short_title')
        else:
            self.short_title = "MiG"
        if config.has_option('SITE', 'base_menu'):
            menus = ['default', 'simple', 'advanced']
            req = config.get('SITE', 'base_menu').split()
            self.site_base_menu = [i for i in req if i in menus]
        else:
            self.site_base_menu = ['default']
        if config.has_option('SITE', 'default_menu'):
            req = config.get('SITE', 'default_menu').split()
            self.site_default_menu = [i for i in req if menu_items.has_key(i)]
        else:
            self.site_default_menu = ['dashboard', 'submitjob', 'files',
                                      'jobs', 'vgrids', 'resources',
                                      'downloads', 'runtimeenvs', 'people',
                                      'settings', 'docs', 'logout']
        if config.has_option('SITE', 'simple_menu'):
            req = config.get('SITE', 'simple_menu').split()
            self.site_simple_menu = [i for i in req if menu_items.has_key(i)]
        else:
            self.site_simple_menu = ['dashboard', 'files', 'vgrids',
                                     'settings', 'logout']
        if config.has_option('SITE', 'advanced_menu'):
            req = config.get('SITE', 'advanced_menu').split()
            self.site_advanced_menu = [i for i in req if menu_items.has_key(i)]
        else:
            self.site_advanced_menu = ['dashboard', 'submitjob', 'files',
                                      'jobs', 'vgrids', 'resources',
                                      'downloads', 'runtimeenvs', 'people',
                                      'settings', 'vmachines', 'shell', 'docs',
                                       'logout']
        if config.has_option('SITE', 'user_menu'):
            req = config.get('SITE', 'user_menu').split()
            self.site_user_menu = [i for i in req if menu_items.has_key(i)]
        else:
            self.site_user_menu = []
        if config.has_option('SITE', 'vgrid_links'):
            self.site_vgrid_links = config.get('SITE', 'vgrid_links').split()
        else:
            self.site_vgrid_links = ['files', 'web', 'tracker', 'workflows',
                                     'monitor']
        if config.has_option('SITE', 'vgrid_creators'):
            req = config.get('SITE', 'vgrid_creators').split()
            self.site_vgrid_creators = [i.split(':', 2) for i in req]
        if config.has_option('SITE', 'script_deps'):
            self.site_script_deps = config.get('SITE', 'script_deps').split()
        else:
            self.site_script_deps = []
        if config.has_option('SITE', 'external_doc'):
            self.site_external_doc = config.get('SITE', 'external_doc')
        else:
            self.site_external_doc = "http://code.google.com/p/migrid/wiki/FrontPage"
        if config.has_option('SITE', 'enable_wsgi'):
            self.site_enable_wsgi = config.getboolean('SITE', 'enable_wsgi')
        else:
            self.site_enable_wsgi = False
        if config.has_option('SITE', 'enable_griddk'):
            self.site_enable_griddk = config.getboolean('SITE', 'enable_griddk')
        else:
            self.site_enable_griddk = False
        if config.has_option('SITE', 'enable_sandboxes'):
            self.site_enable_sandboxes = config.getboolean('SITE', 'enable_sandboxes')
        else:
            self.site_enable_sandboxes = False
        if config.has_option('SITE', 'enable_sftp'):
            self.site_enable_sftp = config.getboolean('SITE', 'enable_sftp')
        else:
            self.site_enable_sftp = False
        if config.has_option('SITE', 'enable_davs'):
            self.site_enable_davs = config.getboolean('SITE', 'enable_davs')
        else:
            self.site_enable_davs = False
        if config.has_option('SITE', 'enable_ftps'):
            self.site_enable_ftps = config.getboolean('SITE', 'enable_ftps')
        else:
            self.site_enable_ftps = False
        if config.has_option('SITE', 'enable_openid'):
            self.site_enable_openid = config.getboolean('SITE', 'enable_openid')
        else:
            self.site_enable_openid = False
        if config.has_option('SITE', 'enable_vmachines'):
            self.site_enable_vmachines = config.getboolean('SITE',
                                                           'enable_vmachines')
        else:
            self.site_enable_vmachines = False
        if config.has_option('SITE', 'enable_freeze'):
            self.site_enable_freeze = config.getboolean('SITE', 'enable_freeze')
        else:
            self.site_enable_freeze = False
        if config.has_option('SITE', 'permanent_freeze'):
            self.site_permanent_freeze = config.getboolean('SITE',
                                                           'permanent_freeze')
        else:
            self.site_permanent_freeze = True
        # Fall back to a static 'random' salt string since we need it to
        # remain constant
        static_rand = 'w\xff\xcft\xaf/\x089 B\x1eG\x84i\x97a'
        self.site_digest_salt = base64.b16encode(static_rand)
        if config.has_option('SITE', 'digest_salt'):
            # Salt must be upper case hex
            salt = config.get('SITE', 'digest_salt').upper()
            try:
                _ = base64.b16decode(salt)                
                self.site_digest_salt = salt
            except:
                raise ValueError("Invalid digest_salt value: %s" % salt)

        if config.has_option('SITE', 'swrepo_url'):
            self.site_swrepo_url = config.get('SITE', 'swrepo_url')
        else:
            self.site_swrepo_url = ''
        if config.has_option('SITE', 'default_css'):
            self.site_default_css = config.get('SITE', 'default_css')
        else:
            self.site_default_css = '%s/default.css' % self.site_styles
        if config.has_option('SITE', 'custom_css'):
            self.site_custom_css = config.get('SITE', 'custom_css')
        else:
            self.site_custom_css = '%s/site-custom.css' % self.site_styles
        if config.has_option('SITE', 'user_css'):
            self.site_user_css = config.get('SITE', 'user_css')
        else:
            self.site_user_css = '%s/.default.css' % self.site_user_redirect
        if config.has_option('SITE', 'fav_icon'):
            self.site_fav_icon = config.get('SITE', 'fav_icon')
        else:
            self.site_fav_icon = '%s/MiG-favicon.ico' % self.site_images
        if config.has_option('SITE', 'logo_text'):
            self.site_logo_text = config.get('SITE', 'logo_text')
        else:
            self.site_logo_text = "Minimum intrusion Grid"
        if config.has_option('SITE', 'logo_image'):
            self.site_logo_image = config.get('SITE', 'logo_image')
        else:
            self.site_logo_image = '%s/MiG-logo-small.png' % self.site_images
        if config.has_option('SITE', 'credits_text'):
            self.site_credits_text = config.get('SITE', 'credits_text')
        else:
            self.site_credits_text = '2003-2014, <a href="http://www.migrid.org">The MiG Project</a>'
        if config.has_option('SITE', 'credits_image'):
            self.site_credits_image = config.get('SITE', 'credits_image')
        else:
            self.site_credits_image = '%s/copyright.png' % self.site_images

        # set test modes if requested

        if config.has_option('GLOBAL', 'enable_server_dist'):
            try:
                self.enable_server_dist = config.getboolean('GLOBAL',
                        'enable_server_dist')
            except:
                logger.error('enable_server_dist: expected True or False!'
                             )

        # Only parse server dist options if actually enabled

        if self.enable_server_dist:
            logger.info('enabling server distribution')

            if config.has_option('GLOBAL', 'peerfile'):
                peerfile = config.get('GLOBAL', 'peerfile')
                self.peers = self.parse_peers(peerfile)

            if config.has_option('GLOBAL', 'migrate_limit'):
                self.migrate_limit = config.get('GLOBAL',
                        'migrate_limit')

            if config.has_option('GLOBAL', 'expire_peer'):
                self.expire_peer = config.getint('GLOBAL', 'expire_peer'
                        )

            # configure certs and keys

            if config.has_option('GLOBAL', 'server_cert'):
                self.server_cert = config.get('GLOBAL', 'server_cert')
            if config.has_option('GLOBAL', 'server_key'):
                self.server_key = config.get('GLOBAL', 'server_key')
            if config.has_option('GLOBAL', 'passphrase_file'):
                self.passphrase_file = config.get('GLOBAL',
                        'passphrase_file')
            ca_path = ''
            if config.has_option('GLOBAL', 'ca_path'):
                ca_path = config.get('GLOBAL', 'ca_path')
                if os.path.isdir(ca_path):
                    self.ca_dir = ca_path
                elif os.path.isfile(ca_path):
                    self.ca_file = ca_path
                else:
                    logger.error('ca_path is neither a file or directory!'
                                 )
        # Force absolute log paths

        for log_var in ('user_sftp_log', 'user_davs_log', 'user_ftps_log',
                        'user_openid_log', 'user_events_log'):
            log_path = getattr(self, log_var)
            if not os.path.isabs(log_path):
                setattr(self, log_var, os.path.join(self.log_dir, log_path))
            
        # cert and key for generating a default proxy for nordugrid/ARC resources 

        if config.has_option('GLOBAL', 'nordugrid_cert'):
            self.nordugrid_cert = config.get('GLOBAL', 'nordugrid_cert')
        if config.has_option('GLOBAL', 'nordugrid_key'):
            self.nordugrid_key = config.get('GLOBAL', 'nordugrid_key')
        if config.has_option('GLOBAL', 'nordugrid_proxy'):
            self.nordugrid_proxy = config.get('GLOBAL', 'nordugrid_proxy')


        # if usage record dir is configured, generate them:

        if config.has_option('GLOBAL', 'usage_record_dir'):
            self.usage_record_dir = config.get('GLOBAL',
                    'usage_record_dir')

        # Automatic creation of users with a valid certificate

        if config.has_option('GLOBAL', 'auto_add_cert_user'):
            self.auto_add_cert_user = config.getboolean('GLOBAL',
                    'auto_add_cert_user')
        if config.has_option('GLOBAL', 'auto_add_oid_user'):
            self.auto_add_oid_user = config.getboolean('GLOBAL',
                    'auto_add_oid_user')
        if config.has_option('GLOBAL', 'auto_add_resource'):
            self.auto_add_resource = config.getboolean('GLOBAL',
                    'auto_add_resource')

        # if arc cluster URLs configured, read them in:

        if config.has_option('ARC', 'arc_clusters'):
            self.arc_clusters = config.get('ARC',
                    'arc_clusters').split()

    def parse_peers(self, peerfile):

        # read peer information from peerfile

        logger = self.logger
        peers_dict = {}
        peer_conf = ConfigParser()

        try:
            peer_conf.read([peerfile])
            for section in peer_conf.sections():

                # set up defaults

                peer = {
                    'protocol': 'https',
                    'fqdn': 'no-such-mig-host.net',
                    'port': '443',
                    'migrate_cost': '1.0',
                    'rel_path': 'status',
                    }
                for (key, val) in peer_conf.items(section):
                    peer[key] = val

                    peers_dict[section] = peer
                    logger.debug('Added peer: %s', peer['fqdn'])
        except:

            logger.error('parsing peer conf file: %s', peerfile)

            # Show exception details

            logger.error('%s: %s', sys.exc_info()[0], sys.exc_info()[1])

        logger.info('Added %d peer(s) from %s', len(peers_dict.keys()),
                    peerfile)
        return peers_dict


if '__main__' == __name__:
    conf = \
        Configuration(os.path.expanduser('~/mig/server/MiGserver.conf'
                      ), True)
