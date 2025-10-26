<template>
    <v-container class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="elevation-12 pa-4">
            <v-card-title class="text-h4 text-center mb-4">
              <v-icon left color="primary">mdi-login</v-icon>
              Login
            </v-card-title>
  
            <v-card-text>
              <v-form @submit.prevent="handleLogin">
                <v-text-field
                  v-model="credentials.username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  required
                  class="mb-3"
                />
  
                <v-text-field
                  v-model="credentials.password"
                  label="Password"
                  prepend-inner-icon="mdi-lock"
                  :type="showPassword ? 'text' : 'password'"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="showPassword = !showPassword"
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
                  Login
                </v-btn>
              </v-form>
  
              <div class="text-center mt-4">
                <p class="text-body-2">
                  Don't have an account? 
                  <router-link to="/authentication/register" class="text-primary">Register</router-link>
                </p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import { mapActions, mapGetters } from 'vuex'
  
  export default {
    name: 'LoginForm',
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        },
        showPassword: false,
        loading: false
      }
    },
    computed: {
      ...mapGetters(['userRole'])
    },
    methods: {
      ...mapActions(['login']),
      
      async handleLogin() {
        if (!this.credentials.username || !this.credentials.password) {
          return
        }
  
        this.loading = true
        try {
          await this.login(this.credentials)
  
          // Redirect based on role
          if (this.userRole === 'applicant') {
            this.$router.push('/applicant/dashboard')
          } else if (this.userRole === 'recruiter') {
            this.$router.push('/recruiter/dashboard')
          }
        } catch (error) {
          console.error('Login failed:', error)
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
  