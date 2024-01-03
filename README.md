## Description
This is a tool for exporting your AO3 Reading History into a text based UTF-8 file, such as .txt or .csv. 

The data exported from this is separated using a distinct separator, the default being `Ƈ`. This is just the default and can be modified when running the program. 

## Setup
Download from releases and unzip the folder, and it should be ready to run. The program does require python to be run. 

## Usage
In order to run the program you can use cmd in the downloaded folder with the command

`python main.py`

However, this will do nothing without the arguments provided. 

To have it export the data, three things are required in the arguments. 
* The username of the account being used. 
* The password of the account being used. 
* The intended destination of the exported file. 

The password is only used locally and is not stored outside the running program. 

In order to input these you run the command:

`python main.py -u (USERNAME) -p (PASSWORD) -o (OUTPUT)`

or you can use the longer arguments:

`python main.py --username (USERNAME) --password (PASSWORD) --output (OUTPUT)`

The username and password are self-explanatory, and the output is just the destination file, such as `ao3.csv` or `ao3.txt` depending on how you want to use the exported data. 

Another argument that isn't required is the separator. This is what separates the things about each work in the file. For example, if the separator is just the default `Ƈ`, this is the result: 

`NameƇAuthorƇRecipientƇFandomsƇWarningsƇRelationshipsƇCharactersƇFreeform_TagsƇLanguageƇWord_CountƇLast_UpdatedƇChaptersƇFinishedƇSeriesƇKudosƇCommentsƇBookmarksƇHitsƇURLƇRatingƇPairingsƇSummary`

This can then be replaced with a `, ` with a space for it to be:

`Name, Author, Recipient, Fandoms, Warnings, Relationships, Characters, Freeform_Tags, Language, Word_Count, Last_Updated, Chapters, Finished, Series, Kudos, Comments, Bookmarks, Hits, URL, Rating, Pairings, Summary`

However using something like a comma can cause issues with using the file later. 

Using the program with a custom separator would use the command:

`python main.py -u (USERNAME) -p (PASSWORD) -o (OUTPUT) -s (SEPARATOR)`

Or using longer arguments:

`python main.py --username (USERNAME) --password (PASSWORD) --output (OUTPUT) --separator (SEPARATOR)`

Once the program has started it will open an instance of Google Chrome, and use the provided username and password to log into the account. Once logged in it will navigate to the history page and begin going through the pages. 

This part is partially dependent on your internet speed to load the pages, and may take a bit as it goes through each page manually. 

Once it has finished going through every page of the history the exported file will be wherever you specified. 