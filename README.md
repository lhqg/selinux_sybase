![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/hubertqc/selinux_sybase)
[![License](https://img.shields.io/badge/License-GPL%203--Clause-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![GitHub issues](https://img.shields.io/github/issues/hubertqc/selinux_sybase)](https://github.com/hubertqc/selinux_sybase/issues)
[![GitHub PR](https://img.shields.io/github/issues-pr/hubertqc/selinux_sybase)](https://github.com/hubertqc/selinux_sybase/pulls)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/hubertqc/selinux_sybase)](https://github.com/hubertqc/selinux_sybase/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/hubertqc/selinux_sybase)](https://github.com/hubertqc/selinux_sybase/commits/main)
![GitHub Downloads](https://img.shields.io/github/downloads/hubertqc/selinux_sybase/total)]


# SElinux policy module for Sybase ASE

<https://github.com/hubertqc/selinux_sybase>

## Table of Contents

1. [Introduction](#introduction)
2. [How to use this SELinux module](#how-to-use-this-selinux-module)
    * [Filesystem labelling](#filesystem-labelling)
    * [Networking](#networking)
        * [Listen port](#listen-port)
    * [SELinux booleans](#selinux-booleans)
    * [Starting the Sybase ASE processes](#starting-the-sybase-ase-processes)
        * [Systemd service units](#systemd-service-units)
        * [Systemd target units](#systemd-target-units)
3. [Disclaimer](#disclaimer)

## Introduction

This SELinux policy module aims to both protext Sybase ASE instances/databases and to prevent
them to perform unexpected actions on a Linux host.

It should be used when the Sybase ASE database is possibly exposed to a world full of
 *bad guys*, or just when the database contents must be proctected from unauthorised access
 at the operating system level.

The module should prevent the Sybase ASE processes from going rogue, and should the server be
compromised by an attacker this SELinux policy module should help limit the damage on the
system on which the database is hosted.

When used correctly, this SELinux policy module will make the Sybase ASE server processes
run on the host in the dedicated `sybase_t` SELinux domain.

IMPORTANT: please note that this module is still WORK IN PROGRESS

    * the SELinux context the Sybase ASE server processes are defined as *permissive* in order to avoid SELinux preventing normal operations of the database instance.
    * Use it AT YOUR OWN RISKS on production critical environments
    * Your feed back is highly valued

## How to use this SELinux module

Once the SELinux policy module is compiled and installed in the running Kernel SELinux
 policy, a few actions must be taken for the new policy to apply to the Sybase ASE server
 installation and to the database files and devices.
 
The policy can be adjusted with a handfull of SELinux booleans.

### Filesystem labelling

This SELinux policy module SELinux file context definitions are based on the Filesystem
Hierarchy Standards [https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard].

The root for the Sybase ASE engine installation is expected to be /opt/sybase.
The root for log files of the Sybase ASE servers is expected to be
 /var/log/sybase.
The root for Sybase database files is expected to be /srv/sybase or /var/lib/sybase.

When using raw devices to store the database contents, the special device character file
 should be located in /dev/sybase.

Should you prefer to use a different directory structure, you should consider using
SELinux fcontext equivalence rules to map your specifics to the filesystem layout expected
in the policy module, using the `semanage fcontext -a -e ORIGINAL CUSTOMISATION` command.

### Networking

#### Listen port

The TCP ports the various Sybase ASE server processes bind and listen to MUST be assigned the
 `sybase_port_t` SELinux type.

#### SELinux booleans

### Starting the Sybase ASE processes

#### Systemd service units

The systemd service unit file must be labbeled with the `sybase_unit_file_t` SELinux file type.

#### Systemd units RPM

The `sybase-systemd` RPM contains multiple systemd units definition.

Template systemd units are available to manage processes for a given Sybase ASE server instance:

* the sybase-env@SERVER1.service unit generates/refreshes the /run/sybase/env/SERVER1/systemd-env environment file for the Sybase ASE SERVER1 server,
* the sybase-dataserver@SERVER1.service unit controls the Sybase ASE dataserver process for the SERVER1 server,
* the sybase-backupserver@SERVER1.service unit controls the Sybase ASE backupserver process for the SERVER1 server,
* then sybase@SERVER1.target unit coordinates all three previous units for the Sybase ASE SERVER1 server.

Global systemd units are available to manage at once all processes of all Sybase ASE servers defined on the host.

## Disclaimer

The code of the this SELinux policy module is provided AS-IS. People and organisation
willing to use it must be fully aware that they are doing so at their own risks and
expenses.

The Author(s) of this SELinux policy module SHALL NOT be held liable nor accountable, in
 any way, of any malfunction or limitation of said module, nor of the resulting damage, of
 any kind, resulting, directly or indirectly, of the usage of this SELinux policy module.

It is strongly advised to always use the last version of the code, to check for the
compatibility of the platform where it is about to be deployed, to compile the module on
the target specific Linux distribution and version where it is intended to be used.

Finally, users should check regularly for updates.
