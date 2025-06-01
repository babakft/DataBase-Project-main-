// Essential Service Worker for University Maintenance System
const CACHE_NAME = 'maintenance-system-v1';

// Install event
self.addEventListener('install', function(event) {
    console.log('Service Worker: Installing...');
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', function(event) {
    console.log('Service Worker: Activating...');
    event.waitUntil(self.clients.claim());
});

// Fetch event - basic caching strategy
self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
            .catch(function() {
                // If network fails, try cache
                return caches.match(event.request);
            })
    );
});