# 🚧 Development Mode - Authentication Disabled

## Current State

✅ **Authentication is DISABLED** for development

You can now access:
- ✅ `/` - Homepage
- ✅ `/authentication/login` - Login page
- ✅ `/authentication/register` - Register page  
- ✅ `/applicant/dashboard` - Applicant dashboard (no auth required)
- ✅ `/recruiter/dashboard` - Recruiter dashboard (no auth required)

## What Was Changed

### 1. Router Guard Disabled (`src/router/index.js`)
```javascript
// ❌ BEFORE: Checked authentication and redirected
if (!isAuthenticated) {
  next('/authentication/login')
  return
}

// ✅ NOW: Allows all navigation
console.log('✅ Navigation allowed to:', to.path, '(no auth required)')
next()
```

### 2. Homepage Auto-Redirect Disabled (`src/pages/index.vue`)
```javascript
// ❌ BEFORE: Auto-redirected to dashboard if logged in
if (this.isAuthenticated && this.userRole) {
  this.$router.push('/applicant/dashboard')
}

// ✅ NOW: Commented out
// Auto-redirect disabled for dev mode
```

### 3. Dashboards Show Warning (`src/pages/applicant/dashboard.vue` & `recruiter/dashboard.vue`)
```vue
<!-- Shows warning chip when not authenticated -->
<v-chip v-if="!isAuthenticated" color="warning">
  Dev Mode - Not Authenticated
</v-chip>
```

## How to Use

### Navigate Directly to Any Page:

```javascript
// In browser console or address bar:
window.location.href = 'http://localhost:3000/applicant/dashboard'
window.location.href = 'http://localhost:3000/recruiter/dashboard'
window.location.href = 'http://localhost:3000/authentication/register'
```

### Using Links:

All links work now without authentication:
- Click "Get Started" → Works
- Click "Login" link → Works
- Type URLs directly → Works
- Use Vue Router → Works

## Console Logs

You'll see:
```
📍 Auto-generated routes: [...]
🔍 Router Guard (DEV MODE - Auth Disabled): { to: "/applicant/dashboard", ... }
✅ Navigation allowed to: /applicant/dashboard (no auth required)
```

## API Calls

⚠️ **Important**: While pages are accessible, API calls may still fail if backend requires authentication!

Example:
```javascript
// This will fail with 401 if backend requires auth
GET /resumes/my-resumes
```

### To Test UI Without Backend:

1. Comment out API calls in `mounted()` hooks
2. Use mock data instead
3. Or handle 401 errors gracefully

## Re-Enabling Authentication

When you're ready to re-enable authentication:

### Option 1: Restore Router Guard

In `src/router/index.js`, replace the simplified guard with:

```javascript
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!Store.state.token
  const userRole = Store.state.user?.role

  // Protected routes
  const applicantRoutes = ['/applicant/dashboard']
  const recruiterRoutes = ['/recruiter/dashboard']
  
  const isApplicantRoute = applicantRoutes.some(route => to.path.startsWith(route))
  const isRecruiterRoute = recruiterRoutes.some(route => to.path.startsWith(route))

  if (isApplicantRoute || isRecruiterRoute) {
    if (!isAuthenticated) {
      next('/authentication/login')
      return
    }
  }

  // Guest-only routes
  const guestRoutes = ['/authentication/login', '/authentication/register']
  if (guestRoutes.includes(to.path) && isAuthenticated) {
    if (userRole === 'applicant') {
      next('/applicant/dashboard')
    } else if (userRole === 'recruiter') {
      next('/recruiter/dashboard')
    }
    return
  }

  next()
})
```

### Option 2: Environment-Based Toggle

```javascript
const DEV_DISABLE_AUTH = import.meta.env.VITE_DISABLE_AUTH === 'true'

router.beforeEach((to, from, next) => {
  if (DEV_DISABLE_AUTH) {
    next() // Allow all
    return
  }
  
  // ... normal auth checks
})
```

Then in `.env`:
```env
VITE_DISABLE_AUTH=true  # Dev mode
```

## Testing Checklist

Now you can test:

✅ UI Layout and Design
- Check all pages render correctly
- Test responsive design
- Verify Vuetify components work
- Check color schemes and themes

✅ Navigation
- Test all router links
- Check breadcrumbs
- Verify back/forward buttons

✅ Forms
- Test all input fields
- Check validation (client-side)
- Verify file uploads UI

✅ Data Display
- Test with mock data
- Check empty states
- Verify loading states

❌ Cannot Test (requires auth):
- Actual API calls
- Real data fetching
- Backend integration
- Token handling

## Quick Navigation Menu

Add this to browser console for easy navigation:

```javascript
const nav = {
  home: () => location.href = 'http://localhost:3000/',
  login: () => location.href = 'http://localhost:3000/authentication/login',
  register: () => location.href = 'http://localhost:3000/authentication/register',
  applicant: () => location.href = 'http://localhost:3000/applicant/dashboard',
  recruiter: () => location.href = 'http://localhost:3000/recruiter/dashboard',
}

// Usage:
nav.applicant()
nav.recruiter()
```

## Notes

- Warning chips will show on dashboards when not authenticated
- Console logs show "DEV MODE - Auth Disabled"
- This is for **development only** - don't deploy with auth disabled!
- Remember to re-enable auth before production

