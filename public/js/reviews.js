// Success stories functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll to contact section with highlighting animation
    const scrollButtons = document.querySelectorAll('[data-scroll-to]');
    const contactSection = document.getElementById('contact');
    let isButtonScroll = false;
    
    // Create an Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && isButtonScroll) {
                // When contact section is fully in view and scroll was initiated by button
                const contactInfo = entry.target.querySelector('.contact-info');
                if (contactInfo) {
                    // Add animation to all elements within contact-info
                    const contactElements = contactInfo.querySelectorAll('*');
                    contactElements.forEach(element => {
                        element.classList.add('scale-contact');
                        setTimeout(() => {
                            element.classList.remove('scale-contact');
                        }, 2000);
                    });
                }
                // Reset the flag after animation
                setTimeout(() => {
                    isButtonScroll = false;
                }, 2000);
            }
        });
    }, {
        threshold: 0.8 // Trigger when 80% of the section is visible
    });
    
    // Start observing the contact section
    if (contactSection) {
        observer.observe(contactSection);
    }
    
    scrollButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('data-scroll-to');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Set flag to indicate button-initiated scroll
                isButtonScroll = true;
                
                // Calculate the offset to account for the fixed header
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Success stories panel functionality
    const showStoriesBtn = document.getElementById('show-success-stories');
    const closeStoriesBtn = document.getElementById('close-success-stories');
    const storiesPanel = document.getElementById('success-stories-panel');
    const footer = document.querySelector('footer');

    if (showStoriesBtn && closeStoriesBtn && storiesPanel && footer) {
        // Show panel
        showStoriesBtn.addEventListener('click', () => {
            storiesPanel.querySelector('.transform').classList.remove('translate-x-full');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
            footer.style.display = 'none'; // Hide footer
        });

        // Close panel
        closeStoriesBtn.addEventListener('click', () => {
            storiesPanel.querySelector('.transform').classList.add('translate-x-full');
            document.body.style.overflow = ''; // Restore scrolling
            footer.style.display = ''; // Show footer
        });

        // Close panel when clicking outside
        storiesPanel.addEventListener('click', (e) => {
            if (e.target === storiesPanel) {
                storiesPanel.querySelector('.transform').classList.add('translate-x-full');
                document.body.style.overflow = '';
                footer.style.display = ''; // Show footer
            }
        });

        // Load and populate success stories
        fetch('/static/data/success_stories.json')
            .then(response => response.json())
            .then(successStories => {
                const largeReviewsContainer = storiesPanel.querySelector('.space-y-8');
                
                if (largeReviewsContainer) {
                    // Clear existing content
                    largeReviewsContainer.innerHTML = '';
                    
                    // Create cards for each success story
                    successStories.forEach((story, index) => {
                        const metricsHtml = Object.entries(story.metrics)
                            .map(([key, value]) => `
                                <div class="text-white/80">
                                    <span class="text-[#94C46F] font-bold text-xl">${value}</span>
                                    <span class="ml-2">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                                </div>
                            `).join('');

                        // Determine if image should be on left or right based on index
                        const isImageLeft = index % 2 === 0;
                        
                        const largeCard = document.createElement('div');
                        largeCard.className = 'bg-white/10 backdrop-blur-sm p-8 rounded-lg shadow-lg mb-12 last:mb-0';
                        largeCard.innerHTML = `
                            <div class="flex flex-col md:flex-row gap-8 items-start">
                                ${isImageLeft ? `
                                    <div class="w-full md:w-1/3">
                                        <img src="${story.image}" alt="${story.author}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg mb-4">
                                        <div class="bg-white/5 p-4 rounded-lg">
                                            <h4 class="text-white text-xl font-bold mb-2">${story.title}</h4>
                                            <p class="text-white/80">${story.subtitle}</p>
                                        </div>
                                    </div>
                                    <div class="w-full md:w-2/3">
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">Strategie & Aanpak</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.strategy}</p>
                                        </div>
                                        
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">Resultaten & KPI's</h3>
                                            <div class="space-y-6">
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📍 Start samenwerking (september 2023):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.start.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.start.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.start.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📊 Impactmeting na 3 maanden (november 2023):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.three_months.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.three_months.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.three_months.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📈 Huidige situatie (maart 2025):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.current.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.current.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.current.visitors}</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <h3 class="text-white text-2xl font-bold mb-4">Conclusie</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.conclusion}</p>
                                        </div>
                                    </div>
                                ` : `
                                    <div class="w-full md:w-2/3">
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">Strategie & Aanpak</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.strategy}</p>
                                        </div>
                                        
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">Resultaten & KPI's</h3>
                                            <div class="space-y-6">
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📍 Start samenwerking (september 2023):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.start.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.start.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.start.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📊 Impactmeting na 3 maanden (november 2023):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.three_months.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.three_months.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.three_months.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">📈 Huidige situatie (maart 2025):</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>Totale aantal leden: ${story.metrics.current.members}</li>
                                                        <li>Actieve Technogym app gebruikers: ${story.metrics.current.app_users}</li>
                                                        <li>Aantal recente bezoekers: ${story.metrics.current.visitors}</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <h3 class="text-white text-2xl font-bold mb-4">Conclusie</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.conclusion}</p>
                                        </div>
                                    </div>
                                    <div class="w-full md:w-1/3">
                                        <img src="${story.image}" alt="${story.author}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg mb-4">
                                        <div class="bg-white/5 p-4 rounded-lg">
                                            <h4 class="text-white text-xl font-bold mb-2">${story.title}</h4>
                                            <p class="text-white/80">${story.subtitle}</p>
                                        </div>
                                    </div>
                                `}
                            </div>
                        `;
                        largeReviewsContainer.appendChild(largeCard);
                    });
                }
            })
            .catch(error => console.error('Error loading success stories:', error));
    }
}); 