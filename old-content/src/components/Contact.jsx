import React from 'react'

const Contact = () => {
  const searchFunc = () => {
    let filter1 = document.getElementById('locationInput').value.toUpperCase();
    let filter2 = document.getElementById('roleInput').value.toUpperCase();
    let myTable = document.getElementById('myTable');
    let tr = myTable.getElementsByTagName('tr');
    for (let i = 0; i < tr.length; i++) {
      let location = tr[i].getElementsByTagName('td')[2];
      let role = tr[i].getElementsByTagName('td')[1];
      if (location && role) {
        let locationText = location.textContent || location.innerText;
        let roleText = role.textContent || role.innerText;

        if (
          locationText.toUpperCase().indexOf(filter1) > -1 &&
          roleText.toUpperCase().indexOf(filter2) > -1
        ) {
          tr[i].style.display = '';
        } else {
          tr[i].style.display = 'none';
        }
      }
    }
  };
  return (
    <div name='CandidateList' className='w-full h-screen bg-[#0a192f] flex justify-center items-center p-4'>
    
        <form method='POST' action="https://getform.io/f/a699a1b2-f225-434e-b317-1fbbde8e006c" className='flex flex-col max-w-[600px] w-full'>
            <div className='pb-8'>
                <p className='text-4xl font-bold inline border-b-4 border-pink-600 text-gray-300'>Candidate List</p>
            </div>
            <input type = 'text' name='' id='locationInput' placeholder='Location' onKeyUp={searchFunc}></input>
    <input type = 'text' name='' id='roleInput' placeholder='Job role' onKeyUp={searchFunc}></input>
    
        </form>
      <div className='table-container'>
            

    {/* <button className="search" onClick={searchFunc()}>SEARCH</button> */}

        <table className="min-w-full bg-white" id='myTable'>
  <thead>
    <tr>
      <th>Name</th>
      <th>Job Role</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>Software Engineer</td>
      <td>New York</td>
    </tr>
    <tr>
      <td>Jane Smith</td>
      <td>Product Manager</td>
      <td>San Francisco</td>
    </tr>
    <tr>
      <td>Mike Johnson</td>
      <td>UI/UX Designer</td>
      <td>London</td>
    </tr>
    <tr>
      <td>Emily Davis</td>
      <td>Data Scientist</td>
      <td>Chicago</td>
    </tr>
    <tr>
      <td>David Lee</td>
      <td>Marketing Specialist</td>
      <td>Toronto</td>
    </tr>
    <tr>
      <td>Sarah Thompson</td>
      <td>Project Manager</td>
      <td>Seattle</td>
    </tr>
    <tr>
      <td>Michael Chen</td>
      <td>Full Stack Developer</td>
      <td>Sydney</td>
    </tr>
    <tr>
      <td>Lisa Rodriguez</td>
      <td>Graphic Designer</td>
      <td>Mexico City</td>
    </tr>
    <tr>
      <td>Ryan Patel</td>
      <td>Business Analyst</td>
      <td>Mumbai</td>
    </tr>
    <tr>
      <td>Emma Kim</td>
      <td>UX Researcher</td>
      <td>Seoul</td>
    </tr>
    <tr>
      <td>Adam Wilson</td>
      <td>Software Developer</td>
      <td>Paris</td>
    </tr>
    <tr>
      <td>Natalie Brown</td>
      <td>Product Designer</td>
      <td>Berlin</td>
    </tr>
    <tr>
      <td>Chris Thompson</td>
      <td>Frontend Developer</td>
      <td>Los Angeles</td>
    </tr>
    <tr>
      <td>Olivia Chen</td>
      <td>Marketing Manager</td>
      <td>Hong Kong</td>
    </tr>
    <tr>
      <td>Jason Taylor</td>
      <td>Database Administrator</td>
      <td>Dallas</td>
    </tr>
    <tr>
      <td>Victoria Hernandez</td>
      <td>UI Designer</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <td>Daniel Park</td>
      <td>Software Engineer</td>
      <td>Seoul</td>
    </tr>
    <tr>
      <td>Amy Johnson</td>
      <td>Content Writer</td>
      <td>Sydney</td>
    </tr>
    <tr>
      <td>Justin Lee</td>
      <td>Mobile App Developer</td>
      <td>Toronto</td>
    </tr>
    <tr>
      <td>Sophia Nguyen</td>
      <td>Product Manager</td>
      <td>San Francisco</td>
    </tr>
  </tbody>
</table>
    </div>
    </div>
  )
}

export default Contact