<template>
  <v-container>
    <!-- Back Button -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn variant="text" @click="goBack">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Dashboard
        </v-btn>
      </v-col>
    </v-row>

    <!-- Job Details Card -->
    <v-row v-if="jobDetails">
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center bg-primary text-white">
            <v-icon left>mdi-briefcase</v-icon>
            {{ jobDetails.job_title }}
            <v-spacer></v-spacer>
            <v-chip
              :color="jobDetails.is_active ? 'success' : 'grey'"
              size="small"
            >
              {{ jobDetails.is_active ? 'Active' : 'Inactive' }}
            </v-chip>
          </v-card-title>

          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" md="6">
                <div class="mb-3">
                  <strong><v-icon left size="small">mdi-office-building</v-icon> Company:</strong> 
                  {{ jobDetails.company_name }}
                </div>
                <div class="mb-3" v-if="jobDetails.location">
                  <strong><v-icon left size="small">mdi-map-marker</v-icon> Location:</strong> 
                  {{ jobDetails.location }}
                </div>
                <div class="mb-3" v-if="jobDetails.salary_range">
                  <strong><v-icon left size="small">mdi-cash</v-icon> Salary:</strong> 
                  {{ jobDetails.salary_range }}
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="mb-3" v-if="jobDetails.employment_type">
                  <strong><v-icon left size="small">mdi-clock</v-icon> Type:</strong> 
                  {{ jobDetails.employment_type }}
                </div>
                <div class="mb-3" v-if="jobDetails.experience_level">
                  <strong><v-icon left size="small">mdi-account-star</v-icon> Experience:</strong> 
                  {{ jobDetails.experience_level }}
                </div>
                <div class="mb-3">
                  <strong><v-icon left size="small">mdi-account-multiple</v-icon> Applications:</strong> 
                  <v-chip size="small" color="primary">{{ applications.length }}</v-chip>
                </div>
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <div class="mb-3">
              <strong>Skills Required:</strong>
              <div class="mt-2">
                <v-chip
                  v-for="skill in getSkillsList(jobDetails.skills)"
                  :key="skill"
                  size="small"
                  color="primary"
                  class="mr-2 mb-2"
                >
                  {{ skill }}
                </v-chip>
              </div>
            </div>

            <v-divider class="my-4"></v-divider>

            <div class="mb-2">
              <strong>Job Description:</strong>
            </div>
            <div class="text-body-1 pa-4 bg-grey-lighten-5 rounded" style="white-space: pre-wrap;">
              {{ jobDetails.job_description }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Applicants Section -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center bg-success text-white">
            <v-icon left>mdi-account-multiple</v-icon>
            Applicants ({{ applications.length }})
          </v-card-title>

          <v-card-text class="pa-6">
            <v-progress-circular
              v-if="loadingApplications"
              indeterminate
              color="primary"
              class="d-block mx-auto"
            ></v-progress-circular>

            <v-alert v-else-if="applications.length === 0" type="info" variant="tonal">
              No applications yet for this job.
            </v-alert>

            <v-list v-else>
              <v-list-item
                v-for="app in applications"
                :key="app.id"
                class="mb-3 border rounded clickable-applicant"
                @click="viewApplicantDetails(app)"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" size="48">
                    {{ app.applicant_name.charAt(0) }}
                  </v-avatar>
                </template>

                <v-list-item-title class="text-h6">
                  {{ app.applicant_name }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-body-1">
                  <v-icon left size="small">mdi-email</v-icon>
                  {{ app.applicant_email }}
                </v-list-item-subtitle>
                <v-list-item-subtitle class="text-body-2">
                  <v-icon left size="small">mdi-file-document</v-icon>
                  {{ app.resume_filename }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <div class="d-flex flex-column align-end">
                    <v-chip
                      :color="getScoreColor(app.resume_score)"
                      size="large"
                      class="mb-2"
                    >
                      <v-icon left>mdi-star</v-icon>
                      Score: {{ app.resume_score }}/100
                    </v-chip>
                    <v-chip
                      :color="getStatusColor(app.status)"
                      size="small"
                    >
                      {{ app.status.toUpperCase() }}
                    </v-chip>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Applicant Details Dialog -->
    <v-dialog v-model="showApplicantDialog" max-width="900" persistent>
      <v-card v-if="selectedApplication">
        <v-card-title class="text-h5 bg-primary text-white">
          <v-icon left>mdi-account-details</v-icon>
          Applicant Details
        </v-card-title>

        <v-card-text class="pa-6">
          <v-row>
            <v-col cols="12" md="6">
              <div class="text-h6 mb-3">Applicant Information</div>
              <v-list dense>
                <v-list-item>
                  <v-list-item-title>Name</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedApplication.applicant_name }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedApplication.applicant_email }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Resume File</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedApplication.resume_filename }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Application Status</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip
                      :color="getStatusColor(selectedApplication.status)"
                      size="small"
                    >
                      {{ selectedApplication.status }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <div class="text-center">
                <v-progress-circular
                  :model-value="selectedApplication.resume_score"
                  :size="180"
                  :width="20"
                  :color="getScoreColor(selectedApplication.resume_score)"
                >
                  <div class="text-h3">{{ selectedApplication.resume_score }}</div>
                  <div class="text-body-1">Overall Score</div>
                </v-progress-circular>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="text-h6 mb-3">Resume Evaluation</div>
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Overall Score</span>
                  <strong>{{ selectedApplication.resume_score }}/100</strong>
                </div>
                <v-progress-linear
                  :model-value="selectedApplication.resume_score"
                  :color="getScoreColor(selectedApplication.resume_score)"
                  height="12"
                  rounded
                ></v-progress-linear>
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showApplicantDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import Ajax from '@/scripts/axios'

export default {
  name: 'JobDetail',
  data() {
    return {
      jobId: null,
      jobDetails: null,
      applications: [],
      loadingApplications: false,
      showApplicantDialog: false,
      selectedApplication: null
    }
  },
  computed: {
    ...mapState(['user'])
  },
     mounted() {
     this.jobId = this.$route.params.id
     if (this.jobId) {
       this.loadJobDetails()
     }
   },
   watch: {
     '$route'() {
       this.jobId = this.$route.params.id
       if (this.jobId) {
         this.loadJobDetails()
       }
     }
   },
  methods: {
    goBack() {
      this.$router.push('/recruiter/dashboard')
    },
    
    async loadJobDetails() {
      this.loadingApplications = true
      try {
        // Load job details
        const jobResponse = await Ajax(`jobs/${this.jobId}`, {}, 'GET')
        this.jobDetails = jobResponse
        
        // Load applications
        const appResponse = await Ajax(`jobs/${this.jobId}/applications`, {}, 'GET')
        this.applications = appResponse
        
        // Check if we need to open a specific applicant's details
        const applicantId = this.$route.query.applicant
        if (applicantId) {
          const application = this.applications.find(
            app => app.applicant_id === parseInt(applicantId)
          )
          if (application) {
            this.viewApplicantDetails(application)
          }
        }
      } catch (error) {
        console.error('Failed to load job details:', error)
      } finally {
        this.loadingApplications = false
      }
    },
    
    viewApplicantDetails(application) {
      this.selectedApplication = application
      this.showApplicantDialog = true
    },
    
    getSkillsList(skillsString) {
      if (!skillsString) return []
      return skillsString.split(',').map(s => s.trim()).filter(s => s)
    },
    
    getScoreColor(score) {
      if (score >= 80) return 'success'
      if (score >= 60) return 'info'
      if (score >= 40) return 'warning'
      return 'error'
    },
    
    getStatusColor(status) {
      const colors = {
        pending: 'warning',
        reviewed: 'info',
        accepted: 'success',
        rejected: 'error'
      }
      return colors[status] || 'grey'
    }
  }
}
</script>

<style scoped>
.border {
  border: 1px solid rgba(0, 0, 0, 0.12);
  padding: 16px;
  border-radius: 8px;
}

.clickable-applicant {
  cursor: pointer;
  transition: all 0.2s ease;
}

.clickable-applicant:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}
</style>
