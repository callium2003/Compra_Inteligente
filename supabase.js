import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://wrzuwwvnyzflsohrgyin.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndyenV3d3ZueXpmbHNvaHJneWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTQyNDksImV4cCI6MjA3NTA3MDI0OX0.iiLEOqT4wcRLNfgcjmc3IvsAYNTJ4D5g7XSqpNH69Dw'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
