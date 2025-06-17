import { Route, Routes } from 'react-router-dom'
import { MainLayout } from './layout/main.layout'
import DocumentPage from './pages/document.page'
import ChatPage from './pages/chat.page'
import SettingPage from './pages/setting.page'
import SignupPage from './pages/auth/signup.page'
import { ProtectedRoute } from './context/AuthContext'
import LoginPage from './pages/auth/login.page'
import OverviewPage from './pages/overview.page'

export const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route
          path='/'
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />
        <Route
          path='/documents'
          element={
            <ProtectedRoute>
              <DocumentPage />
            </ProtectedRoute>
          }
        />
        <Route
          path='/overview'
          element={
            <ProtectedRoute>
              <OverviewPage />
            </ProtectedRoute>
          }
        />
        <Route
          path='/settings'
          element={
            <ProtectedRoute>
              <SettingPage />
            </ProtectedRoute>
          }
        />
        <Route path='*' element={<div className='p-8 text-center'>Page Not Found</div>} />
        <Route path='/auth/signup' element={<SignupPage />} />
        <Route path='/auth/login' element={<LoginPage />} />
      </Route>
    </Routes>
  )
}
