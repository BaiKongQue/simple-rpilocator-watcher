# simple-rpilocator-watcher
Starts up a headless browser and watches the https://rpilocator.com/ website every x minutes.

Currently only supported on windows

# Requirements
This script was made in python 3.8.6, you will need python 3+ to run this.

The following libraries were used and need to be installed on your system in order for this script to run:
<table>
  <tr>
    <td>Selenium 4.1.3</td>
    <td>pip install selenium</td>
  </tr>
  <tr>
    <td>pywin32 303</td>
    <td>pip install pywin32</td>
  </tr>
</table>

# How to
To run the program just run the `pi_watch.py` file.

You will be presented with a menu where you can change any settings. A `options.json` file will be created to save your options for the next time you start it up again.

Once you have configured everything to your liking, use the option to run the program and leave it idle. It will run infinitely until closed or exitted.

When the rpilocator website has a match to your liking, the script will ring the windows notification sound three times if you have the sound option on, and/or it will prompt you if you have the notification option on.

to end the infinite loop use the keyboard interrupt key and wait for the program to properly close the headless browser. Once it finishes closing you will be back at the main menu where to can choose to close the program or change any options and run it again.
