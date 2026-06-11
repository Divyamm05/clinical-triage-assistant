export default function HeatmapViewer({ originalFile, heatmap }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">GradCAM Explainability</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-500 mb-2 text-center">Original</p>
          <img
            src={URL.createObjectURL(originalFile)}
            alt="Original X-ray"
            className="rounded-xl w-full object-cover"
          />
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-2 text-center">Areas of Concern</p>
          <img
            src={`data:image/png;base64,${heatmap}`}
            alt="GradCAM Heatmap"
            className="rounded-xl w-full object-cover"
          />
        </div>
      </div>
      <p className="text-xs text-gray-400 mt-3">
        🔴 Red regions indicate areas the model focused on most
      </p>
    </div>
  )
}