-- ============================================
-- COMPRA INTELIGENTE - MVP
-- Configuração do Banco de Dados Supabase
-- ============================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABELA: user_addresses
-- ============================================
CREATE TABLE IF NOT EXISTS user_addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    label VARCHAR(100) NOT NULL,
    cep VARCHAR(9) NOT NULL,
    street VARCHAR(255),
    number VARCHAR(20),
    complement VARCHAR(100),
    neighborhood VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(2),
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para consultas por usuário
CREATE INDEX IF NOT EXISTS idx_user_addresses_user_id ON user_addresses(user_id, created_at DESC);

-- RLS: Habilitar Row Level Security
ALTER TABLE user_addresses ENABLE ROW LEVEL SECURITY;

-- Policy: Usuários só veem seus próprios endereços
CREATE POLICY "Users can view their own addresses" ON user_addresses
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own addresses" ON user_addresses
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own addresses" ON user_addresses
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own addresses" ON user_addresses
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- TABELA: shopping_lists
-- ============================================
CREATE TABLE IF NOT EXISTS shopping_lists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para consultas por usuário
CREATE INDEX IF NOT EXISTS idx_shopping_lists_user_id ON shopping_lists(user_id, created_at DESC);

-- RLS: Habilitar Row Level Security
ALTER TABLE shopping_lists ENABLE ROW LEVEL SECURITY;

-- Policy: Usuários só veem suas próprias listas
CREATE POLICY "Users can view their own lists" ON shopping_lists
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own lists" ON shopping_lists
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own lists" ON shopping_lists
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own lists" ON shopping_lists
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- TABELA: shopping_items
-- ============================================
CREATE TABLE IF NOT EXISTS shopping_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    list_id UUID NOT NULL REFERENCES shopping_lists(id) ON DELETE CASCADE,
    qty NUMERIC(10, 2) NOT NULL CHECK (qty >= 1),
    product_name VARCHAR(255) NOT NULL,
    size_value NUMERIC(10, 2),
    size_unit VARCHAR(10) CHECK (size_unit IN ('g', 'kg', 'ml', 'l', 'un')),
    brand VARCHAR(100),
    preference VARCHAR(20) DEFAULT 'any' CHECK (preference IN ('any', 'cheapest', 'exact_brand', 'similar')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para consultas por lista
CREATE INDEX IF NOT EXISTS idx_shopping_items_list_id ON shopping_items(list_id);

-- RLS: Habilitar Row Level Security
ALTER TABLE shopping_items ENABLE ROW LEVEL SECURITY;

-- Policy: Usuários só veem itens de suas próprias listas
CREATE POLICY "Users can view items from their own lists" ON shopping_items
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM shopping_lists
            WHERE shopping_lists.id = shopping_items.list_id
            AND shopping_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert items to their own lists" ON shopping_items
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM shopping_lists
            WHERE shopping_lists.id = shopping_items.list_id
            AND shopping_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update items from their own lists" ON shopping_items
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM shopping_lists
            WHERE shopping_lists.id = shopping_items.list_id
            AND shopping_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete items from their own lists" ON shopping_items
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM shopping_lists
            WHERE shopping_lists.id = shopping_items.list_id
            AND shopping_lists.user_id = auth.uid()
        )
    );

-- ============================================
-- TABELA: quotes
-- ============================================
CREATE TABLE IF NOT EXISTS quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    list_id UUID REFERENCES shopping_lists(id) ON DELETE SET NULL,
    address_id UUID REFERENCES user_addresses(id) ON DELETE SET NULL,
    stores TEXT[] NOT NULL,
    result_json JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para consultas por usuário
CREATE INDEX IF NOT EXISTS idx_quotes_user_id ON quotes(user_id, created_at DESC);

-- RLS: Habilitar Row Level Security
ALTER TABLE quotes ENABLE ROW LEVEL SECURITY;

-- Policy: Usuários só veem suas próprias cotações
CREATE POLICY "Users can view their own quotes" ON quotes
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own quotes" ON quotes
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own quotes" ON quotes
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own quotes" ON quotes
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- FUNÇÃO: Garantir apenas um endereço padrão por usuário
-- ============================================
CREATE OR REPLACE FUNCTION ensure_single_default_address()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_default = true THEN
        UPDATE user_addresses
        SET is_default = false
        WHERE user_id = NEW.user_id
        AND id != NEW.id
        AND is_default = true;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para garantir apenas um endereço padrão
DROP TRIGGER IF EXISTS trigger_ensure_single_default ON user_addresses;
CREATE TRIGGER trigger_ensure_single_default
    BEFORE INSERT OR UPDATE ON user_addresses
    FOR EACH ROW
    EXECUTE FUNCTION ensure_single_default_address();

-- ============================================
-- FIM DA CONFIGURAÇÃO
-- ============================================
