# PiMVG
Using the Raspberry Pi to check Munich's public transport system
It uses the Command Line Interface (CLI) from rrmoritz's project [rmoriz/mvg-live](https://github.com/rmoriz/mvg-live#mvg-live)
to get the information from the mvg and filters it.

I still have to upload the part of the code that displays those times on an LED 8Segment display...

# Setup

## Install rmoriz/mvg-live
Follow his `README.md` to install his rubygem. Essentially, it requires running:
```bash
gem install mvg-live
```
If you get an error that says ``'mkmf.rb can't find header files for ruby'`` try doing what it says on this [stackoverflow page](https://stackoverflow.com/questions/20559255/error-while-installing-json-gem-mkmf-rb-cant-find-header-files-for-ruby), i.e. run this command in the bash shell:
```bash
sudo apt-get install ruby`ruby -e 'puts RUBY_VERSION[/\d+\.\d+/]'`-dev
```

Make sure it is running correctly by running `mvg hauptbahnhof`` in the terminal. If you got a timetable, you're all set.

## Setting up a 4 digit 7 segment (4d7s) LED display
An explanation of how to use 4d8s displays with can be found on [raspi.tv](http://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python). They did a nice job of explaining the pinout:
![Alt text](/images/7seg-pinout-annotated_700.jpg?raw=true "4d8s pinout from raspi.tv")

I modified their wiring because I thought it made more sense to physically separate the wires that controll the digit selection from the wires that light up a specific segment. The resulting wiring is:
![Alt text](/images/4d7s_wiring.bmp?raw=true "4d7s display wiring")

## Setting up a 8 digit 8 segment (8d8s) LED display through SPI
coming soon...

# Comissioning
## Running it on a 4d8s display

## Running it on a 4d8s display
