import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { supabase } from '@/lib/supabase'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MapPin, Plus, Trash2, Check } from 'lucide-react'

export default function Addresses({ onAddressSelected }) {
  const { user } = useAuth()
  const [addresses, setAddresses] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    label: '',
    cep: '',
    street: '',
    number: '',
    complement: '',
    neighborhood: '',
    city: '',
    state: '',
  })

  useEffect(() => {
    loadAddresses()
  }, [user])

  const loadAddresses = async () => {
    try {
      const { data, error } = await supabase
        .from('user_addresses')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (error) throw error
      setAddresses(data || [])
    } catch (error) {
      console.error('Erro ao carregar endereços:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const { error } = await supabase.from('user_addresses').insert([
        {
          ...formData,
          user_id: user.id,
          is_default: addresses.length === 0,
        },
      ])

      if (error) throw error

      setFormData({
        label: '',
        cep: '',
        street: '',
        number: '',
        complement: '',
        neighborhood: '',
        city: '',
        state: '',
      })
      setShowForm(false)
      loadAddresses()
    } catch (error) {
      console.error('Erro ao salvar endereço:', error)
      alert('Erro ao salvar endereço')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Deseja realmente excluir este endereço?')) return

    try {
      const { error } = await supabase.from('user_addresses').delete().eq('id', id)

      if (error) throw error
      loadAddresses()
    } catch (error) {
      console.error('Erro ao excluir endereço:', error)
      alert('Erro ao excluir endereço')
    }
  }

  const handleSetDefault = async (id) => {
    try {
      // Remover default de todos
      await supabase
        .from('user_addresses')
        .update({ is_default: false })
        .eq('user_id', user.id)

      // Definir novo default
      const { error } = await supabase
        .from('user_addresses')
        .update({ is_default: true })
        .eq('id', id)

      if (error) throw error
      loadAddresses()
    } catch (error) {
      console.error('Erro ao definir endereço padrão:', error)
      alert('Erro ao definir endereço padrão')
    }
  }

  const defaultAddress = addresses.find((addr) => addr.is_default)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Meus Endereços</h2>
          <p className="text-muted-foreground">Gerencie seus endereços de entrega</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="w-4 h-4 mr-2" />
          Novo Endereço
        </Button>
      </div>

      {defaultAddress && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              Endereço Ativo
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <p className="font-medium">{defaultAddress.label}</p>
              <p className="text-sm text-muted-foreground">
                {defaultAddress.street}, {defaultAddress.number}
                {defaultAddress.complement && ` - ${defaultAddress.complement}`}
              </p>
              <p className="text-sm text-muted-foreground">
                {defaultAddress.neighborhood} - {defaultAddress.city}/{defaultAddress.state}
              </p>
              <p className="text-sm font-medium">CEP: {defaultAddress.cep}</p>
            </div>
          </CardContent>
        </Card>
      )}

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>Novo Endereço</CardTitle>
            <CardDescription>Preencha os dados do endereço de entrega</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="text-sm font-medium">Nome do Endereço</label>
                  <Input
                    placeholder="Ex: Casa, Trabalho"
                    value={formData.label}
                    onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">CEP</label>
                  <Input
                    placeholder="00000-000"
                    value={formData.cep}
                    onChange={(e) => setFormData({ ...formData, cep: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Número</label>
                  <Input
                    placeholder="123"
                    value={formData.number}
                    onChange={(e) => setFormData({ ...formData, number: e.target.value })}
                    required
                  />
                </div>
                <div className="col-span-2">
                  <label className="text-sm font-medium">Rua</label>
                  <Input
                    placeholder="Nome da rua"
                    value={formData.street}
                    onChange={(e) => setFormData({ ...formData, street: e.target.value })}
                  />
                </div>
                <div className="col-span-2">
                  <label className="text-sm font-medium">Complemento</label>
                  <Input
                    placeholder="Apto, bloco, etc"
                    value={formData.complement}
                    onChange={(e) => setFormData({ ...formData, complement: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Bairro</label>
                  <Input
                    placeholder="Bairro"
                    value={formData.neighborhood}
                    onChange={(e) => setFormData({ ...formData, neighborhood: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Cidade</label>
                  <Input
                    placeholder="Cidade"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Estado</label>
                  <Input
                    placeholder="UF"
                    maxLength={2}
                    value={formData.state}
                    onChange={(e) => setFormData({ ...formData, state: e.target.value.toUpperCase() })}
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button type="submit" disabled={loading}>
                  Salvar
                </Button>
                <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4">
        {addresses.map((address) => (
          <Card key={address.id} className={address.is_default ? 'border-primary' : ''}>
            <CardContent className="pt-6">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <p className="font-medium flex items-center gap-2">
                    {address.label}
                    {address.is_default && (
                      <span className="text-xs bg-primary text-primary-foreground px-2 py-1 rounded">
                        Ativo
                      </span>
                    )}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {address.street}, {address.number}
                    {address.complement && ` - ${address.complement}`}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {address.neighborhood} - {address.city}/{address.state}
                  </p>
                  <p className="text-sm">CEP: {address.cep}</p>
                </div>
                <div className="flex gap-2">
                  {!address.is_default && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleSetDefault(address.id)}
                    >
                      <Check className="w-4 h-4" />
                    </Button>
                  )}
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => handleDelete(address.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
