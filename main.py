
from utils.task_manager import (
    add_task,
    view_tasks,
    complete_task,
    delete_task,
    filter_tasks,
)


def show_menu():
    print("\n" + "=" * 35)
    print("       PYTHON TO-DO LIST")
    print("=" * 35)
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. View pending tasks")
    print("6. View completed tasks")
    print("7. Exit")
    print("=" * 35)


def main():
    print("Welcome to your To-Do List!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            filter_tasks(False)
        elif choice == "6":
            filter_tasks(True)
        elif choice == "7":
            print("Thank you for using To-Do List!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
