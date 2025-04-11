document.addEventListener('DOMContentLoaded', function() {
  // Get DOM elements
  const slider = document.getElementById('slider');
  const slides = document.getElementById('slides');
  const dotsContainer = document.getElementById('review-dots');
  
  if (!slider || !slides) {
    console.error('Required carousel elements not found');
    return;
  }
  
  // Carousel configuration
  const config = {
    slideWidth: 0,
    slideCount: 0,
    currentIndex: 0,
    isDragging: false,
    startPos: 0,
    currentTranslate: 0,
    prevTranslate: 0,
    animationID: 0,
    autoplayInterval: null,
    autoplayDelay: 5000,
    threshold: 50,
    isTransitioning: false,
    transitionDuration: 300
  };
  
  // Initialize carousel
  function init() {
    // Get slide elements
    const slideItems = slides.getElementsByClassName('slide');
    
    config.slideCount = slideItems.length;
    
    if (config.slideCount === 0) {
      console.error('No slides found');
      return;
    }
    
    // Set slide width
    config.slideWidth = slideItems[0].offsetWidth;
    
    // Clone first and last slides for infinite effect
    const firstSlide = slideItems[0].cloneNode(true);
    const lastSlide = slideItems[config.slideCount - 1].cloneNode(true);
    
    // Add clones to the DOM
    slides.appendChild(firstSlide);
    slides.insertBefore(lastSlide, slides.firstChild);
    
    // Set initial position to first real slide (index 1)
    config.currentIndex = 1;
    setPositionByIndex(1, false);
    
    // Create dots
    createDots();
    
    // Add event listeners
    addEventListeners();
    
    // Start autoplay
    startAutoplay();
  }
  
  // Create navigation dots
  function createDots() {
    if (!dotsContainer) return;
    
    // Clear existing dots
    dotsContainer.innerHTML = '';
    
    // Create a dot for each slide (excluding clones)
    for (let i = 0; i < config.slideCount; i++) {
      const dot = document.createElement('button');
      dot.classList.add('w-3', 'h-3', 'rounded-full', 'bg-gray-300', 'transition-colors', 'duration-300');
      dot.setAttribute('aria-label', `Go to review ${i + 1}`);
      dot.setAttribute('data-index', i);
      
      dot.addEventListener('click', function() {
        // Add 1 to account for the clone at the beginning
        goToSlide(parseInt(this.dataset.index) + 1);
      });
      
      dotsContainer.appendChild(dot);
    }
    
    // Update active dot
    updateActiveDot(0); // Start with the first dot active
  }
  
  // Add event listeners
  function addEventListeners() {
    // Touch events
    slides.addEventListener('touchstart', touchStart);
    slides.addEventListener('touchmove', touchMove);
    slides.addEventListener('touchend', touchEnd);
    
    // Mouse events
    slides.addEventListener('mousedown', touchStart);
    slides.addEventListener('mousemove', touchMove);
    slides.addEventListener('mouseup', touchEnd);
    slides.addEventListener('mouseleave', touchEnd);
    
    // Prevent context menu
    window.oncontextmenu = function(event) {
      if (event.target.closest('#slider')) {
        event.preventDefault();
        event.stopPropagation();
        return false;
      }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
      const slideItems = slides.getElementsByClassName('slide');
      if (slideItems.length > 0) {
        config.slideWidth = slideItems[0].offsetWidth;
        setPositionByIndex(config.currentIndex, false);
      }
    });
    
    // Pause autoplay on hover or touch
    slider.addEventListener('mouseenter', stopAutoplay);
    slider.addEventListener('touchstart', stopAutoplay);
    
    // Resume autoplay when mouse leaves
    slider.addEventListener('mouseleave', startAutoplay);
    
    // Handle transition end
    slides.addEventListener('transitionend', handleTransitionEnd);
  }
  
  // Handle transition end
  function handleTransitionEnd() {
    config.isTransitioning = false;
    
    // Check if we need to jump to the other end
    if (config.currentIndex === 0) {
      // Jump to the last real slide without animation
      config.currentIndex = config.slideCount;
      setPositionByIndex(config.currentIndex, false);
    } else if (config.currentIndex === config.slideCount + 1) {
      // Jump to the first real slide without animation
      config.currentIndex = 1;
      setPositionByIndex(config.currentIndex, false);
    }
  }
  
  // Touch start event
  function touchStart(event) {
    if (event.type.includes('mouse')) {
      event.preventDefault();
    }
    
    config.startPos = getPositionX(event);
    config.isDragging = true;
    
    // Pause autoplay when user interacts
    stopAutoplay();
    
    config.animationID = requestAnimationFrame(animation);
    slides.style.cursor = 'grabbing';
  }
  
  // Touch move event
  function touchMove(event) {
    if (!config.isDragging) return;
    
    const currentPosition = getPositionX(event);
    config.currentTranslate = config.prevTranslate + currentPosition - config.startPos;
    
    // Add resistance at the edges
    if (config.currentTranslate > 0) {
      config.currentTranslate = config.currentTranslate / 4;
    } else if (config.currentTranslate < -(config.slideWidth * (config.slideCount + 1))) {
      config.currentTranslate = config.currentTranslate + (config.currentTranslate + (config.slideWidth * (config.slideCount + 1))) / 4;
    }
  }
  
  // Touch end event
  function touchEnd() {
    config.isDragging = false;
    cancelAnimationFrame(config.animationID);
    
    const movedBy = config.currentTranslate - config.prevTranslate;
    
    // Determine if slide should advance
    if (Math.abs(movedBy) > config.threshold) {
      if (movedBy < 0) {
        config.currentIndex += 1;
      } else {
        config.currentIndex -= 1;
      }
    }
    
    setPositionByIndex(config.currentIndex);
    slides.style.cursor = 'grab';
    
    // Resume autoplay after a delay
    setTimeout(startAutoplay, config.autoplayDelay);
  }
  
  // Animation frame
  function animation() {
    setSliderPosition();
    if (config.isDragging) requestAnimationFrame(animation);
  }
  
  // Set slider position
  function setSliderPosition() {
    slides.style.transform = `translateX(${config.currentTranslate}px)`;
  }
  
  // Set position by index
  function setPositionByIndex(index, animate = true) {
    // Calculate the translation
    config.currentTranslate = -(config.slideWidth * index);
    config.prevTranslate = config.currentTranslate;
    
    // Set transition based on animate parameter
    if (animate) {
      slides.style.transition = `transform ${config.transitionDuration}ms ease-out`;
      config.isTransitioning = true;
    } else {
      slides.style.transition = 'none';
    }
    
    setSliderPosition();
    
    // Update the active dot (accounting for the clone at the beginning)
    const dotIndex = index === 0 ? config.slideCount - 1 : 
                    index === config.slideCount + 1 ? 0 : 
                    index - 1;
    updateActiveDot(dotIndex);
  }
  
  // Update active dot
  function updateActiveDot(index) {
    if (!dotsContainer) return;
    
    const dots = dotsContainer.querySelectorAll('button');
    dots.forEach((dot, i) => {
      if (i === index) {
        dot.classList.remove('bg-gray-300');
        dot.classList.add('bg-[#3D2E7C]', 'scale-125');
      } else {
        dot.classList.remove('bg-[#3D2E7C]', 'scale-125');
        dot.classList.add('bg-gray-300');
      }
    });
  }
  
  // Go to slide
  function goToSlide(slideIndex) {
    if (slideIndex === config.currentIndex) return;
    
    setPositionByIndex(slideIndex);
  }
  
  // Get position X from event
  function getPositionX(event) {
    return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
  }
  
  // Start autoplay
  function startAutoplay() {
    if (config.autoplayInterval) clearInterval(config.autoplayInterval);
    
    config.autoplayInterval = setInterval(() => {
      if (!config.isDragging && !config.isTransitioning) {
        config.currentIndex += 1;
        setPositionByIndex(config.currentIndex);
      }
    }, config.autoplayDelay);
  }
  
  // Stop autoplay
  function stopAutoplay() {
    if (config.autoplayInterval) clearInterval(config.autoplayInterval);
  }
  
  // Initialize the carousel
  init();
}); 