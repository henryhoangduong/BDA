import AppSidebar from '@/components/app-sidebar'
import Header from '@/components/header'
import { Outlet } from 'react-router-dom'
export const MainLayout = () => {
  return (
    <div className='h-screen flex flex-row w-screen'>
      <div>
        <AppSidebar />
      </div>
      <div className='flex-1  min-w-0 overflow-auto'>
        <Outlet />
      </div>
    </div>
  )
}
