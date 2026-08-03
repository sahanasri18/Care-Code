import { Link } from 'react-router-dom'

const FEATURES = [
  {
    title: 'Scan. Care. Save Lives.',
    text: 'In an emergency every second counts. Your QR code gives responders the critical information they need — instantly.',
  },
  {
    title: 'Your medical profile, ready in a heartbeat',
    text: 'Blood group, allergies, medications, conditions, emergency contacts and more — accessible from any smartphone, no app or login required.',
  },
  {
    title: 'Secure and private',
    text: 'Your data is protected with bank-grade encryption practices, and you stay in full control — including permanent deletion.',
  },
  {
    title: 'Take it anywhere',
    text: 'Download, print or wear your QR. Add it to a wallet card, ID, bracelet, helmet or keychain.',
  },
]

const STEPS = [
  { n: '01', t: 'Create an account', d: 'Register in under a minute with just your email.' },
  { n: '02', t: 'Build your medical profile', d: 'Enter your essential emergency information.' },
  { n: '03', t: 'Get your QR code', d: 'Download it as PNG or SVG, or print a ready-made card.' },
  { n: '04', t: 'Be ready for anything', d: 'Responders scan and instantly know how to help you.' },
]

export default function Landing() {
  return (
    <div className="space-y-16">
      <section className="rounded-3xl bg-gradient-to-br from-primary to-primary-800 px-6 py-16 text-center text-white sm:py-24">
        <h1 className="mx-auto max-w-2xl text-4xl font-extrabold leading-tight sm:text-5xl">
          Scan. Care. Save Lives.
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-base text-blue-100 sm:text-lg">
          CareCode turns your essential medical information into a scannable QR code that speaks for you when
          you can't.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link to="/register" className="rounded-xl bg-white px-6 py-3 font-bold text-primary hover:bg-blue-50">
            Create your CareCode
          </Link>
          <Link to="/hospitals" className="rounded-xl border border-white/40 px-6 py-3 font-semibold text-white hover:bg-white/10">
            Find a hospital
          </Link>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2">
        {FEATURES.map((f) => (
          <div key={f.title} className="card">
            <h2 className="font-bold text-slate-900">{f.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-slate-600">{f.text}</p>
          </div>
        ))}
      </section>

      <section>
        <h2 className="text-center text-2xl font-extrabold text-slate-900">How it works</h2>
        <div className="mt-8 grid gap-4 sm:grid-cols-4">
          {STEPS.map((s) => (
            <div key={s.n} className="card">
              <p className="text-3xl font-extrabold text-primary/30">{s.n}</p>
              <h3 className="mt-2 font-bold text-slate-900">{s.t}</h3>
              <p className="mt-1 text-sm text-slate-600">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-3xl bg-slate-900 px-6 py-12 text-center">
        <h2 className="text-2xl font-extrabold text-white">Be ready for the unexpected</h2>
        <p className="mx-auto mt-3 max-w-md text-sm text-slate-400">
          Your medical information, in the hands of the people who need it — exactly when they need it.
        </p>
        <Link to="/register" className="btn-primary mt-6">
          Get started free
        </Link>
      </section>
    </div>
  )
}
