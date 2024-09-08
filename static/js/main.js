document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/drinks')
        .then(response => response.json())
        .then(data => {
            const table = $('#drinkTable').DataTable({
                data: data,
                columns: [
                    { data: 'name' },
                    { data: 'source' },
                    { 
                        data: 'taste',
                        render: function(data) {
                            return data.toFixed(1);
                        }
                    },
                    { 
                        data: 'cost',
                        render: function(data) {
                            return data.toFixed(1);
                        }
                    },
                    { 
                        data: 'fun_factor',
                        render: function(data) {
                            return data.toFixed(1);
                        }
                    },
                    { 
                        data: 'overall_score',
                        render: function(data) {
                            return data.toFixed(1);
                        }
                    }
                ],
                order: [[5, 'desc']], // Sort by overall score by default
                responsive: true,
                pageLength: 10,
                lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
                language: {
                    search: "Search drinks:",
                    lengthMenu: "Show _MENU_ drinks per page",
                    info: "Showing _START_ to _END_ of _TOTAL_ drinks",
                    infoEmpty: "No drinks available",
                    infoFiltered: "(filtered from _MAX_ total drinks)"
                }
            });
        })
        .catch(error => console.error('Error:', error));
});
