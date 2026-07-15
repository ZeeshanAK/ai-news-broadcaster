import React from 'react'

export default function FilterBar({ onFilterChange }) {
  const [category, setCategory] = React.useState('')
  const [source, setSource] = React.useState('')

  const handleCategoryChange = (e) => {
    setCategory(e.target.value)
    onFilterChange?.({ category: e.target.value, source })
  }

  const handleSourceChange = (e) => {
    setSource(e.target.value)
    onFilterChange?.({ category, source: e.target.value })
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <input
            type="text"
            value={category}
            onChange={handleCategoryChange}
            placeholder="Filter by category..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Source
          </label>
          <input
            type="text"
            value={source}
            onChange={handleSourceChange}
            placeholder="Filter by source..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>
    </div>
  )
}