import React from 'react'

const HomePage = () => {
  return (
    <div className="hero min-h-full flex-1" 
    style={{ 
      backgroundImage: `url("https://api.lorem.space/image/car?w=1000&h=800")` 
    }}>
  
  <div className="hero-overlay bg-opacity-60"></div>
  <div className="hero-content text-center text-neutral-content bg-opacity-80">
    <div className="max-w-md">
      <h1 className="mb-5 text-5xl font-bold">FARM Stack Cars App!</h1>
      <p className="mb-5">FastAPI + MongoDB + React and some really affordable cars.</p>
      <button className="btn btn-secondary">Get Started</button>
    </div>
  </div>
</div>
  )
}

export default HomePage