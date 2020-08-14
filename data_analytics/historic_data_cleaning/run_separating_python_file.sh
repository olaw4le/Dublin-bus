#!/bin/bash

files=(
Leavetimes10_Cleaned.csv
Leavetimes11_Cleaned.csv
Leavetimes12_Cleaned.csv
Leavetimes13_Cleaned.csv
Leavetimes14_Cleaned.csv
Leavetimes15_Cleaned.csv
Leavetimes16_Cleaned.csv
Leavetimes17_Cleaned.csv
Leavetimes18_Cleaned.csv
Leavetimes19_Cleaned.csv
Leavetimes1_Cleaned.csv
Leavetimes20_Cleaned.csv
Leavetimes21_Cleaned.csv
Leavetimes22_Cleaned.csv
Leavetimes23_Cleaned.csv
Leavetimes24_Cleaned.csv
Leavetimes25_Cleaned.csv
Leavetimes26_Cleaned.csv
Leavetimes27_Cleaned.csv
Leavetimes28_Cleaned.csv
Leavetimes29_Cleaned.csv
Leavetimes2_Cleaned.csv
Leavetimes30_Cleaned.csv
Leavetimes31_Cleaned.csv
Leavetimes32_Cleaned.csv
Leavetimes33_Cleaned.csv
Leavetimes34_Cleaned.csv
Leavetimes35_Cleaned.csv
Leavetimes36_Cleaned.csv
Leavetimes37_Cleaned.csv
Leavetimes38_Cleaned.csv
Leavetimes39_Cleaned.csv
Leavetimes3_Cleaned.csv
Leavetimes40_Cleaned.csv
Leavetimes41_Cleaned.csv
Leavetimes42_Cleaned.csv
Leavetimes43_Cleaned.csv
Leavetimes44_Cleaned.csv
Leavetimes45_Cleaned.csv
Leavetimes46_Cleaned.csv
Leavetimes47_Cleaned.csv
Leavetimes48_Cleaned.csv
Leavetimes49_Cleaned.csv
Leavetimes4_Cleaned.csv
Leavetimes50_Cleaned.csv
Leavetimes51_Cleaned.csv
Leavetimes52_Cleaned.csv
Leavetimes53_Cleaned.csv
Leavetimes5_Cleaned.csv
Leavetimes6_Cleaned.csv
Leavetimes7_Cleaned.csv
Leavetimes8_Cleaned.csv
Leavetimes9_Cleaned.csv
)

route_files=(Eighteen.csv FortySixE.csv Seventeen.csv ThirtyNineA.csv)


for i in "${route_files[@]}"; do
    	python3 separate_data_by_bus_route_plus_new_features.py "$i" Leavetimes0_Cleaned.csv initial
	echo "$i" + "processed for Leavetimes0_Cleaned.csv"
done

for i in "${route_files[@]}"; do
    for j in "${files[@]}"; do
    	python3 separate_data_by_bus_route_plus_new_features.py "$i" "$j" foo
    done

	echo "$i" + "processed for" + "$j"
done
