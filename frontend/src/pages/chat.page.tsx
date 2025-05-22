import ChatFrame from '@/components/chat/chat-frame'
import { Message } from '@/types/chat'
import { useState } from 'react'

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>([])

  return (
    <div className='p-6 h-[100vh]'>
      <ChatFrame messages={messages} setMessages={setMessages} />
    </div>
  )
}

export default ChatPage
