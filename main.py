from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from database import init_db, add_task, get_tasks, delete_task

class TaskApp(App):
    def __init__(self, **kwargs):
        super(TaskApp, self).__init__(**kwargs)

        self.layout = None
        self.task_input = None
        self.tasks_layout = None

    def build(self):
        init_db() # инициализация базы данных
        # Основной макет
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Поле для ввода новой задачи
        self.task_input = TextInput(hint_text="Введите задачу", size_hint_y=None, height=50)
        self.layout.add_widget(self.task_input)

        # Кнопка для добавления задачи
        add_button = Button(text="Добавить задачу", size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_task)
        self.layout.add_widget(add_button)

        # Список задач
        self.tasks_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

        # ScrollView для прокрутки списка задач
        scroll_view = ScrollView(size_hint=(1, None), size=(self.layout.width, 300))
        scroll_view.add_widget(self.tasks_layout)
        self.layout.add_widget(scroll_view)

        # загрузка задач из базы данных
        self.load_tasks()

        return self.layout

    def load_tasks(self):
        tasks = get_tasks()
        for task in tasks:
            task_id, task_text = task
            self.add_task_to_layout(task_id, task_text)

    def add_task(self, instance):
        # Добавление задачи в список
        task_text = self.task_input.text
        if task_text:
            task_id = add_task(task_text) # сохраняем задачу в базе данных
            self.add_task_to_layout(task_id, task_text)
            self.task_input.text = '' # очистка поля ввода

    def add_task_to_layout(self, task_id, task_text):
        task_label = Label(text=task_text, size_hint_y=None, height=40)
        delete_button = Button(text="Удалить", size_hint_y=None, height=40)
        delete_button.bind(on_press=lambda btn: self.remove_task(task_id, task_label))

        task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        task_box.add_widget(task_label)
        task_box.add_widget(delete_button)

        self.tasks_layout.add_widget(task_box)


    def remove_task(self, task_id, task_label):
        delete_task(task_id)
        self.tasks_layout.remove_widget(task_label.parent)

if __name__ == "__main__":
    TaskApp().run()
