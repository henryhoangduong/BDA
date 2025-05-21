import AppSidebar from '@/components/app-sidebar'
import { Outlet } from 'react-router-dom'
export const MainLayout = () => {
  return (
    <div className='h-screen flex flex-row w-screen'>
      <div>
        <AppSidebar />
      </div>
      <div className='w-full'>
        <Outlet />
      </div>
    </div>
  )
}
