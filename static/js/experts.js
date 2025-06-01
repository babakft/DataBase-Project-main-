// static/js/experts.js
new Vue({
    el: '#expertsApp',
    data() {
        return {
            experts: [],
            loading: true,
            error: null
        };
    },
    async mounted() {
        await this.loadExperts();
    },
    methods: {
        async loadExperts() {
            try {
                const response = await fetch('/api/experts/');
                if (!response.ok) {
                    throw new Error('Failed to load experts data');
                }
                const data = await response.json();
                
                if (data.success) {
                    this.experts = data.experts;
                } else {
                    throw new Error(data.error || 'Unknown error occurred');
                }
            } catch (error) {
                console.error('Error loading experts:', error);
                this.error = error.message;
                // Fallback data in case of API failure
                this.experts = this.getFallbackExperts();
            } finally {
                this.loading = false;
            }
        },
        
        getFallbackExperts() {
            return [
                {
                    id: 1,
                    name: 'احمد محمدی',
                    specialty: 'برق و روشنایی',
                    icon: 'fas fa-bolt',
                    rating: 4.8,
                    completed: 45,
                    experience: 5
                },
                {
                    id: 2,
                    name: 'فاطمه احمدی',
                    specialty: 'لوله‌کشی و آب',
                    icon: 'fas fa-faucet',
                    rating: 4.9,
                    completed: 38,
                    experience: 4
                },
                {
                    id: 3,
                    name: 'علی رضایی',
                    specialty: 'تهویه مطبوع',
                    icon: 'fas fa-wind',
                    rating: 4.7,
                    completed: 42,
                    experience: 6
                },
                {
                    id: 4,
                    name: 'مریم کریمی',
                    specialty: 'نجاری و تعمیرات',
                    icon: 'fas fa-hammer',
                    rating: 4.8,
                    completed: 35,
                    experience: 3
                },
                {
                    id: 5,
                    name: 'حسن موسوی',
                    specialty: 'تعمیرات عمومی',
                    icon: 'fas fa-tools',
                    rating: 4.6,
                    completed: 50,
                    experience: 7
                },
                {
                    id: 6,
                    name: 'سارا نوری',
                    specialty: 'نظافت و بهداشت',
                    icon: 'fas fa-broom',
                    rating: 4.9,
                    completed: 28,
                    experience: 2
                },
                {
                    id: 7,
                    name: 'محمد صادقی',
                    specialty: 'امنیت و نظارت',
                    icon: 'fas fa-shield-alt',
                    rating: 4.8,
                    completed: 33,
                    experience: 4
                },
                {
                    id: 8,
                    name: 'زهرا حسینی',
                    specialty: 'برق و روشنایی',
                    icon: 'fas fa-bolt',
                    rating: 4.7,
                    completed: 41,
                    experience: 5
                }
            ];
        }
    }
});