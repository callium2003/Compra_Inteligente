import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { supabase } from '@/lib/supabase'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { ShoppingCart, Sparkles, Save, TrendingDown } from 'lucide-react'
import QuoteResults from './QuoteResults'

const EXAMPLE_LIST = `2 leite integral 1l
arroz tipo 1 5kg
3 ovos brancos
feijão preto 1kg
café 500g
açúcar cristal 2kg
óleo de soja 900ml
macarrão 500g`

export default function NewQuote() {
  const { user } = useAuth()
  const [rawText, setRawText] = useState('')
  const [items, setItems] = useState([])
  const [listTitle, setListTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState('input') // input, preview, results
  const [quoteResults, setQuoteResults] = useState(null)
  const [defaultAddress, setDefaultAddress] = useState(null)

  useEffect(() => {
    loadDefaultAddress()
  }, [user])

  const loadDefaultAddress = async () => {
    try {
      const { data, error } = await supabase
        .from('user_addresses')
        .select('*')
        .eq('user_id', user.id)
        .eq('is_default', true)
        .single()

      if (error) throw error
      setDefaultAddress(data)
    } catch (error) {
      console.error('Erro ao carregar endereço:', error)
    }
  }

  const handleNormalize = async () => {
    if (!rawText.trim()) {
      alert('Digite sua lista de compras')
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/normalize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text: rawText }),
      })

      const data = await response.json()

      if (data.success) {
        setItems(data.items)
        setStep('preview')
      } else {
        alert(data.error || 'Erro ao normalizar lista')
      }
    } catch (error) {
      console.error('Erro:', error)
      alert('Erro ao processar lista')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveList = async () => {
    if (!listTitle.trim()) {
      alert('Digite um título para a lista')
      return
    }

    setLoading(true)
    try {
      // Salvar lista
      const { data: listData, error: listError } = await supabase
        .from('shopping_lists')
        .insert([{ user_id: user.id, title: listTitle }])
        .select()
        .single()

      if (listError) throw listError

      // Salvar itens
      const itemsToInsert = items.map((item) => ({
        list_id: listData.id,
        ...item,
      }))

      const { error: itemsError } = await supabase
        .from('shopping_items')
        .insert(itemsToInsert)

      if (itemsError) throw itemsError

      alert('Lista salva com sucesso!')
      return listData.id
    } catch (error) {
      console.error('Erro ao salvar lista:', error)
      alert('Erro ao salvar lista')
      return null
    } finally {
      setLoading(false)
    }
  }

  const handleQuote = async () => {
    if (!defaultAddress) {
      alert('Cadastre um endereço antes de fazer a cotação')
      return
    }

    setLoading(true)
    try {
      // Salvar lista primeiro
      const listId = await handleSaveList()
      if (!listId) return

      // Fazer cotação
      const response = await fetch('/api/quote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          list_id: listId,
          address_id: defaultAddress.id,
          items: items,
          stores: ['Carrefour', 'Extra'],
        }),
      })

      const data = await response.json()

      if (data.success) {
        setQuoteResults(data)
        setStep('results')
      } else {
        alert(data.error || 'Erro ao gerar cotação')
      }
    } catch (error) {
      console.error('Erro:', error)
      alert('Erro ao processar cotação')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateItem = (index, field, value) => {
    const newItems = [...items]
    newItems[index][field] = value
    setItems(newItems)
  }

  const handleRemoveItem = (index) => {
    setItems(items.filter((_, i) => i !== index))
  }

  const handleNewQuote = () => {
    setRawText('')
    setItems([])
    setListTitle('')
    setQuoteResults(null)
    setStep('input')
  }

  if (step === 'results' && quoteResults) {
    return <QuoteResults results={quoteResults} onNewQuote={handleNewQuote} />
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Nova Cotação</h2>
        <p className="text-muted-foreground">
          Digite sua lista de compras e encontre os melhores preços
        </p>
      </div>

      {!defaultAddress && (
        <Card className="border-yellow-500 bg-yellow-50">
          <CardContent className="pt-6">
            <p className="text-sm text-yellow-800">
              ⚠️ Você precisa cadastrar um endereço antes de fazer cotações
            </p>
          </CardContent>
        </Card>
      )}

      {step === 'input' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingCart className="w-5 h-5" />
              Digite sua Lista
            </CardTitle>
            <CardDescription>
              Digite um item por linha. Exemplo: "2 leite 1l" ou "arroz 5kg"
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder={EXAMPLE_LIST}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              rows={10}
              className="font-mono"
            />
            <Button onClick={handleNormalize} disabled={loading} className="w-full">
              <Sparkles className="w-4 h-4 mr-2" />
              {loading ? 'Processando...' : 'Validar & Normalizar'}
            </Button>
          </CardContent>
        </Card>
      )}

      {step === 'preview' && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Título da Lista</CardTitle>
            </CardHeader>
            <CardContent>
              <Input
                placeholder="Ex: Compras do mês"
                value={listTitle}
                onChange={(e) => setListTitle(e.target.value)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Itens Normalizados</CardTitle>
              <CardDescription>Revise e edite os itens antes de continuar</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {items.map((item, index) => (
                  <div key={index} className="grid grid-cols-12 gap-2 items-center">
                    <Input
                      className="col-span-1"
                      type="number"
                      value={item.qty}
                      onChange={(e) => handleUpdateItem(index, 'qty', parseFloat(e.target.value))}
                      min="1"
                      step="0.1"
                    />
                    <Input
                      className="col-span-4"
                      value={item.product_name}
                      onChange={(e) => handleUpdateItem(index, 'product_name', e.target.value)}
                    />
                    <Input
                      className="col-span-2"
                      type="number"
                      value={item.size_value || ''}
                      onChange={(e) => handleUpdateItem(index, 'size_value', parseFloat(e.target.value) || null)}
                      placeholder="Tamanho"
                      step="0.1"
                    />
                    <select
                      className="col-span-2 h-10 rounded-md border border-input bg-background px-3 py-2 text-sm"
                      value={item.size_unit}
                      onChange={(e) => handleUpdateItem(index, 'size_unit', e.target.value)}
                    >
                      <option value="un">un</option>
                      <option value="kg">kg</option>
                      <option value="g">g</option>
                      <option value="l">l</option>
                      <option value="ml">ml</option>
                    </select>
                    <Input
                      className="col-span-2"
                      value={item.brand || ''}
                      onChange={(e) => handleUpdateItem(index, 'brand', e.target.value)}
                      placeholder="Marca"
                    />
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleRemoveItem(index)}
                      className="col-span-1"
                    >
                      ✕
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="flex gap-2">
            <Button onClick={() => setStep('input')} variant="outline">
              Voltar
            </Button>
            <Button onClick={handleQuote} disabled={loading || !defaultAddress} className="flex-1">
              <TrendingDown className="w-4 h-4 mr-2" />
              {loading ? 'Processando...' : 'Fazer Cotação'}
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
