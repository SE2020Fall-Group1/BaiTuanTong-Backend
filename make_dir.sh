#!/usr/bin/env bash
mkdir -p "logs"
for dir in user club
do
  mkdir -p "static/images/tiny/$dir"
  mkdir -p "static/images/$dir"
done
