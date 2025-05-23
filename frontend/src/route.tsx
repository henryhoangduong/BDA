import { Route, Routes } from 'react-router-dom'
import { MainLayout } from './layout/main.layout'
import DocumentPage from './pages/document.page'
import ChatPage from './pages/chat.page'
import EvaluationPage from './pages/evaluation.page'
import SettingPage from './pages/setting.page'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path='/' element={<ChatPage />} />
        <Route path='/documents' element={<DocumentPage />} />
        <Route path='/evaluation' element={<EvaluationPage />} />
        <Route path='/settings' element={<SettingPage />} />

        <Route path='*' element={<div className='p-8 text-center'>Page Not Found</div>} />
      </Route>
    </Routes>
  )
}
