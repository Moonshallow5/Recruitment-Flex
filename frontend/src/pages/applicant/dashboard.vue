<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-account-circle</v-icon>
            <span>Welcome, {{ user?.name || 'Guest User' }}!</span>
            <v-spacer></v-spacer>
            <v-chip v-if="!isAuthenticated" color="warning" class="mr-2">
              <v-icon left size="small">mdi-alert</v-icon>
              Dev Mode - Not Authenticated
            </v-chip>
            <v-btn color="error" variant="text" @click="handleLogout">
              <v-icon left>mdi-logout</v-icon>
              Logout
            </v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Upload Resume Section -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-4">
            <v-icon left color="primary">mdi-file-upload</v-icon>
            Upload Your Resume
          </v-card-title>
          
          <v-card-text>
            <v-file-input
              v-model="selectedFile"
              label="Select Resume"
              prepend-icon="mdi-file-document"
              accept=".pdf,.doc,.docx"
              show-size
              :loading="uploading"
              :disabled="uploading"
              @change="handleFileChange"
            ></v-file-input>

            <v-alert
              v-if="uploadMessage"
              :type="uploadMessageType"
              class="mt-3"
              closable
              @click:close="uploadMessage = ''"
            >
              {{ uploadMessage }}
            </v-alert>

            <v-progress-linear
              v-if="uploading"
              v-model="uploadProgress"
              color="primary"
              height="25"
              class="mt-3"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.ceil(value) }}%</strong>
              </template>
            </v-progress-linear>

            <v-btn
              color="primary"
              size="large"
              block
              class="mt-4"
              :loading="uploading"
              :disabled="!selectedFile || uploading"
              @click="uploadResume"
            >
              <v-icon left>mdi-upload</v-icon>
              Upload Resume
            </v-btn>

            <v-alert type="info" variant="tonal" class="mt-4">
              <div class="text-body-2">
                <strong>Accepted formats:</strong> PDF, DOC, DOCX<br>
                <strong>Max size:</strong> 10MB<br><br>
                Your resume will be automatically graded on:
                <ul class="mt-2">
                  <li>Formatting & Structure</li>
                  <li>Content Quality</li>
                  <li>Relevant Keywords</li>
                  <li>Experience Documentation</li>
                  <li>Education Background</li>
                </ul>
              </div>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- My Resumes Section -->
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-4 d-flex align-center">
            <v-icon left color="primary">mdi-file-document-multiple</v-icon>
            My Resumes
            <v-spacer></v-spacer>
            <v-btn icon size="small" @click="loadResumes">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
              class="d-block mx-auto"
            ></v-progress-circular>

            <v-alert v-else-if="resumes.length === 0" type="info" variant="tonal">
              No resumes uploaded yet. Upload your first resume to get started!
            </v-alert>

            <v-list v-else>
              <v-list-item
                v-for="resume in resumes"
                :key="resume.id"
                class="mb-2 border rounded"
                @click="selectedResume = resume"
              >
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-file-document</v-icon>
                </template>

                <v-list-item-title>{{ resume.filename }}</v-list-item-title>
                <v-list-item-subtitle>
                  Uploaded: {{ formatDate(resume.uploaded_at) }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-chip
                    :color="getScoreColor(resume.overall_score)"
                    text-color="white"
                  >
                    {{ resume.overall_score }}/100
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Available Jobs Section -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-4">
            <v-icon left color="primary">mdi-briefcase</v-icon>
            Available Jobs
            <v-spacer></v-spacer>
            <v-btn icon size="small" @click="loadJobs">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-progress-circular
              v-if="loadingJobs"
              indeterminate
              color="primary"
              class="d-block mx-auto"
            ></v-progress-circular>

            <v-alert v-else-if="jobs.length === 0" type="info" variant="tonal">
              No jobs available at the moment. Check back later!
            </v-alert>

            <v-row v-else>
              <v-col
                v-for="job in jobs"
                :key="job.id"
                cols="12"
                md="6"
                lg="4"
              >
                <v-card class="job-card" :class="{ 'applied-job': hasAppliedToJob(job.id) }" hover @click="openJobDialog(job)">
                  <v-card-title class="text-h6">
                    {{ job.job_title }}
                    <v-spacer></v-spacer>
                    <v-chip v-if="hasAppliedToJob(job.id)" color="success" size="small">
                      <v-icon left size="small">mdi-check</v-icon>
                      Applied
                    </v-chip>
                  </v-card-title>

                  <v-card-subtitle>
                    <v-icon left size="small">mdi-office-building</v-icon>
                    {{ job.company_name }}
                  </v-card-subtitle>

                  <v-card-text>
                    <div class="mb-2">
                      <v-chip
                        v-for="skill in getSkillsList(job.skills)"
                        :key="skill"
                        size="small"
                        color="primary"
                        variant="outlined"
                        class="mr-1 mb-1"
                      >
                        {{ skill }}
                      </v-chip>
                    </div>

                    <div class="text-body-2">
                      <div v-if="job.location" class="mb-1">
                        <v-icon left size="small">mdi-map-marker</v-icon>
                        {{ job.location }}
                      </div>
                      <div v-if="job.salary_range" class="mb-1">
                        <v-icon left size="small">mdi-cash</v-icon>
                        {{ job.salary_range }}
                      </div>
                      <div v-if="job.employment_type">
                        <v-icon left size="small">mdi-clock</v-icon>
                        {{ job.employment_type }}
                      </div>
                    </div>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" variant="text">
                      View Details
                      <v-icon right>mdi-arrow-right</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Resume Details Dialog -->
    <v-dialog v-model="showDetails" max-width="800">
      <v-card v-if="selectedResume">
        <v-card-title class="text-h5 bg-primary">
          <v-icon left>mdi-file-chart</v-icon>
          Resume Score Details
        </v-card-title>

        <v-card-text class="pa-6">
          <div class="text-h6 mb-4">{{ selectedResume.filename }}</div>
          
          <v-row>
            <v-col cols="12" md="6">
              <div class="text-center mb-4">
                <v-progress-circular
                  :model-value="selectedResume.overall_score"
                  :size="150"
                  :width="15"
                  :color="getScoreColor(selectedResume.overall_score)"
                >
                  <div class="text-h4">{{ selectedResume.overall_score }}</div>
                  <div class="text-caption">Overall Score</div>
                </v-progress-circular>
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <v-list dense>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-format-align-left</v-icon>
                  </template>
                  <v-list-item-title>Formatting</v-list-item-title>
                  <template v-slot:append>
                    <strong>{{ selectedResume.formatting_score }}/20</strong>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-text-box</v-icon>
                  </template>
                  <v-list-item-title>Content</v-list-item-title>
                  <template v-slot:append>
                    <strong>{{ selectedResume.content_score }}/20</strong>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-key</v-icon>
                  </template>
                  <v-list-item-title>Keywords</v-list-item-title>
                  <template v-slot:append>
                    <strong>{{ selectedResume.keyword_score }}/20</strong>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-briefcase</v-icon>
                  </template>
                  <v-list-item-title>Experience</v-list-item-title>
                  <template v-slot:append>
                    <strong>{{ selectedResume.experience_score }}/20</strong>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-school</v-icon>
                  </template>
                  <v-list-item-title>Education</v-list-item-title>
                  <template v-slot:append>
                    <strong>{{ selectedResume.education_score }}/20</strong>
                  </template>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="text-h6 mb-2">Feedback:</div>
          <v-alert type="info" variant="tonal">
            <pre class="text-body-2" style="white-space: pre-wrap; font-family: inherit;">{{ selectedResume.feedback }}</pre>
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showDetails = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Job Details Dialog -->
    <v-dialog v-model="showJobDialog" max-width="800">
      <v-card v-if="selectedJob">
        <v-card-title class="text-h5 bg-primary text-white">
          <v-icon left>mdi-briefcase-outline</v-icon>
          Job Details
        </v-card-title>

        <v-card-text class="pa-6">
          <div class="text-h5 mb-2">{{ selectedJob.job_title }}</div>
          <div class="text-h6 mb-4 text-grey">
            <v-icon left size="small">mdi-office-building</v-icon>
            {{ selectedJob.company_name }}
          </div>

          <v-divider class="my-4"></v-divider>

          <div class="mb-3">
            <strong>Skills Required:</strong>
            <v-chip
              v-for="skill in getSkillsList(selectedJob.skills)"
              :key="skill"
              size="small"
              color="primary"
              class="ml-1"
            >
              {{ skill }}
            </v-chip>
          </div>

          <v-row class="mt-3">
            <v-col v-if="selectedJob.location" cols="12" sm="6">
              <strong>Location:</strong> {{ selectedJob.location }}
            </v-col>
            <v-col v-if="selectedJob.salary_range" cols="12" sm="6">
              <strong>Salary:</strong> {{ selectedJob.salary_range }}
            </v-col>
            <v-col v-if="selectedJob.employment_type" cols="12" sm="6">
              <strong>Type:</strong> {{ selectedJob.employment_type }}
            </v-col>
            <v-col v-if="selectedJob.experience_level" cols="12" sm="6">
              <strong>Experience:</strong> {{ selectedJob.experience_level }}
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="mb-2">
            <strong>Job Description:</strong>
          </div>
          <div class="text-body-1" style="white-space: pre-wrap;">
            {{ selectedJob.job_description }}
          </div>

          <v-divider class="my-4"></v-divider>

          <!-- Application Status -->
          <v-alert
            v-if="hasAppliedToJob(selectedJob.id)"
            type="success"
            variant="tonal"
            class="mb-3"
          >
            <v-icon left>mdi-check-circle</v-icon>
            You have already applied to this job!
            <div class="text-caption mt-2">
              Resume: {{ getResumeFilenameForJob(selectedJob.id) }}
            </div>
          </v-alert>

          <div v-else class="text-h6 mb-3">Upload Your Resume for This Job</div>
          
          <v-file-input
            v-model="selectedFileForApplication"
            label="Select Resume to Upload"
            prepend-icon="mdi-file-document"
            accept=".pdf,.doc,.docx"
            show-size
            variant="outlined"
            class="mb-3"
            :disabled="hasAppliedToJob(selectedJob.id)"
          ></v-file-input>

          <v-progress-linear
            v-if="uploadingForApplication"
            indeterminate
            color="primary"
            class="mb-3"
          ></v-progress-linear>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeJobDialog">Close</v-btn>
          <v-btn
            v-if="!hasAppliedToJob(selectedJob.id)"
            color="primary"
            :disabled="!selectedFileForApplication || uploadingForApplication"
            :loading="uploadingForApplication"
            @click="uploadAndApply"
          >
            Upload & Apply
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import Ajax from '@/scripts/axios'
import AjaxUpload from '@/scripts/axiosUpload'
import { useToast } from 'vue-toast-notification'

export default {
  name: 'ApplicantDashboard',
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadProgress: 0,
      uploadMessage: '',
      uploadMessageType: 'success',
      loading: false,
      resumes: [],
      selectedResume: null,
      showDetails: false,
      // Job-related data
      jobs: [],
      loadingJobs: false,
      selectedJob: null,
      showJobDialog: false,
      selectedFileForApplication: null,
      uploadingForApplication: false,
      myApplications: []
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['currentUser', 'isAuthenticated'])
  },
  watch: {
    selectedResume(val) {
      if (val) {
        this.showDetails = true
      }
    },
    showDetails(val) {
      if (!val) {
        // Clear selectedResume when dialog closes
        this.selectedResume = null
      }
    }
  },
  mounted() {
    this.loadResumes()
    this.loadJobs()
    this.loadApplications()
  },
  methods: {
    ...mapActions(['logout']),
    
    async loadResumes() {
      this.loading = true
      try {
        const response = await Ajax('resumes/my-resumes', {}, 'GET')
        this.resumes = response
      } catch (error) {
        console.error('Failed to load resumes:', error)
        this.uploadMessage = 'Failed to load resumes'
        this.uploadMessageType = 'error'
      } finally {
        this.loading = false
      }
    },
    
    handleFileChange(event) {
      this.uploadMessage = ''
    },
    
    async uploadResume() {
      if (!this.selectedFile) return

      const $toast = useToast()
      this.uploading = true
      this.uploadProgress = 0
      this.uploadMessage = ''

      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        
        const response = await AjaxUpload(
          'resumes/upload',
          formData,
          (progressEvent) => {
            this.uploadProgress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            )
          }
        )

        $toast.success('Resume uploaded and graded successfully!', {
          duration: 3000,
          position: 'top-right'
        })
        
        this.selectedFile = null
        
        // Reload resumes list
        await this.loadResumes()
      } catch (error) {
        console.error('Upload failed:', error)
      } finally {
        this.uploading = false
        this.uploadProgress = 0
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },
    
    getScoreColor(score) {
      if (score >= 80) return 'success'
      if (score >= 60) return 'info'
      if (score >= 40) return 'warning'
      return 'error'
    },
    
    handleLogout() {
      this.logout()
      this.$router.push('/authentication/login')
    },
    
    // Job-related methods
    async loadJobs() {
      this.loadingJobs = true
      try {
        const response = await Ajax('jobs', {}, 'GET')
        this.jobs = response
      } catch (error) {
        console.error('Failed to load jobs:', error)
      } finally {
        this.loadingJobs = false
      }
    },
    
    async loadApplications() {
      try {
        const response = await Ajax('applications/my-applications', {}, 'GET')
        this.myApplications = response
      } catch (error) {
        console.error('Failed to load applications:', error)
      }
    },
    
    hasAppliedToJob(jobId) {
      return this.myApplications.some(app => app.job_id === jobId)
    },
    
    getApplicationForJob(jobId) {
      console.log(this.myApplications)
      return this.myApplications.find(app => app.job_id === jobId)
    },
    
    getResumeFilenameForJob(jobId) {
      const application = this.getApplicationForJob(jobId)
      if (application && application.resume && application.resume.filename) {
        return application.resume.filename
      }
      return 'N/A'
    },
    
    openJobDialog(job) {
      this.selectedJob = job
      this.selectedFileForApplication = null
      this.showJobDialog = true
    },
    
    closeJobDialog() {
      this.showJobDialog = false
      this.selectedJob = null
      this.selectedFileForApplication = null
    },
    
    async uploadAndApply() {
      if (!this.selectedJob || !this.selectedFileForApplication) return

      const $toast = useToast()
      this.uploadingForApplication = true
      
      try {
        // First upload the resume
        const formData = new FormData()
        formData.append('file', this.selectedFileForApplication)
        
        const response = await AjaxUpload(
          'resumes/upload',
          formData
        )
        
        // Then apply with the uploaded resume ID
        await Ajax('applications', {
          job_id: this.selectedJob.id,
          resume_id: response.id
        }, 'POST')
        
        $toast.success('Successfully applied to job!', {
          duration: 3000,
          position: 'top-right'
        })
        
        this.closeJobDialog()
        await this.loadResumes()
        await this.loadApplications()
      } catch (error) {
        console.error('Failed to apply:', error)
        const message = error.response?.data?.detail || 'Failed to apply to job'
        $toast.error(message, {
          duration: 3000,
          position: 'top-right'
        })
      } finally {
        this.uploadingForApplication = false
      }
    },
    
    getSkillsList(skillsString) {
      if (!skillsString) return []
      return skillsString.split(',').map(s => s.trim()).filter(s => s)
    }
  }
}
</script>

<style scoped>
.border {
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.job-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

/* .applied-job {
  border: 2px solid #4caf50 !important;
  background-color: #f1f8e9;
} */
</style>

