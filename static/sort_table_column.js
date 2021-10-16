const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

// Comparer logic lambda. Takes in column index and flips asc each time
const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    // If v1 and v1 is not empty, subtract v2 from v1 and compare value to v2, return a number
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));  //

// Create a click event listener for all 'th' elements
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    const table = th.closest('table');  // Get table element of 'th'
    Array.from(table.querySelectorAll('tbody > tr'))    // Get all 'tr' row elements in 'tbody'
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc =! this.asc))   // Sort with comparer lambda
        .forEach(tr => table.querySelector('tbody').appendChild(tr));   // Append 'tr' row element back to 'tbody'
})));