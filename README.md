# RCOS-Groupme-Bot
Free, open source groupme bot that can execute python code, among other features.

https://docs.google.com/document/d/13vYDd6ASlxYQIDTDsknEDNRrywFXTNe7VduzZi_VxBo/edit?usp=sharing

Beginner's guide to using the bot:

First, clone our repo. This can easily be done from the github page.

Once you've set up a folder for it and copied over the structure, you'll need to make a couple changes.

So, up next you'll need a GroupMe bot account. The tutorial can be found at this link: https://dev.groupme.com/tutorials/bots, but the quick version is: create a group or select an existing group, and then use the GroupMe form (on their site) to create a bot for that group.

After it is created, you will need to create a pass.txt in the main folder where controller.py is. The contents of pass.txt need to be exactly as follows: on the first line, the bot ID, with no additional text whatsoever. On the second line goes the userID of the user who owns/created the bot. No other text in the file is required.

Now the bot can be run- simply open CMD in the target directory, and type "python controller.py"- you can then use all of the commands and features of the bot. To list them, simply type "help" in the chat where the bot is located while it is running.

Enjoy! This project is fully open source under the GNU GENERAL PUBLIC LICENSE. " Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed."

 Be sure to log any feature requests on our github!
