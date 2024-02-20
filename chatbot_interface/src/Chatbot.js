import React, { useState } from 'react';
import './App.css'

// fetch(process.env.REACT_APP_CHATBOT_API_IP)
//   .then(response => {
//     console.log(response);
//     response.json();
//   })
//   .then(data => console.log(data))
//   .catch(error => console.error('Error fetching data: ', error));

function Chatbot() {
  const preparedMessage = { text: 'Hello there,\nI am your personal assistant for the street science days in L\'Aquila.\n\nYou can tell me what you want to do and I will help you.\n\nI can help you with the following:\n - Parking recommendations\n - Getting weather information\n - Checking ticket availability for events\n - Booking tickets for events', sender: 'bot'};
  const convertStringToReact = (inputString) => {
    const lines = inputString.split('\n');
  
    return lines.map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index !== lines.length - 1 && <br />} {/* Add <br> except for the last line */}
      </React.Fragment>
    ));
  };

  const [messages, setMessages] = useState([preparedMessage]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(null);
  const [notepad, setNotepad] = useState(null);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const messageEmpty = () => {
    return input.trim() === ''
  }

  const handleEnter = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = () => {
    if (messageEmpty()) return;

    setError(null)
  
    const newMessages = [...messages, { text: input, sender: 'user' }];
    setMessages(newMessages);
    const currInput = input
    setInput('');
  
    const fetchBotResponse = async () => {
      try {
        setIsLoading(true)
        const dataToSend = { 
          'notepad': notepad,
          'message': currInput,
          'status': status,
        };
        const response = await fetch('http://127.0.0.1:5001/api/chatbot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(dataToSend),
        }); 
        console.log(response);
  
        if (!response.ok) {
          const data = await response.json();
          throw new Error(`HTTP error! status: ${response.status}, error: ${data.error}`);
        }
  
        const data = await response.json();

        
        setStatus(data.status)
        setNotepad(data.notepad)
        setMessages(prevMessages => [...prevMessages, { text: data.message, sender: 'bot' }]);
      } catch (error) {
        setError(error)
        console.error("Fetching bot response failed:", error);
      } finally {
        setIsLoading(false)
      }

    }
    fetchBotResponse();
  }

  let buttonText = isLoading ? "Loading..." : "Send"

  return (
    <div className="chatbot">
        <div className="chatbot_header">
            State Your Goal
        </div>
        <div className="chatbot_history"> 
            {messages.map((message, index) => {
                const message_by = message.sender === 'bot' ? 'message_by_bot' : 'message_by_user'
                const sender = message.sender === 'bot' ? 'Bot' : 'You'
                return (
                    <div key={index} className={`chatbot_message_row ${message_by} `}>
                        <div className="message_bubble">
                            <div className="sender">{sender}</div>
                            <div className="message">{convertStringToReact(message.text)}</div>
                        </div>
                    </div>
                )
            })}
            { error !== null ? <div className='error'>{error.message}</div> : null}
        </div>
        <div className="chatbot_input_area">
            <textarea
                className="chatbot_input"
                value={input}
                onChange={handleInputChange}
                placeholder="Type here..."
                onKeyDown={handleEnter}
            />
            <button 
              className={`chatbot_submit`} 
              onClick={handleSendMessage} 
              disabled={messageEmpty() || isLoading}
            >{buttonText}</button>
        </div>
    </div>
  );
}

export default Chatbot;
