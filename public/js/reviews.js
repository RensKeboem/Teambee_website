// Reviews carousel with automatic scrolling, dot navigation, and touch support
document.addEventListener('DOMContentLoaded', function() {
  // Carousel class to encapsulate all functionality
  class ReviewCarousel {
    constructor(options = {}) {
      // DOM elements
      this.container = document.getElementById('reviews-container');
      this.cards = document.querySelectorAll('.review-card');
      this.dotsContainer = document.getElementById('review-dots');
      
      // Validate required elements
      if (!this.container || !this.dotsContainer || this.cards.length === 0) {
        console.error('Reviews carousel elements not found');
        return;
      }
      
      // Configuration with defaults
      this.config = {
        autoplayDelay: options.autoplayDelay || 5000,
        pauseDelay: options.pauseDelay || 10000,
        transitionSpeed: options.transitionSpeed || 500,
        touchThreshold: options.touchThreshold || 50
      };
      
      // State
      this.currentIndex = 0;
      this.totalCards = this.cards.length;
      this.autoplayInterval = null;
      this.isPaused = false;
      this.isTransitioning = false;
      this.touchStartX = 0;
      this.touchDeltaX = 0;
      this.dots = [];
      
      // Initialize carousel
      this.init();
    }
    
    init() {
      this.setupInfiniteCarousel();
      this.createDots();
      this.setupTouchEvents();
      this.startAutoplay();
      this.setupEventListeners();
    }
    
    setupInfiniteCarousel() {
      // Clone first and last cards for infinite scrolling
      const firstClone = this.cards[0].cloneNode(true);
      const lastClone = this.cards[this.totalCards - 1].cloneNode(true);
      
      this.container.appendChild(firstClone);
      this.container.insertBefore(lastClone, this.container.firstChild);
      
      // Position to first real slide (after clone)
      this.currentIndex = 1;
      this.updateCarousel(this.currentIndex, false);
    }
    
    createDots() {
      // Create a dot for each original card (not clones)
      for (let i = 0; i < this.totalCards; i++) {
        const dot = document.createElement('button');
        dot.classList.add('w-3', 'h-3', 'rounded-full', 'bg-gray-300', 'transition-colors', 'duration-300');
        dot.setAttribute('aria-label', `Go to review ${i + 1}`);
        dot.setAttribute('data-index', i);
        
        // Set up click handler
        dot.addEventListener('click', () => {
          this.goToSlide(parseInt(dot.dataset.index) + 1);
          this.pauseAutoplay();
        });
        
        this.dotsContainer.appendChild(dot);
        this.dots.push(dot);
      }
      
      this.updateActiveDot(0);
    }
    
    updateActiveDot(index) {
      this.dots.forEach((dot, i) => {
        if (i === index) {
          dot.classList.remove('bg-gray-300');
          dot.classList.add('bg-[#3D2E7C]', 'scale-125');
        } else {
          dot.classList.remove('bg-[#3D2E7C]', 'scale-125');
          dot.classList.add('bg-gray-300');
        }
      });
    }
    
    getContainerWidth() {
      return this.container.parentElement.offsetWidth;
    }
    
    calculateOffset(index) {
      const containerWidth = this.getContainerWidth();
      const cardWidth = this.cards[0].offsetWidth;
      
      // Center the card in the container
      const centeredPosition = (containerWidth - cardWidth) / 2;
      
      // Calculate position based on index
      return centeredPosition - (index * cardWidth);
    }
    
    updateCarousel(index, animate = true) {
      if (this.isTransitioning) return;
      
      const offset = this.calculateOffset(index);
      
      // Set transition based on animate parameter
      this.container.style.transition = animate ? 
        `transform ${this.config.transitionSpeed}ms ease` : 'none';
      this.container.style.transform = `translateX(${offset}px)`;
      
      if (!animate) {
        // Force reflow to apply the change immediately
        void this.container.offsetWidth;
        this.container.style.transition = `transform ${this.config.transitionSpeed}ms ease`;
      } else {
        // Set transitioning flag to prevent rapid movements
        this.isTransitioning = true;
        setTimeout(() => {
          this.isTransitioning = false;
        }, this.config.transitionSpeed);
      }
      
      // Update state
      this.currentIndex = index;
      
      // Update the active dot
      const dotIndex = this.getDotIndexFromSlideIndex(index);
      this.updateActiveDot(dotIndex);
    }
    
    getDotIndexFromSlideIndex(slideIndex) {
      // Convert slide index (including clones) to dot index (only real slides)
      let dotIndex = slideIndex - 1;
      if (dotIndex < 0) dotIndex = this.totalCards - 1;
      if (dotIndex >= this.totalCards) dotIndex = 0;
      return dotIndex;
    }
    
    goToSlide(index) {
      this.updateCarousel(index);
      
      // Handle infinite scroll wrap-around
      setTimeout(() => {
        if (index >= this.totalCards + 1) {
          // If at end clone, jump to first real slide
          this.updateCarousel(1, false);
        } else if (index <= 0) {
          // If at beginning clone, jump to last real slide
          this.updateCarousel(this.totalCards, false);
        }
      }, this.config.transitionSpeed);
    }
    
    nextSlide() {
      this.goToSlide(this.currentIndex + 1);
    }
    
    prevSlide() {
      this.goToSlide(this.currentIndex - 1);
    }
    
    startAutoplay() {
      if (this.autoplayInterval) clearInterval(this.autoplayInterval);
      
      this.autoplayInterval = setInterval(() => {
        if (!this.isPaused) {
          this.nextSlide();
        }
      }, this.config.autoplayDelay);
    }
    
    pauseAutoplay() {
      this.isPaused = true;
      
      // Resume after delay
      clearTimeout(this.pauseTimeout);
      this.pauseTimeout = setTimeout(() => {
        this.isPaused = false;
      }, this.config.pauseDelay);
    }
    
    setupTouchEvents() {
      // Touch events for mobile
      this.container.addEventListener('touchstart', (e) => {
        this.touchStartX = e.touches[0].clientX;
        this.pauseAutoplay();
      }, { passive: true });
      
      this.container.addEventListener('touchmove', (e) => {
        if (this.isTransitioning) return;
        
        const currentX = e.touches[0].clientX;
        this.touchDeltaX = currentX - this.touchStartX;
        
        // Apply drag effect
        const offset = this.calculateOffset(this.currentIndex);
        this.container.style.transition = 'none';
        this.container.style.transform = `translateX(${offset + this.touchDeltaX}px)`;
      }, { passive: true });
      
      this.container.addEventListener('touchend', this.handleSwipeEnd.bind(this));
      
      // Mouse events for desktop dragging
      this.container.addEventListener('mousedown', this.handleMouseDown.bind(this));
      
      // Prevent text selection during drag
      this.container.addEventListener('dragstart', (e) => e.preventDefault());
    }
    
    handleSwipeEnd() {
      if (Math.abs(this.touchDeltaX) > this.config.touchThreshold) {
        if (this.touchDeltaX > 0) {
          this.prevSlide();
        } else {
          this.nextSlide();
        }
      } else {
        // Not enough movement, snap back
        this.updateCarousel(this.currentIndex);
      }
      
      this.touchDeltaX = 0;
    }
    
    handleMouseDown(e) {
      e.preventDefault();
      this.touchStartX = e.clientX;
      this.pauseAutoplay();
      
      // Change cursor to indicate grabbing
      document.body.style.cursor = 'grabbing';
      this.container.style.cursor = 'grabbing';
      
      // Setup temporary event listeners
      document.addEventListener('mousemove', this.mouseMoveHandler = this.handleMouseMove.bind(this));
      document.addEventListener('mouseup', this.mouseUpHandler = this.handleMouseUp.bind(this));
    }
    
    handleMouseMove(e) {
      if (this.isTransitioning) return;
      
      const currentX = e.clientX;
      this.touchDeltaX = currentX - this.touchStartX;
      
      // Apply drag effect
      const offset = this.calculateOffset(this.currentIndex);
      this.container.style.transition = 'none';
      this.container.style.transform = `translateX(${offset + this.touchDeltaX}px)`;
    }
    
    handleMouseUp() {
      // Remove temporary event listeners
      document.removeEventListener('mousemove', this.mouseMoveHandler);
      document.removeEventListener('mouseup', this.mouseUpHandler);
      
      // Reset cursor
      document.body.style.cursor = '';
      this.container.style.cursor = '';
      
      this.handleSwipeEnd();
    }
    
    setupEventListeners() {
      // Click on carousel pauses autoplay
      this.container.addEventListener('click', () => this.pauseAutoplay());
      
      // Handle resize events
      window.addEventListener('resize', () => this.handleResize());
      
      // Handle transition end
      this.container.addEventListener('transitionend', () => {
        this.isTransitioning = false;
      });
    }
    
    handleResize() {
      // Update carousel position on window resize
      this.updateCarousel(this.currentIndex, false);
    }
  }
  
  // Initialize the carousel with default options
  new ReviewCarousel();
});

