#!/bin/bash
#
# This file is part of monfetch, a remote system monitoring tool based on the
# conecpt of fetch programs.
#
# Copyright (c) 2021 Emily <elishikawa@jagudev.net>
# This program is provided under the AGPL-3.0 License. See LICENSE for more details.

# Load config
. ./config.sh

# Vars that'll remain the same through the entire run
hostname="$(hostname ${HOSTNAMEARGS})"
chassis="$(cat /sys/devices/virtual/dmi/id/product_name)"
get_os() {
    . /etc/os-release
    os="${PRETTY_NAME}"
}
get_cpu() {
    cpu="$(grep -i 'model name' /proc/cpuinfo | head -1 | cut -f3- -d' ')"
    cpucore="$(nproc)"
    cpufreq="$(cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq)"
    cpu+=" (${cpucore}) @ ${cpufreq} KHz"
}
get_os
get_cpu

get_kern() {
    kernel="$(uname -r)"
}

get_sh() {
    shell="$(basename ${SHELL})"
}

get_pkgs() {
    if [ -x "$(command -v apk)" ]; then
        pkgs="$(apk info | wc -l)"
        pkgs+=" (apk)"
    fi
    if [ -x "$(command -v dpkg)" ]; then
        pkgs="$(dpkg -l | grep -c ^i)"
        pkgs+=" (dpkg)"
    fi
    if [ -x "$(command -v dnf)" ]; then
        pkgs="$(dnf list installed | sed '1d' | wc -l)"
        pkgs+=" (dnf)"
    fi
    if [ -x "$(command -v emerge)" ]; then
        pkgs="$(ls -d /var/db/pkg/*/* | wc -l)"
        pkgs+=" (emerge)"
    fi
    if [ -x "$(command -v nix)" ]; then
        pkgs="$(ls -d -1 /nix/store/*/ | wc -l)"
        pkgs+=" (nix)"
    fi
    if [ -x "$(command -v rpm)" ]; then
        pkgs="$(rpm -qa --last | wc -l)"
        pkgs+=" (rpm)"
    fi
    if [ -x "$(command -v xbps)" ]; then
        pkgs="$(xbps-query -l | wc -l)"
        pkgs+=" (xbps)"
    fi
    if [ -x "$(command -v yum)" ]; then
        pkgs="$(yum list installed | wc -l)"
        pkgs+=" (yum)"
    fi
    if [ -x "$(command -v zypper)" ]; then
        pkgs="$(zypper se -i | wc -l)"
        pkgs+=" (zypper)"
    fi
}

get_disk() {
    disk="$(df -h 2> /dev/null | awk '/\/$/ {print $3 " / " $2 " (" $5 ")"}')"
}

get_thermals() {
    if [ -d /sys/class/thermal/thermal_zone0 ]; then
        thermals="$(cat /sys/class/thermal/thermal_zone0/temp | head -n1)"
    else
        thermals="0"
    fi
}

get_mem() {
    memavail="$(grep MemAvailable /proc/meminfo | awk '{print $2}')"
    memtotal="$(grep MemTotal /proc/meminfo | awk '{print $2}')"
    memused=$((memtotal - memavail))

    ((memused /= 1024))
    ((memtotal /= 1024))

    mem="${memused} MiB / ${memtotal} MiB"
}

get_load() {
    read -r load1 load5 load15 _ _ < /proc/loadavg
}

get_uptime() {
    read -r uptime _ < /proc/uptime
}

run() {
    while true; do
        get_kern
        get_sh
        get_pkgs
        get_disk
        get_thermals
        get_mem
        get_load
        get_uptime

        curl --silent -X POST "http://$SERVER/$AUTH/$hostname" -F "chassis=$chassis" -F "os=$os" -F "cpu=$cpu" -F "kernel=$kernel" -F "shell=$shell" -F "pkgs=$pkgs" -F "disk=$disk" -F "thermals=$thermals" -F "mem=$mem" -F "load1=$load1" -F "load5=$load5" -F "load15=$load15" -F "uptime=$uptime"
        sleep "$INTERVAL"
    done
}

run
