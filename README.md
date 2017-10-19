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

Make sure it is running correctly by running ``mvg hauptbahnhof``` in the terminal. If you got a timetable, you're all set.

## 2 Comming soon
