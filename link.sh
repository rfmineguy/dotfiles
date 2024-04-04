#!/bin/bash
readonly TARGET_COUNT=3
targets=(nvim qtile tmux)
linkdirs=(~/.config/nvim ~/.config/qtile ~/.tmux.conf)

function fail_if_invalid_target() {
	for t in ${targets[@]}; do
		if [[ $t == $1 ]]; then
			return 1
		fi
	done
	echo "Target '$1' not a valid target choice"
	usage
	exit
}

function get_target_linkdir() {
	fail_if_invalid_target $1
	for i in $(seq 0 $(($TARGET_COUNT - 1))); do
		if [[ ${targets[$i]} == $1 ]]; then
			linkdir=${linkdirs[$i]}
		fi
	done
}

function usage() {
	printf "Usage:\n"
	printf "===================================================\n"
	printf "  ./links.sh create <target>\n"
	printf "  ./links.sh remove <target>\n"
	printf "  ./links.sh getlinkdir <target>\n"
	printf "===========+=======================================\n"
	printf "Target     | Linkdir     \n"
	printf "===========+=======================================\n"
	for i in $(seq 0 $(($TARGET_COUNT - 1))); do
		printf "%-10s | %-10s\n" ${targets[i]} ${linkdirs[i]}
	done
	exit
}

#
# This function is called whenever creating a new symlink to
#   ensure no damage is done if accidentally run for any
#   reason
#
function fail_if_exists() {
	if test -d $1 || test -e $1; then
		echo "This script avoids the responsibility of accidentally overwriting your shit if it exists."
		echo "$1 exists in this case, so manually create a backup to continue"
		exit
	fi
}

function fail_if_not_symlink() {
	if [[ ! -L "$1" ]]; then
		echo "Error: cannot remove $1. It's not a symlink."
		exit
	fi
}

#
# This function will create a symbolic link from this repo's contents into the
# 	appropriate config directory
# For safety is always invokes 'fail_if_exists' to ensure no damage to your system
#   is done
#
function createSymlink() {
	get_target_linkdir $1
	fail_if_exists $linkdir

 	ln -s $(realpath $1) $linkdir
  echo "Created symlink to : $(realpath $XDG_CONFIG_HOME)/$1"
} 

function removeSymlink() {
	get_target_linkdir $1
	fail_if_not_symlink $linkdir

	unlink $linkdir
	echo "Remove symlink for : $linkdir"
}

case $1 in
	'create')
		createSymlink $2
		;;

	'remove')
		removeSymlink $2
		;;

	'getlinkdir')
		get_target_linkdir $2
		echo $linkdir
		;;
	
	*)
		echo "'$1' is not a valid subcommand" >&2
		usage
		;;
esac
