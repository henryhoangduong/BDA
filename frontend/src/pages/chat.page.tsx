import ChatFrame from '@/components/chat/chat-frame'
import { Message } from '@/types/chat'

const ChatPage = () => {
  const messages: Message[] = [
    {
      id: 'id-1234',
      role: 'assistant',
      content: 'content',
      state: { sources: [{ file_name: 'abdc.pdf' }] },
      followUpQuestions: ['what is this']
    },
    {
      id: 'id-234',
      role: 'user',
      content: 'conent'
    }
  ]
  return (
    <div>
      <ChatFrame messages={messages} />
    </div>
  )
}

export default ChatPage
