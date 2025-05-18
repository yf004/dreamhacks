// Calendar functionality
document.addEventListener('DOMContentLoaded', function() {
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();
    
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    
    const dayNames = [
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ];
    
    // Elements
    const calendarBody = document.getElementById('calendar-body');
    const calendarTable = document.querySelector('.calendar');
    const monthYearElement = document.getElementById('month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const currentMonthBtn = document.getElementById('current-month');
    const dayMonthElement = document.querySelector('.day-month');
    
    // Event listeners for navigation
    prevMonthBtn.addEventListener('click', goToPrevMonth);
    nextMonthBtn.addEventListener('click', goToNextMonth);
    currentMonthBtn.addEventListener('click', goToCurrentMonth);
    
    // Initialize the calendar and day-month display
    generateCalendar(currentMonth, currentYear);
    updateDayMonth();
    
    // Function to update the day-month display
    function updateDayMonth() {
        const today = new Date();
        const dayName = dayNames[today.getDay()];
        const monthName = monthNames[today.getMonth()];
        const dayNumber = today.getDate();
        
        // Format: "Monday May 18"
        dayMonthElement.innerHTML = `${dayName} <b>${monthName} ${dayNumber}</b>`;
    }
    
    // Function to generate the calendar
    function generateCalendar(month, year) {
        // Clear previous calendar
        calendarBody.innerHTML = '';
        
        // Update month-year display
        monthYearElement.innerHTML = `${monthNames[month]} <b>${year}</b>`;
        
        // Get the first day of the month (0 = Sunday, 1 = Monday, etc.)
        const firstDay = new Date(year, month, 1).getDay();
        
        // Get the number of days in the month
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Get the number of days in the previous month
        const daysInPrevMonth = new Date(year, month, 0).getDate();
        
        // Calculate rows needed for this month
        const rowsNeeded = Math.ceil((firstDay + daysInMonth) / 7);
        
        // Adjust spacing based on number of rows needed
        if (rowsNeeded <= 5) {
            const cellSize = rowsNeeded === 4 ? '50px' : '45px';
            const spacing = rowsNeeded === 4 ? '15px 10px' : '12px 8px';
            calendarTable.style.borderSpacing = spacing;
            
            // Update date number size
            const dateNumbers = document.querySelectorAll('.date-number');
            dateNumbers.forEach(num => {
                num.style.width = cellSize;
                num.style.height = cellSize;
            });
        } else {
            calendarTable.style.borderSpacing = '10px 5px';
        }
        
        // Create calendar cells
        let date = 1;
        let nextMonthDate = 1;
        
        // Create rows (typically 6 rows can fit all month variations)
        for (let i = 0; i < 6; i++) {
            // Create a table row
            const row = document.createElement('tr');
            
            // Create cells for each day of the week
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                
                // Fill in dates from previous month
                if (i === 0 && j < firstDay) {
                    const prevMonthDay = daysInPrevMonth - (firstDay - j - 1);
                    const dateNumber = document.createElement('div');
                    dateNumber.className = 'date-number other-month';
                    dateNumber.textContent = prevMonthDay;
                    cell.appendChild(dateNumber);
                } 
                // Fill in dates for the current month
                else if (date <= daysInMonth) {
                    const dateNumber = document.createElement('div');
                    dateNumber.className = 'date-number';
                    dateNumber.textContent = date;
                    
                    // Highlight today's date
                    if (
                        date === currentDate.getDate() && 
                        month === currentDate.getMonth() && 
                        year === currentDate.getFullYear()
                    ) {
                        dateNumber.classList.add('current-date');
                    }
                    
                    cell.appendChild(dateNumber);
                    date++;
                } 
                // Fill in dates from next month
                else {
                    const dateNumber = document.createElement('div');
                    dateNumber.className = 'date-number other-month';
                    dateNumber.textContent = nextMonthDate;
                    cell.appendChild(dateNumber);
                    nextMonthDate++;
                }
                
                row.appendChild(cell);
            }
            
            calendarBody.appendChild(row);
            
            // Stop creating rows if we've already used all days of the month
            // and we've completed at least 4 rows (for consistency)
            if (date > daysInMonth && i >= 3) break;
        }
        
        // Set the appropriate cell size based on row count
        const cellSize = rowsNeeded <= 5 ? (rowsNeeded === 4 ? '50px' : '45px') : '40px';
        const dateNumbers = document.querySelectorAll('.date-number');
        dateNumbers.forEach(num => {
            num.style.width = cellSize;
            num.style.height = cellSize;
        });
    }
    
    // Navigation functions
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