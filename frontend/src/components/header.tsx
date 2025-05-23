import React from 'react'
import { Input } from './ui/input'

const Header = () => {
  return (
    <div className='w-full p-4 shadow-sm flex flex-row'>
      {' '}
      <div className='w-[30%]'>
        <Input type='text' className='pl-10 pr-20 sm:text-sm sm:leading-5' placeholder='Search products...' />
      </div>
    </div>
  )
}

export default Header
