document.addEventListener('DOMContentLoaded', function() {
    const scrollPosition = "{{ scroll_position }}";
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const tableRows = document.querySelectorAll('tbody tr');
    const headers = document.querySelectorAll('th');



    const filterInput = document.createElement('input');
    filterInput.type = 'text';
    filterInput.placeholder = 'Filter...';
    document.body.insertBefore(filterInput, document.body.firstChild);

    filterInput.addEventListener('input', () => {
        const filter = filterInput.value.toLowerCase();

        tableRows.forEach(row => {
            let match = false;
            Array.from(row.cells).forEach((cell, cellIndex) => {
                if (cellIndex !== headers.length - 1) { 
                    const text = cell.innerText.toLowerCase();
                    if (text.includes(filter)) {
                        match = true;
                    }
                }
            });
            row.style.display = match ? '' : 'none';
        });
    });
});
