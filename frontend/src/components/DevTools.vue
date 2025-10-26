<template>
  <v-fab
    v-if="isDev"
    icon="mdi-tools"
    location="bottom right"
    size="small"
    color="warning"
    @click="showDialog = true"
    style="position: fixed; bottom: 80px; right: 16px;"
  ></v-fab>

  <v-dialog v-model="showDialog" max-width="400">
    <v-card>
      <v-card-title class="bg-warning">
        <v-icon left>mdi-tools</v-icon>
        Dev Tools
      </v-card-title>

      <v-card-text class="pa-4">
        <v-list>
          <v-list-item>
            <v-list-item-title>Auth Status</v-list-item-title>
            <v-list-item-subtitle>
              {{ isAuthenticated ? '✅ Authenticated' : '❌ Not Authenticated' }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item v-if="isAuthenticated">
            <v-list-item-title>User</v-list-item-title>
            <v-list-item-subtitle>
              {{ currentUser?.name }} ({{ currentUser?.role }})
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item v-if="token">
            <v-list-item-title>Token</v-list-item-title>
            <v-list-item-subtitle class="text-truncate" style="max-width: 300px;">
              {{ token.substring(0, 30) }}...
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <v-divider class="my-4"></v-divider>

        <v-btn
          color="error"
          block
          @click="clearAuth"
          prepend-icon="mdi-delete"
        >
          Clear Auth State
        </v-btn>

        <v-btn
          color="info"
          block
          class="mt-2"
          @click="reload"
          prepend-icon="mdi-refresh"
        >
          Reload Page
        </v-btn>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="showDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'

export default {
  name: 'DevTools',
  data() {
    return {
      showDialog: false,
      isDev: import.meta.env.DEV
    }
  },
  computed: {
    ...mapState(['token', 'user']),
    ...mapGetters(['isAuthenticated', 'currentUser'])
  },
  methods: {
    ...mapActions(['logout']),
    
    clearAuth() {
      this.logout()
      this.showDialog = false
      this.$router.push('/')
      alert('✅ Authentication cleared! You can now access register/login pages.')
    },
    
    reload() {
      window.location.reload()
    }
  }
}
</script>

