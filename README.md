# The Story Behind This Project
It all started when I realized that I wasn't feeling good about myself and my productivity. I needed a way to track my deep work sessions, specifically the time spent on focused study. By doing so, I hoped to gain confidence and boost my self-esteem. I wasn't sure how much time I was truly dedicating to my studies each day. And worse, I feared I might not be working as hard as I thought.

At the same time, I felt an urge to start contributing more actively on GitHub—building something meaningful that could help me grow, learn, and share with others. So, I thought, why not combine the two?

What if I could create a program that tracks my deep work duration? This would not only help me measure my progress but also serve as a tool for self-development. And as I was learning Linux, I thought it would be awesome to build this program in a terminal-based environment—just like the Linux tools I was studying.

This project became my start. I wanted to put it on GitHub so others could also contribute to its growth. By doing so, I envisioned a tool that could help anyone looking to track their focus and study time, and improve themselves day by day. It could even have features like tracking new English words learned each day or other self-improvement features!

How It Works
This project uses a simple list-based data structure to help you track your deep work sessions. It stores your data in a .json file that’s automatically created on your desktop. You can interact with it using terminal-style commands.


## Project Status
This project is a work in progress. Some features are incomplete or experimental. If you encounter bugs, please report them as issues, and we will address them when possible.


## Commands

### 1. >>> deepwork HH:MM  
#### append a single deep work session duration.  
#### Example:  
#### >>> deepwork 00:20  
---

### 2. >>> deepwork HH:MM N  
#### insert a single deep work session duration with index N.  
#### Example:  
#### >>> deepwork 00:20 1  
---

### 3. >>> deepwork list HH:MM HH:MM ...  
#### append multiple deep work durations at once.  
#### Example:  
#### >>> deepwork list 00:20 01:20 10:00  
---

### 4. >>> deepwork pop N  
#### remove a recorded duration from the list with index N.  
#### Example:  
#### >>> deepwork pop 1  
---

### 5. >>> deepwork pop  
#### remove the last recorded duration from the list.  
---

### 6. >>> deepwork popall  
#### clear all durations from the list.  
---



### 7. >>> deepwork today  
#### get today’s recorded sessions.  
---

### 8. >>> deepwork retotal  
#### reset the total duration.  
---

### 9. >>> deepwork alldata  
#### print all recorded data.  
#### Example:  
```python
{'2025-04-11': ['01:00', '03:00', '~04:00'],  
 '2025-04-12': ['00:30', '01:00', '01:30', '02:15', '~05:15']}
```  
---

### 10. >>> deepwork [YYYY-MM-DD] HH:MM  
#### append a deep work session to a specific date.  
#### Example:  
#### >>> deepwork 2025-04-18 00:20  
---

### 11. >>> deepwork [YYYY-MM-DD] HH:MM N  
#### append a deep work session to a specific date with index N.  
#### Example:  
#### >>> deepwork 2025-04-18 00:20 1  
---

### 12. >>> deepwork [YYYY-MM-DD]  
#### get all deep work sessions for a specific date.  
#### Example:  
#### >>> deepwork 2025-04-18  
---

### 13. >>> deepwork [YYYY-MM-DD] pop  
#### remove the last recorded duration for a date.  
#### Example:  
#### >>> deepwork 2025-04-18 pop  
---

### 14. >>> deepwork [YYYY-MM-DD] pop N  
#### Remove a specific duration from a date with index N.  
#### Example:  
#### >>> deepwork 2025-04-18 pop 1  
---

### 15. >>> deepwork [YYYY-MM-DD] popall  
#### clear all durations for a specific date.  
#### Example:  
#### >>> deepwork 2025-04-18 popall  
---

### 16. >>> deepwork [YYYY-MM-DD] list HH:MM HH:MM ...  
#### append multiple durations to a specific date.  
#### Example:  
#### >>> deepwork 2025-04-18 list 00:30 01:30  
---

## 📊 Statistics  
---

### 17. >>> deepwork [YYYY-MM-DD] [YYYY-MM-DD]  
#### show statistics between two dates.  
#### Example:  
#### >>> deepwork 2025-04-18 2025-04-30  
---

### 18. >>> deepwork [YYYY-MM-DD] today  
#### show statistics between a specific date and today.  
#### Note: You can also use:  
#### >>> deepwork today [YYYY-MM-DD]  
#### Example:  
#### >>> deepwork 2025-04-18 today  
---

### 19. >>> deepwork N  
#### Show statistics for N days ago until today.  
#### Example:  
#### >>> deepwork 10  
---

### 20. >>> deepwork total  
#### Show Statistics from first recorded date. 
---
