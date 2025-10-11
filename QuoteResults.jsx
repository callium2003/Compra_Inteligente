import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { TrendingDown, Store, Package, Truck, DollarSign, Plus } from 'lucide-react'

export default function QuoteResults({ results, onNewQuote }) {
  const { single_store, mixed_basket, savings } = results

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Resultados da Cotação</h2>
          <p className="text-muted-foreground">Compare as opções e escolha a melhor para você</p>
        </div>
        <Button onClick={onNewQuote}>
          <Plus className="w-4 h-4 mr-2" />
          Nova Cotação
        </Button>
      </div>

      {/* Economia */}
      {savings.amount > 0 && (
        <Card className="border-green-500 bg-green-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-500 rounded-full">
                <TrendingDown className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-sm text-green-800 font-medium">Economia com Cesta Mista</p>
                <p className="text-2xl font-bold text-green-900">
                  R$ {savings.amount.toFixed(2)} ({savings.percentage.toFixed(1)}%)
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {/* Cesta Única */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Store className="w-5 h-5" />
              Cesta Única
            </CardTitle>
            <CardDescription>Tudo em uma loja só</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">Loja</p>
              <p className="text-xl font-bold">{single_store.store}</p>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Subtotal</span>
                <span className="font-medium">R$ {single_store.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground flex items-center gap-1">
                  <Truck className="w-4 h-4" />
                  Frete
                </span>
                <span className="font-medium">R$ {single_store.frete.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Mínimo</span>
                <span className="font-medium">R$ {single_store.minimo.toFixed(2)}</span>
              </div>
              {!single_store.meets_minimum && (
                <p className="text-xs text-yellow-600">⚠️ Não atinge o valor mínimo</p>
              )}
            </div>

            <div className="pt-4 border-t">
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold">Total</span>
                <span className="text-2xl font-bold text-primary">
                  R$ {single_store.total.toFixed(2)}
                </span>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-sm font-medium">Itens ({single_store.items.length})</p>
              <div className="max-h-48 overflow-y-auto space-y-2">
                {single_store.items.map((item, index) => (
                  <div key={index} className="text-sm flex justify-between">
                    <span className="text-muted-foreground">
                      {item.qty}x {item.product_name}
                      {item.size_value && ` ${item.size_value}${item.size_unit}`}
                    </span>
                    <span className="font-medium">R$ {item.total.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Cesta Mista */}
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="w-5 h-5" />
              Cesta Mista Otimizada
            </CardTitle>
            <CardDescription>Itens divididos para menor preço</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {mixed_basket.stores.map((store, storeIndex) => (
              <div key={storeIndex} className="p-4 bg-muted rounded-lg space-y-2">
                <p className="font-bold">{store.store}</p>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>R$ {store.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Frete</span>
                    <span>R$ {store.frete.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-medium">
                    <span>Total</span>
                    <span>R$ {store.total.toFixed(2)}</span>
                  </div>
                  {!store.meets_minimum && (
                    <p className="text-xs text-yellow-600">⚠️ Não atinge o valor mínimo</p>
                  )}
                </div>
                <div className="mt-2 space-y-1">
                  <p className="text-xs font-medium">Itens ({store.items.length})</p>
                  <div className="max-h-32 overflow-y-auto space-y-1">
                    {store.items.map((item, itemIndex) => (
                      <div key={itemIndex} className="text-xs flex justify-between">
                        <span className="text-muted-foreground">
                          {item.qty}x {item.product_name}
                        </span>
                        <span>R$ {item.total.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}

            <div className="pt-4 border-t space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Total Fretes</span>
                <span className="font-medium">R$ {mixed_basket.total_frete.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold">Total Geral</span>
                <span className="text-2xl font-bold text-primary">
                  R$ {mixed_basket.total.toFixed(2)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
