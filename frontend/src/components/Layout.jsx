import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navLinkClass = ({ isActive }) =>
  `rounded-lg px-3 py-2 text-sm font-medium transition ${
    isActive ? 'bg-primary-50 text-primary-700' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
  }`

export default function Layout() {
  const { user, isAdmin, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <Link to="/" className="flex items-center gap-2 text-lg font-extrabold text-primary">
            <span className="grid h-8 w-8 place-items-center rounded-lg bg-primary text-white">◉</span>
            CareCode
          </Link>

          {user && (
            <nav className="flex items-center gap-1">
              <NavLink to="/dashboard" className={navLinkClass}>
                Dashboard
              </NavLink>
              <NavLink to="/profile" className={navLinkClass}>
                Profile
              </NavLink>
              <NavLink to="/qr" className={navLinkClass}>
                My QR
              </NavLink>
              <NavLink to="/hospitals" className={navLinkClass}>
                Hospitals
              </NavLink>
              {isAdmin && (
                <NavLink to="/admin" className={navLinkClass}>
                  Admin
                </NavLink>
              )}
            </nav>
          )}

          <div className="flex items-center gap-3">
            {user ? (
              <>
                <Link
                  to="/settings"
                  className="hidden text-sm font-medium text-slate-600 hover:text-slate-900 sm:block"
                >
                  {user.full_name}
                </Link>
                <button onClick={handleLogout} className="btn-ghost">
                  Logout
                </button>
              </>
            ) : (
              <div className="flex gap-2">
                <Link to="/login" className="btn-ghost">
                  Log in
                </Link>
                <Link to="/register" className="btn-primary">
                  Sign up
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        <Outlet />
      </main>

      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-2 px-4 py-6 text-sm text-slate-500 sm:flex-row">
          <p className="font-semibold text-slate-700">
            CareCode <span className="font-normal">— Scan. Care. Save Lives.</span>
          </p>
          <p>Emergency medical identification · Built for a safer tomorrow</p>
        </div>
      </footer>
    </div>
  )
}
