#!/bin/bash
si=`uuidgen`
serialnumber="$(cut -d'-' -f5 <<<"$si")"
echo $serialnumber
