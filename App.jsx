import { useState } from 'react'
import { AuthProvider, useAuth } from '@/contexts/AuthContext'
import Auth from '@/components/Auth'
import Addresses from '@/components/Addresses'
import NewQuote from '@/components/NewQuote'
import History from '@/components/History'
import { Button } from '@/components/ui/button'
import { ShoppingCart, MapPin, TrendingDown, History as HistoryIcon, LogOut } from 'lucide-react'
import './App.css'

function MainApp() {
  const { user, signOut, loading } = useAuth()
  const [currentTab, setCurrentTab] = useState('quote')

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <ShoppingCart className="w-12 h-12 mx-auto mb-4 animate-pulse" />
          <p className="text-muted-foreground">Carregando...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Auth />
  }

  const handleSignOut = async () => {
    await signOut()
  }

  const tabs = [
    { id: 'quote', label: 'Nova Cotação', icon: TrendingDown },
    { id: 'addresses', label: 'Endereços', icon: MapPin },
    { id: 'history', label: 'Histórico', icon: HistoryIcon },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary rounded-lg">
                <ShoppingCart className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold">Compra Inteligente</h1>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </div>
            <Button variant="outline" onClick={handleSignOut}>
              <LogOut className="w-4 h-4 mr-2" />
              Sair
            </Button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setCurrentTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
                    currentTab === tab.id
                      ? 'border-primary text-primary font-medium'
                      : 'border-transparent text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {currentTab === 'quote' && <NewQuote />}
        {currentTab === 'addresses' && <Addresses />}
        {currentTab === 'history' && <History />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <p className="text-center text-sm text-muted-foreground">
            Compra Inteligente MVP - Economize nas suas compras
          </p>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  )
}

export default App
