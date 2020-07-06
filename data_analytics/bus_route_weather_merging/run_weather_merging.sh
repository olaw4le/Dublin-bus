#!/bin/bash

route_files=(EightyFourA_Master.csv		SeventyD_Master.csv
EightyFourX_Master.csv		SeventyFive_Master.csv
EightyThreeA_Master.csv		SeventyNineA_Master.csv
EightyThree_Master.csv		SeventyNine_Master.csv
Eleven_Master.csv		SeventySevenA_Master.csv
FifteenA_Master.csv		SeventySevenX_Master.csv
FifteenB_Master.csv		SeventySixA_Master.csv
FifteenD_Master.csv		SeventySix_Master.csv
Fifteen_Master.csv		Seventy_Master.csv
FiftyFourA_Master.csv		SixteenC_Master.csv
FiftyNine_Master.csv		SixteenD_Master.csv
FiftyOneD_Master.csv		Sixteen_Master.csv
FiftyOneX_Master.csv		SixtyEightA_Master.csv
FiftySixA_Master.csv		SixtyEightX_Master.csv
FiftyThree_Master.csv		SixtyEight_Master.csv
FortyB_Master.csv		SixtyFiveB_Master.csv
FortyD_Master.csv		SixtyFive_Master.csv
FortyE_Master.csv		SixtyNineX_Master.csv
FortyFiveA_Master.csv		SixtyNine_Master.csv
FortyFourB_Master.csv		SixtyOne_Master.csv
FortyFour_Master.csv		SixtySevenX_Master.csv
FortyNine_Master.csv		SixtySeven_Master.csv
FortyOneA_Master.csv		SixtySixA_Master.csv
FortyOneB_Master.csv		SixtySixB_Master.csv
FortyOneC_Master.csv		SixtySixX_Master.csv
FortyOneD_Master.csv		SixtySix_Master.csv
FortyOneX_Master.csv		SixtyThree_Master.csv
FortyOne_Master.csv		Thirteen_Master.csv
FortySeven_Master.csv		ThirtyEightA_Master.csv
FortySixA_Master.csv		ThirtyEightB_Master.csv
FortySixE_Master.csv		ThirtyEightD_Master.csv
FortyThree_Master.csv		ThirtyEight_Master.csv
FortyTwoD_Master.csv		ThirtyNineA_Master.csv
FortyTwo_Master.csv		ThirtyNineX_Master.csv
Forty_Master.csv		ThirtyNine_Master.csv
Four_Master.csv			ThirtyOneA_Master.csv
FourteenC_Master.csv		ThirtyOneB_Master.csv
Fourteen_Master.csv		ThirtyOneD_Master.csv	ThirtyOne_Master.csv
Nine_Master.csv			ThirtySeven_Master.csv
OneEighteen_Master.csv		ThirtyThreeA_Master.csv
OneEightyFive_Master.csv	ThirtyThreeB_Master.csv
OneEightyFour_Master.csv	ThirtyThreeD_Master.csv
OneEleven_Master.csv		ThirtyThreeE_Master.csv
OneFiftyOne_Master.csv		ThirtyThreeX_Master.csv
OneFifty_Master.csv		ThirtyThree_Master.csv
OneFortyFive_Master.csv		ThirtyTwoX_Master.csv
OneFortyTwo_Master.csv		ThirtyTwo_Master.csv
OneForty_Master.csv		TwentyFiveA_Master.csv
OneFourteen_Master.csv		TwentyFiveB_Master.csv
OneOFour_Master.csv		TwentyFiveD_Master.csv
OneOTwo_Master.csv		TwentyFiveX_Master.csv
OneSixteen_Master.csv		TwentyFive_Master.csv
OneSixtyOne_Master.csv		TwentyNineA_Master.csv
OneThirty_Master.csv		TwentySevenA_Master.csv
OneTwentyThree_Master.csv	TwentySevenB_Master.csv
OneTwentyTwo_Master.csv		TwentySevenX_Master.csv
OneTwenty_Master.csv		TwentySeven_Master.csv
One_Master.csv			TwentySix_Master.csv
SevenA_Master.csv		TwoSeventy_Master.csv
SevenB_Master.csv		TwoThirtyEight_Master.csv
SevenD_Master.csv		TwoThirtyNine_Master.csv
Seven_Master.csv		TwoThirtySix_Master.csv
SeventeenA_Master.csv		TwoTwenty_Master.csv
Seventeen_Master.csv
)


for i in "${route_files[@]}"; do
        bus_file=~/Desktop/Master-Route-Files/"$i"
        python3 route_weather_merge.py "$bus_file" ~/Desktop/Trimester_3/research-project/data_analytics/weather_data_cleaning/combined_weather_data_historical.csv --write_to_file true
        echo "$i" + "processed."
done


