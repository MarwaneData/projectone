document.addEventListener('DOMContentLoaded', () => {
    // Burger menu functionality
    const burger = document.querySelector('.burger');
    const sidebar = document.querySelector('.sidebar');
    
    burger.addEventListener('click', () => {
        burger.classList.toggle('active');
        sidebar.classList.toggle('active');
    });

    // Navigation click handling
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            // Only prevent default for contact scroll
            if (link.classList.contains('scroll-to-contact')) {
                e.preventDefault();
                // Scroll to contact section
                const contactSection = document.querySelector('.contact-container');
                if (contactSection) {
                    gsap.to(window, {
                        duration: 1,
                        scrollTo: {
                            y: contactSection,
                            offsetY: 50
                        },
                        ease: 'power2.inOut'
                    });
                }
                return;
            }

            // Remove active class from all links
            document.querySelectorAll('.nav-links a').forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');

            // Handle mobile menu
            if (window.innerWidth <= 768) {
                burger.classList.remove('active');
                sidebar.classList.remove('active');
            }
        });
    });

    // Window resize handler for responsive behaviors
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth > 768) {
                sidebar.classList.remove('active');
                burger.classList.remove('active');
            }
        }, 250);
    });

    // Add this to your existing DOMContentLoaded event listener
    document.addEventListener('scroll', () => {
        const docElement = document.documentElement;
        const scrollTotal = docElement.scrollHeight - docElement.clientHeight;
        const scrollProgress = window.scrollY / scrollTotal;
        
        document.body.classList.toggle('scrolling', window.scrollY > 50);
        document.body.style.setProperty('--scroll-percent', scrollProgress);
    });
}); 