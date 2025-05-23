import React from 'react'
import { ActiveTable } from 'active-table-react'

const EvaluationPage = () => {
  const data = [
    ['Question', 'Generated Answer'],
    ['Earth', 12756],
    ['Mars', 6792]
  ]
  return (
    <div className=''>
      <header className='p-4 w-full shadow-sm mb-5'>
        <p className='font-medium text-2xl'>Evaluation</p>
      </header>
      <ActiveTable
        data={data}
        headerStyles={{ default: { backgroundColor: '#d6d6d630' } }}
        tableStyle={{ position: 'relative', width: '90%', border: 'box-sizing' }}
      />
    </div>
  )
}

export default EvaluationPage
