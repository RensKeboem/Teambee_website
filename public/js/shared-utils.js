// Shared utility functions for Teambee application
window.TeambeeUtils = (function() {
    'use strict';
    
    // === LANGUAGE UTILITIES ===
    function getCurrentLanguage() {
        return window.location.pathname.startsWith('/en') ? 'en' : 'nl';
    }
    
    // === VALIDATION UTILITIES ===
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    function validateEmail(email) {
        return email && emailRegex.test(email);
    }
    
    // === SCROLL UTILITIES ===
    function preventScroll(e) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
    
    function disableScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollTop}px`;
        document.body.style.left = `-${scrollLeft}px`;
        document.body.style.width = '100%';
        
        document.body.setAttribute('data-scroll-top', scrollTop);
        document.body.setAttribute('data-scroll-left', scrollLeft);
    }
    
    function enableScroll() {
        const scrollTop = parseInt(document.body.getAttribute('data-scroll-top') || '0');
        const scrollLeft = parseInt(document.body.getAttribute('data-scroll-left') || '0');
        
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.width = '';
        
        window.scrollTo(scrollLeft, scrollTop);
        
        document.body.removeAttribute('data-scroll-top');
        document.body.removeAttribute('data-scroll-left');
    }
    
    // === MESSAGE UTILITIES ===
    function showMessage(element, message) {
        if (element) {
            element.textContent = message;
            element.classList.remove('hidden');
        }
    }
    
    function hideMessage(element) {
        if (element) {
            element.classList.add('hidden');
            element.textContent = '';
        }
    }
    
    // === TRANSLATION UTILITIES ===
    function createTranslationFunction(messages) {
        return function(key) {
            const lang = getCurrentLanguage();
            return messages[lang][key] || messages.en[key];
        };
    }
    
    // Public API
    return {
        getCurrentLanguage,
        validateEmail,
        preventScroll,
        disableScroll,
        enableScroll,
        showMessage,
        hideMessage,
        createTranslationFunction
    };
})(); 