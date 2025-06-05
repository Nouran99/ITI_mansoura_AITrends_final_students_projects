let currentJobId = null;
let statusCheckInterval = null;

const form = document.getElementById('learningForm');
const submitBtn = document.getElementById('submitBtn');
const progressSection = document.getElementById('progressSection');
const progressText = document.getElementById('progressText');
const progressFill = document.getElementById('progressFill');
const resultsSection = document.getElementById('resultsSection');
const summaryContent = document.getElementById('summaryContent');
const downloadBtn = document.getElementById('downloadBtn');
const memoryGameSection = document.getElementById('memoryGameSection');

// Memory Game Variables
let gameCards = [];
let flippedCards = [];
let matchedPairs = 0;
let moves = 0;
let gameTime = 0;
let gameTimer = null;
let isGamePaused = false;
let canFlip = true;

// Memory Game Symbols (using emojis for visual appeal)
const gameSymbols = ['🚀', '🎯', '💡', '🔥', '⭐', '🎨', '🧠', '💎'];

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const topic = formData.get('topic').trim();
    const level = formData.get('level');

    if (!topic || !level) {
        showError('Please fill in all fields');
        return;
    }

    startLearningProcess(topic, level);
});

async function startLearningProcess(topic, level) {
    try {
        // Update UI
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        progressSection.classList.add('show');
        resultsSection.classList.remove('show');
        
        progressText.textContent = 'Starting your learning journey...';
        progressFill.style.width = '10%';

        // Show memory game
        memoryGameSection.classList.add('show');
        initializeMemoryGame();

        // Start the learning process
        const response = await fetch('/api/start-learning', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic_name: topic,
                learning_level: level
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to start learning process');
        }

        currentJobId = data.job_id;
        
        // Start checking status
        checkJobStatus();
        statusCheckInterval = setInterval(checkJobStatus, 2000);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
        resetUI();
    }
}

async function checkJobStatus() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`/api/job-status/${currentJobId}`);
        const job = await response.json();

        if (!response.ok) {
            throw new Error(job.error || 'Failed to check job status');
        }

        updateProgress(job);

        if (job.status === 'completed') {
            clearInterval(statusCheckInterval);
            showResults(job);
            resetUI();
            hideMemoryGame();
        } else if (job.status === 'failed') {
            clearInterval(statusCheckInterval);
            showError(job.error || 'Job failed');
            resetUI();
            hideMemoryGame();
        }

    } catch (error) {
        console.error('Status check error:', error);
        clearInterval(statusCheckInterval);
        showError('Failed to check job status');
        resetUI();
        hideMemoryGame();
    }
}

function updateProgress(job) {
    const statusMap = {
        'starting': { text: 'Preparing your learning journey...', progress: 20 },
        'running': { text: job.progress || 'Processing...', progress: 60 },
        'completed': { text: 'Complete! Processing results...', progress: 100 }
    };

    const status = statusMap[job.status] || { text: 'Processing...', progress: 40 };
    progressText.textContent = status.text;
    progressFill.style.width = status.progress + '%';
}

function showResults(job) {
    if (job.summary) {
        // Parse and render markdown
        renderMarkdown(job.summary);
        downloadBtn.href = `/api/download-report/${currentJobId}`;
        resultsSection.classList.add('show');
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function hideMemoryGame() {
    setTimeout(() => {
        memoryGameSection.classList.remove('show');
        stopGameTimer();
    }, 1000);
}

function renderMarkdown(markdownText) {
    // Configure marked with GitHub-like options
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: true,
        mangle: false,
        sanitize: false,
        smartLists: true,
        smartypants: false,
        xhtml: false,
        highlight: function(code, lang) {
            if (Prism.languages[lang]) {
                return Prism.highlight(code, Prism.languages[lang], lang);
            }
            return code;
        }
    });

    // Custom renderer for better formatting
    const renderer = new marked.Renderer();
    
    // Custom link renderer to add target="_blank"
    renderer.link = function(href, title, text) {
        const link = marked.Renderer.prototype.link.call(this, href, title, text);
        return link.replace('<a', '<a target="_blank" rel="noopener noreferrer"');
    };

    // Custom list item renderer for better styling
    renderer.listitem = function(text) {
        return `<li class="resource-item">${text}</li>`;
    };

    marked.setOptions({ renderer: renderer });

    // Parse markdown and inject into DOM
    const htmlContent = marked.parse(markdownText);
    summaryContent.innerHTML = htmlContent;

    // Highlight code blocks
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }

    // Add copy buttons to code blocks
    addCopyButtons();
}

function addCopyButtons() {
    const codeBlocks = summaryContent.querySelectorAll('pre code');
    codeBlocks.forEach((block, index) => {
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.title = 'Copy code';
        
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent).then(() => {
                button.innerHTML = '<i class="fas fa-check"></i>';
                button.style.color = '#10b981';
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-copy"></i>';
                    button.style.color = '';
                }, 2000);
            });
        });

        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
    });
}

