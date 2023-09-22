from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3

#Logging level, to get data about bot operations
logging.basicConfig(level=logging.INFO)

#Connecting to Sqlite database
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

#Creating table for tasks if it isn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT,
                     done INTEGER DEFAULT 0
                  )''')
conn.commit()

#Initialization
storage = MemoryStorage()
bot = Bot(token="6591245041:AAEmWe9OccY5UcDIZMNISS3E8mxq7r4EaEI")
dp = Dispatcher(bot, storage=storage)

#Class for tasks
class TaskForm(StatesGroup):
    title = State()
    description = State()

#Add task
def add_task(title, description=None):
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    conn.commit()

#Mark done
def mark_task_as_done(task_id):
    cursor.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()

#Get all tasks
def get_all_tasks():
    cursor.execute("SELECT id, title, description, done FROM tasks")
    return cursor.fetchall()

#Delete the task by id
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

#First reply after launching bot
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Этот бот поможет тебе управлять списком дел. Используй /add <текст задачи> "
                        "для добавления задачи, /show для просмотра списка задач и /delete <id> для удаления "
                        "задачи по её номеру.")

#Operating with /add command
@dp.message_handler(commands=['add'])
async def start_add_task(message: types.Message):
    await message.reply("Введите заголовок задачи:")
    await TaskForm.title.set()

@dp.message_handler(state=TaskForm.title)
async def get_description(message: types.Message, state: FSMContext):
    title = message.text

    # Сохраняем заголовок задачи в контексте состояния
    await state.update_data(title=title)

    await message.reply("Введите описание задачи (или просто нажмите Enter, чтобы пропустить):")
    await TaskForm.description.set()

@dp.message_handler(state=TaskForm.description)
async def add_task_to_database(message: types.Message, state: FSMContext):
    description = message.text

    async with state.proxy() as data:
        title = data['title']

    add_task(title, description)

    await state.finish()

    await message.reply(f"Задача '{title}' добавлена.")

#Operating with command /done
@dp.message_handler(commands=['done'])
async def done_task_command(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        mark_task_as_done(task_id)
        await message.reply(f"Задача с ID {task_id} отмечена как выполненная.")
    else:
        await message.reply("Для обозначения задачи как выполненной используй команду /done <id>")

#Get list of tasks with their state
@dp.message_handler(commands=['list'])
async def list_tasks_command(message: types.Message):
    tasks = get_all_tasks()
    if tasks:
        tasks_list = "\n".join([f"{task[0]}. {'[x]' if task[3] else '[ ]'} {task[1]} - {task[2]}" for task in tasks])
        await message.reply(f"Список задач:\n{tasks_list}")
    else:
        await message.reply("Список задач пуст.")

#Operating with /delete command
@dp.message_handler(commands=['delete'])
async def delete_task_command(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        delete_task(task_id)
        await message.reply(f"Задача с ID {task_id} удалена.")
    else:
        await message.reply("Для удаления задачи используй команду /delete <id>")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)