// Smooth scroll to contact section with highlighting animation
document.addEventListener('DOMContentLoaded', function() {
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

    if (showStoriesBtn && closeStoriesBtn && storiesPanel) {
        // Show panel
        showStoriesBtn.addEventListener('click', () => {
            storiesPanel.querySelector('.transform').classList.remove('translate-x-full');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        });

        // Close panel
        closeStoriesBtn.addEventListener('click', () => {
            storiesPanel.querySelector('.transform').classList.add('translate-x-full');
            document.body.style.overflow = ''; // Restore scrolling
        });

        // Close panel when clicking outside
        storiesPanel.addEventListener('click', (e) => {
            if (e.target === storiesPanel) {
                storiesPanel.querySelector('.transform').classList.add('translate-x-full');
                document.body.style.overflow = '';
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
                            <div class="flex flex-col md:flex-row gap-8 items-center">
                                ${isImageLeft ? `
                                    <div class="w-full md:w-1/3">
                                        <img src="${story.image}" alt="${story.author}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg">
                                    </div>
                                    <div class="w-full md:w-2/3">
                                        <div class="mb-6">
                                            <img src="/static/assets/quote.svg" alt="Quote" class="w-12 h-12 text-[#E8973A] mb-4">
                                            <p class="text-white/90 text-lg mb-6 whitespace-pre-line">${story.quote}</p>
                                        </div>
                                        <div class="space-y-6">
                                            <div class="flex items-center">
                                                <div>
                                                    <div class="font-semibold text-white text-xl">${story.author}</div>
                                                    <div class="text-white/70">${story.title}</div>
                                                </div>
                                            </div>
                                            <div class="space-y-2 pt-4 border-t border-white/10">
                                                ${metricsHtml}
                                            </div>
                                        </div>
                                    </div>
                                ` : `
                                    <div class="w-full md:w-2/3">
                                        <div class="mb-6">
                                            <img src="/static/assets/quote.svg" alt="Quote" class="w-12 h-12 text-[#E8973A] mb-4">
                                            <p class="text-white/90 text-lg mb-6 whitespace-pre-line">${story.quote}</p>
                                        </div>
                                        <div class="space-y-6">
                                            <div class="flex items-center">
                                                <div>
                                                    <div class="font-semibold text-white text-xl">${story.author}</div>
                                                    <div class="text-white/70">${story.title}</div>
                                                </div>
                                            </div>
                                            <div class="space-y-2 pt-4 border-t border-white/10">
                                                ${metricsHtml}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="w-full md:w-1/3">
                                        <img src="${story.image}" alt="${story.author}" class="w-full h-auto rounded-lg object-cover aspect-square shadow-lg">
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