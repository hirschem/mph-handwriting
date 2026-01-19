'use client'

import { useState } from 'react'
import Link from 'next/link'
import UploadForm from '@/components/UploadForm'
import ProposalDisplay from '@/components/ProposalDisplay'
import LoginPage from '@/components/LoginPage'
import { useAuth } from '@/contexts/AuthContext'

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [proposalData, setProposalData] = useState<any>(null)
  const { isAuthenticated, isAdmin, logout } = useAuth()

  if (!isAuthenticated) {
    return <LoginPage />
  }

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                MPH Construction Proposals
              </h1>
              <p className="text-gray-600">
                Transform handwritten proposals into professional documents
              </p>
            </div>
            <div className="flex gap-3">
              {isAdmin && (
                <Link
                  href="/history"
                  className="bg-gray-700 text-white px-4 py-2 rounded-lg
                    hover:bg-gray-800 transition-colors flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  View History
                </Link>
              )}
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded-lg
                  hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <UploadForm 
          onSuccess={(sessionId, data) => {
            setSessionId(sessionId)
            setProposalData(data)
          }}
        />

        {proposalData && (
          <ProposalDisplay 
            sessionId={sessionId!} 
            data={proposalData} 
          />
        )}
      </div>
    </main>
  )
}
