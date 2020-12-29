#!/usr/bin/env bash
mkdir -p "logs"
for dir in user club post
do
  mkdir -p "static/images/$dir"
done
for dir in user club
do
  mkdir -p "static/images/tiny/$dir"
done
