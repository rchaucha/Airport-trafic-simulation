# Airport-trafic-simulation
This is a Python script that aims at measuring the impact of the use of electric motors for taxiing (EGTS) on travel duration during a day of traffic at Roissy airport.


## Description
This project was based on real data of the airport (3D coordinates of the airport and flights positions during a whole day) that are not available on this repository, however, the only file affected is filesManager.py.

This project allows to run simulations based on the percentage of flights equipped with EGTS, whether we take into account the slopes of the runways and the power of the EGTS.

To allow easier debug, I also made it possible to have a visual feedback of the airport with dynamic flights position, as you can see below (green dots are flights with EGTS, red ones are normal flights).

![Dynamic feedback](https://user-images.githubusercontent.com/18093026/105165323-1a122a80-5b0e-11eb-83d8-e9d718c2d53c.png)
