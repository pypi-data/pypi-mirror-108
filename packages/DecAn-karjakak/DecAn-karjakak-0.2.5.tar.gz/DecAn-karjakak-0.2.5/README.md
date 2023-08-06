# DecAn
## Tool to Analyze and Deconstruct chars in a text
### [Beta-Development]

## Installation
```
pip install DecAn-karjakak
```
## Usage
**For analyzing text file or sentences**
```Console
decan -a path\text.txt 
```
**For search chars or words in text file or sentences**
```Console
decan -a "The Best is yet to come, yeayyy!!!" -s "Best" e y

# result:
"Best": {1: ((4, 8),)}
"Best" is 1 out of total 7 words!

'e': {5: (2, 5, 13, 22, 26)}
'e' is 5 out of total 34 chars!

'y': {5: (12, 25, 28, 29, 30)}
'y' is 5 out of total 34 chars!
```
**For Deconstruct text file or sentences to .json file or .pickle file**
```Console
# The text file, save as json/pickle filename, and save to a directory path.
decan -d path\text.txt text.json path\dir 
```
**For Constructing the deconstructed text that save in .json file or .pickle file**
```Console
decan -c path\text.pickle
```
**For fixing text punctuation like [".", ",", ":", ";"] that need space or less space, and save it to a new .txt file.**
```Console
decan -f path\text.txt dir\path text_name.txt
```
**TAKE NOTE:**
* **In -d [deconstruct], the text has been fixed as well but saved as pickle or json file.**
## Note
* **Still development process.**
* **Add write deconstruct to pickle, which much smaller and faster.**
* **Changes on analyze [-a]:**
    * **Count real chars, without the space and other printable.**
    * **Show the chars that used once and chars that used most.**
    * **Details on chars type.**
* **Add new function "-f" for saving text that has been fixed its punctuation position to a new txt file.**
    * **This function use dependency from GenPy-karjakak.** 
    * **https://pypi.org/project/GenPy-karjakak**
* **Add multi-threading for analyzing.**
    * **Using "-m" after "-s".**
    * ```decan -a path\text.txt -s "Best" e y -m```