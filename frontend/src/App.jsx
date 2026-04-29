import { useState, useEffect } from "react"
import axios from "axios"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

const API = "http://localhost:8000"

export default function App() {
  const [transactions, setTransactions] = useState([])
  const [stats, setStats] = useState({})
  const [chartData, setChartData] = useState([])
  const [alerts, setAlerts] = useState([])
  const [tab, setTab] = useState("dashboard")

  const simulate = async () => {
    try {
      const res = await axios.get(
        `${API}/api/transactions/simulate?n=10&fraud_rate=0.3`
      )
      setTransactions(prev =>
        [...res.data.transactions, ...prev].slice(0, 20)
      )
      setStats(res.data.stats)
      setChartData(prev => {
        const newPoint = {
          time: new Date().toLocaleTimeString(),
          newFraud: Math.max(0, (res.data.stats.fraud_detected || 0) - (prev.length > 0 ? prev[prev.length - 1].fraud : 0)),
          newTotal: Math.max(0, (res.data.stats.total_processed || 0) - (prev.length > 0 ? prev[prev.length - 1].total : 0)),
          fraud: res.data.stats.fraud_detected || 0,
          total: res.data.stats.total_processed || 0
        }
        return [...prev, newPoint].slice(-20)
      })
    } catch (err) {
      console.error(err)
    }
  }

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(`${API}/api/transactions/alerts`)
      setAlerts(res.data.alerts || [])
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    simulate()
    fetchAlerts()
    const interval = setInterval(() => {
      simulate()
      fetchAlerts()
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  const tabStyle = (name) => ({
    padding: "10px 24px",
    borderRadius: "8px 8px 0 0",
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "14px",
    background: tab === name ? "#1e293b" : "transparent",
    color: tab === name ? "#38bdf8" : "#64748b",
    border: "none"
  })

  return (
    <div style={{
      background: "#0f172a", minHeight: "100vh",
      color: "white", padding: "20px", fontFamily: "monospace"
    }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <h1 style={{ color: "#38bdf8", fontSize: "32px" }}>🛡️ FraudShield AI</h1>
        <p style={{ color: "#64748b" }}>Real-time fraud detection powered by AI</p>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "4px", marginBottom: "0px" }}>
        <button style={tabStyle("dashboard")} onClick={() => setTab("dashboard")}>
          📊 Dashboard
        </button>
        <button style={tabStyle("alerts")} onClick={() => setTab("alerts")}>
          🚨 Alerts {alerts.length > 0 && (
            <span style={{
              background: "#ef4444", color: "white",
              borderRadius: "10px", padding: "1px 7px",
              fontSize: "11px", marginLeft: "6px"
            }}>{alerts.length}</span>
          )}
        </button>
      </div>

      {tab === "dashboard" && (
        <div>
          {/* Stats Cards */}
          <div style={{ display: "flex", gap: "15px", marginBottom: "25px", marginTop: "4px" }}>
            {[
              { label: "Total Processed", value: stats.total_processed || 0, color: "#38bdf8" },
              { label: "Fraud Detected", value: stats.fraud_detected || 0, color: "#ef4444" },
              { label: "Fraud Rate", value: `${stats.fraud_rate || 0}%`, color: "#f59e0b" },
              { label: "Amount Blocked", value: `$${Number(stats.amount_blocked || 0).toFixed(2)}`, color: "#22c55e" }
            ].map(s => (
              <div key={s.label} style={{
                background: "#1e293b", padding: "20px",
                borderRadius: "12px", flex: 1,
                borderTop: `3px solid ${s.color}`
              }}>
                <div style={{ color: "#94a3b8", fontSize: "11px", marginBottom: "8px" }}>{s.label}</div>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: s.color }}>{s.value}</div>
              </div>
            ))}
          </div>

          {/* Chart */}
          <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", marginBottom: "25px" }}>
            <h3 style={{ marginBottom: "15px", color: "#94a3b8" }}>Fraud Detection Over Time</h3>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={chartData}>
                <XAxis dataKey="time" stroke="#475569" tick={{ fontSize: 10 }} />
                <YAxis stroke="#475569" />
                <Tooltip contentStyle={{ background: "#0f172a", border: "none" }} />
                <Line type="monotone" dataKey="newTotal" stroke="#38bdf8" dot={false} name="Total" />
                <Line type="monotone" dataKey="newFraud" stroke="#ef4444" dot={false} name="Fraud" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Transaction Feed */}
          <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
            <h3 style={{ marginBottom: "15px", color: "#94a3b8" }}>Live Transaction Feed</h3>
            {transactions.map((t, i) => (
              <div key={i} style={{
                display: "flex", justifyContent: "space-between",
                alignItems: "center", padding: "12px",
                borderBottom: "1px solid #334155",
                background: t.is_fraud ? "#450a0a" : "transparent",
                borderRadius: "6px", marginBottom: "4px"
              }}>
                <span style={{ width: "120px" }}>{t.is_fraud ? "🚨" : "✅"} {t.transaction_id}</span>
                <span style={{ color: "#94a3b8" }}>${t.amount}</span>
                <span style={{ color: t.risk_score > 60 ? "#ef4444" : "#22c55e" }}>{t.risk_score}/100</span>
                <span style={{
                  padding: "4px 10px", borderRadius: "20px", fontSize: "12px",
                  background: t.risk_level === "CRITICAL" ? "#7f1d1d" : t.risk_level === "HIGH" ? "#78350f" : t.risk_level === "MEDIUM" ? "#1e3a5f" : "#14532d",
                  color: t.risk_level === "CRITICAL" ? "#fca5a5" : t.risk_level === "HIGH" ? "#fcd34d" : t.risk_level === "MEDIUM" ? "#93c5fd" : "#86efac"
                }}>{t.risk_level}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "alerts" && (
        <div style={{ background: "#1e293b", borderRadius: "0 12px 12px 12px", padding: "20px" }}>
          <h3 style={{ marginBottom: "20px", color: "#94a3b8" }}>
            🚨 Fraud Alerts — {alerts.length} flagged
          </h3>
          {alerts.length === 0 ? (
            <p style={{ color: "#475569" }}>No alerts yet. Transactions are being monitored.</p>
          ) : (
            [...alerts].reverse().map((a, i) => (
              <div key={i} style={{
                background: "#0f172a", borderRadius: "10px",
                padding: "16px", marginBottom: "12px",
                borderLeft: "4px solid #ef4444"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                  <span style={{ color: "#ef4444", fontWeight: "bold" }}>🚨 {a.transaction_id}</span>
                  <span style={{
                    padding: "3px 10px", borderRadius: "20px", fontSize: "12px",
                    background: a.risk_level === "CRITICAL" ? "#7f1d1d" : "#78350f",
                    color: a.risk_level === "CRITICAL" ? "#fca5a5" : "#fcd34d"
                  }}>{a.risk_level}</span>
                </div>
                <div style={{ display: "flex", gap: "30px", color: "#94a3b8", fontSize: "13px" }}>
                  <span>💰 Amount: <strong style={{ color: "white" }}>${a.amount}</strong></span>
                  <span>⚠️ Risk Score: <strong style={{ color: "#ef4444" }}>{a.risk_score}/100</strong></span>
                  <span>🕐 {new Date(a.timestamp).toLocaleTimeString()}</span>
                  <span style={{
                    padding: "2px 8px", borderRadius: "10px",
                    background: "#14532d", color: "#86efac", fontSize: "11px"
                  }}>{a.status}</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
