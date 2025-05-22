import React from 'react'
import { Badge } from '../ui/badge'

const ParsingStatus = ({ status }: { status: string }) => {
  return <Badge variant='secondary'>{status}</Badge>
}

export default ParsingStatus
