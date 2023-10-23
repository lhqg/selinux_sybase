#!/bin/bash
#########################################################
#                                                       #
#			SELinux Sybase policy module			                #
#                                                       #
#	Restore fcontext script:							                #
#		This script restores SELinux fcontexts.			        #
#                                                       #
#    https://github.com/hubertqc/selinux_sybase		      #
#                                                       #
#########################################################

typset -i RC
RC=0

if selinuxenabled
then
  restorecon -RFi /{opt,srv,home}/sybase 
  restorecon -RFi /{lib,etc}/systemd/system/sybase*
  restorecon -RFi /var/{lib,log,run,tmp,opt}/sybase
else
	echo "SElinux is not enabled, unable to restore fcontext."
	RC=1
fi

exit $RC