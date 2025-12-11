/**
 * DeepSonar Custom Chainlit JavaScript
 * - SSO: Redirect to Django login page instead of Chainlit login
 * - Auto-expand live_logs side panel when it appears
 */

(function() {
    'use strict';
    
    // ==========================================================================
    // SSO: Redirect to Django login page
    // ==========================================================================
    const DJANGO_LOGIN_URL = 'http://www.deepsonar.com.cn/login/';
    
    // Check if we're on the Chainlit login page
    if (window.location.pathname === '/login' || window.location.pathname === '/login/') {
        // Check if we have an SSO marker cookie - if we do, the SSO validation failed
        // In that case, don't redirect to avoid a loop
        const hasSSOCookie = document.cookie.includes('deepsonar_sso_active');
        
        if (!hasSSOCookie) {
            console.log('[DeepSonar SSO] No SSO token, redirecting to Django login...');
            window.location.href = DJANGO_LOGIN_URL;
            return;
        } else {
            console.log('[DeepSonar SSO] SSO token exists but validation failed, staying on Chainlit login');
            // Token exists but validation failed - user needs to re-login via Chainlit
            // This could happen if the token is expired or invalid
        }
    }
    
    // ==========================================================================
    // Live Logs Auto-Expand
    // ==========================================================================
    
    // Configuration
    const LIVE_LOGS_NAME = 'live_logs';
    const CHECK_INTERVAL = 500; // Check every 500ms
    const MAX_ATTEMPTS = 120;    // Maximum 60 seconds (120 * 500ms)
    
    let attempts = 0;
    let lastClickedName = null;
    
    /**
     * Find and click the live_logs link to expand the side panel
     */
    function expandLiveLogs() {
        // Look for the clickable link containing "live_logs"
        // Chainlit creates a link with the name of the Text element
        const links = document.querySelectorAll('a, button, span[role="button"], [data-testid*="element"]');
        
        for (const link of links) {
            const text = link.textContent || '';
            const dataName = link.getAttribute('data-name') || '';
            
            // Match by text content or data attribute
            if (text.includes(LIVE_LOGS_NAME) || dataName === LIVE_LOGS_NAME) {
                // Only click if we haven't clicked this one already
                if (lastClickedName !== LIVE_LOGS_NAME) {
                    console.log('[DeepSonar] Found live_logs element, expanding...');
                    link.click();
                    lastClickedName = LIVE_LOGS_NAME;
                    return true;
                }
            }
        }
        
        // Alternative: Look for Material-UI Chip or similar components
        const chips = document.querySelectorAll('.MuiChip-root, .MuiButton-root');
        for (const chip of chips) {
            const text = chip.textContent || '';
            if (text.includes(LIVE_LOGS_NAME) || text.includes('live_logs')) {
                if (lastClickedName !== LIVE_LOGS_NAME) {
                    console.log('[DeepSonar] Found live_logs chip, expanding...');
                    chip.click();
                    lastClickedName = LIVE_LOGS_NAME;
                    return true;
                }
            }
        }
        
        return false;
    }
    
    /**
     * Reset state when a new analysis starts
     */
    function resetState() {
        lastClickedName = null;
        attempts = 0;
    }
    
    /**
     * Observer to detect new messages with live_logs
     */
    function setupObserver() {
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                // Check if new nodes contain live_logs reference
                if (mutation.addedNodes.length > 0) {
                    for (const node of mutation.addedNodes) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const text = node.textContent || '';
                            if (text.includes('Starting analysis') || text.includes('开始分析')) {
                                // New analysis started, reset state
                                resetState();
                            }
                            if (text.includes(LIVE_LOGS_NAME)) {
                                // Give a small delay for UI to stabilize
                                setTimeout(() => {
                                    expandLiveLogs();
                                }, 300);
                            }
                        }
                    }
                }
            }
        });
        
        // Start observing
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('[DeepSonar] Side panel auto-expand observer initialized');
    }
    
    /**
     * Initial check loop for early load
     */
    function startInitialCheck() {
        const checkInterval = setInterval(() => {
            attempts++;
            
            // Try to expand if found
            if (expandLiveLogs()) {
                console.log('[DeepSonar] Successfully expanded live_logs');
            }
            
            // Stop after max attempts
            if (attempts >= MAX_ATTEMPTS) {
                clearInterval(checkInterval);
            }
        }, CHECK_INTERVAL);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setupObserver();
            startInitialCheck();
        });
    } else {
        setupObserver();
        startInitialCheck();
    }
    
})();
