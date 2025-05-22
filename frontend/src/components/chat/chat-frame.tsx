import React from 'react'
import { Card, CardContent, CardHeader } from '../ui/card'
import { Message } from '@/types/chat'
import ChatMessage from './chat-message'
import Thinking from './Thinking'
interface ChatFrameProps {
  messages: Message[]
}
const ChatFrame = ({ messages }: ChatFrameProps) => {
  return (
    <Card className='h-full flex flex-col'>
      <CardContent>
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            isAi={message.role === 'assistant'}
            message={message.content}
            streaming={message.streaming}
            followUpQuestions={message.followUpQuestions}
            onFollowUpClick={() => {}}
            state={message.state}
          />
        ))}
        {true && <Thinking />}
      </CardContent>
    </Card>
  )
}

export default ChatFrame
