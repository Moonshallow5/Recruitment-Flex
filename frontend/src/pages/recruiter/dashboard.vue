<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-account-tie</v-icon>
            <span>Recruiter Dashboard - {{ user?.name || 'Guest User' }}</span>
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

    <!-- Statistics Cards -->
    <v-row>
      <v-col cols="12" md="3">
        <v-card class="pa-4 text-center">
          <v-icon size="48" color="primary">mdi-briefcase</v-icon>
          <div class="text-h4 mt-2">{{ jobs.length }}</div>
          <div class="text-body-2 text-grey">Total Jobs Posted</div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="pa-4 text-center">
          <v-icon size="48" color="success">mdi-account-multiple</v-icon>
          <div class="text-h4 mt-2">{{ totalApplications }}</div>
          <div class="text-body-2 text-grey">Total Applications</div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="pa-4 text-center">
          <v-icon size="48" color="info">mdi-file-document-multiple</v-icon>
          <div class="text-h4 mt-2">{{ resumes.length }}</div>
          <div class="text-body-2 text-grey">Total Resumes</div>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="pa-4 text-center">
          <v-icon size="48" color="warning">mdi-chart-line</v-icon>
          <div class="text-h4 mt-2">{{ averageScore }}</div>
          <div class="text-body-2 text-grey">Average Score</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Job Management Section -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-briefcase-outline</v-icon>
            Job Management
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openCreateJobDialog">
              <v-icon left>mdi-plus</v-icon>
              Create New Job
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
              No jobs posted yet. Create your first job posting!
            </v-alert>

            <v-row v-else>
              <v-col
                v-for="job in jobs"
                :key="job.id"
                cols="12"
                md="6"
              >
                <v-card 
                  class="mb-3 clickable-job-card"
                  @click="goToJobDetails(job.id)"
                >
                  <v-card-title>
                    {{ job.job_title }}
                    <v-spacer></v-spacer>
                    <v-chip
                      :color="job.is_active ? 'success' : 'grey'"
                      size="small"
                    >
                      {{ job.is_active ? 'Active' : 'Inactive' }}
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
                      <div v-if="job.location">
                        <v-icon left size="small">mdi-map-marker</v-icon>
                        {{ job.location }}
                      </div>
                      <div v-if="job.salary_range">
                        <v-icon left size="small">mdi-cash</v-icon>
                        {{ job.salary_range }}
                      </div>
                      <div>
                        <v-icon left size="small">mdi-account-multiple</v-icon>
                        {{ job.applications_count }} Applications
                      </div>
                    </div>
                  </v-card-text>

                  <v-card-actions>
                    <v-btn
                      size="small"
                      variant="text"
                      @click.stop="deleteJob(job.id)"
                      color="error"
                    >
                      <v-icon left>mdi-delete</v-icon>
                      Delete
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-icon>mdi-chevron-right</v-icon>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Resume List -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon left color="primary">mdi-clipboard-list</v-icon>
            All Applicant Resumes
            <v-spacer></v-spacer>
            <v-btn icon size="small" @click="loadResumes">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="search"
                  prepend-inner-icon="mdi-magnify"
                  label="Search by name or filename"
                  variant="outlined"
                  density="compact"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="sortBy"
                  :items="sortOptions"
                  label="Sort By"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="filterScore"
                  :items="scoreFilters"
                  label="Filter by Score"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
            </v-row>

            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
              class="d-block mx-auto"
            ></v-progress-circular>

            <v-alert v-else-if="filteredResumes.length === 0" type="info" variant="tonal">
              No resumes found matching your criteria.
            </v-alert>

            <v-data-table
              v-else
              :headers="headers"
              :items="filteredResumes"
              :items-per-page="10"
              class="elevation-1"
            >
              <template v-slot:item.applicant_name="{ item }">
                <div class="d-flex align-center">
                  <v-icon left color="primary">mdi-account</v-icon>
                  <div>
                    <div class="font-weight-bold">{{ item.applicant_name }}</div>
                    <div class="text-caption text-grey">{{ item.applicant_email }}</div>
                  </div>
                </div>
              </template>

              <template v-slot:item.overall_score="{ item }">
                <v-chip
                  :color="getScoreColor(item.overall_score)"
                  text-color="white"
                  size="large"
                >
                  {{ item.overall_score }}/100
                </v-chip>
              </template>

              <template v-slot:item.breakdown="{ item }">
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small" class="mr-1">
                      F: {{ item.formatting_score }}
                    </v-chip>
                  </template>
                  <span>Formatting Score</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small" class="mr-1">
                      C: {{ item.content_score }}
                    </v-chip>
                  </template>
                  <span>Content Score</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small" class="mr-1">
                      K: {{ item.keyword_score }}
                    </v-chip>
                  </template>
                  <span>Keyword Score</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small" class="mr-1">
                      Ex: {{ item.experience_score }}
                    </v-chip>
                  </template>
                  <span>Experience Score</span>
                </v-tooltip>
                <v-tooltip location="top">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small">
                      Ed: {{ item.education_score }}
                    </v-chip>
                  </template>
                  <span>Education Score</span>
                </v-tooltip>
              </template>

              <template v-slot:item.uploaded_at="{ item }">
                {{ formatDate(item.uploaded_at) }}
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                  color="primary"
                  size="small"
                  variant="text"
                  @click="viewDetails(item)"
                >
                  <v-icon left>mdi-eye</v-icon>
                  View
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Resume Details Dialog -->
    <v-dialog v-model="showDetails" max-width="900">
      <v-card v-if="selectedResume">
        <v-card-title class="text-h5 bg-primary">
          <v-icon left>mdi-file-chart</v-icon>
          Resume Analysis Details
        </v-card-title>

        <v-card-text class="pa-6">
          <v-row>
            <v-col cols="12" md="6">
              <div class="text-h6 mb-2">Applicant Information</div>
              <v-list dense>
                <v-list-item>
                  <v-list-item-title>Name</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedResume.applicant_name }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedResume.applicant_email }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Resume File</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedResume.filename }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Upload Date</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(selectedResume.uploaded_at) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" md="6">
              <div class="text-center">
                <v-progress-circular
                  :model-value="selectedResume.overall_score"
                  :size="180"
                  :width="20"
                  :color="getScoreColor(selectedResume.overall_score)"
                >
                  <div class="text-h3">{{ selectedResume.overall_score }}</div>
                  <div class="text-body-1">Overall Score</div>
                </v-progress-circular>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="text-h6 mb-3">Score Breakdown</div>
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Formatting</span>
                  <strong>{{ selectedResume.formatting_score }}/20</strong>
                </div>
                <v-progress-linear
                  :model-value="(selectedResume.formatting_score / 20) * 100"
                  color="primary"
                  height="8"
                ></v-progress-linear>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Content</span>
                  <strong>{{ selectedResume.content_score }}/20</strong>
                </div>
                <v-progress-linear
                  :model-value="(selectedResume.content_score / 20) * 100"
                  color="primary"
                  height="8"
                ></v-progress-linear>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Keywords</span>
                  <strong>{{ selectedResume.keyword_score }}/20</strong>
                </div>
                <v-progress-linear
                  :model-value="(selectedResume.keyword_score / 20) * 100"
                  color="primary"
                  height="8"
                ></v-progress-linear>
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Experience</span>
                  <strong>{{ selectedResume.experience_score }}/20</strong>
                </div>
                <v-progress-linear
                  :model-value="(selectedResume.experience_score / 20) * 100"
                  color="primary"
                  height="8"
                ></v-progress-linear>
              </div>

              <div class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span>Education</span>
                  <strong>{{ selectedResume.education_score }}/20</strong>
                </div>
                <v-progress-linear
                  :model-value="(selectedResume.education_score / 20) * 100"
                  color="primary"
                  height="8"
                ></v-progress-linear>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="text-h6 mb-2">Detailed Feedback</div>
          <v-alert type="info" variant="tonal">
            <pre class="text-body-2" style="white-space: pre-wrap; font-family: inherit;">{{ selectedResume.feedback }}</pre>
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-btn 
            v-if="selectedResume.job_id"
            color="success"
            variant="elevated"
            @click="viewJobDetailsFromResume(selectedResume.job_id)"
          >
            <v-icon left>mdi-briefcase</v-icon>
            View Job Details
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showDetails = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Create Job Dialog -->
    <v-dialog v-model="showCreateJobDialog" max-width="800" persistent>
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white">
          <v-icon left>mdi-briefcase-plus</v-icon>
          Create New Job Posting
        </v-card-title>

        <v-card-text class="pa-6">
          <v-form ref="jobForm" v-model="jobFormValid">
            <v-text-field
              v-model="newJob.job_title"
              label="Job Title *"
              required
              :rules="[v => !!v || 'Job title is required']"
              variant="outlined"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="newJob.company_name"
              label="Company Name *"
              required
              :rules="[v => !!v || 'Company name is required']"
              variant="outlined"
              class="mb-3"
            ></v-text-field>

            <v-textarea
              v-model="newJob.job_description"
              label="Job Description *"
              required
              :rules="[v => !!v || 'Job description is required']"
              variant="outlined"
              rows="6"
              class="mb-3"
            ></v-textarea>

            <v-text-field
              v-model="newJob.skills"
              label="Required Skills (comma-separated) *"
              required
              :rules="[v => !!v || 'Skills are required']"
              hint="e.g., Python, React, SQL, AWS"
              variant="outlined"
              class="mb-3"
            ></v-text-field>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="newJob.location"
                  label="Location"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="newJob.salary_range"
                  label="Salary Range"
                  variant="outlined"
                  hint="e.g., $80k - $120k"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="newJob.employment_type"
                  :items="employmentTypes"
                  label="Employment Type"
                  variant="outlined"
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="newJob.experience_level"
                  :items="experienceLevels"
                  label="Experience Level"
                  variant="outlined"
                ></v-select>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeCreateJobDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!jobFormValid"
            :loading="creatingJob"
            @click="createJob"
          >
            Create Job
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import Ajax from '@/scripts/axios'
import { useToast } from 'vue-toast-notification'

