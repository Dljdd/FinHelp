import React from 'react';
import Navbar from "./Navbar.jsx";

const About = () => {
  return (
    <div name='about' className='w-full h-screen bg-[#0a192f] text-gray-300'>
      <Navbar />
      <div className='flex flex-col justify-center items-center w-full h-full'>
        <div className='max-w-[1000px] w-full grid grid-cols-2 gap-8'>
          <div className='sm:text-right pb-8 pl-4'>
            <p className='text-4xl font-bold inline border-b-4 border-pink-600'>
              About Us
            </p>
          </div>
          <div></div>
          </div>
          <div className='max-w-[1000px] w-full grid sm:grid-cols-2 gap-8 px-4'>
            <div className='sm:text-right text-4xl font-bold'>
              <p>We like to help connect companies to candidates and we're good at it.</p>
            </div>
            <div>
              <p>We have successfully connected 10,000+ candidates to over 100 MNCs and counting, solidifying our position as a leading digital recruitment solution. Our platform, Recruit+, has revolutionized the hiring process, providing a seamless and efficient experience for both candidates and companies. Through advanced technology and comprehensive screening tools, we ensure that top talent meets exceptional opportunities. Our dedicated team works tirelessly to match the right candidates with the right positions, fostering long-term partnerships and driving business growth. With a proven track record of successful placements and satisfied clients, we continue to make strides in transforming the recruitment landscape. Join Recruit+ today and experience the future of hiring firsthand.</p>  
            </div>
          </div>
      </div>
    </div>
  );
};

export default About;
