import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { SidebarTrigger } from '@/components/ui/sidebar'
import { ArrowRight } from 'lucide-react'

const OverviewPage = () => {
  return (
    <div className='p-[100px] relative'>
      <SidebarTrigger className='absolute left-0 top-0' />
      <h1 className='text-5xl font-medium mb-5 '>👋 Welcome User!</h1>
      <span className='text-gray-400 dark:text-muted '>Get started with BDA</span>
      <div className='grid grid-cols-2 gap-5 mt-[50px]'>
        <Card className='hover:shadow-md cursor-pointer bg-[#FA500E]'>
          <CardHeader>
            <CardTitle className='text-xl text-white'>Create an agent</CardTitle>
            <CardDescription className='text-white'>
              Use models, instructions and demonstrations to create a custom agent to deploy chat AI
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <ArrowRight className='text-right ml-auto text-white' />
          </CardFooter>
        </Card>
      </div>
      <div className=' mt-[50px]'>
        <p className='text-lg font-semibold mb-5'>Quick Start</p>
        <div className=' grid grid-cols-2 gap-5'>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader className='flex flex-row items-center'>
              <CardTitle>API Request</CardTitle>
            </CardHeader>
          </Card>
        </div>
      </div>
      <div className='mt-[50px]'>
        <p className='text-lg font-semibold mb-5'>Docs</p>
        <div className=' grid grid-cols-2 gap-5'>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>RAG</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Text Generation</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Embeddings</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Guardrailing</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Function Calling</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Prompt Engineering</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Structured outputs</CardTitle>
            </CardHeader>
          </Card>
          <Card className='hover:shadow-md cursor-pointer'>
            <CardHeader>
              <CardTitle>Deployment</CardTitle>
            </CardHeader>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default OverviewPage
