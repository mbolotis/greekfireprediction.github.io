@ECHO OFF
CD fire_data/greek_fire_data
set "year_start=2000"
set "year_end=2020"
echo ON
for /l %%x in (%year_start%, 1, %year_end%) do (
	echo %%x
	mkdir %def_prefix%%%x
)
PAUSE