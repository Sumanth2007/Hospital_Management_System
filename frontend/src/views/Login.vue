<template>
  <div style="display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif">
    <div style="border:1px solid #ccc;padding:2rem;border-radius:8px;width:300px">
      <h2>HMS Login</h2>
      <p v-if="error" style="color:red">{{ error }}</p>
      <div>
        <label>Email</label><br/>
        <input v-model="email" type="email" style="width:100%;padding:8px;margin:6px 0 12px;box-sizing:border-box" />
      </div>
      <div>
        <label>Password</label><br/>
        <input v-model="password" type="password" style="width:100%;padding:8px;margin:6px 0 12px;box-sizing:border-box" />
      </div>
      <button @click="login" style="width:100%;padding:10px;background:#4f46e5;color:white;border:none;border-radius:6px;cursor:pointer">
        Login
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'

const email    = ref('')
const password = ref('')
const error    = ref('')
const router   = useRouter()

async function login() {
  try {
    const res = await api.post('/api/login', {
      email:    email.value,
      password: password.value
    })
    if (res.data.status === 'success') {
         localStorage.setItem('isLoggedIn', 'true')
      router.push('/patient')
    } else {
      error.value = res.data.message || 'Login failed'
    }
  } catch (e) {
    error.value = 'Login failed. Check credentials.'
  }
}
</script>
