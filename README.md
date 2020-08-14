#Chai Goyal's Bond Trading System

##How to traverse the code

The entire workflow of the system is described in "Bond Trading Project Monetary Base.ipynb"

Individually, the components are separated into Python files, as follows:
1. MonetaryBaseIndicator.py — creates daily signals for just a single country, using the MB indicator
2. GloballyNeutralIndicator.py —creates daily signals for 2 countries, using the MB indicator 
3. CreatePNL.py — used to easily convert signals to 
4. stats.py — abstracted statistics functions used in code
