# Makefile for libnss-mig

### Start MiG site variables
# You can leave MIG_DEFAULTS like this to read the values dynamically from
# your MiGserver.conf (or $MIG_CONF if set in service environment).
# If on the other hand you define the values here the PAM module will save a
# bit of time on each login, since it doesn't have to look them up in the file.
# In any case you can always override the values at runtime by setting the same
# environment variables when running sshd or whichever service you use the PAM
# module in.

# Leave like this to use module defaults - likely won't fit your installation!
#MIG_DEFAULTS=
# TODO: implement this conf lookup!!
# Leave like this to lookup values in $MIG_CONF or default MiGserver.conf .
#MIG_DEFAULTS=-D'SHARELINK_HOME=""' -D'SHARELINK_LENGTH=-1' -D'USERNAME_REGEX=""' 
# ... or hard code to your site values like this (NOTE: escaped dollar = '$$')
MIG_DEFAULTS=-D'SHARELINK_HOME="$(shell ~mig/mig/server/readconfval.py sharelink_home)"' \
	-D'SHARELINK_LENGTH=10' \
	-D'JOBSIDMOUNT_HOME="$(shell ~mig/mig/server/readconfval.py webserver_home)"' \
	-D'JOBSIDMOUNT_LENGTH=64' \
	-D'JUPYTERSIDMOUNT_HOME="$(shell ~mig/mig/server/readconfval.py sessid_to_jupyter_mount_link_home)"' \
	-D'JUPYTERSIDMOUNT_LENGTH=64' \
	-D'USERNAME_REGEX="^[a-zA-Z0-9][a-zA-Z0-9.@_-]{0,127}$$"'
### End of MiG site variables

#### Start of compiler configuration section ### 

DEBUG_DEFINES=
DEBUG_CFLAGS=
#DEBUG_DEFINES=-D'DEBUG'
#DEBUG_CFLAGS=-g

CC = gcc
INCLUDES=-I./
DEFINES=$(MIG_DEFAULTS) \
		$(DEBUG_DEFINES)
CFLAGS=-Wall \
	   -Wpedantic \
	   ${DEBUG_CFLAGS}
LDFLAGS= -shared

#### End of compiler configuration section ###

#### Start of system configuration section. ####

INSTALL = /usr/bin/install
INSTALL_PROGRAM = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

prefix = ""
exec_prefix = ${prefix}

# Where the installed binary goes.
bindir = ${exec_prefix}/bin
binprefix =

# Where the installed library goes.
# On deb systems NSS modules are stored in /lib/x86_64-linux-gnu/
# On rpm systems NSS modules go into /lib64/
# If on other platforms override nsslibdir with:
# nsslibdir=/path/to/dir/with/libnss_*.so make -e install
nsslibdir := $(shell dirname $(firstword $(wildcard /lib*/libnss_*.so /lib/*-linux-gnu/libnss_*.so)))
libdir = ${prefix}/${nsslibdir}
sysconfdir = /etc

# mandir = /usr/local/src/less-394/debian/less/usr/share/man
manext = 1
manprefix =

#### End of system configuration section. ####

all:	libnss_mig.so.2

libnss_mig.so.2:    libnss_mig.c
	${CC} -std=gnu99 -fPIC ${INCLUDES} ${DEFINES} ${CFLAGS} -o $@ $< ${LDFLAGS} 


install:	libnss_mig.so.2
	# remember  /lib64/libnss_mig.so.2 -> libnss_mig-2.3.6.so
	${INSTALL_DATA} libnss_mig.so.2 ${libdir}/libnss_mig-2.3.6.so
	cd ${libdir} && ln -fs libnss_mig-2.3.6.so libnss_mig.so.2

clean:
	rm -f libnss_mig.so.2
	rm -f build-stamp
