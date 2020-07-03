#!/bin/bash

route_files= /Users/laura/Desktop/Master-Route-Files/Eighteen_Master.csv


for i in "${route_files[@]}"; do
    	python3 getting-termini.py "$i"
	echo "$i" completed
done
