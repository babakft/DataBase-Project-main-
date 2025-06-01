// Experts Vue.js Component
document.addEventListener('DOMContentLoaded', function() {
    new Vue({
        el: '#expertsApp',
        data: {
            experts: [
                {
                    id: 1,
                    name: 'احمد محمدی',
                    specialty: 'متخصص برق و روشنایی',
                    icon: 'fas fa-bolt',
                    rating: 5,
                    completed: 156,
                    experience: 8
                },
                {
                    id: 2,
                    name: 'فاطمه احمدی',
                    specialty: 'متخصص لوله‌کشی',
                    icon: 'fas fa-faucet',
                    rating: 5,
                    completed: 142,
                    experience: 6
                },
                {
                    id: 3,
                    name: 'علی رضایی',
                    specialty: 'متخصص تهویه مطبوع',
                    icon: 'fas fa-wind',
                    rating: 4,
                    completed: 98,
                    experience: 5
                },
                {
                    id: 4,
                    name: 'مریم کریمی',
                    specialty: 'متخصص نجاری',
                    icon: 'fas fa-hammer',
                    rating: 5,
                    completed: 87,
                    experience: 7
                },
                {
                    id: 5,
                    name: 'حسن موسوی',
                    specialty: 'متخصص نظافت',
                    icon: 'fas fa-broom',
                    rating: 4,
                    completed: 203,
                    experience: 4
                },
                {
                    id: 6,
                    name: 'سارا نوری',
                    specialty: 'متخصص امنیت',
                    icon: 'fas fa-shield-alt',
                    rating: 5,
                    completed: 76,
                    experience: 3
                },
                {
                    id: 7,
                    name: 'محمد صادقی',
                    specialty: 'تعمیرات عمومی',
                    icon: 'fas fa-tools',
                    rating: 4,
                    completed: 134,
                    experience: 9
                },
                {
                    id: 8,
                    name: 'زهرا حسینی',
                    specialty: 'کنترل کیفیت',
                    icon: 'fas fa-check-circle',
                    rating: 5,
                    completed: 89,
                    experience: 6
                }
            ]
        },
        mounted() {
            this.animateCards();
        },
        methods: {
            animateCards() {
                // Add staggered animation to expert cards
                const cards = document.querySelectorAll('.expert-card');
                cards.forEach((card, index) => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(30px)';

                    setTimeout(() => {
                        card.style.transition = 'all 0.6s ease';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 150);
                });
            },

            getExpertsBySpecialty(specialty) {
                return this.experts.filter(expert =>
                    expert.specialty.includes(specialty)
                );
            },

            getTopExperts() {
                return this.experts
                    .sort((a, b) => b.rating - a.rating || b.completed - a.completed)
                    .slice(0, 4);
            },

            formatRating(rating) {
                return '★'.repeat(rating) + '☆'.repeat(5 - rating);
            }
        }
    });
});

// Expert card hover effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover sound effect (optional)
    const expertCards = document.querySelectorAll('.expert-card');

    expertCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add intersection observer for scroll animations
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe expert cards
    const expertCards = document.querySelectorAll('.expert-card');
    expertCards.forEach(card => {
        observer.observe(card);
    });
});

// Add CSS for scroll animation
const style = document.createElement('style');
style.textContent = `
    .expert-card {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }

    .expert-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);