export default {
  setup() {
    const toast = useToast()
    return { toast }
  },
  name: 'RecruiterDashboard',
  data() {
    return {
      loading: false,
      resumes: [],
      selectedResume: null,
      showDetails: false,
      search: '',
      sortBy: 'score_desc',
      filterScore: 'all',
      sortOptions: [
        { title: 'Score (High to Low)', value: 'score_desc' },
        { title: 'Score (Low to High)', value: 'score_asc' },
        { title: 'Date (Newest)', value: 'date_desc' },
        { title: 'Date (Oldest)', value: 'date_asc' },
        { title: 'Name (A-Z)', value: 'name_asc' },
      ],
      scoreFilters: [
        { title: 'All Scores', value: 'all' },
        { title: 'Excellent (80+)', value: '80' },
        { title: 'Good (60-79)', value: '60' },
        { title: 'Fair (40-59)', value: '40' },
        { title: 'Needs Work (<40)', value: '0' },
      ],
      headers: [
        { title: 'Applicant', value: 'applicant_name', sortable: true },
        { title: 'Resume', value: 'filename', sortable: true },
        { title: 'Overall Score', value: 'overall_score', sortable: true, align: 'center' },
        { title: 'Score Breakdown', value: 'breakdown', sortable: false },
        { title: 'Upload Date', value: 'uploaded_at', sortable: true },
        { title: 'Actions', value: 'actions', sortable: false, align: 'center' },
      ],
      // Job-related data
      jobs: [],
      loadingJobs: false,
      showCreateJobDialog: false,
      creatingJob: false,
      jobFormValid: false,
      newJob: {
        job_title: '',
        company_name: '',
        job_description: '',
        skills: '',
        location: '',
        salary_range: '',
        employment_type: '',
        experience_level: ''
      },
      employmentTypes: ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'],
      experienceLevels: ['Entry', 'Mid', 'Senior', 'Executive']
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['currentUser', 'isAuthenticated']),
    
    filteredResumes() {
      let filtered = [...this.resumes]

      // Apply search filter
      if (this.search) {
        const searchLower = this.search.toLowerCase()
        filtered = filtered.filter(r => 
          r.applicant_name.toLowerCase().includes(searchLower) ||
          r.filename.toLowerCase().includes(searchLower) ||
          r.applicant_email.toLowerCase().includes(searchLower)
        )
      }

      // Apply score filter
      if (this.filterScore !== 'all') {
        const minScore = parseInt(this.filterScore)
        if (minScore === 80) {
          filtered = filtered.filter(r => r.overall_score >= 80)
        } else if (minScore === 60) {
          filtered = filtered.filter(r => r.overall_score >= 60 && r.overall_score < 80)
        } else if (minScore === 40) {
          filtered = filtered.filter(r => r.overall_score >= 40 && r.overall_score < 60)
        } else if (minScore === 0) {
          filtered = filtered.filter(r => r.overall_score < 40)
        }
      }

      // Apply sorting
      if (this.sortBy === 'score_desc') {
        filtered.sort((a, b) => b.overall_score - a.overall_score)
      } else if (this.sortBy === 'score_asc') {
        filtered.sort((a, b) => a.overall_score - b.overall_score)
      } else if (this.sortBy === 'date_desc') {
        filtered.sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at))
      } else if (this.sortBy === 'date_asc') {
        filtered.sort((a, b) => new Date(a.uploaded_at) - new Date(b.uploaded_at))
      } else if (this.sortBy === 'name_asc') {
        filtered.sort((a, b) => a.applicant_name.localeCompare(b.applicant_name))
      }

      return filtered
    },
    
    excellentCount() {
      return this.resumes.filter(r => r.overall_score >= 80).length
    },
    
    goodCount() {
      return this.resumes.filter(r => r.overall_score >= 60 && r.overall_score < 80).length
    },
    
    averageScore() {
      if (this.resumes.length === 0) return 0
      const sum = this.resumes.reduce((acc, r) => acc + r.overall_score, 0)
      return Math.round(sum / this.resumes.length)
    },
    
    totalApplications() {
      return this.jobs.reduce((sum, job) => sum + (job.applications_count || 0), 0)
    }
  },
  mounted() {
    this.loadResumes()
    this.loadJobs()
  },
  methods: {
    ...mapActions(['logout']),
    
    async loadResumes() {
      this.loading = true
      try {
        const response = await Ajax('resumes/all', {}, 'GET')
        this.resumes = response
      } catch (error) {
        console.error('Failed to load resumes:', error)
      } finally {
        this.loading = false
      }
    },
    
    viewDetails(resume) {
      this.selectedResume = resume
      this.showDetails = true
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
    
    // Job management methods
    async loadJobs() {
      this.loadingJobs = true
      try {
        const response = await Ajax('jobs/my-jobs', {}, 'GET')
        this.jobs = response
      } catch (error) {
        console.error('Failed to load jobs:', error)
      } finally {
        this.loadingJobs = false
      }
    },
    
    openCreateJobDialog() {
      this.showCreateJobDialog = true
    },
    
    closeCreateJobDialog() {
      this.showCreateJobDialog = false
      this.newJob = {
        job_title: '',
        company_name: '',
        job_description: '',
        skills: '',
        location: '',
        salary_range: '',
        employment_type: '',
        experience_level: ''
      }
    },
    
    async createJob() {
      this.creatingJob = true
      try {
        await Ajax('jobs', this.newJob, 'POST')
        this.toast.success('Job created successfully!', {
          duration: 3000,
          position: 'top-right'
        })
        this.closeCreateJobDialog()
        await this.loadJobs()
      } catch (error) {
        console.error('Failed to create job:', error)
        this.toast.error('Failed to create job', {
          duration: 3000,
          position: 'top-right'
        })
      } finally {
        this.creatingJob = false
      }
    },
    
    async deleteJob(jobId) {
      if (confirm('Are you sure you want to delete this job?')) {
        try {
          await Ajax(`jobs/${jobId}`, {}, 'DELETE')
          this.toast.success('Job deleted successfully!', {
            duration: 3000,
            position: 'top-right'
          })
          await this.loadJobs()
        } catch (error) {
          console.error('Failed to delete job:', error)
          this.toast.error('Failed to delete job', {
            duration: 3000,
            position: 'top-right'
          })
        }
      }
    },
    
    goToJobDetails(jobId) {
      this.$router.push(`/recruiter/job-detail/${jobId}`)
    },
    
    viewJobDetailsFromResume(jobId) {
      this.showDetails = false
      // Pass the applicant_id as a query parameter to open their details
      this.$router.push({
        path: `/recruiter/job-detail/${jobId}`,
        query: { applicant: this.selectedResume.applicant_id }
      })
    },
    
    getSkillsList(skillsString) {
      if (!skillsString) return []
      return skillsString.split(',').map(s => s.trim()).filter(s => s)
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
.v-data-table {
  background: transparent;
}

.clickable-job-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.clickable-job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
}
</style>

