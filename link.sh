#!/bin/bash

function usage() {
	echo "Usage:"
	echo "  ./links.sh create <target>"
	echo "  ./links.sh remove <target>"
	echo "Targets:"
	echo "  nvim"
}

#
# This function is called whenever creating a new symlink to
#   ensure no damage is done if accidentally run for any
#   reason
#
function fail_if_exists() {
	if test -d $1; then
		echo "This script avoids the responsibility of accidentally overwriting your shit if it exists."
		echo "$1 exists in this case, so manually create a backup to continue"
		exit
	fi
}

function fail_if_config_not_defined() {
	# Check to see if a config directory is defined
	if [[ -z "$XDG_CONFIG_HOME" ]]; then
		echo "Error: This script relies on \$XDG_CONFIG_HOME being defined" >&2
		echo "Error:   A common location for this is ~/.config" >&2
		echo "To set this variable run `export XDG_CONFIG_HOME=\<directory\>`"
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
	local FULL_PATH
	FULL_PATH="$XDG_CONFIG_HOME/$1"
	fail_if_exists $FULL_PATH

	ln -s $(realpath $1) $(realpath $XDG_CONFIG_HOME)/$1
	echo "Created symlink to : $(realpath $XDG_CONFIG_HOME)/$1"
}

function removeSymlink() {
	local FULL_PATH
	FULL_PATH="$XDG_CONFIG_HOME/$1"
	echo $FULL_PATH
	fail_if_not_symlink $FULL_PATH

	unlink $(realpath $XDG_CONFIG_HOME)/$1
	echo "Remove symlink for : $(realpath $XDG_CONFIG_HOME)/$1"
}

fail_if_config_not_defined
case $1 in
	'create')
		createSymlink $2
		;;

	'remove')
		removeSymlink $2
		;;
	
	*)
		echo "'$1' is not a valid subcommand" >&2
		usage
		;;
esac
