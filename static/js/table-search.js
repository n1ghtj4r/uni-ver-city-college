function initTableSearch(searchInputId, tableId, noResultsId) {
    const input = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    const rows = table.querySelectorAll('tbody tr');
    const noResults = document.getElementById(noResultsId);

    input.addEventListener('input', function () {
        const query = input.value.toLowerCase().trim();
        let visible = 0;

        rows.forEach(function (row) {
            const match = row.textContent.toLowerCase().includes(query);
            row.style.display = match ? '' : 'none';
            if (match) visible++;
        });

        if (noResults) {
            noResults.classList.toggle('hidden', visible > 0 || query === '');
        }
        table.classList.toggle('hidden', visible === 0 && query !== '');
    });
}