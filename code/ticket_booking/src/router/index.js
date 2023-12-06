import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../views/UserLoginView.vue';
import UserSignUp from '../views/UserSignUpView.vue';
import UserDashboard from '../views/UserDashBoardView.vue';
import SearchResults from '../views/SearchView.vue';
import VenueDetails from '../views/VenueView.vue';
import MyBookings from '../views/BookingsView.vue';
import AdminLogin from '../views/AdminLoginView.vue';
import AdminDashboard from '../views/AdminDashboardView.vue';
import BookShow from '../views/BookShowView.vue';
import SummaryView from '../views/SummaryView.vue';


const routes = [
    {
        path: '/',
        component: UserLogin,
    },
    {
        path: '/user_signup',
        component: UserSignUp,
    },
    {
        path: '/user_dashboard',
        component: UserDashboard,

    },
    {
        path: '/search',
        component: SearchResults,
    },
    {
        path: '/venue/:venue_id',
        component: VenueDetails,

    },
    {
        path: '/my_bookings',
        component: MyBookings,
    },
    {
        path: '/admin_login',
        component: AdminLogin,
    },
    {
        path: '/admin_dashboard',
        component: AdminDashboard,
    },
    {
        path: '/book_show/:show_id',
        component: BookShow,
    },
    {
        path: '/summary',
        component: SummaryView,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  });

export default router;