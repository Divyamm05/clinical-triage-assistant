const TRIAGE_STYLES = {
  URGENT:  { bg: "bg-red-100",    text: "text-red-700",    badge: "🔴 URGENT"  },
  MONITOR: { bg: "bg-yellow-100", text: "text-yellow-700", badge: "🟡 MONITOR" },
  ROUTINE: { bg: "bg-green-100",  text: "text-green-700",  badge: "🟢 ROUTINE" },
}

export default function ResultCard({ predictions, triage }) {
  const style = TRIAGE_STYLES[triage]

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">Diagnosis Results</h2>

      {/* Triage badge */}
      <div className={`${style.bg} ${style.text} font-bold text-center py-2 rounded-xl mb-4 text-lg`}>
        {style.badge}
      </div>

      {/* Top predictions */}
      <div className="space-y-3">
        {predictions.map((p, i) => (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="font-medium text-gray-700">{p.condition}</span>
              <span className="text-gray-500">{(p.confidence * 100).toFixed(1)}%</span>
            </div>
            {/* Confidence bar */}
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${p.confidence * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-400 mt-4">
        ⚠️ For research purposes only. Not a substitute for clinical diagnosis.
      </p>
    </div>
  )
}