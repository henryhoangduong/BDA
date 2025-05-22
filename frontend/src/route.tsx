import { Route, Routes } from 'react-router-dom'
import { MainLayout } from './layout/main.layout'
import DocumentPage from './pages/document.page'
import ChatPage from './pages/chat.page'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<ChatPage />} />
        <Route path='/documents' element={<DocumentPage />} />
        <Route path='*' element={<div className='p-8 text-center'>Page Not Found</div>} />
      </Route>
    </Routes>
  )
}
