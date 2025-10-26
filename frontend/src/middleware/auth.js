// Auth middleware for route protection
export function requireAuth(to, from, next) {
  const token = localStorage.getItem('auth_token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (!token || !user) {
    // Not authenticated, redirect to login
    next('/authentication/login')
  } else {
    next()
  }
}

export function requireRole(role) {
  return (to, from, next) => {
    const user = JSON.parse(localStorage.getItem('user') || 'null')
    
    if (!user) {
      next('/authentication/login')
    } else if (user.role !== role) {
      // Wrong role, redirect to their appropriate dashboard
      if (user.role === 'applicant') {
        next('/applicant/dashboard')
      } else if (user.role === 'recruiter') {
        next('/recruiter/dashboard')
      } else {
        next('/authentication/login')
      }
    } else {
      next()
    }
  }
}

export function guestOnly(to, from, next) {
  const token = localStorage.getItem('auth_token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (token && user) {
    // Already authenticated, redirect to dashboard
    if (user.role === 'applicant') {
      next('/applicant/dashboard')
    } else if (user.role === 'recruiter') {
      next('/recruiter/dashboard')
    } else {
      next('/')
    }
  } else {
    next()
  }
}

