import axios from 'axios'

// ─── Base instance ──────────────────────────────────────────────────────────
// All requests go to your Flask backend with cookies (session) included
const host = globalThis?.location?.hostname || '127.0.0.1'
const defaultBaseURL = `http://${host}:5000`

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || defaultBaseURL,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' }
})

const API_BASE = (api.defaults.baseURL || '').replace(/\/$/, '')


// ─────────────────────────────────────────
// DASHBOARD STATS
// GET /api/dashboard_data
// Returns: { status, stats, patient }
// ─────────────────────────────────────────
export async function getDashboardData() {
  const res = await api.get('/api/dashboard_data')
  return res.data
}


// ─────────────────────────────────────────
// APPOINTMENTS
// ─────────────────────────────────────────

// GET /api/appointments?tab=upcoming  OR  ?tab=past
// Returns: { status, tab, appointments: [...] }
export async function getAppointments(tab = 'upcoming') {
  const res = await api.get(`/api/appointments?tab=${tab}`)
  return res.data
}

// GET /api/appointments/:id
// Returns: { status, appointment: { id, date_full, time, status, doctor, doctor_id, specialty, department } }
export async function getAppointmentDetail(aptId) {
  const res = await api.get(`/api/appointments/${aptId}`)
  return res.data
}

// POST /api/appointments
// Body: { doctor_id, date, time_slot }
// Returns: { status, message }
export async function bookAppointment(doctorId, date, timeSlot) {
  const res = await api.post('/api/appointments', {
    doctor_id: doctorId,
    date,
    time_slot: timeSlot
  })
  return res.data
}

// POST /api/appointments/:id/cancel
// Returns: { status, message }
export async function cancelAppointment(aptId) {
  const res = await api.post(`/api/appointments/${aptId}/cancel`)
  return res.data
}

// PUT /api/appointments/:id/reschedule
// Body: { date, time_slot }
// Returns: { status, message }
export async function rescheduleAppointment(aptId, date, timeSlot) {
  const res = await api.put(`/api/appointments/${aptId}/reschedule`, {
    date,
    time_slot: timeSlot
  })
  return res.data
}


// ─────────────────────────────────────────
// DOCTORS
// ─────────────────────────────────────────

// GET /api/doctors?search=&specialization=&department_id=
// Returns: { status, doctors: [...] }
export async function getDoctors(params = {}) {
  const res = await api.get('/api/doctors', { params })
  return res.data
}

// GET /api/doctors/:id/slots?date=YYYY-MM-DD
// Returns: { status, slots, daily_count, daily_limit, daily_limit_reached }
export async function getDoctorSlots(doctorId, date) {
  const res = await api.get(`/api/doctors/${doctorId}/slots`, {
    params: { date }
  })
  return res.data
}


// ─────────────────────────────────────────
// MY DATA — DOWNLOADS
// These open directly in the browser as file downloads
// ─────────────────────────────────────────

// Opens /api/download_report → downloads .txt file
export function downloadReport() {
  window.open(`${API_BASE}/api/download_report`, '_blank')
}

export function downloadReportPdf() {
  window.open(`${API_BASE}/api/download_report_pdf`, '_blank')
}


// ─────────────────────────────────────────
// ─────────────────────────────────────────

// ─── Default export (optional — for direct axios use) ──────────────────────
export async function getPrescriptions() {
  const res = await api.get('/api/prescriptions')
  return res.data
}

export async function getPrescriptionDetail(prescriptionId) {
  const res = await api.get(`/api/prescriptions/${prescriptionId}`)
  return res.data
}
export default api



