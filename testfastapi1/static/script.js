// Получаем все задачи при загрузке страницы
window.onload = function() {
    fetchTodos();
};

// Отправка формы для добавления задачи
document.getElementById("todo-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    const taskData = {
        title: title,
        description: description
    };

    fetch("/todos/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(taskData)
    })
    .then(response => response.json())
    .then(data => {
        fetchTodos();  // Обновляем список задач после добавления
        document.getElementById("title").value = "";
        document.getElementById("description").value = "";
    });
});

// Получение всех задач
function fetchTodos() {
    fetch("/todos/")
    .then(response => response.json())
    .then(data => {
        const todoList = document.getElementById("todo-list");
        todoList.innerHTML = "";  // Очищаем список перед обновлением

        data.forEach(todo => {
            const todoItem = document.createElement("li");
            todoItem.textContent = `${todo.title} - ${todo.description}`;
            if (todo.done) {
                todoItem.classList.add("completed");
            }
            todoList.appendChild(todoItem);
        });
    });
}
