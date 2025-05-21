import { Route, Routes } from 'react-router-dom'
import { MainLayout } from './layout/main.layout'
import DocumentPage from './pages/document.page'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<>chat page</>} />
        <Route path='/documents' element={<DocumentPage />} />
        <Route path='*' element={<div className='p-8 text-center'>Page Not Found</div>} />
      </Route>
    </Routes>
  )
}
