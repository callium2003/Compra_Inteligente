import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { supabase } from '@/lib/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { History as HistoryIcon, ShoppingCart, TrendingDown } from 'lucide-react'

export default function History() {
  const { user } = useAuth()
  const [quotes, setQuotes] = useState([])
  const [lists, setLists] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [user])

  const loadHistory = async () => {
    try {
      // Carregar cotações
      const { data: quotesData, error: quotesError } = await supabase
        .from('quotes')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })
        .limit(10)

      if (quotesError) throw quotesError

      // Carregar listas
      const { data: listsData, error: listsError } = await supabase
        .from('shopping_lists')
        .select('*, shopping_items(*)')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })
        .limit(10)

      if (listsError) throw listsError

      setQuotes(quotesData || [])
      setLists(listsData || [])
    } catch (error) {
      console.error('Erro ao carregar histórico:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (loading) {
    return <div className="text-center py-8">Carregando histórico...</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Histórico</h2>
        <p className="text-muted-foreground">Suas listas e cotações anteriores</p>
      </div>

      {/* Cotações */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <TrendingDown className="w-5 h-5" />
          Cotações Recentes
        </h3>

        {quotes.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-center text-muted-foreground">Nenhuma cotação encontrada</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {quotes.map((quote) => {
              const result = quote.result_json
              return (
                <Card key={quote.id}>
                  <CardHeader>
                    <CardTitle className="text-base">
                      Cotação - {formatDate(quote.created_at)}
                    </CardTitle>
                    <CardDescription>
                      Lojas: {quote.stores.join(', ')}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Cesta Única</p>
                        <p className="text-lg font-bold">
                          R$ {result.single_store.total.toFixed(2)}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {result.single_store.store}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Cesta Mista</p>
                        <p className="text-lg font-bold text-primary">
                          R$ {result.mixed_basket.total.toFixed(2)}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {result.mixed_basket.stores.length} lojas
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Economia</p>
                        <p className="text-lg font-bold text-green-600">
                          R$ {result.savings.amount.toFixed(2)}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {result.savings.percentage.toFixed(1)}% de desconto
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        )}
      </div>

      {/* Listas */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <ShoppingCart className="w-5 h-5" />
          Listas Salvas
        </h3>

        {lists.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-center text-muted-foreground">Nenhuma lista encontrada</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {lists.map((list) => (
              <Card key={list.id}>
                <CardHeader>
                  <CardTitle className="text-base">{list.title}</CardTitle>
                  <CardDescription>{formatDate(list.created_at)}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-2">
                    {list.shopping_items.length} itens
                  </p>
                  <div className="space-y-1">
                    {list.shopping_items.slice(0, 5).map((item, index) => (
                      <p key={index} className="text-sm">
                        • {item.qty}x {item.product_name}
                        {item.size_value && ` ${item.size_value}${item.size_unit}`}
                      </p>
                    ))}
                    {list.shopping_items.length > 5 && (
                      <p className="text-sm text-muted-foreground">
                        ... e mais {list.shopping_items.length - 5} itens
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
