# PiMVG
Using the Raspberry Pi to check Munich's public transport system
It uses the Command Line Interface (CLI) from rrmoritz's project [rmoriz/mvg-live](https://github.com/rmoriz/mvg-live#mvg-live)
to get the information from the mvg and filters it.

I still have to upload the part of the code that displays those times on an LED 8Segment display...

# How to use it

## 1 Install rmoriz/mvg-live
Follow his `README.md` to install his rubygem. Essentially, it requires running:
```bash
gem install mvg-live
```
If you get an error that says ``'mkmf.rb can't find header files for ruby'`` try doing what it says on this [stackoverflow page](https://stackoverflow.com/questions/20559255/error-while-installing-json-gem-mkmf-rb-cant-find-header-files-for-ruby), i.e. run this command in the bash shell:
```bash
sudo apt-get install ruby`ruby -e 'puts RUBY_VERSION[/\d+\.\d+/]'`-dev
```

Make sure it is running correctly by running ``mvg hauptbahnhof``` in the terminal. If you got a timetable, you're all set.

## 2 Coming soon
