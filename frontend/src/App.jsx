import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import { RequireAdmin, RequireAuth, RequireGuest } from './components/guards'
import Landing from './pages/Landing'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import ForgotPassword from './pages/auth/ForgotPassword'
import ResetPassword from './pages/auth/ResetPassword'
import Dashboard from './pages/dashboard/Dashboard'
import ProfileEditor from './pages/dashboard/ProfileEditor'
import QRManager from './pages/dashboard/QRManager'
import AccountSettings from './pages/dashboard/AccountSettings'
import EmergencyPage from './pages/public/EmergencyPage'
import Hospitals from './pages/hospitals/Hospitals'
import HospitalDetail from './pages/hospitals/HospitalDetail'
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminHospitals from './pages/admin/AdminHospitals'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Landing />} />
        <Route path="/login" element={<RequireGuest><Login /></RequireGuest>} />
        <Route path="/register" element={<RequireGuest><Register /></RequireGuest>} />
        <Route path="/forgot-password" element={<RequireGuest><ForgotPassword /></RequireGuest>} />
        <Route path="/reset-password" element={<RequireGuest><ResetPassword /></RequireGuest>} />
        <Route path="/hospitals" element={<Hospitals />} />
        <Route path="/hospitals/:id" element={<HospitalDetail />} />
        <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="/profile" element={<RequireAuth><ProfileEditor /></RequireAuth>} />
        <Route path="/qr" element={<RequireAuth><QRManager /></RequireAuth>} />
        <Route path="/settings" element={<RequireAuth><AccountSettings /></RequireAuth>} />
        <Route path="/admin" element={<RequireAdmin><AdminDashboard /></RequireAdmin>} />
        <Route path="/admin/hospitals" element={<RequireAdmin><AdminHospitals /></RequireAdmin>} />
        <Route path="*" element={<NotFound />} />
      </Route>
      <Route path="/e/:code" element={<EmergencyPage />} />
    </Routes>
  )
}
