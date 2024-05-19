import React from 'react';
import { data } from "../data/data.js";
import './Work.css'
import Navbar from "./Navbar.jsx";

const Work = () => {

    // projects file
    const project = data;
    //setProject(data);
  
  return (
    <div name='work' className='w-full md:h-screen text-gray-300 bg-[#0a192f]'>
      <Navbar />
      {/* Container */}
      <div className='max-w-[1000px] mx-auto p-4 flex flex-col justify-center w-full h-full'>
        <div className='pb-8'>
          <p className='text-4xl font-bold inline border-b-4 text-gray-300 border-pink-600'>
            Reviews
          </p>
        </div>

{/* container for projects */}
<div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          
          {/* Grid Item */}
          {project.map((item, index) => (
  <div
    key={index}
    style={{ backgroundImage: `url(${item.image})` }}
    className="shadow-lg shadow-[#040c16] group container rounded-md 
              flex justify-center text-center items-center mx-auto content-div "
  >
    {/* Hover effect for images */}
    <div>
    <span className="hovered ">
        {item.name}
      </span>
    </div>
  </div>
))}
</div>
      </div>
    </div>
  );
};

export default Work;
