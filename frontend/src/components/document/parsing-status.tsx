import React from 'react'
import { Badge } from '../ui/badge'

const ParsingStatus = ({ status }: { status: string }) => {
  return (
    <Badge variant={status == 'SUCCESS' ? 'success' : 'warning'} className='w-max'>
      {status}
    </Badge>
  )
}

export default ParsingStatus
