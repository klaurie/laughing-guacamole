import React from 'react'

const Container = ({
  children
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <div
      className='container mx-auto px-10 lg:px-20 max-w-7xl'
    >{children}</div>
  )
}

export default Container