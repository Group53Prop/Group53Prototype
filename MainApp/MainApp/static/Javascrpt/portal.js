
//Creates Calender
function createCalendar(containerId) {
    const now = new Date();
    const today = now.getDay();
    const currentDate = now.getDate();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();

    const container = document.getElementById(containerId);
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const calendarTable = document.createElement('table');
    calendarTable.className = 'calendar-table';

    const headerRow = document.createElement('tr');
    daysOfWeek.forEach((day, index) => {
        const dayCell = document.createElement('th');
        dayCell.innerHTML = `${day}<br>`;

        const dateForDay = new Date(currentYear, currentMonth, currentDate - today + index);
        const dateSpan = document.createElement('span');
        dateSpan.className = 'date-span';
        dateSpan.textContent = dateForDay.getDate();

        dayCell.appendChild(dateSpan);

        if (today === index) {
            dayCell.classList.add('today');
        }
        headerRow.appendChild(dayCell);
    });
    calendarTable.appendChild(headerRow);

    const hourStart = 9;
    const hourEnd = 18;
    for (let hour = hourStart; hour <= hourEnd; hour++) {
        const timeRow = document.createElement('tr');
        for (let day = 0; day < 7; day++) {
            const timeCell = document.createElement('td');
            if (day === 0) {
                const timeLabel = document.createElement('span');
                timeLabel.textContent = `${hour}:00`;
                timeCell.appendChild(timeLabel);
            }
            timeRow.appendChild(timeCell);
        }
        calendarTable.appendChild(timeRow);
    }

    container.appendChild(calendarTable);

    const tasks = [{
            day: 0,
            duration: 1,
            startTime: '09:00',
            endTime: '10:20',
            title: 'Task 1'
        },
        {
            day: 2,
            duration: 2,
            startTime: '10:30',
            endTime: '11:50',
            title: 'Task 2'
        },
        {
            day: 4,
            duration: 2,
            startTime: '14:30',
            endTime: '16:15',
            title: 'Task 3'
        }
    ];

    function createTaskElement(task) {
        const taskElement = document.createElement('div');
        taskElement.className = 'task';
        taskElement.textContent = `${task.title}: ${task.startTime}-${task.endTime}`;
        return taskElement;
    }

    tasks.forEach(task => {
        const dayIndex = task.day + 1;
        const taskElement = createTaskElement(task);
        const taskStartHour = parseInt(task.startTime.split(':')[0], 10);
        const taskRow = calendarTable.children[taskStartHour - hourStart + 1];

        if (task.duration > 1) {
            for (let i = 1; i < task.duration; i++) {
                const cellToClear = taskRow.children[dayIndex + i];
                cellToClear.parentNode.removeChild(cellToClear);
            }

            taskRow.children[dayIndex].colSpan = task.duration;
        }

        taskRow.children[dayIndex].appendChild(taskElement);
    });
}

window.onload = function () {
    createCalendar('calendar');
};
// AUTO LOGOUT
let logoutTimer;
const logoutAfterInactivity = () => {
    
    fetch('/accounts/logout/', {
        method: 'POST',
        credentials: 'same-origin', 
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), 
        },
    }).then(response => {
        if (response.ok) {
            window.location.href = '/';
            
        }
    });
};

const resetLogoutTimer = () => {
    clearTimeout(logoutTimer);
    logoutTimer = setTimeout(logoutAfterInactivity, 900000); 
};

document.onload = resetLogoutTimer;
document.onmousemove = resetLogoutTimer;
document.onkeypress = resetLogoutTimer;

// Function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;


}