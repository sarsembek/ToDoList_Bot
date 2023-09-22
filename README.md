# ToDoList Bot with Aiogram

## Overview

This is a Telegram bot built with the Aiogram library for managing a to-do list. The bot allows users to add tasks, mark them as done, view the list of tasks, and delete tasks. Tasks are stored in a SQLite database. This README provides an overview of the bot's functionality, how to set it up, and additional sections about database and author information.

## Features

- Add tasks with titles and optional descriptions.
- Mark tasks as done.
- View the list of tasks, including their IDs, titles, descriptions, and status (done or not done).
- Delete tasks by ID.

## Prerequisites

Before running this bot, make sure you have the following dependencies installed:

- **aiogram**: The library for creating Telegram bots.
- **sqlite3**: For managing the SQLite database.
- **logging**: For bot operation logging.

You can install these libraries using pip if they are not already installed:

```bash
pip install aiogram sqlite3
```

## Getting Started

To use this bot, follow these steps:

1. Clone or download the repository to your local machine.
2. Create a Telegram bot and get its API token from the **BotFather**.
3. Replace `"YOUR_BOT_API_TOKEN"` with your actual bot API token in the script.
4. Run the script `telegram_bot.py`.
5. Start a chat with your bot on Telegram and use the following commands:
   * `/start`: Get an introduction to the bot and its commands.
   * `/add` <task>: Add a new task with a title. You can also include a description.
   * `/done` <task_id>: Mark a task as done by providing its ID.
   * `/list`: View the list of tasks.
   * `/delete <task_id>`: Delete a task by providing its ID.

## Database

The bot uses an SQLite database named `todo_list.db` to store tasks. The database and the `tasks` table are created automatically if they do not exist.

## Usage

* Add tasks with `/add` command.
* Mark tasks as done with `/done` command.
* View the list of tasks with `/list` command.
* Delete tasks with `/delete` command.

## Author

[Arman Sarsembek](https://github.com/sarsembek)
