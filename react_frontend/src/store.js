import { configureStore } from '@reduxjs/toolkit';
import { productDetailsReducers, productsListReducers } from './reducers/productsReducers';
import { userLoginReducer, userRegisterReducer, userVerifyReducer } from './reducers/userReducers';
import { cartReducer } from './reducers/cartReducers';
import { orderDetailsReducer, orderCreateReducer } from './reducers/orderReducer';
import {
    userDetailsReducer,
    userUpdateProfileReducer,
  } from './reducers/userReducers';

// Get user info from localStorage
const userInfoFromStorage = localStorage.getItem('userInfo')
    ? JSON.parse(localStorage.getItem('userInfo'))
    : null;

// Get cart and shipping from localStorage
const cartItemsFromStorage = localStorage.getItem('cartItems')
    ? JSON.parse(localStorage.getItem('cartItems'))
    : [];

const shippingAddressFromStorage = localStorage.getItem('shippingAddress')
    ? JSON.parse(localStorage.getItem('shippingAddress'))
    : {};


// Initial state
const initialState = {
    userLogin: {
        userInfo: userInfoFromStorage,
        loading: false,
        error: null
    },
    cart: {
        cartItems: cartItemsFromStorage,
        shippingAddress: shippingAddressFromStorage
    },
    productsList: {
        products: [],
        loading: false,
        error: null
    },
    productDetails: {
        product: null,
        loading: false,
        error: null
    }
};

// Create store
const store = configureStore({
    reducer: {
        orderDetails: orderDetailsReducer,
        productsList: productsListReducers,
        orderCreate: orderCreateReducer,
        productDetails: productDetailsReducers,
        userLogin: userLoginReducer,
        userRegister: userRegisterReducer,
        userVerify: userVerifyReducer, 
        cart: cartReducer,
        userDetails: userDetailsReducer,
        userUpdateProfile: userUpdateProfileReducer,
    },
    preloadedState: initialState,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
            immutableCheck: false,
        }),
    devTools: process.env.NODE_ENV !== 'production',
});

// Persist store changes
store.subscribe(() => {
    const state = store.getState();

    if (state.userLogin.userInfo && state.userLogin.userInfo.token) {
        localStorage.setItem('userInfo', JSON.stringify(state.userLogin.userInfo));
    }

    if (state.cart.cartItems) {
        localStorage.setItem('cartItems', JSON.stringify(state.cart.cartItems));
    }

    if (state.cart.shippingAddress) {
        localStorage.setItem('shippingAddress', JSON.stringify(state.cart.shippingAddress));
    }
});

export default store;
