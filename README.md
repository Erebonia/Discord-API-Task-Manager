# ✅ Discord Task Bot

A simple, emoji-enhanced task checklist bot for Discord. Organize your to-dos with categories, mark them complete, and see everything in a beautifully formatted embed — all from chat.

---

## ✨ Features

- 📓 **Task Categories**
  - Organize your tasks into:  
    - 📓 Work  
    - 🧹 Chores  
    - 🏋 Workout  
    - 📄 Miscellaneous (uncategorized)

- 📝 **Smart Task Management**
  - Add, edit, complete, uncomplete, or remove tasks by number.
  - Supports multiple tasks at once using spaces, commas, or ranges (e.g., `1 2 3`, `1,3`, `2-4`).

- ✅ **Completion Tracking**
  - Tasks display with ✅ or ❌ to show their current status.
  - Use `!uncompleteall` to reset all completed tasks instantly.

- 📋 **Embed Checklist View**
  - Your list is displayed in a clear, colorful Discord embed.
  - Updated automatically after each task action.

- 🏷️ **Custom Checklist Name**
  - Rename your list to fit your project or mood.

- 💬 **User-Friendly Commands**
  - Helpful error messages and guidance if something goes wrong.

---

## 📌 Example Commands

- `!add work Finish the report`
- `!edit chores 2 Take out trash`
- `!complete workout 1 2`
- `!remove work 3`
- `!mylist`
- `!rename Weekly Goals`

---

## 🚀 Getting Started

1. Clone this repo.
2. Add your Discord bot token to a `.env` file:


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

