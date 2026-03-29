// import React, { useState, useEffect } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import '../styles/Sidebar.css';
// import { assets } from '../assets/assets';
// import { useNavigate } from 'react-router-dom';

// const useWindowSize = () => {
//   const [width, setWidth] = useState(window.innerWidth);
//   useEffect(() => {
//     const handleResize = () => setWidth(window.innerWidth);
//     window.addEventListener('resize', handleResize);
//     return () => window.removeEventListener('resize', handleResize);
//   }, []);
//   return width;
// };

// const Sidebar = ({ visible, setSidebarVisible }) => {
//   const [extended, setExtended] = useState(true);
//   const navigate = useNavigate();
//   const windowWidth = useWindowSize();

//   const handleClick = (path) => {
//     navigate(path);
//     if (windowWidth <= 500) setSidebarVisible(false); // close sidebar on mobile after click
//   };

//   return (
//     <>
//       {/* Overlay for mobile */}
//       {visible && windowWidth <= 500 && (
//         <div className="overlay" onClick={() => setSidebarVisible(false)}></div>
//       )}

//       <motion.div
//         className="sidebar"
//         animate={{
//           // x: visible ? 0 : -260,
//           width: extended ? 260 : 60
//         }}
//         transition={{ duration: 0.0, ease: [0.25, 0.8, 0.25, 1] }}
//       >
//         {/* Top Section */}
//         <div className="top">
//           <div className="sidebar-logo">
//             <img src={assets.logo} onClick={() => setExtended(prev => !prev)}
//               alt="Toggle menu"
//               aria-expanded={extended}
//               aria-label="Toggle sidebar" />
//             {extended && (<img
//               className="menu"
//               onClick={() => setExtended(prev => !prev)}
//               src={assets.menu_icon}
//             />)}
//           </div>
//           <AnimatePresence>
//             {extended && (
//               <motion.div
//                 className="tabs"
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 exit={{ opacity: 0 }}
//                 transition={{ duration: 0.15 }}
//               >
//                 <button onClick={() => handleClick('/fivelens')}>5-Lens</button>
//                 <button onClick={() => handleClick('/relivency')}>Relivency</button>
//                 <button onClick={() => handleClick('/opportunity')}>Opportunity</button>
//               </motion.div>
//             )}
//           </AnimatePresence>
//         </div>

//         {/* Bottom Section */}
//         <div className="bottom">
//           <AnimatePresence>
//             {extended && (
//               <motion.div
//                 key="bottom"
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 exit={{ opacity: 0 }}
//                 transition={{ duration: 0.3 }}
//                 className="bottom-item"
//               >
//                 <div className="bottomUp">
//                   <div className="new-chat">
//                     {extended && (<img src={assets.plus_icon} alt="New chat" />)}
//                     <p>New Chat</p>
//                   </div>

//                   <div className="recent">
//                     <div className="recent-title">Chats</div>
//                     <div className="recent-entry">
//                       <p>What is React ...</p>
//                     </div>
//                   </div>
//                 </div>
//               </motion.div>
//             )}
//           </AnimatePresence>
//         </div>

//        {extended && (
//         <div className="recent-entry">
//             <img src={assets.setting_icon} alt="Settings" />
//           <p onClick={() => handleClick('/settings')}>Settings</p>
//         </div>
//        )} 
//       </motion.div>
//     </>
//   );
// };

// export default Sidebar;

// import React, { useState, useEffect } from 'react';
// import { motion, AnimatePresence } from 'framer-motion';
// import '../styles/Sidebar.css';
// import { assets } from '../assets/assets';
// import { useNavigate } from 'react-router-dom';

// const useWindowSize = () => {
//   const [width, setWidth] = useState(window.innerWidth);
//   useEffect(() => {
//     const handleResize = () => setWidth(window.innerWidth);
//     window.addEventListener('resize', handleResize);
//     return () => window.removeEventListener('resize', handleResize);
//   }, []);
//   return width;
// };

// const Sidebar = ({ visible, setSidebarVisible }) => {
//   const [extended, setExtended] = useState(true);
//   const navigate = useNavigate();
//   const windowWidth = useWindowSize();
//   const isMobile = windowWidth <= 500;

//   useEffect(() => {
//     if (isMobile && visible) {
//       setExtended(true);
//     }
//     else if (isMobile && !visible) {
//       setExtended(false);
//     }
//   }, [isMobile, visible]);


//   const handleClick = (path) => {
//     navigate(path);
//     if (isMobile) setSidebarVisible(false);
//   };

//   const getAnimationProps = () => {
//     if (isMobile) {
//       return {
//         x: visible ? 0 : -270,
//         width: extended ? 230 : 60,
//       };
//     } else {
//       return {
//         x: 0,
//         width: extended ? 230 : 60,
//       };
//     }
//   };


//   return (
//     <>
//       {/* Overlay for mobile */}
//       {visible && isMobile && (
//         <div className="overlay" onClick={() => setSidebarVisible(false)}></div>
//       )}

//       <motion.div
//         className="sidebar"
//         animate={getAnimationProps()} // Dynamic animation props
//         transition={{
//           duration: 0.2,
//           ease: [0.25, 0.8, 0.25, 1],
//         }}
//         style={{
//           zIndex: 50,
//           position: isMobile ? 'fixed' : 'relative',
//           overflowX: 'hidden',
//         }}
//       >
//         {/* Top Section */}
//         <div className="top">
//           <div className="sidebar-logo">
//             <img src={assets.logo} onClick={() => setExtended(prev => !prev)}
//               alt="Toggle menu"
//               aria-expanded={extended}
//               aria-label="Toggle sidebar"
//               style={{ cursor: "pointer " }} />
//             {extended && (<img
//               className="menu"
//               onClick={() => setExtended(prev => !prev)}
//               src={assets.menu_icon}
//             />)}
//           </div>

