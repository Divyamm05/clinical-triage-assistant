export default function UploadPanel({ onFileSelect, onSubmit, loading, file }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">Upload Chest X-Ray</h2>

      <label className="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-blue-300 rounded-xl cursor-pointer hover:bg-blue-50 transition overflow-hidden">
        {file ? (
          <img
            src={URL.createObjectURL(file)}
            alt="Selected"
            className="h-full w-full object-contain rounded-xl py-1"
          />
        ) : (
          <>
            <span className="text-4xl mb-2">🫁</span>
            <span className="text-sm text-gray-500">Click to upload X-ray image</span>
            <span className="text-xs text-gray-400 mt-1">JPG, PNG supported</span>
          </>
        )}
        <input
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => onFileSelect(e.target.files[0])}
        />
      </label>

      <button
        onClick={onSubmit}
        disabled={loading || !file}
        className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-2 rounded-xl transition"
      >
        {loading ? "Analyzing..." : "Analyze X-Ray"}
      </button>
    </div>
  )
}