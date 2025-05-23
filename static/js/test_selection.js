document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const subjectFilter = document.getElementById('subject-filter');
    const testCards = document.querySelectorAll('.test-card');
    
    if (subjectFilter) {
        const uniqueSubjects = new Map();
        Array.from(subjectFilter.options).forEach(option => {
            if (option.value) {
                uniqueSubjects.set(option.value, option.text);
            }
        });
        
        subjectFilter.innerHTML = '<option value="">Все предметы</option>';
        
        uniqueSubjects.forEach((text, value) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = text;
            subjectFilter.appendChild(option);
        });
    }
    
    if (searchInput && subjectFilter) {
        searchInput.addEventListener('input', filterTests);
        subjectFilter.addEventListener('change', filterTests);
        
        if (searchButton) {
            searchButton.addEventListener('click', filterTests);
        }
        
        function filterTests() {
            const searchTerm = searchInput.value.toLowerCase();
            const subjectId = subjectFilter.value;
            let matchFound = false;
            
            testCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                const cardSubjectId = card.dataset.subject;
                
                const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
                const matchesSubject = subjectId === '' || cardSubjectId === subjectId;
                
                if (matchesSearch && matchesSubject) {
                    card.style.display = '';
                    matchFound = true;
                } else {
                    card.style.display = 'none';
                }
            });
            
            const noResultsElement = document.getElementById('no-results');
            if (noResultsElement) {
                if (matchFound) {
                    noResultsElement.classList.add('d-none');
                } else {
                    noResultsElement.classList.remove('d-none');
                }
            }
        }
    }
    
    testCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
        card.classList.add('animate__animated', 'animate__fadeIn');
    });
}); 