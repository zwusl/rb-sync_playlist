#!/bin/bash

#Thanks to Petko Ditchev. This code is taken from the playlists-import-export plugin
#   and there he #Thanks to David Mohammed. This code is taken from the coverart-browser plugin

################################ USAGE #######################################

usage=$(
cat <<EOF
Usage:
$0 [OPTION]
-h, --help      show this message.
-2, --rb2     install the plugin for rhythmbox version 2.96 to 2.99 .
-3, --rb3       install the plugin for rhythmbox 3 (default)
EOF
)

########################### OPTIONS PARSING #################################

#parse options
TMP=`getopt --name=$0 -a --longoptions=rb2,rb3,help -o 2,3,h -- $@`

if [[ $? == 1 ]]
then
    echo
    echo "$usage"
    exit
fi

eval set -- $TMP

until [[ $1 == -- ]]; do
    case $1 in
        -2|--rb2)
            RB=false
            ;;
        -3|--rb3)
            RB=true
            ;;
        -h|--help)
            echo "$usage"
            exit
            ;;
    esac
    shift # move the arg list to the next option or '--'
done
shift # remove the '--', now $1 positioned at first argument if any

#default values
RB=${RB:=true}

########################## START INSTALLATION ################################

SCRIPT_NAME=`basename "$0"`
SCRIPT_PATH=${0%`basename "$0"`}
PLUGIN_PATH="${HOME}/.local/share/rhythmbox/plugins/sync_playlist/"
GLIB_SCHEME="org.gnome.rhythmbox.plugins.sync_playlist.gschema.xml"
GLIB_DIR="${HOME}/.local/share/rhythmbox/plugins/sync_playlist/schemas/"

#build the dirs
mkdir -p $PLUGIN_PATH
mkdir -p $GLIB_DIR

#copy the files
cp -r "${SCRIPT_PATH}"* "$PLUGIN_PATH"

#install the plugin; the install path depends on the install mode
if [[ $RB == false ]]
then
    mv "$PLUGIN_PATH"sync_playlist.plugin2 "$PLUGIN_PATH"sync_playlist.plugin
fi

#remove the install script from the dir (not needed)
rm "${PLUGIN_PATH}${SCRIPT_NAME}"

#install translations
#cd po; sudo ./lang.sh /usr/share/locale/

#install the glib schema
if [ ! -f $GLIB_DIR$GLIB_SCHEME ]; then
    echo "Installing the glib schema" && cp "${PLUGIN_PATH}${GLIB_SCHEME}" "$GLIB_DIR" && glib-compile-schemas "$GLIB_DIR"
fi

read -p "Script execution ended, press [Enter] key to exit..."