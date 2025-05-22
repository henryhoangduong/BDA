import React, { ReactNode, useEffect } from 'react'
import { SidebarProvider } from '@/components/ui/sidebar'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { config } from '@/config/config'
import { toast } from '@/hooks/use-toast'
import { Toaster } from '@/components/ui/toaster'
const RootProvider = ({ children }: { children: ReactNode }) => {
  const queryClient = new QueryClient()
  useEffect(() => {
    if (config.apiUrl == null || config.apiUrl.length == 0) {
      toast({
        variant: 'destructive',
        description: 'Please provide .env'
      })
    }
  }, [])
  return (
    <QueryClientProvider client={queryClient}>
      <SidebarProvider>
        {children}
        <Toaster />
      </SidebarProvider>
    </QueryClientProvider>
  )
}

export default RootProvider
