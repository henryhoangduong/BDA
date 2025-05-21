import AppSidebar from '@/components/app-sidebar'
import { Outlet } from 'react-router-dom'
export const MainLayout = () => {
  return (
    <div className='h-screen'>
      <AppSidebar />
      <Outlet />
    </div>
  )
}
