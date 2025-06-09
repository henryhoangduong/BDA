import React, { useState } from 'react'
import { Card, CardContent, CardFooter } from '../ui/card'
import { Message } from '@/types/chat'
import ChatMessage from './chat-message'
import Thinking from './thinking'
import { Button } from '../ui/button'
import { Paperclip, Send } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/tooltip'
import { Input } from '../ui/input'
import { handleChatStream, sendMessage } from '@/lib/api'
interface ChatFrameProps {
  messages: Message[]
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
  //   onUploadClick: () => void
}
const ChatFrame = ({ messages, setMessages }: ChatFrameProps) => {
  const [isThinking, setIsThinking] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [inputMessage, setInputMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const userTimestamp = Date.now()
    const botTimestamp = userTimestamp + 1

    const userMessage: Message = {
      id: `user-${userTimestamp}`,
      role: 'user',
      content: inputMessage.trim()
    }
    setMessages((prev) => [...prev, userMessage])
    setIsThinking(true)
    setInputMessage('')
    setIsLoading(true)
    try {
      const response = await sendMessage(userMessage.content)
      const assistantMessage: Message = {
        id: `assistant-${botTimestamp}`,
        role: 'assistant',
        content: '',
        streaming: true,
        state: {},
        followUpQuestions: []
      }
      setMessages((prev) => [...prev, assistantMessage])
      await handleChatStream(
        response,
        (content, state) => {
          setMessages((prev) => {
            const lastMessage = prev[prev.length - 1]
            if (lastMessage && lastMessage.id === assistantMessage.id) {
              return [
                ...prev.slice(0, -1),
                {
                  ...lastMessage,
                  content: content ? lastMessage.content + content : lastMessage.content,
                  state: state || lastMessage.state,
                  followUpQuestions: state?.followUpQuestions || lastMessage.followUpQuestions
                }
              ]
            }
            return prev
          })
        },
        () => {
          setMessages((prev) => {
            const lastMessage = prev[prev.length - 1]
            if (lastMessage && lastMessage.id === assistantMessage.id) {
              return [...prev.slice(0, -1), { ...lastMessage, streaming: false }]
            }
            return prev
          })
          setIsLoading(false)
        }
      )
    } catch (error) {
      console.error('Error:', error)
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: 'Sorry, something went wrong. Please try again.'
        }
      ])
    } finally {
      setIsLoading(false)
      setIsThinking(false)
    }
  }
  const onUploadClick = async () => {}
  return (
    <Card className='h-full flex flex-col'>
      <CardContent className='flex-1 overflow-y-auto p-4 space-y-4'>
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
        {isThinking && <Thinking />}
      </CardContent>
      <CardFooter className='p-4 border-t'>
        <form onSubmit={handleSubmit} className='flex w-full gap-2 items-center'>
          <div className='flex-1 flex items-center gap-2 px-3 py-2 rounded-lg border bg-white'>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    type='button'
                    variant='ghost'
                    size='icon'
                    onClick={onUploadClick}
                    className='h-8 w-8 hover:bg-transparent p-0'
                  >
                    <Paperclip className='h-5 w-5 text-gray-500 rotate-45' />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Upload document</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder='Type a message...'
              disabled={isLoading}
              className='border-0 shadow-none focus-visible:ring-0 focus-visible:ring-offset-0 px-0'
            />
          </div>
          <Button type='submit' disabled={isLoading || !inputMessage.trim()}>
            <Send className='h-4 w-4' />
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}

export default ChatFrame
