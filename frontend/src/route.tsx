import { Route, Routes } from 'react-router-dom'
import { MainLayout } from './layout/main-layout'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<>chat page</>} />
        <Route path='/documents' element={<>document page</>} />
        <Route path='*' element={<div className='p-8 text-center'>Page Not Found</div>} />
      </Route>
    </Routes>
  )
}
