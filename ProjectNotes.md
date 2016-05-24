# Project: Loader Controller


# Purpose:
Prevent the material loader from loading the wrong material into a press based on the BOM/Work order.


# Solution:
- Use a mini computer (MPC), a barcode scanner, and a solid state relay (SSR) to control the material loader.
    + Raspberry Pi
- Setup detection for the loader outlet (button, IR beam?).
- Setup detection for the raw material container (whisker, proximity switch).


# Steps:
- A Solid State Relay is installed between the AC power source and the loader in a Normally-Open (off) state.
- Scan the current workorder barcode.  The MPC will query the IQMS database to check the following.
    + Is this workorder in the first position on this press (ie., is it currently being produced)?  [The Press ID will be static in the MPC]
    + If yes, return the Raw Material Item Number that should be used to make this part.  If not, fail and restart.
- Scan the Raw Material Serial Number Barcode (add a qualifier check).
    + Query IQMS for the Item Number associated with the Serial Number.
    + Compare the stored RM Item Number from IQ with the scanned Item Number.
- If the material matches the part currently being produced then send a signal to the SSR to allow AC power to the loader.
- Continue running until one of the following conditions are met:
    + Loader plug is removed from the outlet.
    + The Raw Material container is removed from its staging location.


# Hardware Parts List and Notes:
##### Loader Power Control:
- AC power is controlled by a Powertail Switch II (PTS) device.  A signal from the MPC will trigger the PTS on when all logic passes.
- ~~A non-invasive current sensor (split core Current Transformer [CT]) will detect the presence of AC power coming out of the PTS.  It will know when the loader is unplugged (or power is lost through the PTS).~~  This will not work because the loader is not constantly on.  It turns on when more material is required.
- A 3.3V (or 5V leveled to 3.3V) power adapter will be plugged into the output of the PTS.  The 3.3VDC output is sent to the MPC to determine the state of the AC output loadline on the PTS.
    + If the MPC signal is HIGH and the power adapter signal goes low, turn off the MPC signal, turning off the loader and resetting the whole process.

##### LCD Feedback:
- Keep the user informed of the current state of the loader (running/stopped) and the current step in the validation process.
    + Scan Workorder
    + Scan Raw Material

##### Parts List:
- Raspberry Pi 2 (MPC)
- Barcode scanner, USB wired (Use the manual to program the scanner to suffix an <ENTER> [page 13-5])
- Powertail Switch II, isolated DC actuated AC power switch
- 3.3VDC power adapter and divider circuit (2-10K resistors)
- ~~Non-Invasive Current Sensor (split core current transformer), SF# SEN-11005~~
- ~~Analog-to-Digital Converter, MCP3002, SF# COM-08636 (for the CT)~~


# Software Logic and Notes:
- The MPC will prompt the user to scan the workorder barcode.
- The MPC will capture the workorder number from the barcode scanner.
- The MPC will send the workorder number in the form of a JSON request to the web service.
- The Web Service (Flask?) running on a VM server will query the database.
- The web service will reply with the RM item number.
- The MPC will compare the Work Center ID to the Press it is currently assigned.
    + If this fails the user is notified and the program returns to step one.
    + If it passes it will continue.
- The MPC will store the returned information.
- The MPC will prompt the user to scan the raw material barcode.
- The MPC compares the stored information the scanned information.
- If it matches the loader control PIN will go HIGH.

##### Web Service Notes:
- Flask (flask-restless, flask-sqlalchemy, sqlacodegen) to query Oracle and return JSON.

##### MPC Client Notes:
- Python to read JSON into variables.

##### Fail Points:
- Network unavailable.
- Outlet button malfunction.
- Material is placed too far away from loader controller.  It will be too far away to rescan.



