import React, { ReactNode } from 'react'
import { SidebarProvider } from '@/components/ui/sidebar'
const RootProvider = ({ children }: { children: ReactNode }) => {
  return <SidebarProvider>{children}</SidebarProvider>
}

export default RootProvider
