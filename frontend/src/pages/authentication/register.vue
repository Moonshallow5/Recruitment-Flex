<template>
    <v-container class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="elevation-12 pa-4">
            <v-card-title class="text-h4 text-center mb-4">
              <v-icon left color="primary">mdi-account-plus</v-icon>
              Register
            </v-card-title>
  
            <v-card-text>
              <v-form @submit.prevent="handleRegister">
                <v-text-field
                  v-model="userData.username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  required
                  class="mb-3"
                />
  
                <v-text-field
                  v-model="userData.name"
                  label="Full Name"
                  prepend-inner-icon="mdi-card-account-details"
                  variant="outlined"
                  required
                  class="mb-3"
                />

                <v-text-field
                  v-model="userData.email"
                  label="Email"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  type="email"
                  required
                  class="mb-3"
                />

                <v-select
                  v-model="userData.role"
                  :items="roles"
                  label="I am a..."
                  prepend-inner-icon="mdi-account-group"
                  variant="outlined"
                  required
                  class="mb-3"
                />

                <v-text-field
                  v-model="userData.password"
                  label="Password"
                  prepend-inner-icon="mdi-lock"
                  :type="showPassword ? 'text' : 'password'"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  required
                  class="mb-3"
                />
  
                <v-text-field
                  v-model="userData.confirm_password"
                  label="Confirm Password"
                  prepend-inner-icon="mdi-lock-check"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showConfirmPassword = !showConfirmPassword"
                  variant="outlined"
                  required
                  class="mb-4"
                />
  
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="loading"
                >
                  Register
                </v-btn>
              </v-form>
  
              <div class="text-center mt-4">
                <p class="text-body-2">
                  Already have an account? 
                  <router-link to="/authentication/login" class="text-primary">Login</router-link>
                </p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import { mapActions } from 'vuex'
  import { useToast } from 'vue-toast-notification'
  
  export default {
    name: 'RegisterForm',
    data() {
      return {
        userData: {
          username: '',
          name: '',
          email: '',
          password: '',
          confirm_password: '',
          role: 'applicant'
        },
        roles: [
          { title: 'Job Applicant', value: 'applicant' },
          { title: 'Recruiter', value: 'recruiter' }
        ],
        showPassword: false,
        showConfirmPassword: false,
        loading: false
      }
    },
    methods: {
      ...mapActions(['register']),
      
      async handleRegister() {
        const $toast = useToast()
        
        if (!this.userData.username || !this.userData.name || !this.userData.email ||
            !this.userData.password || !this.userData.confirm_password) {
          $toast.error('All fields are required', {
            duration: 3000,
            position: 'top-right'
          })
          return
        }
  
        if (this.userData.password !== this.userData.confirm_password) {
          $toast.error('Passwords do not match', {
            duration: 3000,
            position: 'top-right'
          })
          return
        }
  
        this.loading = true
        try {
          await this.register(this.userData)
          $toast.success('Registration successful! Please login.', {
            duration: 3000,
            position: 'top-right'
          })
          this.$router.push('/authentication/login')
        } catch (error) {
          console.error('Registration failed:', error)
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .v-card {
    border-radius: 12px;
  }
  </style>
  