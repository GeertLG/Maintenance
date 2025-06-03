import os
import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.file_name = "tasks.json"
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    self.tasks = json.load(file)
            except:
                print("Error loading task data. Starting with empty task list.")
                self.tasks = []
    
    def save_tasks(self):
        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file)
    
    def add_task(self, title, description, due_date=None):
        """
        due_date debe ser string en formato 'YYYY-MM-DD' o None
        """
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "status": "Pending",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date if due_date else ""
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{title}' added successfully!")
    
    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        
        # Ordenar las tareas por fecha de vencimiento (due_date)
        # Las tareas sin due_date van al final
        def due_date_key(task):
            if task['due_date']:
                return datetime.strptime(task['due_date'], "%Y-%m-%d")
            else:
                # Si no hay fecha, poner fecha muy lejana para que queden al final
                return datetime.max
        
        sorted_tasks = sorted(self.tasks, key=due_date_key)
        
        print("\n" + "=" * 100)
        print(f"{'ID':<5} {'TITLE':<20} {'STATUS':<10} {'CREATED DATE':<20} {'DUE DATE':<12} {'DESCRIPTION':<30}")
        print("-" * 100)
        
        for task in sorted_tasks:
            due = task['due_date'] if task['due_date'] else "No due date"
            print(f"{task['id']:<5} {task['title'][:18]:<20} {task['status']:<10} {task['created_date']:<20} {due:<12} {task['description'][:28]:<30}")
        
        print("=" * 100 + "\n")
    
    def mark_complete(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "Completed"
                self.save_tasks()
                print(f"Task '{task['title']}' marked as completed!")
                return
        print(f"Task with ID {task_id} not found.")
    
    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(i)
                self.save_tasks()
                print(f"Task '{removed['title']}' deleted successfully!")
                return
        print(f"Task with ID {task_id} not found.")


def main():
    task_manager = TaskManager()
    
    while True:
        print("\nTASK MANAGER")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            title = input("Enter task title: ")
            if not title.strip():
                print("Error: Task title cannot be empty.")
                continue  # vuelve al menú principal sin agregar la tarea
            description = input("Enter task description: ")
            due_date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
            
            # Validar formato de fecha
            if due_date_input:
                try:
                    datetime.strptime(due_date_input, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format! Task will be added without due date.")
                    due_date_input = None
            else:
                due_date_input = None
            
            task_manager.add_task(title, description, due_date_input)
        
        elif choice == "2":
            task_manager.list_tasks()
        
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to mark as complete: "))
                task_manager.mark_complete(task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
