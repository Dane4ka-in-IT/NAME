document.addEventListener('DOMContentLoaded', function() {
    const apiModeCheckbox = document.getElementById('api-mode');
    const testContainer = document.getElementById('test-container');
    const progressBar = document.querySelector('.progress-bar');
    const questionText = document.getElementById('question-text');
    const choicesContainer = document.getElementById('choices-container');
    const answerForm = document.getElementById('answer-form');
    const submitButton = document.getElementById('submit-button');
    const testInfoElement = document.getElementById('test-info');
    
    let sessionId = null;
    let currentQuestionId = null;
    let currentQuestionType = null;
    let totalQuestions = 0;
    let currentIndex = 0;
    
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('session_id')) {
        sessionId = urlParams.get('session_id');
        fetchNextQuestion();
    }
    
    function startTest(testId) {
        fetch(`/api/tests/${testId}/start/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            sessionId = data.session_id;
            totalQuestions = data.total_questions;
            
            const newUrl = `${window.location.pathname}?session_id=${sessionId}`;
            window.history.pushState({}, '', newUrl);
            
            if (testInfoElement) {
                testInfoElement.textContent = data.test_title;
            }
            
            fetchNextQuestion();
        })
        .catch(error => {
            console.error('Error starting test:', error);
            alert('Произошла ошибка при запуске теста. Пожалуйста, попробуйте снова.');
        });
    }
    
    function fetchNextQuestion() {
        if (!sessionId) return;
        
        fetch(`/api/sessions/${sessionId}/next/`)
        .then(response => response.json())
        .then(data => {
            if (data.completed) {
                window.location.href = data.redirect_url;
                return;
            }
            
            currentQuestionId = data.question_id;
            currentQuestionType = data.question_type;
            currentIndex = data.current_index;
            totalQuestions = data.total_questions;
            
            updateProgress();
            questionText.textContent = data.text;
            
            choicesContainer.innerHTML = '';
            
            if (data.question_type === 'MC') {
                renderMultipleChoice(data.choices);
            } else if (data.question_type === 'OA') {
                renderOpenAnswer();
            } else if (data.question_type === 'ORD') {
                renderOrderingQuestion(data.choices);
            }
            
            testContainer.classList.remove('d-none');
        })
        .catch(error => {
            console.error('Error fetching question:', error);
            alert('Произошла ошибка при загрузке вопроса. Пожалуйста, попробуйте снова.');
        });
    }
    
    function submitAnswer(answerData) {
        if (!sessionId || !currentQuestionId) return;
        
        fetch(`/api/sessions/${sessionId}/questions/${currentQuestionId}/submit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(answerData)
        })
        .then(response => response.json())
        .then(data => {
            fetchNextQuestion();
        })
        .catch(error => {
            console.error('Error submitting answer:', error);
            alert('Произошла ошибка при отправке ответа. Пожалуйста, попробуйте снова.');
        });
    }
    
    function updateProgress() {
        if (progressBar) {
            const percentage = (currentIndex / totalQuestions) * 100;
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
            progressBar.textContent = `${currentIndex} / ${totalQuestions}`;
        }
    }
    
    function renderMultipleChoice(choices) {
        const choicesHtml = choices.map(choice => `
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" name="choice" 
                       value="${choice.id}" id="choice_${choice.id}">
                <label class="form-check-label" for="choice_${choice.id}">
                    ${choice.text}
                </label>
            </div>
        `).join('');
        
        choicesContainer.innerHTML = choicesHtml;
    }
    
    function renderOpenAnswer() {
        choicesContainer.innerHTML = `
            <div class="mb-4">
                <textarea class="form-control" name="answer" rows="5" 
                          placeholder="Введите ваш ответ здесь..."></textarea>
            </div>
        `;
    }
    
    function renderOrderingQuestion(choices) {
        const listItems = choices.map(choice => `
            <li class="list-group-item list-group-item-action" data-id="${choice.id}">
                <i class="fas fa-grip-lines me-2"></i>
                ${choice.text}
            </li>
        `).join('');
        
        choicesContainer.innerHTML = `
            <p class="text-muted">Перетаскивайте элементы, чтобы расположить их в правильном порядке:</p>
            <ul id="sortable-list" class="list-group">
                ${listItems}
            </ul>
        `;
        
        const sortableList = document.getElementById('sortable-list');
        if (sortableList) {
            new Sortable(sortableList, {
                animation: 150,
                ghostClass: 'bg-light'
            });
        }
    }
    
    if (answerForm) {
        answerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            let answerData = {};
            
            if (currentQuestionType === 'MC') {
                const selectedChoices = Array.from(
                    document.querySelectorAll('input[name="choice"]:checked')
                ).map(input => parseInt(input.value));
                
                answerData = {
                    selected_choices: selectedChoices
                };
            } else if (currentQuestionType === 'OA') {
                const answer = document.querySelector('textarea[name="answer"]').value;
                answerData = { answer };
            } else if (currentQuestionType === 'ORD') {
                const sortableList = document.getElementById('sortable-list');
                const orderedChoices = Array.from(
                    sortableList.querySelectorAll('li')
                ).map(li => parseInt(li.dataset.id));
                
                answerData = {
                    ordered_choices: orderedChoices
                };
            }
            
            submitAnswer(answerData);
        });
    }
    
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
}); 