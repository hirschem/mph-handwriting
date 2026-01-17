import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MPH Construction Proposals',
  description: 'Transform handwritten proposals into professional documents',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