// Memory Game Functions
function initializeMemoryGame() {
    resetGameStats();
    createGameBoard();
    startGameTimer();
    setupGameControls();
}

function resetGameStats() {
    moves = 0;
    matchedPairs = 0;
    gameTime = 0;
    flippedCards = [];
    canFlip = true;
    isGamePaused = false;
    
    updateGameStats();
}

function createGameBoard() {
    const grid = document.getElementById('memoryGrid');
    grid.innerHTML = '';
    
    // Create pairs of cards
    gameCards = [...gameSymbols, ...gameSymbols]
        .sort(() => Math.random() - 0.5);
    
    gameCards.forEach((symbol, index) => {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.dataset.symbol = symbol;
        card.dataset.index = index;
        
        card.innerHTML = `
            <div class="card-face card-back">
                <i class="fas fa-question"></i>
            </div>
            <div class="card-face card-front">
                ${symbol}
            </div>
        `;
        
        card.addEventListener('click', () => flipCard(card));
        grid.appendChild(card);
    });
}

function flipCard(card) {
    if (!canFlip || card.classList.contains('flipped') || card.classList.contains('matched') || isGamePaused) {
        return;
    }
    
    card.classList.add('flipped');
    flippedCards.push(card);
    
    if (flippedCards.length === 2) {
        moves++;
        updateGameStats();
        canFlip = false;
        
        setTimeout(() => checkForMatch(), 600);
    }
}

function checkForMatch() {
    const [card1, card2] = flippedCards;
    const isMatch = card1.dataset.symbol === card2.dataset.symbol;
    
    if (isMatch) {
        card1.classList.add('matched');
        card2.classList.add('matched');
        matchedPairs++;
        updateGameStats();
        
        if (matchedPairs === gameSymbols.length) {
            gameComplete();
        }
    } else {
        setTimeout(() => {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
        }, 500);
    }
    
    flippedCards = [];
    canFlip = true;
}

function gameComplete() {
    stopGameTimer();
    
    const grid = document.getElementById('memoryGrid');
    const completeMessage = document.createElement('div');
    completeMessage.className = 'game-complete';
    completeMessage.innerHTML = `
        <h4><i class="fas fa-trophy"></i> Congratulations!</h4>
        <p>You completed the game in ${moves} moves and ${formatTime(gameTime)}!</p>
    `;
    
    grid.parentNode.appendChild(completeMessage);
}

function startGameTimer() {
    gameTimer = setInterval(() => {
        if (!isGamePaused) {
            gameTime++;
            updateGameStats();
        }
    }, 1000);
}

function stopGameTimer() {
    if (gameTimer) {
        clearInterval(gameTimer);
        gameTimer = null;
    }
}

function pauseGame() {
    isGamePaused = !isGamePaused;
    const pauseBtn = document.getElementById('pauseGameBtn');
    
    if (isGamePaused) {
        pauseBtn.innerHTML = '<i class="fas fa-play"></i> Resume';
        // Hide card faces when paused
        document.querySelectorAll('.memory-card.flipped:not(.matched)').forEach(card => {
            card.style.opacity = '0.5';
        });
    } else {
        pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
        document.querySelectorAll('.memory-card').forEach(card => {
            card.style.opacity = '1';
        });
    }
}

function resetGame() {
    stopGameTimer();
    document.querySelector('.game-complete')?.remove();
    initializeMemoryGame();
}

function setupGameControls() {
    const resetBtn = document.getElementById('resetGameBtn');
    const pauseBtn = document.getElementById('pauseGameBtn');
    
    resetBtn.onclick = resetGame;
    pauseBtn.onclick = pauseGame;
}

function updateGameStats() {
    document.getElementById('movesCount').textContent = moves;
    document.getElementById('matchesCount').textContent = matchedPairs;
    document.getElementById('timeCount').textContent = formatTime(gameTime);
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function showError(message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.error-message, .success-message');
    existingMessages.forEach(msg => msg.remove());

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    form.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function resetUI() {
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
    setTimeout(() => {
        progressSection.classList.remove('show');
    }, 1000);
}

// Add some interactive animations
document.addEventListener('DOMContentLoaded', () => {
    // Add focus animations to form elements
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('focus', () => {
            control.style.transform = 'translateY(-2px)';
        });
        
        control.addEventListener('blur', () => {
            control.style.transform = 'translateY(0)';
        });
    });

    // Add floating animation to header
    const header = document.querySelector('.header h1');
    setInterval(() => {
        header.style.transform = 'translateY(-5px)';
        setTimeout(() => {
            header.style.transform = 'translateY(0)';
        }, 1000);
    }, 4000);
});