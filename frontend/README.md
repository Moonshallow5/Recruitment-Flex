# Recruitment Platform - Frontend

Vue 3 application with Vuetify for the recruitment platform.

## State Management Architecture

### ✅ Pure Vuex Store (No LocalStorage)

This application uses **pure Vuex** for state management with **NO localStorage persistence**:

- ✅ JWT token stored ONLY in Vuex memory
- ✅ User data stored ONLY in Vuex memory  
- ✅ No localStorage/sessionStorage for auth data
- ✅ Clean, secure, memory-only state

### Trade-offs:

**Pros:**
- No localStorage security concerns
- No XSS attacks on stored tokens
- Clean state on page refresh
- Forces explicit login flow

**Cons:**
- Users logged out on page refresh (by design)
- Users logged out on tab close
- Must login again after navigation away

## How Authentication Works

1. **Login**: User credentials sent to backend → JWT received → stored in Vuex
2. **API Calls**: Axios interceptor reads token from Vuex store → adds to headers
3. **Navigation**: Router guards check Vuex state for authentication
4. **Page Refresh**: State cleared → user redirected to login
5. **Logout**: Vuex state cleared → redirect to home

## Setup

```bash
npm install
npm run dev
```

## Environment Variables

Create `.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_DEBUG=true
```

## Project Structure

```
src/
├── pages/              # File-based routing
│   ├── index.vue       # Home page
│   ├── authentication/
│   │   ├── login.vue   # Login page
│   │   └── register.vue # Registration page
│   ├── applicant/
│   │   └── dashboard.vue
│   └── recruiter/
│       └── dashboard.vue
├── states/
│   └── store.js        # Vuex store (pure, no persistence)
├── scripts/
│   ├── axios.js        # API wrapper
│   └── axiosUpload.js  # File upload wrapper
├── router/
│   └── index.js        # Router with auth guards
└── components/
    └── DevTools.vue    # Dev debugging tools
```

## State Management

### Vuex Store Structure

```javascript
state: {
  user: {},      // Current user object { id, username, name, role }
  token: null,   // JWT authentication token
  loading: {},   // Loading states for UI
}
```

### Using Vuex in Components

```vue
<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState(['user', 'token']),
    ...mapGetters(['isAuthenticated', 'userRole', 'currentUser'])
  },
  methods: {
    ...mapActions(['login', 'logout', 'register'])
  }
}
</script>
```

### Available Getters

- `isAuthenticated` - Returns true if user has token
- `currentUser` - Returns user object
- `userRole` - Returns 'applicant' or 'recruiter'
- `isApplicant` - Returns true if user is applicant
- `isRecruiter` - Returns true if user is recruiter

### Available Actions

- `login({ username, password })` - Authenticate user
- `register(userData)` - Register new user
- `logout()` - Clear authentication state

## API Integration

All API calls automatically include JWT from Vuex:

```javascript
import Ajax from '@/scripts/axios'

// Token automatically added from Vuex store
const data = await Ajax('resumes/my-resumes', {}, 'GET')
```

The axios wrapper:
- Reads token from Vuex store (`Store.state.token`)
- Adds `Authorization: Bearer {token}` header
- Handles errors globally
- Shows toast notifications
- Auto-redirects to login on 401

## Development Tools

In development mode, a floating wrench icon (🛠️) appears in the bottom-right corner:

**Features:**
- View current auth status
- See user info and token
- Clear auth state instantly
- Reload page

## Security Features

### Why No LocalStorage?

1. **XSS Protection**: No tokens stored in localStorage that could be stolen
2. **CSRF Protection**: Tokens in memory only
3. **Session Management**: Users explicitly login each session
4. **Clean State**: No stale tokens

### How JWT is Handled

```
Login → Backend returns JWT → Stored in Vuex → Used in API calls
```

The token NEVER touches localStorage or cookies. It exists only in JavaScript memory.

### On Page Refresh

```
Page Refresh → Vuex cleared → Token lost → Redirect to login
```

This is **by design** for maximum security.

## Router Guards

### Protected Routes

```javascript
// Requires authentication
/applicant/dashboard  → Only for applicants
/recruiter/dashboard  → Only for recruiters
```

### Guest Routes

```javascript
// Redirects to dashboard if already authenticated
/authentication/login
/authentication/register
```

### Navigation Flow

1. User navigates to route
2. Router guard checks `Store.state.token`
3. If protected route && no token → redirect to login
4. If guest route && has token → redirect to dashboard
5. If wrong role → redirect to correct dashboard

## Common Tasks

### Check if User is Logged In

```javascript
import { mapGetters } from 'vuex'

computed: {
  ...mapGetters(['isAuthenticated'])
}

// Or access store directly
import Store from '@/states/store'
const isLoggedIn = !!Store.state.token
```

### Get Current User

```vue
<template>
  <div>Welcome, {{ currentUser.name }}!</div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['currentUser'])
  }
}
</script>
```

### Logout User

```javascript
import { mapActions } from 'vuex'

methods: {
  ...mapActions(['logout']),
  
  handleLogout() {
    this.logout()
    this.$router.push('/authentication/login')
  }
}
```

## API Endpoints Used

- `POST /auth/login` - Login
- `POST /auth/register` - Register
- `GET /auth/me` - Get current user
- `POST /resumes/upload` - Upload resume
- `GET /resumes/my-resumes` - Get user resumes
- `GET /resumes/all` - Get all resumes (recruiter)

## Building for Production

```bash
npm run build
```

Output in `dist/` folder.

## Best Practices

1. **Always use Vuex actions** for auth operations
2. **Use mapGetters** instead of accessing state directly
3. **Check isAuthenticated** before protected operations
4. **Handle 401 errors** (axios does this automatically)
5. **Use DevTools** in development for debugging

## Troubleshooting

### Can't Access Register Page

**Cause**: You have authentication state in Vuex  
**Fix**: Click DevTools → Clear Auth State

### Lost Login After Refresh

**This is normal!** The app uses memory-only storage. Users must login again after refresh.

### Token Not Being Sent

**Check**: Vuex store has token
```javascript
console.log(Store.state.token)
```

### TypeErrors on Store Access

**Fix**: Import store correctly
```javascript
import Store from '@/states/store'
```

## Dependencies

- `vue` - Vue 3 framework
- `vuex` - State management (NO persistence)
- `vue-router` - Routing with auto-routes
- `vuetify` - Material Design components
- `axios` - HTTP client
- `vue-toast-notification` - Toast messages

**Note**: `vuex-persistedstate` and `secure-ls` are NOT used - pure memory storage only.

## License

MIT
