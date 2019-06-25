# Streamlabs Chatbot Custom Script Example (modMehen)

This is a script suite of a few moderation options that are designed to work with StreamLabs Chatbot. It allows you to
penalize users (of points), and will cause the Chatbot to ask users to type a command to agree to the channel rules if
they have no currency (which should generally correlate to being new)

## Usage

!exile $targetid - strip a user of all point currency

Example: ```!exile mushuyowushu```
Result: ```MushuYoWushu was erased from our ranks.```

!fine $targetid $value - fines a user $value points, or all of their points if they are fined more than they have

Example: ```!fine mushuyowushu 100000000000```
Result: ```MushuYoWushu was fined 386 Dice.```

!verify - if the person who calls this has 0 currency, they are given 1 point, in a point based rank system this helps tell apart bots. 
The script will also pester all users with 0 points through public chat until they agree to the rules by verifying.

Example: ```!verify```
Result: ```Thanks for verifying MushuYoWushu! Welcome to the chat!```

## Purpose

This is made public in hopes that it will help people who want to script for the Streamlabs Chatbot with less programming experience
by giving them a live example of a script that supports multiple commands and command changes.  The commands here are pretty
easily replicated in the `!commands` section of the Chatbot. If this helps you or you like it, please let me know by 
starring/watching/forking the project!

# License
This software package is a derivative work of the code from the repo below and the derivation is licensed under the 
GNU Public License as mentioned in the included LICENSE file. If you have not received a copy of the GNU General Public 
License along with this program see <https://www.gnu.org/licenses/>.

https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate


