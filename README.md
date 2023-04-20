# UIUC Course God 🌽

## Introduction

Automatically check and register courses for UIUC students. This software is able to bypass school's auto-detection system.

You should be able to use this with your own school with some easy tweaks if they are using similar systems.

This script was originally written by [chitianhao](https://github.com/chitianhao/uiuc-course-god)

## Future features

- [] Twilio can be added to send message for remaining seats finding and successful registration.
- [] `argparse` or configuration file can be added. (currently the logic is straightforward so they are not involved)
- [] Telegram bot support?
- [x] Support of courses with lab/discussion section.

## Warning

This is a rule-breaking software, so please beware the risks.

## Requirements

The following Python packages are required:

- bs4
- selenium
- chromedriver

To install them, run: `pip3 install -r requirement.txt`

or

```
pip3 install beautifulsoup4
pip3 install selenium
pip3 install webdriver-manager
```

Compatible with Python2 and Python3

## Usage and features

1. Clone or download the script to your local machine.

2. Open a terminal and navigate to the folder containing the script.

3. Run the script using the following command:

```bash
python run.py <semester> <netid> <password> <crn1> <crn2> ...
```

Options:

- `--turbo`: no sleeping time between checks
- `--headless`: Runs Firefox in headless mode

Replace `<semester>` with the desired semester in this format: `YYYY-spring`, `YYYY-summer`, or `YYYY-fall`. For example: `2023-spring`.

Replace `<netid>` and `<password>` with your UIUC NetID and plaintext password.

Replace `<crn1>`, `<crn2>`, and so on with the desired course CRNs.

To group CRNs together, wrap them in `{}`. For example, to group CRNs 11451 and 41919, use the following syntax:

```bash
python run.py 2023-spring mynetid mypassword {11451 41919} 34567
```

## Important Notes

- Do not log in to the registration system yourself while using this script.
- The login URL or other aspects of the script may need to be updated in the future. Be sure to check for updates if you encounter any issues.
- Ensure that the semester format is correct, or the script will not work as intended.

## Contributing

If there is any outdated component, please make a pull request or contact the author.

## License

Licensed under MIT.
