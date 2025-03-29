import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiChevronDown } from 'react-icons/fi';
import forest from '/src/assets/forest.jpg'; // use your actual image path

const Hero = () => {
  const [text, setText] = useState('');
  const sayings = ["Save the planet.", "Go green, live clean.", "Be the change.", "Sustainability first."];
  const [index, setIndex] = useState(0);
  const typingSpeed = 100; // Speed of typing (ms per character)
  const erasingSpeed = 70; // Speed of erasing (ms per character)
  const pauseBetweenText = 1000; // Pause between each text before erasing

  useEffect(() => {
    let typingTimeout;
    let erasingTimeout;

    // Typing effect function
    const typeText = () => {
      let currentText = '';
      const currentSaying = sayings[index];
      let charIndex = 0;

      // Typing each character with setTimeout to control timing
      const typeCharacter = () => {
        currentText += currentSaying.charAt(charIndex);
        setText(currentText);
        charIndex++;

        if (charIndex < currentSaying.length) {
          typingTimeout = setTimeout(typeCharacter, typingSpeed); // Call recursively with timeout
        } else {
          // Once typing is complete, start erasing after a pause
          setTimeout(() => eraseText(), pauseBetweenText);
        }
      };

      // Start typing the first character
      typeCharacter();
    };

    // Erasing effect function (character-by-character)
    const eraseText = () => {
      let currentText = text;

      // Erasing each character one at a time
      const eraseCharacter = () => {
        currentText = currentText.slice(0, -1);
        setText(currentText);

        if (currentText.length > 0) {
          erasingTimeout = setTimeout(eraseCharacter, erasingSpeed); // Call recursively with timeout
        } else {
          // Once all text is erased, move to the next saying
          setIndex((prevIndex) => (prevIndex + 1) % sayings.length); // Move to the next saying
        }
      };

      // Start erasing the first character
      eraseCharacter();
    };

    // Start typing the first saying
    typeText();

    // Cleanup function to clear intervals when the component unmounts or re-renders
    return () => {
      clearTimeout(typingTimeout);
      clearTimeout(erasingTimeout);
    };
  }, [index]); // Runs when the index changes

  return (
    <div
      className="w-full bg-cover bg-center bg-no-repeat"
      style={{ backgroundImage: `url(${forest})` }}
    >
      <div className="w-full bg-black/60 px-4 py-24">
        <div className="max-w-[1240px] mx-auto text-center text-white px-8">
          <p className="text-[#A0FEC0] font-bold text-2xl">Get reports</p>
          <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4">
            Make earth better
          </h1>
          <p className="md:text-2xl text-xl font-medium text-gray-200">
            some good stuff
          </p>

          {/* Typing effect with a fixed or min-height container to prevent jumping */}
          <p
            className="md:text-xl text-lg font-light text-gray-300 mt-4"
            style={{ minHeight: "30px", overflow: "hidden" }} // Ensure the container doesn't shrink or jump
          >
            {text}
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 mt-10">
            <Link to="/business">
              <button className="bg-white text-[#1A1A1A] w-[200px] rounded-md font-medium py-3 hover:scale-105 transition-all duration-300 ease-in-out">
                For Businesses
              </button>
            </Link>
            <Link to="/individual">
              <button className="bg-[#00A86B] text-[#1A1A1A] w-[200px] rounded-md font-medium py-3 hover:scale-105 transition-all duration-300 ease-in-out">
                For Individuals
              </button>
            </Link>
          </div>

          <p className="text-gray-300 mt-10">Scroll for more information</p>
          <div className="mt-4 flex justify-center">
            <FiChevronDown className="text-3xl text-white animate-bounce" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
