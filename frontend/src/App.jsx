import { useEffect, useMemo, useState } from 'react'

const API_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

function request(path, token, options = {}) {
  return fetch(`${API_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  })
}

function AuthScreen({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  async function submit(event) {
    event.preventDefault(); setLoading(true); setMessage('')
    try {
      const response = await request(`/api/auth/${mode}`, null, { method: 'POST', body: JSON.stringify({ email, password }) })
      const data = await response.json()
      if (!response.ok) return setMessage(data.detail || 'Unable to continue.')
      if (mode === 'login') onLogin(data.access_token)
      else { setMode('login'); setMessage('Account created. You can now sign in.') }
    } catch { setMessage('Cannot reach the API. Start the FastAPI server and try again.') }
    finally { setLoading(false) }
  }
  return <main className="min-h-screen bg-slate-950 px-5 py-10 text-white"><div className="mx-auto grid max-w-5xl overflow-hidden rounded-3xl bg-white shadow-2xl md:grid-cols-2"><section className="bg-gradient-to-br from-blue-600 to-indigo-800 p-10 md:p-14"><p className="text-sm font-semibold tracking-[0.25em] text-blue-200">DRIVEFLOW</p><h1 className="mt-16 text-4xl font-bold leading-tight">Dealer inventory, beautifully managed.</h1><p className="mt-5 max-w-sm text-blue-100">Search live inventory, purchase available vehicles, and manage stock with confidence.</p></section><section className="p-8 text-slate-900 md:p-14"><h2 className="text-2xl font-bold">{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2><p className="mt-2 text-slate-500">{mode === 'login' ? 'Sign in to explore the inventory.' : 'Registration creates a standard customer account.'}</p><form onSubmit={submit} className="mt-8 space-y-4"><input value={email} onChange={e => setEmail(e.target.value)} type="email" placeholder="Email address" required className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500"/><input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password (8+ characters)" minLength="8" required className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500"/><button disabled={loading} className="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:opacity-60">{loading ? 'Please wait...' : mode === 'login' ? 'Sign in' : 'Create account'}</button></form>{message && <p className="mt-4 text-sm text-slate-600">{message}</p>}<button onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setMessage('') }} className="mt-6 text-sm font-semibold text-blue-600">{mode === 'login' ? 'New here? Create an account' : 'Already have an account? Sign in'}</button></section></div></main>
}

function Dashboard({ token, onLogout }) {
  const [vehicles, setVehicles] = useState([]); const [query, setQuery] = useState(''); const [message, setMessage] = useState(''); const [loading, setLoading] = useState(true); const [newVehicle, setNewVehicle] = useState({ make: '', model: '', category: '', price: '', quantity: '' })
  const isAdmin = (() => { try { return JSON.parse(atob(token.split('.')[1])).role === 'admin' } catch { return false } })()
  async function load() { setLoading(true); const response = await request('/api/vehicles', token); const data = await response.json(); setLoading(false); if (response.ok) setVehicles(data); else { setMessage(data.detail || 'Your session expired.'); if (response.status === 401) onLogout() } }
  useEffect(() => { load() }, [])
  const visible = useMemo(() => vehicles.filter(v => `${v.make} ${v.model} ${v.category}`.toLowerCase().includes(query.toLowerCase())), [vehicles, query])
  async function purchase(vehicle) { const response = await request(`/api/vehicles/${vehicle.id}/purchase`, token, { method: 'POST' }); const data = await response.json(); if (response.ok) setVehicles(items => items.map(v => v.id === data.id ? data : v)); else setMessage(data.detail || 'Purchase could not be completed.') }
  async function addVehicle(event) { event.preventDefault(); const response = await request('/api/vehicles', token, { method: 'POST', body: JSON.stringify({ ...newVehicle, price: Number(newVehicle.price), quantity: Number(newVehicle.quantity) }) }); const data = await response.json(); if (response.ok) { setVehicles(items => [...items, data]); setNewVehicle({ make: '', model: '', category: '', price: '', quantity: '' }) } else setMessage(data.detail || 'Could not add vehicle.') }
  async function removeVehicle(id) { if (!window.confirm('Delete this vehicle?')) return; const response = await request(`/api/vehicles/${id}`, token, { method: 'DELETE' }); if (response.ok) setVehicles(items => items.filter(v => v.id !== id)); else { const data = await response.json(); setMessage(data.detail || 'Could not delete vehicle.') } }
  async function restockVehicle(vehicle) { const amount = window.prompt('Units to add:', '1'); if (!amount) return; const response = await request(`/api/vehicles/${vehicle.id}/restock`, token, { method: 'POST', body: JSON.stringify({ amount: Number(amount) }) }); const data = await response.json(); if (response.ok) setVehicles(items => items.map(v => v.id === data.id ? data : v)); else setMessage(data.detail || 'Could not restock vehicle.') }
  return <main className="min-h-screen bg-slate-50 text-slate-900"><header className="border-b bg-white"><div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5"><div><p className="text-xs font-bold tracking-[0.25em] text-blue-600">DRIVEFLOW</p><h1 className="text-xl font-bold">Vehicle inventory</h1></div><button onClick={onLogout} className="rounded-lg border px-4 py-2 text-sm font-semibold">Sign out</button></div></header><section className="mx-auto max-w-6xl px-5 py-10"><div className="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><h2 className="text-3xl font-bold">Find your next vehicle</h2><p className="mt-2 text-slate-500">Browse current dealership stock and purchase available units.</p></div><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search make, model, or category" className="w-full rounded-xl border bg-white px-4 py-3 md:max-w-sm"/></div>{isAdmin && <form onSubmit={addVehicle} className="mt-6 grid gap-2 rounded-2xl bg-blue-50 p-4 md:grid-cols-6">{['make','model','category','price','quantity'].map(key => <input key={key} value={newVehicle[key]} onChange={e => setNewVehicle({ ...newVehicle, [key]: e.target.value })} placeholder={key} required type={key === 'price' || key === 'quantity' ? 'number' : 'text'} min={key === 'quantity' ? '0' : key === 'price' ? '0.01' : undefined} className="rounded-lg border bg-white px-3 py-2"/>)}<button className="rounded-lg bg-blue-600 px-3 py-2 font-semibold text-white">Add vehicle</button></form>}{message && <p className="mt-5 rounded-lg bg-amber-50 p-3 text-amber-800">{message}</p>}<div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{loading ? <p>Loading inventory...</p> : visible.map(vehicle => <article key={vehicle.id} className="rounded-2xl border bg-white p-6 shadow-sm"><p className="text-sm font-semibold text-blue-600">{vehicle.category}</p><h3 className="mt-2 text-xl font-bold">{vehicle.make} {vehicle.model}</h3><p className="mt-5 text-2xl font-bold">${vehicle.price.toLocaleString()}</p><p className="mt-1 text-sm text-slate-500">{vehicle.quantity} in stock</p><button disabled={vehicle.quantity === 0} onClick={() => purchase(vehicle)} className="mt-6 w-full rounded-xl bg-slate-900 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-300">{vehicle.quantity === 0 ? 'Out of stock' : 'Purchase vehicle'}</button>{isAdmin && <><button onClick={() => restockVehicle(vehicle)} className="mt-2 w-full rounded-xl border border-blue-200 py-2 text-sm font-semibold text-blue-700">Restock</button><button onClick={() => removeVehicle(vehicle.id)} className="mt-2 w-full rounded-xl border border-red-200 py-2 text-sm font-semibold text-red-600">Delete vehicle</button></>}</article>)}</div>{!loading && visible.length === 0 && <p className="mt-8 text-slate-500">No vehicles match your search.</p>}</section></main>
}

export default function App() { const [token, setToken] = useState(() => localStorage.getItem('accessToken')); const logout = () => { localStorage.removeItem('accessToken'); setToken(null) }; return token ? <Dashboard token={token} onLogout={logout}/> : <AuthScreen onLogin={value => { localStorage.setItem('accessToken', value); setToken(value) }}/> }
