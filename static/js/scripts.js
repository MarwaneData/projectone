document.addEventListener('DOMContentLoaded', () => {
    // Initial setup
    gsap.set('.main-content', { visibility: 'visible' });
    gsap.registerPlugin(ScrollTrigger);

    // Create timeline for main animations
    const tl = gsap.timeline({
        defaults: {
            duration: 1,
            ease: 'power3.out'
        }
    });

    // Main animation sequence
    tl.from('.logo', {
        y: -20,
        opacity: 0
    })
    .from('.nav-links li', {
        x: -50,
        opacity: 0,
        stagger: 0.1,
        ease: 'power2.out'
    }, '-=0.5')
    .from('.name-title', {
        y: 50,
        opacity: 0,
        ease: 'power4.out'
    }, '-=0.5')
    .from('.role', {
        y: 20,
        opacity: 0
    }, '-=0.3')
    .from('.cta-button', {
        y: 20,
        opacity: 0,
        scale: 0.9,
        ease: 'back.out(1.7)'
    }, '-=0.3')
    .from('.contact-info', {
        y: 20,
        opacity: 0
    }, '-=0.2')
    .from('.right-section', {
        x: 100,
        opacity: 0,
        duration: 1.2
    }, '-=1');

    // Section Animations
    gsap.from('.text-content', {
        scrollTrigger: {
            trigger: '.section',
            start: 'top 80%',
            once: true
        },
        x: -100,
        opacity: 0,
        duration: 1,
        ease: 'power3.out'
    });
        
    gsap.from('.work-label', {
        scrollTrigger: {
            trigger: '.work-container',
            start: 'top 80%',
            once: true
        },
        y: 20,
        opacity: 0,
        duration: 0.6
    });
    
    gsap.from('.work-heading', {
        scrollTrigger: {
            trigger: '.work-container',
            start: 'top 80%',
            once: true
        },
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 0.2
    });
    
    gsap.from('.work-item', {
        scrollTrigger: {
            trigger: '.work-items-grid',
            start: 'top 80%',
            once: true
        },
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2
    });
    
    gsap.from('.work-load-more', {
        scrollTrigger: {
            trigger: '.work-load-more',
            start: 'top 90%',
            once: true
        },
        y: 20,
        opacity: 0,
        duration: 0.6,
        delay: 0.8
    });
    gsap.from('.blog-label', {
        scrollTrigger: {
            trigger: '.blog-container',
            start: 'top 80%',
            once: true
        },
        y: 20,
        opacity: 0,
        duration: 0.6
    });
    
    gsap.from('.blog-heading', {
        scrollTrigger: {
            trigger: '.blog-container',
            start: 'top 80%',
            once: true
        },
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 0.2
    });
    
    gsap.from('.blog-item', {
        scrollTrigger: {
            trigger: '.blog-grid',
            start: 'top 80%',
            once: true
        },
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2
    });
    
    gsap.from('.blog-load-more', {
        scrollTrigger: {
            trigger: '.blog-load-more',
            start: 'top 90%',
            once: true
        },
        y: 20,
        opacity: 0,
        duration: 0.6,
        delay: 0.8
    });
        // Add these animations to your existing JavaScript file
    gsap.from('.contact-label', {
        scrollTrigger: {
            trigger: '.contact-container',
            start: 'top 80%',
            once: true
        },
        y: 20,
        opacity: 0,
        duration: 0.6
    });

    gsap.from('.contact-heading', {
        scrollTrigger: {
            trigger: '.contact-container',
            start: 'top 80%',
            once: true
        },
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 0.2
    });

    gsap.from('.contact-address, .contact-details, .contact-social', {
        scrollTrigger: {
            trigger: '.contact-info',
            start: 'top 80%',
            once: true
        },
        y: 30,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2
    });
 gsap.from('.contact-form-wrapper', {
        scrollTrigger: {
            trigger: '.contact-form-wrapper',
            start: 'top 80%',
            once: true
        },
        x: 50,
        opacity: 0,
        duration: 1,
        delay: 0.4
    });
   
        

    // Staggered animation for the grid items
    gsap.utils.toArray('.grid-item').forEach((item, index) => {
        gsap.to(item, {
            scrollTrigger: {
                trigger: '.section',
                start: 'top 80%',
                once: true
            },
            opacity: 1,
            y: 0,
            duration: 1,
            delay: 0.2 * index,
            ease: 'power3.out'
        });
    });

    // Hover animations for interactive elements
    const interactiveElements = document.querySelectorAll('.primary-button, .nav-links a, .contact-info a');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            gsap.to(element, {
                scale: 1.05,
                duration: 0.3
            });
        });

        element.addEventListener('mouseleave', () => {
            gsap.to(element, {
                scale: 1,
                duration: 0.3
            });
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    gsap.to(window, {
                        duration: 1,
                        scrollTo: {
                            y: targetElement,
                            offsetY: 50
                        },
                        ease: 'power2.inOut'
                    });
                }
            }
        });
    });
});
