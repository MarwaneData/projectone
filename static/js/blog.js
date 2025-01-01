document.addEventListener('DOMContentLoaded', () => {
    // Reading Progress Bar
    const progressBar = document.querySelector('.progress-inner');
    const article = document.querySelector('.blog-post');

    window.addEventListener('scroll', () => {
        if (article) {
            const articleHeight = article.offsetHeight - window.innerHeight;
            const progress = (window.scrollY / articleHeight) * 100;
            progressBar.style.width = `${Math.min(100, progress)}%`;
        }
    });

    // Table of Contents Highlighting
    const tocLinks = document.querySelectorAll('.toc-list a');
    const sections = document.querySelectorAll('.content-section');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Remove active class from all links
                tocLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to corresponding link
                const activeLink = document.querySelector(`.toc-list a[href="#${entry.target.id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    sections.forEach(section => observer.observe(section));

    // Smooth Scroll for ToC Links
    tocLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Share Buttons
    const shareButtons = document.querySelectorAll('.share-button');
    shareButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent(document.title);
            let shareUrl;

            if (button.classList.contains('twitter')) {
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
            } else if (button.classList.contains('linkedin')) {
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
            } else if (button.classList.contains('facebook')) {
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
            }

            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });

    // Code Syntax Highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }

    // Code Copy Button Functionality
    document.querySelectorAll('.code-example').forEach(block => {
        const copyButton = block.querySelector('.copy-button');
        const code = block.querySelector('code');

        copyButton.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(code.textContent);
                copyButton.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
                copyButton.classList.add('copied');
                
                setTimeout(() => {
                    copyButton.innerHTML = '<i class="far fa-copy"></i><span>Copy</span>';
                    copyButton.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
}); 