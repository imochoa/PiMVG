# PiMVG
Using the Raspberry Pi to check Munich's public transport system
[![Using a 4 digit 7 segment display to display the MVG departure times](https://i.ytimg.com/vi/vvEPnLYukYQ/hqdefault.jpg)](https://www.youtube.com/embed/vvEPnLYukYQ?autoplay=1 "Using a 4 digit 7 segment display to display the MVG departure times")

For information on how to build one yourself, follow the guide on Instructables (coming soon...)

# Setup
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

You can check if it was correctly installed by runningn `mvg hauptbahnhof`` in the terminal. If you got a timetable, you're all set.

## Setting up the hardware
Follow the guide on Instructables (coming soon...)
