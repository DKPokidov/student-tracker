from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from tracker import Course
import os
from utils import read_students_from_file

# === НАСТРОЙКИ ===
DATA_FILE = "data/course_data.json"
PATH = 'data/students_list.txt'
students = read_students_from_file(PATH)

# === ЗАГРУЗКА КУРСА ===
course = Course("Python for beginners", students=students)
try:
    course.load_from_file(DATA_FILE)
    print("✅ Данные загружены из файла.")
except FileNotFoundError:
    print("ℹ️ Файл с данными не найден, создан новый курс.")

# === ОБРАБОТЧИКИ КОМАНД ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start — приветствие и список команд."""
    await update.message.reply_text(
        "📚 Бот для учёта успеваемости\n\n"
        "Доступные команды:\n"
        "/students — список студентов\n"
        "/add_student Имя — добавить студента\n"
        "/remove_student Имя — удалить студента\n"
        "/add_topic Название тип макс_балл — добавить тему\n"
        "/set_grade Студент Тема Оценка — выставить оценку\n"
        "/mark_attendance Студент Тема да/нет — отметить посещаемость\n"
        "/grades Студент — показать оценки студента\n"
        "/debtors Тема проходной_балл — список должников\n"
        "/save — сохранить данные"
    )

async def students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает список всех студентов."""
    if not course.students:
        await update.message.reply_text("📭 Список студентов пуст.")
        return
    text = "\n".join(course.students)
    await update.message.reply_text(f"📋 Студенты:\n{text}")

async def add_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет студента."""
    if not context.args:
        await update.message.reply_text("❌ Укажите имя: /add_student Иванов")
        return
    name = " ".join(context.args)
    try:
        course.add_student(name)
        await update.message.reply_text(f"✅ Студент '{name}' добавлен.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def remove_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет студента."""
    if not context.args:
        await update.message.reply_text("❌ Укажите имя: /remove_student Иванов")
        return
    name = " ".join(context.args)
    try:
        course.remove_student(name)
        await update.message.reply_text(f"✅ Студент '{name}' удалён.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def add_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет тему."""
    if len(context.args) < 3:
        await update.message.reply_text("❌ Формат: /add_topic Название тип макс_балл")
        return
    name = context.args[0]
    topic_type = context.args[1].lower()
    try:
        max_score = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ Максимальный балл должен быть числом.")
        return
    try:
        course.add_topic(name, topic_type, max_score)
        await update.message.reply_text(f"✅ Тема '{name}' добавлена.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def set_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выставляет оценку."""
    if len(context.args) < 3:
        await update.message.reply_text("❌ Формат: /set_grade Студент Тема Оценка")
        return
    student = context.args[0]
    topic = context.args[1]
    try:
        score = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ Оценка должна быть числом.")
        return
    try:
        course.set_grade(student, topic, score)
        await update.message.reply_text(f"✅ Оценка {score} для '{student}' по теме '{topic}' сохранена.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def mark_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмечает посещаемость."""
    if len(context.args) < 3:
        await update.message.reply_text("❌ Формат: /mark_attendance Студент Тема да/нет")
        return
    student = context.args[0]
    topic = context.args[1]
    present = context.args[2].lower() in ('да', 'yes', 'true', '1')
    try:
        course.mark_attendance(student, topic, present)
        await update.message.reply_text(f"✅ Посещаемость для '{student}' по теме '{topic}' отмечена.")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def grades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает оценки студента."""
    if not context.args:
        await update.message.reply_text("❌ Укажите имя: /grades Иванов")
        return
    student = " ".join(context.args)
    grades_dict = course.get_all_grades(student)
    if not grades_dict:
        await update.message.reply_text(f"📭 У студента '{student}' пока нет оценок.")
        return
    text = "\n".join(f"{topic}: {score}" for topic, score in grades_dict.items())
    await update.message.reply_text(f"📊 Оценки '{student}':\n{text}")

async def debtors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает должников по теме."""
    if len(context.args) < 2:
        await update.message.reply_text("❌ Формат: /debtors Тема проходной_балл")
        return
    topic = context.args[0]
    try:
        pass_score = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Проходной балл должен быть числом.")
        return
    try:
        debtors_list = course.get_debtors(topic, pass_score)
        if not debtors_list:
            await update.message.reply_text(f"✅ Все студенты сдали тему '{topic}'.")
        else:
            text = "\n".join(debtors_list)
            await update.message.reply_text(f"📋 Должники по теме '{topic}':\n{text}")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет данные."""
    try:
        course.save_to_file(DATA_FILE)
        await update.message.reply_text("💾 Данные сохранены.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при сохранении: {e}")

# === ЗАПУСК БОТА ===
def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN environment variable not set!")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("students", students))
    app.add_handler(CommandHandler("add_student", add_student))
    app.add_handler(CommandHandler("remove_student", remove_student))
    app.add_handler(CommandHandler("add_topic", add_topic))
    app.add_handler(CommandHandler("set_grade", set_grade))
    app.add_handler(CommandHandler("mark_attendance", mark_attendance))
    app.add_handler(CommandHandler("grades", grades))
    app.add_handler(CommandHandler("debtors", debtors))
    app.add_handler(CommandHandler("save", save))

    print("🤖 Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()