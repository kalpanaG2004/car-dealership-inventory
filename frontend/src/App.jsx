import { useEffect, useState } from 'react'
const API = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const api = (path, token, options = {}) => fetch(`${API}${path}`, { ...options, headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) } })

function Dashboard({ token, onLogout }) {
  const [inventory, setInventory] = useState([]); const [query, setQuery] = useState('')
  const admin = JSON.parse(atob(token.split('.')[1])).role === 'admin'
  useEffect(() => { api('/api/vehicles', token).then(r => r.json()).then(setInventory) }, [token])
  const vehicles = inventory.filter(v => `${v.make} ${v.model} ${v.category}`.toLowerCase().includes(query.toLowerCase()))
  return <main className="min-h-screen bg-slate-50 text-slate-900"><header className="border-b bg-white"><div className="mx-auto flex max-w-6xl justify-between p-5"><b>DRIVEFLOW</b><button onClick={onLogout}>Sign out</button></div></header><section className="mx-auto max-w-6xl p-6"><h1 className="text-3xl font-bold">Vehicle inventory</h1><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search make, model, or category" className="mt-5 w-full max-w-md rounded-xl border bg-white p-3"/><div className="mt-8 grid gap-5 md:grid-cols-3">{vehicles.map(v => <article key={v.id} className="rounded-2xl bg-white p-6 shadow"><p className="text-blue-600">{v.category}</p><h2 className="text-xl font-bold">{v.make} {v.model}</h2><p className="mt-4 text-2xl font-bold">${v.price.toLocaleString()}</p><p>{v.quantity} in stock</p><button disabled={!v.quantity} className="mt-4 w-full rounded-xl bg-slate-900 py-3 text-white">Purchase vehicle</button>{admin && <><button aria-label="Edit vehicle" className="mt-2 w-full rounded-xl border py-2">Edit vehicle</button><button className="mt-2 w-full rounded-xl border py-2">Restock</button><button className="mt-2 w-full rounded-xl border border-red-200 py-2 text-red-600">Delete vehicle</button></>}</article>)}</div></section></main>
}

function Auth({ onLogin }) { return <main className="grid min-h-screen place-items-center bg-slate-950"><button onClick={() => onLogin('')} className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white">Sign in</button></main> }
export default function App() { const [token, setToken] = useState(() => localStorage.getItem('accessToken')); return token ? <Dashboard token={token} onLogout={() => { localStorage.clear(); setToken(null) }} /> : <Auth onLogin={setToken} /> }
