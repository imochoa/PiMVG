# PiMVG
These modules let you track the departure times of Munich's public transport system. The output can either be to the console, to a 4d7s display or to an 8d7s display:

### Using the Raspberry Pi to check Munich's public transport system with a common anode 4 digit 7 segment display (4d7s display) 
[![Using a 4 digit 7 segment display to show the MVG departure times](https://i.ytimg.com/vi/vvEPnLYukYQ/hqdefault.jpg)](https://www.youtube.com/embed/vvEPnLYukYQ?autoplay=1 "Using a 4 digit 7 segment display to display the MVG departure times")
### Using the Raspberry Pi to check Munich's public transport system with a MAX7219 8 digit 7 segment display (8d7s display) 
[![Using an 8 digit 7 segment display to show the MVG departure times](https://i.ytimg.com/vi/AdMd7C4RN0I/hqdefault.jpg)](https://www.youtube.com/embed/AdMd7C4RN0I?autoplay=1 "Using an 8 digit 7 segment display to show the MVG departure times")

For information on how to build one yourself, follow the guide on Instructables (coming soon...)

# Software Setup
## Install rmoriz/mvg-live
These scripts use the Command Line Interface (CLI) from rmoritz's project [rmoriz/mvg-live](https://github.com/rmoriz/mvg-live#mvg-live)
to get the information from the mvg and filters it.

As per his `README.md` file, to install his rubygem you need to run:
```bash
gem install mvg-live
```
If you get an error that says ``'mkmf.rb can't find header files for ruby'`` try doing what it says on this [stackoverflow page](https://stackoverflow.com/questions/20559255/error-while-installing-json-gem-mkmf-rb-cant-find-header-files-for-ruby), i.e. run this command in the bash shell:
```bash
sudo apt-get install ruby`ruby -e 'puts RUBY_VERSION[/\d+\.\d+/]'`-dev
```

You can check if it was correctly installed by runningn `mvg hauptbahnhof` in the terminal. If you got a timetable, you're all set.

## (For the 8d7s display) enable SPI and Install rm-hull/luma.led_matrix
First, run: `sudo raspi-config` and make sure that SPI is enabled on your Raspberry Pi

Another package is required if you want to use the 8d7s displays with the MAX7219 chip; [rm-hull/luma.led_matrix](https://github.com/rm-hull/luma.led_matrix)

Installing it is pretty straightforward, first you need to clone it into your Raspberry Pi
```bash
git clone https://github.com/rm-hull/luma.led_matrix
```

Then open a terminal, go to that directory and run
```bash
sudo python setup.py install
```

Open a python interactive shell and try to import it:
```python
import luma
```
If you didn't get any errors, you're good to go.

# Hardware Setup
Follow the guide on Instructables (coming soon...)

## 4d7s display wiring
(coming soon...)
## 8d7s display wiring
(coming soon...)
By default, it uses the first SPI channel


# How to use it
The `py_mvg_cli.py` python module can be run directly from the bash shell and uses the other modules. Make sure it's executable on your raspberry Pi. If you're not sure, just run `chmod +x pi_mvg_cli.py`

The `-h` argument prints out the help for the command line interface:
```bash
./pi_mvg_cli.py -h
usage: pi_mvg_cli.py [-h] [--display_digits DISPLAY_DIGITS] --station STATION
                     [--line [LINE]] [--dest [DEST]] [--min_t MIN_T]
                     [--max_t MAX_T] [--screen_timeout SCREEN_TIMEOUT]
                     [--update_interval UPDATE_INTERVAL]

MVG inputs

optional arguments:
  -h, --help            show this help message and exit
  --display_digits DISPLAY_DIGITS
                        Number of digits suported by the display. 0 (DEFAULT)
                        = Print to console, 4 = 4d7s display, anything else =
                        combination of 8d7s displays
  --station STATION     Station to check
  --line [LINE]         Public transport type. The recognized values are: [u]
                        Ubahn, [s] Sbahn, [tram] Tram & [bus] Bus
  --dest [DEST]         Final stop of the lines
  --min_t MIN_T         Minimum departure time
  --max_t MAX_T         Maximum departure time
  --screen_timeout SCREEN_TIMEOUT
                        Minutes to display the results, negative values = no
                        limit
  --update_interval UPDATE_INTERVAL
                        Seconds that pass between updates of the departure
                        times
```
So some example commands would be:

* if `display_digits` is <=0 it will print to the console:
``` bash
`./pi_mvg_cli.py --station Olympiazentrum --line u --display_digits 0 --screen_timeout 1
```
* if `display_digits` is ==4 it will print to the 4d7s display:
``` bash
./pi_mvg_cli.py --station Olympiazentrum --line u --display_digits 4 --screen_timeout 1
```
*  if `display_digits` is anything else, it will print to the 8d7s display:
``` bash
./pi_mvg_cli.py --station Olympiazentrum --line u --display_digits 8 --screen_timeout 1
```
