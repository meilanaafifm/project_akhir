/**
 * PRODI WEBSITE - MAIN JAVASCRIPT
 * Inovasi Website Program Studi dengan Django
 */

document.addEventListener('DOMContentLoaded', function() {
    // Hide preloader
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.classList.add('hidden');
        setTimeout(() => {
            preloader.style.display = 'none';
        }, 300);
    }
    
    // Initialize components
    initNavbar();
    initScrollToTop();
    initChatbot();
    initAnimations();
    initGallery();
});

/**
 * Navbar Scroll Effect
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
}

/**
 * Scroll to Top Button
 */
function initScrollToTop() {
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.className = 'scroll-top';
    scrollTopBtn.innerHTML = '<i class="bi bi-chevron-up"></i>';
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * AI Chatbot System - INOVASI UTAMA
 * Sistem chatbot berbasis knowledge base dengan fitur NLP sederhana
 */
function initChatbot() {
    // Create chatbot toggle button
    const chatbotToggle = document.createElement('button');
    chatbotToggle.className = 'chatbot-toggle';
    chatbotToggle.id = 'chatbotToggle';
    chatbotToggle.innerHTML = '<i class="bi bi-chat-dots-fill"></i>';
    document.body.appendChild(chatbotToggle);
    
    // Create chatbot container
    const chatbotContainer = document.createElement('div');
    chatbotContainer.className = 'chatbot-container';
    chatbotContainer.id = 'chatbotContainer';
    chatbotContainer.innerHTML = `
        <div class="chatbot-header">
            <div class="bot-avatar">
                <i class="bi bi-robot"></i>
            </div>
            <div class="bot-info">
                <h6>Prodi Assistant</h6>
                <small><span class="status-dot">●</span> Online</small>
            </div>
            <button class="btn btn-link text-white ms-auto" onclick="toggleChatbot()">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
        <div class="chatbot-body" id="chatbotBody">
            <div class="chat-message bot">
                <div class="message-bubble">
                    Halo! 👋 Saya asisten virtual Program Studi. Ada yang bisa saya bantu?
                    <div class="quick-replies">
                        <button class="quick-reply-btn" onclick="sendQuickReply('Informasi pendaftaran')">📝 Pendaftaran</button>
                        <button class="quick-reply-btn" onclick="sendQuickReply('Informasi kurikulum')">📚 Kurikulum</button>
                        <button class="quick-reply-btn" onclick="sendQuickReply('Jadwal kuliah')">📅 Jadwal</button>
                        <button class="quick-reply-btn" onclick="sendQuickReply('Kontak')">📞 Kontak</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="chatbot-footer">
            <form id="chatbotForm" onsubmit="sendMessage(event)">
                <input type="text" id="chatInput" placeholder="Ketik pesan..." autocomplete="off">
                <button type="submit"><i class="bi bi-send-fill"></i></button>
            </form>
        </div>
    `;
    document.body.appendChild(chatbotContainer);
    
    // Toggle chatbot
    chatbotToggle.addEventListener('click', toggleChatbot);
}

// Toggle chatbot visibility
function toggleChatbot() {
    const container = document.getElementById('chatbotContainer');
    const toggle = document.getElementById('chatbotToggle');
    
    container.classList.toggle('active');
    toggle.classList.toggle('active');
    
    if (container.classList.contains('active')) {
        toggle.innerHTML = '<i class="bi bi-x-lg"></i>';
        document.getElementById('chatInput').focus();
    } else {
        toggle.innerHTML = '<i class="bi bi-chat-dots-fill"></i>';
    }
}

// Send quick reply
function sendQuickReply(message) {
    const input = document.getElementById('chatInput');
    input.value = message;
    sendMessage(new Event('submit'));
}

// Send message to chatbot
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send to backend
        const response = await fetch('/chatbot/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        addMessage(data.response, 'bot', data.quick_replies);
        
    } catch (error) {
        hideTypingIndicator();
        addMessage('Maaf, terjadi kesalahan. Silakan coba lagi.', 'bot');
    }
}

