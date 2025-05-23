import ChatFrame from '@/components/chat/chat-frame'
import { Message } from '@/types/chat'
import { useState } from 'react'

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>([])

  return (
    <div className='h-[100vh] flex flex-col'>
      <header className='p-4 w-full shadow-sm mb-5'>
        <p className='font-medium text-2xl'>Chat</p>
      </header>
      <div className='flex-1 p-6'>
        <ChatFrame messages={messages} setMessages={setMessages} />
      </div>
    </div>
  )
}

export default ChatPage
