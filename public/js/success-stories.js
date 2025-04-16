// Success stories functionality
document.addEventListener('DOMContentLoaded', function() {
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

        // Get current language from URL or default to Dutch
        function getCurrentLanguage() {
            const path = window.location.pathname;
            return path.startsWith('/en') ? 'en' : 'nl';
        }

        // Load and populate success stories
        fetch('/static/data/success_stories.json')
            .then(response => response.json())
            .then(successStories => {
                const largeReviewsContainer = storiesPanel.querySelector('.space-y-8');
                
                if (largeReviewsContainer) {
                    // Clear existing content
                    largeReviewsContainer.innerHTML = '';
                    
                    // Get current language
                    const currentLang = getCurrentLanguage();
                    
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
                                    <div class="w-full md:w-1/3 order-first">
                                        <img src="${story.image}" alt="${story.title[currentLang]}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg mb-4">
                                        <div class="bg-white/5 p-4 rounded-lg">
                                            <h4 class="text-white text-xl font-bold mb-2">${story.title[currentLang]}</h4>
                                            <p class="text-white/80">${story.subtitle[currentLang]}</p>
                                        </div>
                                    </div>
                                    <div class="w-full md:w-2/3 order-last md:order-last">
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Strategie & Aanpak' : 'Strategy & Approach'}</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.strategy[currentLang]}</p>
                                        </div>
                                        
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Resultaten & KPI\'s' : 'Results & KPIs'}</h3>
                                            <div class="space-y-6">
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📍 Start samenwerking (september 2023):' : '📍 Start of collaboration (September 2023):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.start.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.start.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.start.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📊 Impactmeting na 3 maanden (november 2023):' : '📊 Impact measurement after 3 months (November 2023):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.three_months.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.three_months.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.three_months.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📈 Huidige situatie (maart 2025):' : '📈 Current situation (March 2025):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.current.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.current.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.current.visitors}</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Conclusie' : 'Conclusion'}</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.conclusion[currentLang]}</p>
                                        </div>
                                    </div>
                                ` : `
                                    <div class="w-full md:w-1/3 order-first md:order-last">
                                        <img src="${story.image}" alt="${story.title[currentLang]}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg mb-4">
                                        <div class="bg-white/5 p-4 rounded-lg">
                                            <h4 class="text-white text-xl font-bold mb-2">${story.title[currentLang]}</h4>
                                            <p class="text-white/80">${story.subtitle[currentLang]}</p>
                                        </div>
                                    </div>
                                    <div class="w-full md:w-2/3 order-last md:order-first">
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Strategie & Aanpak' : 'Strategy & Approach'}</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.strategy[currentLang]}</p>
                                        </div>
                                        
                                        <div class="mb-8">
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Resultaten & KPI\'s' : 'Results & KPIs'}</h3>
                                            <div class="space-y-6">
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📍 Start samenwerking (september 2023):' : '📍 Start of collaboration (September 2023):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.start.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.start.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.start.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📊 Impactmeting na 3 maanden (november 2023):' : '📊 Impact measurement after 3 months (November 2023):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.three_months.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.three_months.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.three_months.visitors}</li>
                                                    </ul>
                                                </div>
                                                
                                                <div class="bg-white/5 p-4 rounded-lg">
                                                    <h4 class="text-white font-semibold mb-2">${currentLang === 'nl' ? '📈 Huidige situatie (maart 2025):' : '📈 Current situation (March 2025):'}</h4>
                                                    <ul class="list-disc list-inside text-white/80 space-y-1">
                                                        <li>${currentLang === 'nl' ? 'Totale aantal leden:' : 'Total number of members:'} ${story.metrics.current.members}</li>
                                                        <li>${currentLang === 'nl' ? 'Actieve Technogym app gebruikers:' : 'Active Technogym app users:'} ${story.metrics.current.app_users}</li>
                                                        <li>${currentLang === 'nl' ? 'Aantal recente bezoekers:' : 'Number of recent visitors:'} ${story.metrics.current.visitors}</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <h3 class="text-white text-2xl font-bold mb-4">${currentLang === 'nl' ? 'Conclusie' : 'Conclusion'}</h3>
                                            <p class="text-white/90 text-lg whitespace-pre-line">${story.conclusion[currentLang]}</p>
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