document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    const body = document.body;

    // Function to apply theme
    const applyTheme = (theme) => {
        if (theme === 'light') {
            body.classList.add('light-mode');
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            body.classList.remove('light-mode');
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    };

    // Check localStorage for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark'; // Default to dark
    applyTheme(savedTheme);


    // Toggle theme on button click
    themeToggleButton.addEventListener('click', () => {
        const isLightMode = body.classList.contains('light-mode');
        const newTheme = isLightMode ? 'dark' : 'light';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme); // Save preference
    });

    // Scroll-based animation for content sections
    const sections = document.querySelectorAll('.content-section');
    const observerOptions = {
        root: null, // relative to the viewport
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const sectionObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Unobserve after animation to save resources
                // observer.unobserve(entry.target);
            }
             // Optional: Reset animation if element scrolls out of view
            // else {
            //     entry.target.classList.remove('visible');
            // }
        });
    }, observerOptions);

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

     // Initial fade-in for the body is handled by CSS animation
});

