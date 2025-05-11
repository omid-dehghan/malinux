The Story Behind This Project
It all started when I realized that I wasn't feeling good about myself and my productivity. I needed a way to track my deep work sessions, specifically the time spent on focused study. By doing so, I hoped to gain confidence and boost my self-esteem. I wasn't sure how much time I was truly dedicating to my studies each day. And worse, I feared I might not be working as hard as I thought.

At the same time, I felt an urge to start contributing more actively on GitHub—building something meaningful that could help me grow, learn, and share with others. So, I thought, why not combine the two?

What if I could create a program that tracks my deep work duration? This would not only help me measure my progress but also serve as a tool for self-development. And as I was learning Linux, I thought it would be awesome to build this program in a terminal-based environment—just like the Linux tools I was studying.

This project became my start. I wanted to put it on GitHub so others could also contribute to its growth. By doing so, I envisioned a tool that could help anyone looking to track their focus and study time, and improve themselves day by day. It could even have features like tracking new English words learned each day or other self-improvement features!

How It Works
This project uses a simple list-based data structure to help you track your deep work sessions. It stores your data in a .json file that’s automatically created on your desktop. You can interact with it using terminal-style commands.


## Project Status
This project is a work in progress. Some features are incomplete or experimental. If you encounter bugs, please report them as issues, and we will address them when possible.


Available Commands (open this in code mode)
>>> deepwork HH:MM
append a single deep work session duration.
Example:
>>> deepwork 00:20

>>> deepwork HH:MM N
insert a single deep work session duration with index N.
Example:
>>> deepwork 00:20 1

>>> deepwork list HH:MM HH:MM ...
append multiple deep work durations at once.
Example:
>>> deepwork list 00:20 01:20 10:00

>>>  deepwork pop N
Remove a recorded duration from the list with index N.
Example:
>>>  deepwork 00:20 1

>>>  deepwork pop
Remove the last recorded duration from the list.

>>>  deepwork popall
Clear all durations from the list.

>>>  deepwork total
total duration that you worked overall.

>>>  deepwork today
it will get today record.

>>>  deepwork retotal
reset the total duration.

>>> deepwork alldata
print all recorded data
Example:
{'2025-04-11': ['01:00', '03:00', '~04:00']
, '2025-04-12': ['00:30', '01:00', '01:30', '02:15', '~05:15']}

>>>  deepwork [datetime-%Y-%m-%d] HH:MM
append a single deep work session duration to a date.
Example:
>>>  deepwork 2025-04-18 00:20

>>>  deepwork [datetime-%Y-%m-%d] HH:MM N
append a single deep work session duration to a date with index N.
Example:
>>>  deepwork 2025-04-18 00:20 1

>>>  deepwork [datetime-%Y-%m-%d]
get a date data.
Example:
>>>  deepwork 2025-04-18

>>>  deepwork [datetime-%Y-%m-%d] pop
Remove the last recorded duration of a date.
Example:
>>>  deepwork 2025-04-18 pop

>>>  deepwork [datetime-%Y-%m-%d] pop N
Remove the last recorded duration of a date with index N.
Example:
>>>  deepwork 2025-04-18 pop 1

>>>  deepwork [datetime-%Y-%m-%d] popall
Clear all durations from the list.
Example:
>>>  deepwork 2025-04-18 popall

>>>  deepwork [datetime-%Y-%m-%d] list HH:MM HH:MM
Clear all durations from the list.
Example:
>>>  deepwork 2025-04-18 list 0:30 1:30

** statistics:

>>>  deepwork [datetime-%Y-%m-%d] [datetime-%Y-%m-%d]
Bring up statistics between two dates.
Example:
>>>  deepwork 2025-04-18 2020-04-18

>>>  deepwork [datetime-%Y-%m-%d] today
Bring up statistics between a date and today.
note: you can also enter command like this:
>>> deepwork today [datetime-%Y-%m-%d]
Example:
>>>  deepwork 2025-04-18 today

>>>  deepwork N
Bring up statistics N days ago.
Example:
>>>  deepwork 10
