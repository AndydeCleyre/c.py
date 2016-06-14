#!/bin/sh

VERSION="0.5.2"

os_fail() {
    echo "Current Operating System not supported!"
    echo "Please file a bug at github: https://github.com/rumpelsepp/c.py"
    exit 1
}

usage() {
if [ "$(uname)" = "Linux" ]; then
    echo "Usage: $(basename $0) [-AbeEnstTuv] [-N] [-Vh] [file [file ...]] [--] [c.py options]"
    echo ""
    echo "cat(1) options:"
    echo "  -A,     equivalent to -vET"
    echo "  -b,     number nonempty output lines, overrides -n"
    echo "  -e      equivalent to -vE"
    echo "  -E,     display $ at end of each line"
    echo "  -n,     number all output lines"
    echo "  -s,     uppress repeated empty output lines"
    echo "  -t      equivalent to -vT"
    echo "  -T,     display TAB characters as ^I"
    echo "  -v,     use ^ and M- notation, except for LFD and TAB"
elif [ "$(uname)" = "FreeBSD" ]; then
    echo "Usage: $(basename $0) [-belnstuv] [-N] [-Vh] [file [file ...]] [--] [c.py options]"
    echo ""
    echo "cat(1) options:"
    echo "  -b,     Number the non-blank output lines, starting at 1"
    echo "  -e      Display non-printing characters and a '$' sign at the end of the line"
    echo "  -l      Set an exclusive advisory lock on stdout"
    echo "  -n,     Number all output lines, starting at 1"
    echo "  -s,     Squeeze multiple adjacent empty lines"
    echo "  -t      Display non-printing characters and tabs characters as '^I'"
    echo "  -u      Disable output buffering"
    echo "  -v,     Display non-printing characters so they are visible"
else
    os_fail
fi
    echo ""
    echo "less(1) options:"
    echo "  -N      show linenumbers"
    echo ""
    echo "c(1) options:"
    echo "  -p      do not use a pager"
    echo "  -V      show version string"
    echo "  -h      display this page and exit"
    echo ""
    echo "c.py options can be viewed with \"$(basename $0) -- -h\""
}

version() {
    echo "$(basename $0) $VERSION"
}

spawn_cpy() {
    # Only search a local "c.py" file when the environment
    # variable "C_DEV" is set to a non empty value.
    if [ -e "./c.py" ] && [ ! -z "$C_DEV" ]; then
        python "./c.py" "$@"
    elif which "c.py" >& /dev/null; then
        c.py "$@"
    else
        echo "c.py is not installed"
        echo "Leaving..."
        exit 1
    fi
}

if [ "$(uname)" = "Linux" ]; then
    while getopts "AbeEnstTuvNphV" arg; do
        case $arg in
            A)      CATOPTS="$CATOPTS -A";;
            b)      CATOPTS="$CATOPTS -b";;
            e)      CATOPTS="$CATOPTS -e";;
            E)      CATOPTS="$CATOPTS -E";;
            n)      CATOPTS="$CATOPTS -n";;
            s)      CATOPTS="$CATOPTS -s";;
            t)      CATOPTS="$CATOPTS -t";;
            T)      CATOPTS="$CATOPTS -T";;
            v)      CATOPTS="$CATOPTS -v";;
            N)      LESSOPTS="$LESSOPTS -N";;
            p)      C_NO_PAGER='y';;
            h)      usage;   exit 0;;
            V)      version; exit 0;;
        esac
    done

elif [ "$(uname)" = "FreeBSD" ]; then
    while getopts "belnstuvNphV" arg; do
        case $arg in
            b)      CATOPTS="$CATOPTS -b";;
            e)      CATOPTS="$CATOPTS -e";;
            l)      CATOPTS="$CATOPTS -l";;
            n)      CATOPTS="$CATOPTS -n";;
            s)      CATOPTS="$CATOPTS -s";;
            t)      CATOPTS="$CATOPTS -t";;
            u)      CATOPTS="$CATOPTS -u";;
            v)      CATOPTS="$CATOPTS -v";;
            N)      LESSOPTS="$LESSOPTS -N";;
            p)      C_NO_PAGER='y';;
            h)      usage;   exit 0;;
            V)      version; exit 0;;
        esac
    done

else
    os_fail
fi

shift $((OPTIND - 1))

# When c reads from stdin and is interactive, pager must be disabled.
# https://gist.github.com/davejamesmiller/1966557
if [ $# -gt 0 ] || [ ! -t 0 ] && [ -z "$C_NO_PAGER" ]; then
    pager=${C_PAGER:-${PAGER:-less}}
fi

# This behaviour is similar to git:
# https://github.com/git/git/blob/master/Documentation/config.txt#L646
if [ "$pager" = "less" ] && [ -z "$LESS" ]; then
    export LESS='FRX'
fi

if [ -z "$pager" ]; then
    if [ -z "$CATOPTS" ]; then
        spawn_cpy "$@"
    else
        spawn_cpy "$@" | cat $CATOPTS
    fi
else
    if [ -z "$CATOPTS" ]; then
        spawn_cpy "$@" | $pager $LESSOPTS
    else
        spawn_cpy "$@" | cat $CATOPTS | $pager $LESSOPTS
    fi
fi
