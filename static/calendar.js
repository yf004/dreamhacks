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
                    dateNumber.addEventListener('click', () => {
                        let formData = new FormData();
                        formData.append('day', prevMonthDay);
                        formData.append('month', monthNames[prevMonth]);
                            
                        fetch('/journal_entry', {
                            method: 'POST',
                            body: formData
                        })
                        .catch(error => {
                            error.textContent = "error"; 
                            error.style.display = "block";
                        });
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

                    dateNumber.addEventListener('click', () => {
                        let formData = new FormData();
                        formData.append('day', date);
                        formData.append('month', monthNames[month]);
                            
                        fetch('/journal_entry', {
                            method: 'POST',
                            body: formData
                        })
                        .catch(error => {
                            console.log(error);
                        });
                    });

                    date++;
                } else {
                    dateNumber.className = 'date-number other-month';
                    dateNumber.textContent = nextMonthDate;

                    let nextMonth = (month + 1) % 12;
                    dateNumber.addEventListener('click', async function() {
                        let formData = new FormData();
                        formData.append('day', nextMonthDate);
                        formData.append('month', monthNames[nextMonth]);
                            
                        fetch('/journal_entry', {
                            method: 'POST',
                            body: formData
                        }).catch(error => {
                            console.log(error);
                        });
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
});
