from todo.task import *
class ToDoManagerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        geometry = "800x750"
        self.title("Texter")
        self.__build_components()
        self.mainloop()
    def __clear_completed_task(self) -> None: #Прикол 2
        self.completed_task_items = []
        self.completed_task_var.set(
            self.completed_task_items
        )
    def __task_input_window(self, task_edit_window: bool=False, task_value: str="") -> str | None:
        if (not task_edit_window):
            _task_manager = NewTaskManager(self)
            _task_manager.window.grab_set()
        else: 
            _task_manager = EditTaskManager(self, task_value)
            _task_manager.window.grab_set()
        while _task_manager.task_value == None:
            self.update()
        new_task = _task_manager.task_value
        _task_manager.window.destroy()
        if new_task:
            return new_task
        else: 
            return None
    def __add_task(self, _completed: bool=False) -> None:
        if (not _completed):
            new_task_input = self.__task_input_window()
            if (new_task_input):
                number_of_ongoing_tasks = len(self.ongoing_task_items)
                self.ongoing_task_items.append(f"{number_of_ongoing_tasks+1}. {new_task_input}")
                self.ongoing_task_var.set(
                    self.ongoing_task_items
                )
                file = open("data.txt", "w")
                file.close()
                file = open("data.txt", "a")
                for i in self.ongoing_task_items:
                    file.write(i + "\n")
                file.close()
        else:
            number_of_completed_tasks = len(self.completed_task_items)
            _completed_task = self.__delete_task() 
            completed_task = " ".join(
                _completed_task.split()[1:]
            )
            self.completed_task_items.append(
                f"{number_of_completed_tasks+1}. {completed_task}"
            )
            self.completed_task_var.set(
                self.completed_task_items
            )
            self.update()
    def add_task(self, completed: bool=False):
        self.__add_task(completed)
    def __delete_task(self) -> str:
        selected_task_index = self.ongoing_tasks_listbox.curselection()[0] 
        ongoing_tasks = self.ongoing_task_items.copy() 
        removed_item = ongoing_tasks.pop(selected_task_index)
        ongoing_tasks = [
           " ".join(task.split()[1:]) for task in ongoing_tasks
        ]
        new_ongoing_task = [ ]
        for task_id, task in enumerate(ongoing_tasks): 
            new_ongoing_task.append(
                f"{task_id+1}. {task}"
            )
        self.ongoing_task_items = new_ongoing_task 
        self.ongoing_task_var.set(
            self.ongoing_task_items
        )
        file = open("data.txt", "w")
        file.close()
        file = open("data.txt", "a")
        for i in self.ongoing_task_items:
            file.write(i + "\n")
        file.close()
        return removed_item
    def delete_task(self): # прикол1
        self.__delete_task()
    def __edit_task(self) -> None:
        selected_task_index = self.ongoing_tasks_listbox.curselection()[0]
        print(selected_task_index)
        selected_task = self.ongoing_task_items[selected_task_index].split()[1:]
        new_task_input = self.__task_input_window(True, selected_task)
        if (new_task_input):
            self.ongoing_task_items[selected_task_index] = f"{selected_task_index+1}. {new_task_input}"
            self.ongoing_task_var.set(
                self.ongoing_task_items
            )
        file = open("data.txt", "w")
        file.close()
        file = open("data.txt", "a")
        for i in self.ongoing_task_items:
            file.write(i + "\n")
        file.close()
    def edit_task(self):
        self.__edit_task()
    def __build_components(self) -> None:
        Button = ttk.Button
        Frame = ttk.Frame
        Label = ttk.Label
        Listbox = tk.Listbox
        Variable = tk.Variable
        
        label_grid_options = {
            "ipadx" : 5, "ipady" : 5, "padx" : 1.5, "pady" : 1.5, "sticky" : "w"
        } 
        button_grid_options = {
            "ipadx" : 15, "ipady" : 15, "padx" : 1.5, "sticky" : "ne", 
        }

        self.ongoing_task_items = []
        if (len(self.ongoing_task_items) == 0):
            with open('data.txt', 'r') as file:
                self.ongoing_task_items = file.readlines()
        self.completed_task_items = []
        self.ongoing_task_var = Variable(value=self.ongoing_task_items)
        self.completed_task_var = Variable(value=self.completed_task_items)

        ongoing_tasks_label = Label(self, text="ONGOING TASKS")
        ongoing_tasks_label.grid(
            column=0, row=0, **label_grid_options
        )
        self.ongoing_tasks_listbox = Listbox(self, listvariable=self.ongoing_task_var, selectmode="single")
        self.ongoing_tasks_listbox.grid(
            column=0, row=1, sticky="w", ipadx=255, ipady=85, padx=1.5, columnspan=4, 
        )

        completed_task_label = Label(self, text="COMPLETED TASKS")
        completed_task_label.grid(
            column=0, row=2, **label_grid_options
        )
        completed_task_listbox = Listbox(self, listvariable=self.completed_task_var, state="disabled")
        completed_task_listbox.grid(
            column=0, row=3, sticky="w", ipadx=265, ipady=50, padx=1.5, columnspan=4,
        )

        #button moment

        button_frame = Frame(self, width=100, height=200, cursor="dot")
        button_frame.grid(
            column=4, row=1, sticky="nw", ipadx=1.5
        )

        add_button = Button(button_frame, text="add task", command=self.__add_task)
        add_button.grid(
            column=0, row=0, **button_grid_options
        )

        edit_button = Button(button_frame, text="edit task", command=lambda: self.edit_task())
        edit_button.grid(
            column=0, row=1, **button_grid_options
        )

        remove_button = Button(button_frame, text="remove task", command=lambda: self.delete_task())
        remove_button.grid(
            column=0, row=2, **button_grid_options
        )

        check_button = Button(button_frame, text="completed", command=lambda: self.add_task(True))
        check_button.grid(
            column=0, row=3, **button_grid_options
        )

        clear_button = Button(
            self, text="clear", command=self.__clear_completed_task
        )
        clear_button.grid(
            column=4, row=3, sticky="nw", ipadx=15, ipady=15
        )
ToDoManagerGUI()