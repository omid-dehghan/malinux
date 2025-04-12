The Story Behind This Project
It all started when I realized that I wasn't feeling good about myself and my productivity. I needed a way to track my deep work sessions, specifically the time spent on focused study. By doing so, I hoped to gain confidence and boost my self-esteem. I wasn't sure how much time I was truly dedicating to my studies each day. And worse, I feared I might not be working as hard as I thought.

At the same time, I felt an urge to start contributing more actively on GitHub—building something meaningful that could help me grow, learn, and share with others. So, I thought, why not combine the two?

What if I could create a program that tracks my deep work duration? This would not only help me measure my progress but also serve as a tool for self-development. And as I was learning Linux, I thought it would be awesome to build this program in a terminal-based environment—just like the Linux tools I was studying.

This project became my start. I wanted to put it on GitHub so others could also contribute to its growth. By doing so, I envisioned a tool that could help anyone looking to track their focus and study time, and improve themselves day by day. It could even have features like tracking new English words learned each day or other self-improvement features!

How It Works
This project uses a simple list-based data structure to help you track your deep work sessions. It stores your data in a .json file that’s automatically created on your desktop. You can interact with it using terminal-style commands.

Available Commands
>>> deepwork HH:MM
Add a single deep work session duration.
Example:
>>> deepwork 00:20

>>> deepwork list HH:MM HH:MM ...
Add multiple deep work durations at once.
Example:
>>> deepwork list 00:20 01:20 10:00

>>> deepwork pop
Remove the last recorded duration from the list.

>>> deepwork popall
Clear all durations from the list.