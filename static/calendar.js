document.addEventListener('DOMContentLoaded', function () {
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const calendarBody = document.getElementById('calendar-body');
    const calendarTable = document.querySelector('.calendar');
    const monthYearElement = document.getElementById('month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const currentMonthBtn = document.getElementById('current-month');

    prevMonthBtn.addEventListener('click', goToPrevMonth);
    nextMonthBtn.addEventListener('click', goToNextMonth);
    currentMonthBtn.addEventListener('click', goToCurrentMonth);

    generateCalendar(currentMonth, currentYear);

    function generateCalendar(month, year) {
        calendarBody.innerHTML = '';
        monthYearElement.innerHTML = `${monthNames[month]} <b>${year}</b>`;

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const daysInPrevMonth = new Date(year, month, 0).getDate();
        const rowsNeeded = Math.ceil((firstDay + daysInMonth) / 7);

        if (rowsNeeded <= 5) {
            const cellSize = rowsNeeded === 4 ? '50px' : '45px';
            const spacing = rowsNeeded === 4 ? '15px 10px' : '12px 8px';
            calendarTable.style.borderSpacing = spacing;

            const dateNumbers = document.querySelectorAll('.date-number');
            dateNumbers.forEach(num => {
                num.style.width = cellSize;
                num.style.height = cellSize;
            });
        } else {
            calendarTable.style.borderSpacing = '10px 5px';
        }

        let date = 1;
        let nextMonthDate = 1;

        for (let i = 0; i < 6; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                const dateNumber = document.createElement('div');

                if (i === 0 && j < firstDay) {
                    const prevMonthDay = daysInPrevMonth - (firstDay - j - 1);
                    dateNumber.className = 'date-number other-month';
                    dateNumber.textContent = prevMonthDay;

                    let prevMonth = month - 1 < 0 ? 11 : month - 1;
                    dateNumber.addEventListener('dblclick', async function() {
                        await edit(dateNumber.textContent, monthNames[prevMonth]);
                    });

                    dateNumber.addEventListener('click', async function() {
                        await retrieve(dateNumber.textContent, monthNames[prevMonth]);
                    });

                } else if (date <= daysInMonth) {
                    dateNumber.className = 'date-number';
                    dateNumber.textContent = date;

                    if (
                        date === currentDate.getDate() &&
                        month === currentDate.getMonth() &&
                        year === currentDate.getFullYear()
                    ) {
                        dateNumber.classList.add('current-date');
                    }

                    dateNumber.addEventListener('dblclick', async function() {
                        await edit(dateNumber.textContent, monthNames[month]);
                    });
                    
                    dateNumber.addEventListener('click', async function() {
                        await retrieve(dateNumber.textContent, monthNames[month]);  
                    });

                    date++;
                } else {
                    dateNumber.className = 'date-number other-month';
                    dateNumber.textContent = nextMonthDate;

                    let nextMonth = (month + 1) % 12;
                    dateNumber.addEventListener('dblclick', async function() {
                        await edit(dateNumber.textContent, monthNames[nextMonth]);
                    });
                    
                    dateNumber.addEventListener('click', async function() {
                        await retrieve(dateNumber.textContent, monthNames[nextMonth]);
                    });

                    nextMonthDate++;
                }

                cell.appendChild(dateNumber);
                row.appendChild(cell);
            }

            calendarBody.appendChild(row);

            if (date > daysInMonth && i >= 3) break;
        }

        const cellSize = rowsNeeded <= 5 ? (rowsNeeded === 4 ? '50px' : '45px') : '40px';
        const dateNumbers = document.querySelectorAll('.date-number');
        dateNumbers.forEach(num => {
            num.style.width = cellSize;
            num.style.height = cellSize;
        });
    }

    function goToPrevMonth() {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        generateCalendar(currentMonth, currentYear);
    }

    function goToNextMonth() {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        generateCalendar(currentMonth, currentYear);
    }

    function goToCurrentMonth() {
        const now = new Date();
        currentMonth = now.getMonth();
        currentYear = now.getFullYear();
        generateCalendar(currentMonth, currentYear);
    }


    async function edit(day, month){
        let formData = new FormData();
        formData.append('day', day);
        formData.append('month', month);
            
        fetch('/journal_entry', {
            method: 'POST',
            body: formData
        }).then(response => {
            window.location.href = `/journal_entry?day=${date}&month=${monthNames[month]}`;
        })
        .catch(error => {
            console.log(error);
        });
    }

    async function retrieve(day, month){
        let formData = new FormData();
        formData.append('day', day);
        formData.append('month', month);
            
        fetch('/get_journal_entry', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(async  data => {
            if (data.hasOwnProperty('entry')) {
                const entry = data.entry;
                const date = data.date;
                document.getElementById('journal-entry').textContent = entry;
                document.getElementById('title').textContent = date;
                document.getElementById('journal-display').style.display = 'flex';
                if (entry === ''){
                    ocument.getElementById('journal-display').style.display = 'none';
                    await edit(day, month);
                }
            }
        })
        .catch(error => {
            console.log(error);
        });
    }


    document.getElementById('edit').addEventListener('click', async function() {
        const date = document.getElementById('title').toString();
        const temp = date.split(" ");
        const day = temp[0];
        const month = temp[1];
        await edit(day, month);
    });
});

