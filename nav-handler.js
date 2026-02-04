// Navigation handler for ZOE STUDIO Dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation tab clicks
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            navTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Handle navigation
            const href = this.getAttribute('href');
            if (href === '/' || href === '#overview') {
                // Stay on current page (unified dashboard)
                console.log('Overview tab clicked');
            } else if (href === '/aws' || href.includes('aws')) {
                window.location.href = '/aws.html';
            } else if (href === '/workflow' || href.includes('workflow')) {
                window.location.href = '/workflow.html';
            } else if (href === '/simple') {
                window.location.href = '/simple.html';
            } else if (href === '/test') {
                window.location.href = '/test.html';
            }
        });
    });
    
    // Auto-refresh every 5 minutes
    setTimeout(function() {
        window.location.reload();
    }, 300000); // 5 minutes
});