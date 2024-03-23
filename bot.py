import discord
from discord.ext import commands
import re
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("Discord_TOKEN")

async def send_message(message, user_message, is_private):
    try:
        await message.author.send() if is_private else await message.channel.send()
    
    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    intents.members = True

    # Change only the no_category default string
    help_command = commands.DefaultHelpCommand(
        no_category = 'General Commands')

    bot = commands.Bot(intents=intents, command_prefix="!", help_command = help_command)

    load_dotenv()
    TOKEN = os.getenv("Discord_TOKEN")

    tasks = []
    emoji_mapping = {
        "work": "📓", # Can also use emotes instead of unicode: Ex. <:brel:1124420009272299590>
        "chores": "🧹",
        "workout": "🏋",
        "misc": "📄"
    }

    category_mapping = {
        "📓": "Work",
        "🧹": "Chores",
        "🏋": "Workout",
        "📄": "Misc"
    }

    tasks_by_category = {emoji_id: [] for emoji_id in emoji_mapping.values()}
    tasks_by_category["📄"] = []  # Add the "📄" emoji as the key for uncategorized tasks

    @bot.event
    async def on_ready():
        print(f"Bot connected as {bot.user.name}")

    @bot.command(name="edit")
    async def edit(ctx, category, task_index: int, *, new_task):
        lowercase_category = category.lower()
        emoji_id = emoji_mapping.get(lowercase_category)

        if emoji_id:
            category_tasks = tasks_by_category.get(emoji_id)
            if category_tasks and 1 <= task_index <= len(category_tasks):
                task = category_tasks[task_index - 1]
                task["task"] = new_task
                await ctx.send(f'Task {task_index} in category {category_mapping[emoji_id]} edited successfully.')
                await mylist(ctx)  # Call the mylist() command to display the updated task list
            else:
                await ctx.send(f'Invalid task index for category {category_mapping[emoji_id]}.')
        else:
            await ctx.send(f'Invalid category: {category}.')

    @bot.command(name="complete")
    async def complete(ctx, *, task_numbers):
        try:
            category, indices = parse_task_category_indices(task_numbers)

            if category is not None and indices:
                lowercase_category = category.lower()
                emoji_id = emoji_mapping.get(lowercase_category)

                if emoji_id:
                    category_tasks = tasks_by_category.get(emoji_id, [])
                    completed_tasks = []
                    for index in indices:
                        if 1 <= index <= len(category_tasks):
                            completed_index = index - 1
                            task = category_tasks[completed_index]
                            if not task["completed"]:  # Check if task is not already completed
                                task["completed"] = True
                                completed_tasks.append(task["task"])
                            else:
                                raise Exception(f'Task "{task["task"]}" in category {category_mapping[emoji_id]} is already completed.')

                    if completed_tasks:
                        tasks_text = '\n- '.join(completed_tasks)
                        response = f'Tasks completed in category {category_mapping[emoji_id]}:\n- {tasks_text}'
                        await ctx.send(response)
                        await mylist(ctx)  # Call mylist() after completing tasks
                        return

                else:
                    # Handling the case when the category is not represented by an emoji
                    category_tasks = tasks_by_category.get(None, [])
                    if category_tasks:
                        completed_tasks = []
                        for index in indices:
                            if 1 <= index <= len(category_tasks):
                                completed_index = index - 1
                                task = category_tasks[completed_index]
                                if not task["completed"]:  # Check if task is not already completed
                                    task["completed"] = True
                                    completed_tasks.append(task["task"])
                                else:
                                    raise Exception(f'Task "{task["task"]}" in category {category} is already completed.')

                        if completed_tasks:
                            category_name = category_mapping.get(None, "Misc")  # Use "Misc" if mapping is not found
                            tasks_text = '\n- '.join(completed_tasks)
                            response = f'Tasks completed in category {category_name}:\n- {tasks_text}'
                            await ctx.send(response)
                            await mylist(ctx)  # Call mylist() after completing tasks
                            return

            await ctx.send('No valid task numbers provided or category not found.')

        except Exception as e:
            await ctx.send(str(e))  # Send the exception message as the response



    @bot.command(name="uncomplete")
    async def uncomplete(ctx, *, task_numbers):
        try:
            category, indices = parse_task_category_indices(task_numbers)

            if category is not None and indices:
                lowercase_category = category.lower()
                emoji_id = emoji_mapping.get(lowercase_category)

                if emoji_id:
                    category_tasks = tasks_by_category.get(emoji_id, [])
                    uncompleted_tasks = []
                    for index in indices:
                        if 1 <= index <= len(category_tasks):
                            uncompleted_index = index - 1
                            task = category_tasks[uncompleted_index]
                            if task["completed"]:  # Check if task is already completed
                                task["completed"] = False
                                uncompleted_tasks.append(task["task"])
                            else:
                                raise Exception(f'Task "{task["task"]}" in category {category_mapping[emoji_id]} is already not completed.')

                    if uncompleted_tasks:
                        tasks_text = '\n- '.join(uncompleted_tasks)
                        response = f'Tasks uncompleted in category {category_mapping[emoji_id]}:\n- {tasks_text}'
                        await ctx.send(response)
                        await mylist(ctx)  # Call mylist() after uncompleting tasks
                        return

                else:
                    # Handling the case when the category is not represented by an emoji
                    category_tasks = tasks_by_category.get(None, [])
                    if category_tasks:
                        uncompleted_tasks = []
                        for index in indices:
                            if 1 <= index <= len(category_tasks):
                                uncompleted_index = index - 1
                                task = category_tasks[uncompleted_index]
                                if task["completed"]:  # Check if task is already completed
                                    task["completed"] = False
                                    uncompleted_tasks.append(task["task"])
                                else:
                                    raise Exception(f'Task "{task["task"]}" in category {category} is not completed.')

                        if uncompleted_tasks:
                            category_name = category_mapping.get(None, "Misc")  # Use "Misc" if mapping is not found
                            tasks_text = '\n- '.join(uncompleted_tasks)
                            response = f'Tasks uncompleted in category {category_name}:\n- {tasks_text}'
                            await ctx.send(response)
                            await mylist(ctx)  # Call mylist() after uncompleting tasks
                            return

            await ctx.send('No valid task numbers provided or category not found.')

        except Exception as e:
            await ctx.send(str(e))  # Send the exception message as the response

    @bot.command(name="uncompleteall")
    async def uncompleteall(ctx):
        uncompleted_tasks = []

        for category_tasks in tasks_by_category.values():
            for task in category_tasks:
                if task["completed"]:
                    task["completed"] = False
                    uncompleted_tasks.append(task["task"])

        if uncompleted_tasks:
            tasks_text = '\n- '.join(uncompleted_tasks)
            response = f'All tasks uncompleted:\n- {tasks_text}'
            await ctx.send(response)
            await mylist(ctx)  # Call mylist() after uncompleting tasks
        else:
            await ctx.send('No completed tasks found.')

    @bot.command(name="add")
    async def add(ctx, *args):
        task = ' '.join(args)  # Join all arguments into a single string

        if task:
            category = args[0].lower() if args else "misc"  # Assign category if available, else use "miscellaneous"

            lowercase_category = category.lower()
            emoji_id = emoji_mapping.get(lowercase_category)

            if emoji_id:
                category_tasks = tasks_by_category.get(emoji_id, [])
                # Remove the prefix name from the task
                task_without_prefix = re.sub(r'^\w+\s+', '', task)
                category_tasks.append({"task": task_without_prefix, "completed": False})
                tasks_by_category[emoji_id] = category_tasks
                await ctx.send(f'Task "{task_without_prefix}" added to category {category_mapping[emoji_id]}.')
            else:
                uncategorized_tasks = tasks_by_category.get("📄", [])
                # Remove the prefix name from the task
                task_without_prefix = re.sub(r'^\w+\s+', '', task)
                uncategorized_tasks.append({"task": task_without_prefix, "completed": False})
                tasks_by_category["📄"] = uncategorized_tasks
                await ctx.send(f'Task "{task_without_prefix}" added as uncategorized.')

            await mylist(ctx)  # Call mylist() function to display the updated list
        else:
            await ctx.send("No task provided. Please specify a task to add.")



    # Function to parse category and indices from user input
    def parse_task_category_indices(input_string):
        category_indices = re.findall(r'([\w]+)\s*([\d\s,]*)', input_string)
        if category_indices:
            category = category_indices[0][0]
            indices = [int(idx) for idx in re.findall(r'\d+', category_indices[0][1])]
            return category, indices
        return None, None

    @bot.command(name="remove")
    async def remove(ctx, *, task_numbers):
        category, indices = parse_task_category_indices(task_numbers)

        if category is not None and indices:
            emoji_id = emoji_mapping.get(category.lower())

            if emoji_id:
                category_tasks = tasks_by_category.get(emoji_id, [])
                removed_tasks = []
                removed_indices = []
                for index in indices:
                    if 1 <= index <= len(category_tasks):
                        removed_index = index - 1
                        removed_indices.append(removed_index)
                        removed_tasks.append(category_tasks[removed_index]["task"])

                if removed_indices:
                    category_tasks = [task for i, task in enumerate(category_tasks) if i not in removed_indices]
                    tasks_by_category[emoji_id] = category_tasks
                    tasks_text = '\n'.join(removed_tasks)
                    await ctx.send(f'Tasks removed from category {category_mapping[emoji_id]}:\n{tasks_text}')
                    return

        await ctx.send('No valid task numbers provided or category not found.')

    checklist_name = "My Checklist"  # Initialize checklist name as a separate variable

    @bot.command(name="mylist")
    async def mylist(ctx, *, custom_checklist_name=None):
        tasks_text = ""

        for emoji_id, category_tasks in tasks_by_category.items():
            if category_tasks:
                category_name = category_mapping.get(emoji_id, "Unknown Category")
                emoji = emoji_id if emoji_id in emoji_mapping.values() else ""
                category_header = f"{emoji} {category_name}" if emoji else category_name
                tasks_text += f"{category_header}\n"
                for j, category_task in enumerate(category_tasks):
                    completed_icon = "✅" if category_task["completed"] else "❌"
                    tasks_text += f"{j+1}. {completed_icon} {category_task['task']}\n"
                tasks_text += "\n"

        uncategorized_tasks = [task for task in tasks if not any(task in category_tasks for category_tasks in tasks_by_category.values())]
        if uncategorized_tasks:
            misc_symbol = "Misc"
            tasks_text += f"{misc_symbol} {custom_checklist_name or checklist_name}\n"
            for j, uncategorized_task in enumerate(uncategorized_tasks):
                completed_icon = "✅" if uncategorized_task["completed"] else "❌"
                tasks_text += f"{j+1}. {completed_icon} {uncategorized_task['task']}\n"
            tasks_text += "\n"

        if tasks_text:
            embed = discord.Embed(title=custom_checklist_name or checklist_name, description=tasks_text, color=0x00ff00)
            embed.set_footer(text="Commands: !add, !remove, !mylist")

            for emoji_id, category_name in category_mapping.items():
                if emoji_id in emoji_mapping.values():
                    emoji = emoji_id
                else:
                    emoji = category_name
                embed.description = embed.description.replace(emoji_id, emoji)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Your {custom_checklist_name or checklist_name} is empty.')


    @bot.command(name="rename")
    async def rename_checklist(ctx, *, new_title):
        global checklist_name
        checklist_name = new_title.strip('"')
        await ctx.send(f'The checklist has been renamed to "{checklist_name}"')
        await mylist(ctx, custom_checklist_name=checklist_name)  # Call mylist() function with updated checklist_name

    def parse_task_indices(input_str):
        indices = []
        parts = re.split(r',|\s', input_str)
        for part in parts:
            if '-' in part:
                start, end = part.split('-')
                start_index = int(start.strip()) - 1
                end_index = int(end.strip()) - 1
                indices.extend(list(range(start_index, end_index + 1)))
            else:
                index = int(part.strip()) - 1
                indices.append(index)
        return indices

    bot.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()
