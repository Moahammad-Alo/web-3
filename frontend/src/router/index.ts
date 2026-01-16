/**
 * Vue Router configuration for the Auction application.
 */

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Page components
import HomePage from '../pages/HomePage.vue'
import ItemDetailPage from '../pages/ItemDetailPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import CreateItemPage from '../pages/CreateItemPage.vue'
import MyAuctionsPage from '../pages/MyAuctionsPage.vue'

// Base URL handling for development vs production
const base: string = (import.meta.env.MODE === 'development') ? import.meta.env.BASE_URL : ''

// Route definitions with type annotations
const routes: RouteRecordRaw[] = [
    { 
        path: '/', 
        name: 'Home', 
        component: HomePage,
        meta: { title: 'Browse Auctions' }
    },
    { 
        path: '/items/:id', 
        name: 'ItemDetail', 
        component: ItemDetailPage,
        meta: { title: 'Item Details' }
    },
    { 
        path: '/profile', 
        name: 'Profile', 
        component: ProfilePage,
        meta: { title: 'Profile Settings' }
    },
    { 
        path: '/create-item', 
        name: 'CreateItem', 
        component: CreateItemPage,
        meta: { title: 'Create Listing' }
    },
    { 
        path: '/my-auctions', 
        name: 'MyAuctions', 
        component: MyAuctionsPage,
        meta: { title: 'My Auctions' }
    },
]

const router = createRouter({
    history: createWebHistory(base),
    routes,
})

// Flag to track if initial auth check has been performed
let authCheckDone = false

// Authentication guard - redirect to login if not authenticated
router.beforeEach(async (_to, _from, next) => {
    const userStore = useUserStore()
    
    // Only fetch user status once on initial app load
    if (!authCheckDone) {
        authCheckDone = true
        await userStore.fetchUser()
    }
    
    // Redirect to login page if not authenticated
    if (!userStore.isAuthenticated) {
        window.location.href = '/login/'
        return
    }
    
    next()
})

// Update document title on route change
router.afterEach((to) => {
    const title = to.meta.title as string | undefined
    document.title = title ? `${title} | AuctionHub` : 'AuctionHub'
})

export default router
