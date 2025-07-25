# Discord Checklist Bot

## Features:

📋 Smart Task Management

    Add Tasks to Categories
    Users can create tasks under organized groups like Work, Chores, Workout, or leave them uncategorized (Misc).

    Edit Existing Tasks
    Tasks can be updated without re-adding them, using a category and index.

    Mark Tasks as Complete or Incomplete
    Users can check off or undo completed tasks individually or in bulk.

    Clear All Completed Tasks
    With one command, users can uncheck all completed tasks across every category.

    Remove Tasks Easily
    Tasks can be deleted based on their number within a category.

📂 Categorized & Emoji-Labeled

    Tasks are grouped into clear, emoji-marked categories:

        📓 Work

        🧹 Chores

        🏋 Workout

        📄 Miscellaneous

    Emojis make the checklist visually appealing and intuitive in chat.

🎨 Dynamic Checklist Display

    The mylist command generates a rich embed showing:

        Category headers

        Each task with a ✅ or ❌ to indicate status

        Clear task numbering for easy referencing

    The checklist updates automatically after any action, such as adding or completing a task.

🏷️ Custom Checklist Name

    Rename your checklist to suit different goals, themes, or team projects.

🔍 Flexible Input Parsing

    The bot accepts:

        Individual numbers (e.g., 1 2 3)

        Commas (e.g., 1,2,3)

        Ranges (e.g., 2-5)

    This makes it fast and easy to manage multiple tasks at once.

🧠 Smart Error Handling

    Friendly messages when:

        Categories are invalid

        Task numbers are out of range

        Tasks are already marked complete or incomplete

🧩 Modular, Scalable Design

    Internally organized to allow:

        Easy expansion with new categories or commands

        Future integration with persistent databases

        Lightweight deployment on any Discord server

👥 Ideal Use Cases

    Task lists for individuals or small teams

    Daily routines or personal goals (fitness, chores, work, etc.)

    Project management in shared community servers

```
Commands:
  add           
  complete      
  edit          
  help          Shows this message
  mylist        
  remove        
  rename        
  uncomplete    
  uncompleteall 
Type !help command for more info on a command.
You can also type !help category for more info on a category.
```

Demonstration:

![image](https://github.com/Erebonia/Discord-Checklist-bot/assets/52137104/1a2d18ab-f612-4c8f-ae2e-43f1945d639f)

