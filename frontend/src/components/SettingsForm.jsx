import React from 'react'

export default function SettingsForm({ onSubmit }) {
  const [settings, setSettings] = React.useState({
    fetchInterval: 30,
    summaryStyle: 'news_anchor',
    ttsVoice: 'alloy',
    ttsProvider: 'openai',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit?.(settings)
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Fetch Interval (minutes)
        </label>
        <input
          type="number"
          name="fetchInterval"
          value={settings.fetchInterval}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Summary Style
        </label>
        <select
          name="summaryStyle"
          value={settings.summaryStyle}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="brief">Brief</option>
          <option value="detailed">Detailed</option>
          <option value="bullet_points">Bullet Points</option>
          <option value="news_anchor">News Anchor</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          TTS Voice
        </label>
        <select
          name="ttsVoice"
          value={settings.ttsVoice}
          onChange={handleChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="alloy">Alloy</option>
          <option value="echo">Echo</option>
          <option value="fable">Fable</option>
          <option value="onyx">Onyx</option>
          <option value="nova">Nova</option>
          <option value="shimmer">Shimmer</option>
        </select>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Save Settings
      </button>
    </form>
  )
}