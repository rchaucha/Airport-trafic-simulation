
---------- run.bat ----------

@echo off

FOR /L %%i IN (80000, 5000, 90000) DO 	(
	(
		echo PAS = 5                      #s
		echo RAYON_ROUE = 0.56            #m
		echo COUPLE_MAX_EGTS = 16000      #N.m
		echo PUISSANCE_EGTS = %%i       #W
		echo BREAKAWAY_RESISTANCE = 0.01  #daN/kg
		echo ROLLING_RESISTANCE = 0.007   #daN/kg
		echo COEF_AERO = 1.032
		echo PAS_MODELE = 4.1             #s
	) > donnees.py
	
	ping 127.0.0.1 -n 4 > nul

	py simulation.py
)
