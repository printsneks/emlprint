# emlprint
This project came about as a result of me needing a way to accurately figure out how long a 3d print takes. From a practical standpoint, I didn't like the idea of having prints end up running over night (noise) and from a safety point of view I didn't want to run it totally unattended. 

The slicer I was using at the time gave me poor estimates that usually were off by a lot. After doing some research I decided it'd make for an interesting test for linear regression.

I ended up looking for some clues inside the gcode files I had and found out the instructions were easy enough to parse. For my data I rely on changes in x/y and z along with travel distances. 

Initially to prototype whether it would work, I split the file into two managable programs. The first program would take data and spit out a formula I could plug into the second program. The second program would evaluate the gcode and run it through the formula. 

Once I had a skeleton, I populated the data set with short prints. After about prints, I ran a ~10 hour print to test it and was off by about 5%. That ended up being enough of a proof of concept for me to go about refactoring the program into just one to keep track of things. 

To make things as accurate as possible, you have to keep in mind that this program is measuring the movement of the extruder. The program doesn't know if you're moving a laser/rotor/extruder, its just coming up with the weight/bias of movements. What that means is you don't want to contaminate your dataset by changing any speed settings. 

# Description

Uses linear regression to determine how long a 3d Print will take based on the Gcode. 

# How to use


# How to install

Requires : 

-pandas
-sklearn
-seaborn

