import React from 'react'

export default function NewsCard({ article }) {
  return (
    <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{article.title}</h3>
      {article.author && (
        <p className="text-sm text-gray-500 mb-2">By {article.author}</p>
      )}
      {article.summary && (
        <p className="text-gray-700 mb-4 line-clamp-3">{article.summary}</p>
      )}
      {article.content && (
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">{article.content}</p>
      )}
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span>{article.category || 'Uncategorized'}</span>
        <a 
          href={article.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800"
        >
          Read More →
        </a>
      </div>
    </div>
  )
}