//           <AnimatePresence>
//             {extended && (
//               <motion.div
//                 className="tabs"
//                 initial={{ opacity: 0, x: -10 }}
//                 animate={{ opacity: 1, x: 0 }}
//                 exit={{ opacity: 0, x: -10 }}
//                 transition={{ duration: 0.15 }}
//               >
//                 <button onClick={() => handleClick('/fivelens')}>5-Lens</button>
//                 <button onClick={() => handleClick('/relivency')}>Relivency</button>
//                 <button onClick={() => handleClick('/opportunity')}>Opportunity</button>
//               </motion.div>
//             )}
//           </AnimatePresence>
//         </div>

//         {/* Bottom Section */}
//         <div className="bottom">
//           <AnimatePresence>
//             {extended && (
//               <motion.div
//                 key="bottom"
//                 initial={{ opacity: 0 }}
//                 animate={{ opacity: 1 }}
//                 exit={{ opacity: 0 }}
//                 transition={{ duration: 0.3 }}
//                 className="bottom-item"
//               >
//                 <div className="bottomUp">
//                   <div className="new-chat">
//                     {extended && (<img src={assets.plus_icon} alt="New chat" />)}
//                     <p>New Chat</p>
//                   </div>

//                   <div className="recent">
//                     <div className="recent-title">Chats</div>
//                     <div className="recent-entry">
//                       <p>What is React ...</p>
//                     </div>
//                   </div>
//                 </div>
//               </motion.div>)}
//           </AnimatePresence>
//         </div>
//         {extended && (
//         <div className="recent-entry">
//             <img src={assets.setting_icon} alt="Settings" />
//           <p onClick={() => handleClick('/settings')}>Settings</p>
//         </div>
//        )} 
//       </motion.div>
//     </>
//   );
// };

// export default Sidebar;


import { react, useState } from 'react'
import { assets } from '../assets/assets';
import { useNavigate } from 'react-router-dom';
import { HiLightBulb } from "react-icons/hi";
import { FaBridge } from "react-icons/fa6";
import { PiNumberSquareFiveBold } from "react-icons/pi";
import { IoIosSettings } from "react-icons/io";


const Sidebar = ({ open, setOpen }) => {
  // const [open, setOpen] = useState(false)
  const navigate = useNavigate();


  const menuItems = [
    {
      icons: <PiNumberSquareFiveBold size={30} />,
      label: 'Fivelens',
      path: '/fivelens', // Example path
    },
    {
      icons: <FaBridge size={30} />,
      label: 'Relivency',
      path: '/relivency', // Example path
    },
    {
      icons: <HiLightBulb size={30} />,
      label: 'Opportunity',
      path: '/opportunity', // Example path
    }
  ];

  // Function to handle navigation
  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    // <nav className={`shadow-md h-screen p-2 flex flex-col duration-500 bg-[rgba(255,255,255,0.5)] backdrop-blur-2xl  ${open ? 'w-60' : 'w-16'}`}>

    <nav className={`
  shadow-md h-screen p-2 flex flex-col duration-500 bg-[rgba(255,255,255,0.5)] backdrop-blur-2xl
  
      fixed left-0 top-0 z-50 transform 
      ${open ? 'translate-x-0 w-60 opacity-100 pointer-events-auto' : '-translate-x-200 w-0 opacity-0 pointer-events-none'}
         
      md:w-16 md:translate-x-0 md:relative md:visible md:flex md:opacity-100 md:pointer-events-auto
      ${open ? 'md:w-60' : 'md:w-16'} 
      
  `}>
      <div className="overlay" onClick={() => setOpen(false)}></div>
      {/* Header */}
      <div className='p-3 h-13 flex justify-between items-center'>
        <img src={assets.logo} alt="Logo" className={`${open ? 'w-6' : 'w-0'} rounded-md`} />
        <div><img src={assets.menu_icon} className={`w-5 duration-500 cursor-pointer ${!open && ' rotate-180'}`} onClick={() => setOpen(!open)} /></div>
      </div>

      {/* Body */}

      <ul className='flex-1'>
        {
          menuItems.map((item, index) => {
            return (
              <li key={index} className='my-3 px-2.5 py-2 hover:bg-[rgba(255,255,255,0.5)] shadow-sm/10 hover:shadow-[#1ab2b8] rounded-md duration-300 cursor-pointer 
              flex gap-2 items-center relative group' onClick={() => handleNavigation(item.path)}>
                <div className={`md:block ${!open && 'hidden'}`}>                  {item.icons}</div>
                <p className={`${!open && 'w-0 translate-x-20'} duration-400 overflow-hidden`}>{item.label}</p>
                <p className={`${open && 'hidden'} absolute left-32 shadow-md rounded-full
                 w-0 p-0 text-black bg-white duration-100 overflow-hidden text-xs group-hover:w-fit group-hover:p-2 group-hover:left-16
                `}>{item.label}</p>
              </li>

            )
          })
        }
      </ul>

      {/* footer */}
      <div className='flex items-center gap-2 px-2.5 py-2 cursor-pointer hover:bg-[rgba(255,255,255,0.5)] rounded-md' onClick={() => navigate("/settings")}>
        <div className={`md:block ${!open && 'hidden'}`}><IoIosSettings size={26} /></div>
        <div className={`leading-5 ${!open && 'w-0 translate-x-24'} duration-500 overflow-hidden`}>
          <p>Settings</p>
        </div>
      </div>


    </nav>
  )
}

export default Sidebar;