// Add message to chat
function addMessage(text, sender, quickReplies = null) {
    const body = document.getElementById('chatbotBody');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    let quickRepliesHTML = '';
    if (quickReplies && quickReplies.length > 0) {
        quickRepliesHTML = '<div class="quick-replies">';
        quickReplies.forEach(reply => {
            quickRepliesHTML += `<button class="quick-reply-btn" onclick="sendQuickReply('${reply}')">${reply}</button>`;
        });
        quickRepliesHTML += '</div>';
    }
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${text}
            ${quickRepliesHTML}
        </div>
    `;
    
    body.appendChild(messageDiv);
    body.scrollTop = body.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const body = document.getElementById('chatbotBody');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    body.appendChild(typingDiv);
    body.scrollTop = body.scrollHeight;
}

// Hide typing indicator
function hideTypingIndicator() {
    const typing = document.getElementById('typingIndicator');
    if (typing) {
        typing.remove();
    }
}

/**
 * Initialize Animations
 */
function initAnimations() {
    // AOS is loaded via CDN in base.html
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }
}

/**
 * Image Gallery Functions
 */
function initGallery() {
    // Lightbox for images
    document.querySelectorAll('[data-lightbox]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            openLightbox(this.href);
        });
    });
}

function openLightbox(src) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <button class="lightbox-close" onclick="closeLightbox()">&times;</button>
            <img src="${src}" alt="">
        </div>
    `;
    
    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';
    
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
}

function closeLightbox() {
    const lightbox = document.querySelector('.lightbox-overlay');
    if (lightbox) {
        lightbox.remove();
        document.body.style.overflow = '';
    }
}

/**
 * Get CSRF Token
 */
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

/**
 * Live Search Feature - INOVASI
 */
let searchTimeout;

function initLiveSearch() {
    const searchInput = document.querySelector('.live-search-input');
    const searchResults = document.querySelector('.live-search-results');
    
    if (!searchInput || !searchResults) return;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                displaySearchResults(data, searchResults);
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.live-search-container')) {
            searchResults.style.display = 'none';
        }
    });
}

function displaySearchResults(data, container) {
    if (!data.results || data.results.length === 0) {
        container.innerHTML = '<div class="search-no-results">Tidak ada hasil ditemukan</div>';
        container.style.display = 'block';
        return;
    }
    
    let html = '<ul class="search-results-list">';
    
    data.results.forEach(item => {
        html += `
            <li class="search-result-item">
                <a href="${item.url}">
                    <span class="result-type">${item.type}</span>
                    <span class="result-title">${item.title}</span>
                </a>
            </li>
        `;
    });
    
    html += '</ul>';
    
    container.innerHTML = html;
    container.style.display = 'block';
}

/**
 * Form Validation
 */
function validateForm(form) {
    let isValid = true;
    
    form.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    // Email validation
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput && emailInput.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
            isValid = false;
            emailInput.classList.add('is-invalid');
        }
    }
    
    return isValid;
}

/**
 * Counter Animation
 */
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Initialize counters when visible
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.counter);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => observer.observe(counter));
}

/**
 * Like System for Karya
 */
async function likeKarya(slug) {
    try {
        const response = await fetch(`/karya/${slug}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'liked') {
            document.getElementById('likeCount').textContent = data.like_count;
            document.getElementById('likeBtn').classList.add('liked');
            showToast('Terima kasih telah menyukai karya ini!', 'success');
        } else if (data.status === 'already_liked') {
            showToast('Anda sudah menyukai karya ini', 'info');
        }
    } catch (error) {
        showToast('Terjadi kesalahan', 'error');
    }
}

/**
 * Toast Notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Share Functions
 */
function shareToFacebook(url) {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank', 'width=600,height=400');
}

function shareToTwitter(url, text) {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank', 'width=600,height=400');
}

function shareToWhatsApp(url, text) {
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Link berhasil disalin!', 'success');
    });
}

/**
 * Dark Mode Toggle (Optional Feature)
 */
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (!darkModeToggle) return;
    
    // Check saved preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
    
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });
}

/**
 * Accessibility Features
 */
function initAccessibility() {
    // Skip to content
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Keyboard navigation for chatbot
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const chatbot = document.getElementById('chatbotContainer');
            if (chatbot && chatbot.classList.contains('active')) {
                toggleChatbot();
            }
            closeLightbox();
        }
    });
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', initAccessibility);
