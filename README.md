# UIUC Course God

## Introduction

Automatically check and register courses for UIUC students. This software is able to bypass
school's auto-detection system.

You should be able to use this with your own school with some easy tweaks if they are using similar systems.

## Warning

This is a rule-breaking software, so please beware the risks.

## Requirements

Packages installation guide: `pip3 install -r requirement.txt`

Compatible with Python2 and Python3

Requirements: bs4, selenium, chromedriver (using brew cask), webdriver-manager

## Usage and features

`python3 run.py semester netid password {CRN1 CRN2} CRN3 CRN4 {CRN5 CRN6} ...`
Optional: `--headless`

if you put two or more crns inside a `{}` it will be considered as "linked course", meaning that all crns inside the bracket must be available for registration before the program register it.

Use semester in this format: YYYY-season.

Example usage: `python3 run.py 2021-fall abc123 abcdefg12345 11111 22222`

Multiple courses can be put in at the same time.

Crosslist courses are supported. However, you'll need to edit the code to do this.

## Contributing

If there is any outdated component, please make a pull request or contact the author.
Contact me if you want to maintain this repo.

Email: chitianhaoxp@gmail.com

Wechat: chitianhao

## Future features

- [] Twilio can be added to send message for remaining seats finding and successful registration.
- [] `argparse` or configuration file can be added. (currently the logic is straightforward so they are not involved)
- [] Telegram bot support?
- [x] Support of courses with lab/discussion section.

## License

Licensed under MIT.
