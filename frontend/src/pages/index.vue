<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-8 text-center elevation-12">
          <v-icon size="80" color="primary" class="mb-4">mdi-briefcase-search</v-icon>
          
          <h1 class="text-h3 mb-4">Recruitment Platform</h1>
          <p class="text-h6 text-grey mb-6">
            Smart Resume Screening for Modern Hiring
          </p>

          <v-row class="mb-6">
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-4">
                <v-icon size="48" color="primary" class="mb-3">mdi-account</v-icon>
                <h3 class="text-h6 mb-2">For Applicants</h3>
                <p class="text-body-2 mb-4">
                  Upload your resume and get instant feedback with detailed scoring
                </p>
                <v-btn
                  color="primary"
                  size="large"
                  block
                  to="/authentication/register"
                >
                  Get Started
                </v-btn>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-card variant="outlined" class="pa-4">
                <v-icon size="48" color="secondary" class="mb-3">mdi-account-tie</v-icon>
                <h3 class="text-h6 mb-2">For Recruiters</h3>
                <p class="text-body-2 mb-4">
                  Review graded resumes and find the best candidates efficiently
                </p>
                <v-btn
                  color="secondary"
                  size="large"
                  block
                  to="/authentication/register"
                >
                  Get Started
                </v-btn>
              </v-card>
            </v-col>
          </v-row>

          <v-divider class="my-6"></v-divider>

          <p class="text-body-1 mb-4">Already have an account?</p>
          <v-btn
            variant="outlined"
            color="primary"
            size="large"
            to="/authentication/login"
          >
            <v-icon left>mdi-login</v-icon>
            Sign In
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <!-- Features Section -->
    <v-row class="mt-12">
      <v-col cols="12">
        <h2 class="text-h4 text-center mb-8">Features</h2>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-6 text-center h-100">
          <v-icon size="56" color="primary" class="mb-4">mdi-robot</v-icon>
          <h3 class="text-h6 mb-3">AI-Powered Grading</h3>
          <p class="text-body-2">
            Automated resume analysis with detailed scoring across multiple criteria
          </p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-6 text-center h-100">
          <v-icon size="56" color="primary" class="mb-4">mdi-speedometer</v-icon>
          <h3 class="text-h6 mb-3">Instant Feedback</h3>
          <p class="text-body-2">
            Get immediate results with actionable insights to improve your resume
          </p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-6 text-center h-100">
          <v-icon size="56" color="primary" class="mb-4">mdi-shield-check</v-icon>
          <h3 class="text-h6 mb-3">Secure & Private</h3>
          <p class="text-body-2">
            Your data is encrypted and secure. We respect your privacy
          </p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'HomePage',
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole'])
  },
  mounted() {
    console.log('🏠 Homepage mounted:', {
      isAuthenticated: this.isAuthenticated,
      userRole: this.userRole
    })
    
    // 🚧 DEVELOPMENT MODE: Auto-redirect disabled
    // Redirect if already logged in
    // if (this.isAuthenticated && this.userRole) {
    //   console.log('→ Auto-redirecting authenticated user to dashboard')
    //   if (this.userRole === 'applicant') {
    //     this.$router.push('/applicant/dashboard')
    //   } else if (this.userRole === 'recruiter') {
    //     this.$router.push('/recruiter/dashboard')
    //   }
    // }
  }
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style>
