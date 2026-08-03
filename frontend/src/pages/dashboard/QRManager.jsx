import { useEffect, useState } from 'react'
import { client, apiError, absoluteUrl } from '../../api/client'
import { Alert, Modal, PageLoader, Spinner } from '../../components/ui'

export default function QRManager() {
  const [qr, setQr] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [regenerating, setRegenerating] = useState(false)

  const load = () => {
    client
      .get('/api/v1/qr/me')
      .then((res) => setQr(res.data))
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }
  useEffect(load, [])

  const copyUrl = async () => {
    try {
      await navigator.clipboard.writeText(qr.public_url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (e) {
      /* clipboard unavailable */
    }
  }

  const regenerate = async () => {
    setRegenerating(true)
    try {
      const { data } = await client.post('/api/v1/users/me/regenerate-qr')
      setQr(data)
      setConfirmOpen(false)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setRegenerating(false)
    }
  }

  if (loading) return <PageLoader />
  if (!qr) {
    return (
      <div className="card text-center">
        <Alert type="error">{error}</Alert>
        <p className="text-slate-600">Please create your medical profile to get a QR code.</p>
      </div>
    )
  }

  const pngUrl = absoluteUrl(qr.png_url)
  const cardUrl = absoluteUrl(`/api/v1/qr/${qr.carecode}/card`)

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">My QR code</h1>
        <p className="text-sm text-slate-500">
          Print it, add it to your wallet card or ID, wear it on a bracelet, or attach it to a helmet or keychain.
        </p>
      </div>

      <div className="card flex flex-col items-center gap-6 sm:flex-row sm:items-start">
        <div className="rounded-2xl border-4 border-primary p-3">
          <img src={pngUrl} alt="CareCode QR" width={220} height={220} className="rounded-xl" />
        </div>
        <div className="w-full space-y-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Your public URL</p>
            <div className="mt-1 flex items-center gap-2">
              <code className="flex-1 truncate rounded-lg bg-slate-100 px-2 py-1.5 text-xs text-slate-700">
                {qr.public_url}
              </code>
              <button onClick={copyUrl} className="btn-outline !py-1 text-xs">
                {copied ? 'Copied ✓' : 'Copy'}
              </button>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <a href={pngUrl} download="carecode-qr.png" className="btn-primary justify-center">
              Download PNG
            </a>
            <a href={absoluteUrl(qr.svg_url)} download="carecode-qr.svg" className="btn-outline justify-center">
              Download SVG
            </a>
            <a href={cardUrl} target="_blank" rel="noreferrer" className="btn-outline justify-center">
              Print card
            </a>
            <button onClick={() => setConfirmOpen(true)} className="btn-danger justify-center">
              Regenerate QR
            </button>
          </div>
          <p className="text-xs text-slate-500">
            <strong>{qr.scan_count}</strong> scans so far. Anyone scanning the QR sees your emergency page —
            no login required.
          </p>
        </div>
      </div>

      <Modal
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        title="Regenerate QR code?"
        footer={
          <>
            <button className="btn-ghost" onClick={() => setConfirmOpen(false)}>
              Cancel
            </button>
            <button className="btn-danger" onClick={regenerate} disabled={regenerating}>
              {regenerating && <Spinner />} Regenerate
            </button>
          </>
        }
      >
        <Alert type="error">
          <strong>Warning:</strong> regenerating immediately invalidates your current QR code forever. Any
          printed cards or bracelets with the old code will no longer work. You'll need to print the new QR.
        </Alert>
      </Modal>
    </div>
  )
}
