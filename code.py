import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, task_id, description, priority):
        self._task_id = task_id
        self._description = description
        self._priority = priority
        self._completed = False

    @property
    def task_id(self):
        return self._task_id

    @property
    def description(self):
        return self._description

    @property
    def priority(self):
        return self._priority

    @property
    def completed(self):
        return self._completed

    def mark_completed(self):
        self._completed = True

class PriorityQueue:
    def __init__(self):
        self._tasks = []

    def enqueue(self, task):
        self._tasks.append(task)
        self._tasks.sort(key=lambda x: x.priority, reverse=True)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._tasks.pop()

    def is_empty(self):
        return len(self._tasks) == 0

class Stack:
    def __init__(self):
        self._tasks = []

    def push(self, task):
        self._tasks.append(task)

    def pop(self):
        if self.is_empty():
            return None
        return self._tasks.pop()

    def is_empty(self):
        return len(self._tasks) == 0

class TaskManager:
    def __init__(self):
        self.task_queue = PriorityQueue()
        self.task_history = Stack()
        self.task_id_counter = 1

    def add_task(self, description, priority):
        task = Task(self.task_id_counter, description, priority)
        self.task_queue.enqueue(task)
        self.task_id_counter += 1

    def get_task_by_id(self, task_id):
        for task in self.task_queue._tasks:
            if task.task_id == task_id:
                return task
        return None

    def mark_highest_priority_completed(self):
        if not self.task_queue.is_empty():
            task = self.task_queue.dequeue()
            task.mark_completed()
            self.task_history.push(task)
            return task
        return None

    def get_all_tasks(self):
        return [task for task in self.task_queue._tasks]

    def get_incomplete_tasks(self):
        return [task for task in self.task_queue._tasks if not task.completed]

    def get_last_completed_task(self):
        return self.task_history._tasks[-1] if not self.task_history.is_empty() else None

# GUI Implementation using Tkinter

class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.task_manager = TaskManager()

        # Widgets
        self.label_description = tk.Label(master, text="Description:")
        self.label_description.grid(row=0, column=0)
        self.entry_description = tk.Entry(master)
        self.entry_description.grid(row=0, column=1)

        self.label_priority = tk.Label(master, text="Priority:")
        self.label_priority.grid(row=1, column=0)
        self.entry_priority = tk.Entry(master)
        self.entry_priority.grid(row=1, column=1)

        self.button_add_task = tk.Button(master, text="Add Task", command=self.add_task)
        self.button_add_task.grid(row=2, columnspan=2)

        self.button_get_task = tk.Button(master, text="Get Task", command=self.get_task)
        self.button_get_task.grid(row=3, columnspan=2)

        self.button_mark_completed = tk.Button(master, text="Mark Completed", command=self.mark_completed)
        self.button_mark_completed.grid(row=4, columnspan=2)

        self.button_display_all_tasks = tk.Button(master, text="Display All Tasks", command=self.display_all_tasks)
        self.button_display_all_tasks.grid(row=5, columnspan=2)

        self.button_display_incomplete_tasks = tk.Button(master, text="Display Incomplete Tasks", command=self.display_incomplete_tasks)
        self.button_display_incomplete_tasks.grid(row=6, columnspan=2)

        self.button_display_last_completed_task = tk.Button(master, text="Display Last Completed Task", command=self.display_last_completed_task)
        self.button_display_last_completed_task.grid(row=7, columnspan=2)

        self.text_tasks = tk.Text(master, height=10, width=40)
        self.text_tasks.grid(row=8, columnspan=2)

    def add_task(self):
        description = self.entry_description.get()
        priority = int(self.entry_priority.get())
        self.task_manager.add_task(description, priority)
        self.display_tasks()

    def get_task(self):
        task_id = int(self.entry_description.get())
        task = self.task_manager.get_task_by_id(task_id)
        if task:
            messagebox.showinfo("Task Details", f"Task: {task.description}, Priority: {task.priority}, Completed: {task.completed}")
        else:
            messagebox.showinfo("Task Not Found", "Task with the provided ID not found.")

    def mark_completed(self):
        completed_task = self.task_manager.mark_highest_priority_completed()
        if completed_task:
            messagebox.showinfo("Task Completed", f"Task '{completed_task.description}' marked as completed.")
            self.display_tasks()
        else:
            messagebox.showinfo("No Task", "No task to mark as completed.")

    def display_all_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        self.display_tasks(tasks)

    def display_incomplete_tasks(self):
        tasks = self.task_manager.get_incomplete_tasks()
        self.display_tasks(tasks)

    def display_last_completed_task(self):
        last_completed_task = self.task_manager.get_last_completed_task()
        if last_completed_task:
            messagebox.showinfo("Last Completed Task", f"Task: {last_completed_task.description}, Priority: {last_completed_task.priority}")
        else:
            messagebox.showinfo("No Completed Task", "No task has been completed yet.")

    def display_tasks(self, tasks=None):
        if not tasks:
            tasks = self.task_manager.get_all_tasks()
        task_display = ""
        for task in tasks:
            task_display += f"ID: {task.task_id}, Description: {task.description}, Priority: {task.priority}, Completed: {task.completed}\n"
        self.text_tasks.delete(1.0, tk.END)
        self.text_tasks.insert(tk.END, task_display)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
