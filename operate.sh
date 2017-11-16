#!/bin/bash
#


usage() {
    echo $"Usage: $0 {start|rebuild}  -  container operation"
    exit 1
}


case "$1" in
	start)
		export GRAMPSDIR=`pwd`
		export GRAMPSI18N=build/mo/
		export LANGUAGE=zh_TW
		export LANG=zh_TW.UTF-8
		python3 Gramps.py 
		;;
	rebuild)
		python3 setup.py build
	    ;;
	*)  
	    usage
	    ;;
esac

