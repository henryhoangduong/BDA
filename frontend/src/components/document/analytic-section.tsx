import React from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useQuery } from '@tanstack/react-query'
import { ingestionQueryFn } from '@/lib/api'

const AnalyticSection = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents'],
    queryFn: ingestionQueryFn
  })
  return (
    <div className='grid grid-cols-4 gap-2'>
      <Card>
        <CardHeader>
          <CardTitle>Total documents</CardTitle>
          <CardDescription>Total documents</CardDescription>
        </CardHeader>
        <CardContent>
          <p className='text-6xl font-semibold'>{data?.length}</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Last update</CardTitle>
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
      </Card>
    </div>
  )
}

export default AnalyticSection
