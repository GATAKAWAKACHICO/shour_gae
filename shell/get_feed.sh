#!/bin/sh
curl -F user_id=$1 -F password=$2 http://localhost:8080/feeds/$3