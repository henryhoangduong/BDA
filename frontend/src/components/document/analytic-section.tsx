import React from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useQuery } from '@tanstack/react-query'
import { ingestionQueryFn } from '@/lib/api'
import { Database, Loader2, TimerIcon } from 'lucide-react'

const AnalyticSection = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents'],
    queryFn: ingestionQueryFn
  })
  return (
    <div className='grid grid-cols-4 gap-2'>
      <Card>
        <CardHeader className='flex flex-row items-center  gap-2'>
          <Database className='text-muted-foreground' />
          <div>
            <CardTitle>Total documents</CardTitle>
            <CardDescription>Total documents</CardDescription>
          </div>
        </CardHeader>
        <CardContent className='flex flex-row items-end gap-2'>
          <p className='text-6xl font-semibold'>{isLoading ? <Loader2 className='animate-spin' /> : data?.length}</p>
          <p className='text-muted-foreground'>documents</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className='flex flex-row items-center  gap-2'>
          <TimerIcon className='text-muted-foreground' />

          <div>
            <CardTitle>Last update</CardTitle>
            <CardDescription>Last update</CardDescription>
          </div>
        </CardHeader>
        <CardContent className='flex flex-row items-end gap-2'>
          <p className='text-6xl font-semibold'>2</p>
          <p className='text-muted-foreground'> days ago</p>
        </CardContent>
      </Card>
      {/* <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Card Content</p>
        </CardContent>
        <CardFooter>
          <p>Card Footer</p>
        </CardFooter>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Card Content</p>
        </CardContent>
        <CardFooter>
          <p>Card Footer</p>
        </CardFooter>
      </Card> */}
    </div>
  )
}

export default AnalyticSection
