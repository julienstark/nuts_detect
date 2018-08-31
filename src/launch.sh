#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do

  key="$1"

  case $key in
    -n|--number)
      NUMBER="$2"
      shift
      shift
      ;;
    -i|--iter)
      ITER="$2"
      shift
      shift
      ;;
    -s|--scale)
      SCALE="$2"
      shift
      shift
      ;;
    -t|--threshold)
      THRESHOLD="$2"
      shift
      shift
      ;;
    -f|--filename)
      FILENAME="$2"
      shift
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

source setup_env.sh

python3 main.py -n $NUMBER -i $ITER -s $SCALE -t $THRESHOLD -f $FILENAME
