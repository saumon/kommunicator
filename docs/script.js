// ===== DOM Elements =====
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const mobileMenu = document.querySelector('.mobile-menu');
const navbar = document.querySelector('.navbar');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');
const copyBtns = document.querySelectorAll('.copy-btn');

// ===== Mobile Menu Toggle =====
mobileMenuBtn?.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    mobileMenuBtn.classList.toggle('active');
});

// Close mobile menu when clicking a link
document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
    });
});

// ===== Navbar Scroll Effect =====
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.background = 'rgba(10, 10, 15, 0.95)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(10, 10, 15, 0.8)';
        navbar.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
});

// ===== Tab Switching =====
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.dataset.tab;
        
        // Update active states
        tabBtns.forEach(b => b.classList.remove('active'));
        tabPanels.forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
});

// ===== Copy to Clipboard =====
copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const codeBlock = btn.closest('.code-block').querySelector('code');
        const text = codeBlock.textContent;
        
        navigator.clipboard.writeText(text).then(() => {
            btn.classList.add('copied');
            btn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            `;
            
            setTimeout(() => {
                btn.classList.remove('copied');
                btn.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"></path>
                    </svg>
                `;
            }, 2000);
        });
    });
});

// ===== Terminal Typing Animation =====
const commands = [
    {
        cmd: './kommunicator-cli.py send-teams --to john --message "Hello! 👋"',
        output: [
            '<span class="success">✓</span> Message sent successfully to john.doe@example.com',
            '<span class="info">→</span> Delivered via Teams webhook'
        ]
    },
    {
        cmd: './kommunicator-cli.py send-email --to alice --subject "Meeting"',
        output: [
            '<span class="success">✓</span> Email sent successfully to alice.wonder@example.com',
            '<span class="info">→</span> Subject: Meeting'
        ]
    },
    {
        cmd: './kommunicator-cli.py send-teams --to "Dev Team" --message "Deploy complete 🚀"',
        output: [
            '<span class="success">✓</span> Message sent to Dev Team (conversation)',
            '<span class="info">→</span> 8 team members notified'
        ]
    }
];

let currentCommandIndex = 0;
let currentCharIndex = 0;
let isTyping = true;
let isPausing = false;

const typingCmd = document.getElementById('typing-cmd');
const terminalOutput = document.getElementById('terminal-output');

function typeCommand() {
    if (!typingCmd) return;
    
    const currentCommand = commands[currentCommandIndex];
    
    if (isTyping) {
        if (currentCharIndex < currentCommand.cmd.length) {
            typingCmd.textContent += currentCommand.cmd[currentCharIndex];
            currentCharIndex++;
            setTimeout(typeCommand, 30 + Math.random() * 40);
        } else {
            isTyping = false;
            isPausing = true;
            setTimeout(typeCommand, 500);
        }
    } else if (isPausing) {
        isPausing = false;
        // Show output
        terminalOutput.innerHTML = currentCommand.output.map(line => 
            `<div class="output-line">${line}</div>`
        ).join('');
        setTimeout(typeCommand, 3000);
    } else {
        // Reset and move to next command
        typingCmd.textContent = '';
        terminalOutput.innerHTML = '';
        currentCharIndex = 0;
        currentCommandIndex = (currentCommandIndex + 1) % commands.length;
        isTyping = true;
        setTimeout(typeCommand, 500);
    }
}

// Start typing animation after a delay
setTimeout(typeCommand, 1500);

// ===== Intersection Observer for Scroll Animations =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('aos-animate');
        }
    });
}, observerOptions);

// Observe all elements with data-aos attribute
document.querySelectorAll('[data-aos]').forEach(el => {
    observer.observe(el);
});

// ===== Smooth Scroll for Anchor Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80; // Account for fixed navbar
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Parallax Effect for Glows =====
document.addEventListener('mousemove', (e) => {
    const glows = document.querySelectorAll('.glow');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    glows.forEach((glow, index) => {
        const speed = (index + 1) * 20;
        const xOffset = (x - 0.5) * speed;
        const yOffset = (y - 0.5) * speed;
        glow.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
});

// ===== Add Loading State =====
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// ===== Feature Cards Hover Effect =====
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
    });
});

// ===== Counter Animation for Stats (if needed) =====
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

// ===== Keyboard Navigation =====
document.addEventListener('keydown', (e) => {
    // Press 'g' to go to GitHub
    if (e.key === 'g' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            // Only trigger if not in an input field
            // Uncomment to enable: window.open('https://github.com/saumon/kommunicator', '_blank');
        }
    }
});

// ===== Console Easter Egg =====
console.log('%c📡 Kommunicator™', 'font-size: 24px; font-weight: bold; color: #6366f1;');
console.log('%cLooking to contribute? Visit https://github.com/saumon/kommunicator', 'font-size: 14px; color: #a1a1aa;');
