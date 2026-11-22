import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[dict]:
    """Vazifalarni JSON fayldan yuklaydi."""
    if not DATA_FILE.exists():
        return []
    content = DATA_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return json.loads(content)


def save_tasks(tasks: list[dict]) -> None:
    """Vazifalarni JSON faylga saqlaydi."""
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_task(tasks: list[dict], title: str) -> None:
    """Yangi vazifa qo'shadi."""
    cleaned_title = title.strip()
    if not cleaned_title:
        print("Xato: Vazifa nomi bo'sh bo'lishi mumkin emas.")
        return

    next_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({
        "id": next_id,
        "title": cleaned_title,
        "done": False,
    })
    save_tasks(tasks)
    print(f"Qo'shildi: #{next_id} - {cleaned_title}")


def list_tasks(tasks: list[dict]) -> None:
    """Barcha vazifalarni ekranga chiqaradi."""
    if not tasks:
        print("Hozircha vazifalar ro'yxati bo'sh.")
        return

    print("\n--- Vazifalar ro'yxati ---")
    for task in tasks:
        status = "[X]" if task["done"] else "[ ]"
        print(f"{status} #{task['id']}: {task['title']}")
    print("--------------------------\n")


def complete_task(tasks: list[dict], task_id: int) -> None:
    """Ko'rsatilgan ID dagi vazifani bajarilgan deb belgilaydi."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Bajarildi: #{task_id} - {task['title']}")
            return
    print(f"Xato: #{task_id} raqamli vazifa topilmadi.")


def delete_task(tasks: list[dict], task_id: int) -> None:
    """Ko'rsatilgan ID dagi vazifani o'chiradi."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"O'chirildi: #{task_id} - {removed['title']}")
            return
    print(f"Xato: #{task_id} raqamli vazifa topilmadi.")


def parse_positive_int(raw_value: str) -> int | None:
    """Matnni musbat butun songa xavfsiz o'tkazadi."""
    cleaned = raw_value.strip()
    if not cleaned.isdigit():
        print("Xato: Iltimos, faqat butun raqam kiriting.")
        return None
    number = int(cleaned)
    if number <= 0:
        print("Xato: Raqam 0 dan katta bo'lishi kerak.")
        return None
    return number


def run_app() -> None:
    """Asosiy menyu siklini ishga tushiradi."""
    tasks = load_tasks()

    while True:
        print("\n1. Vazifa qo'shish")
        print("2. Vazifalarni ko'rish")
        print("3. Vazifani bajarilgan deb belgilash")
        print("4. Vazifani o'chirish")
        print("0. Chiqish")

        choice = input("Tanlovingizni kiriting: ").strip()

        if choice == "1":
            title = input("Yangi vazifa nomi: ")
            add_task(tasks, title)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            raw_id = input("Bajarilgan vazifa ID si: ")
            task_id = parse_positive_int(raw_id)
            if task_id is not None:
                complete_task(tasks, task_id)
        elif choice == "4":
            raw_id = input("O'chiriladigan vazifa ID si: ")
            task_id = parse_positive_int(raw_id)
            if task_id is not None:
                delete_task(tasks, task_id)
        elif choice == "0":
            print("Dastur yakunlandi. Xayr!")
            break
        else:
            print("Noto'g'ri tanlov. 0 dan 4 gacha raqam kiriting.")


if __name__ == "__main__":
    run_app()