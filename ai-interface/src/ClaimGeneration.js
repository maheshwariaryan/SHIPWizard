import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import UnderstandingSHIP from './UnderstandingSHIP';
import ClaimGeneration from './ClaimGeneration'; 
import './App.css';

const FileDownloadButton = () => {
  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = process.env.PUBLIC_URL + '/filled_template.docx';
    link.download = 'filled_template.docx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <button 
      onClick={handleDownload} 
      style={{ 
        padding: '10px 20px', 
        borderRadius: '10px', 
        backgroundColor: '#1c1c1c', 
        color: 'white', 
        border: 'none', 
        cursor: 'pointer',
        marginTop: '20px'
      }}
    >
      Download File
    </button>
  );
};

function HomePage() {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const [showDownload, setShowDownload] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    // Save state to localStorage when it changes
    useEffect(() => {
        if (response || showDownload || submitted) {
            localStorage.setItem('appState', JSON.stringify({
                response,
                showDownload,
                submitted
            }));
        }
    }, [response, showDownload, submitted]);

    // Load state from localStorage on component mount
    useEffect(() => {
        const savedState = localStorage.getItem('appState');
        if (savedState) {
            const { response: savedResponse, showDownload: savedShowDownload, submitted: savedSubmitted } = JSON.parse(savedState);
            setResponse(savedResponse || '');
            setShowDownload(savedShowDownload || false);
            setSubmitted(savedSubmitted || false);
        }
    }, []);

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const sendInput = async () => {
        setIsLoading(true);
        try {
            const res = await fetch('http://localhost:5678/webhook/2e369d11-bd48-403f-9fd4-04b647b2ca57', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    input,
                    fileId: 3
                }),
            });
            const data = await res.text();
            const formattedResponse = data.replace(/\n/g, '\n') || 'No response received';
            setResponse(formattedResponse);
            setShowDownload(true);
            setSubmitted(true);
            
            // Save the current state immediately after submission
            localStorage.setItem('appState', JSON.stringify({
                response: formattedResponse,
                showDownload: true,
                submitted: true
            }));
        } catch (error) {
            console.error('Error:', error);
            setResponse('Error occurred. Please check the console for details.');
        } finally {
            setIsLoading(false);
        }
    };

    const clearState = () => {
        setInput('');
        setResponse('');
        setShowDownload(false);
        setSubmitted(false);
        localStorage.removeItem('appState');
    };

    return (
        <div className="app-wrapper" style={{ backgroundColor: '#000', minHeight: '100vh', padding: '20px' }}>
            <header className="app-header" style={{ backgroundColor: '#000', color: 'white', padding: '10px 20px' }}>
                <h2 className="app-title">Claim Approval Assistant</h2>
            </header>
            <div className="container" style={{borderRadius: '20px', padding: '70px', maxWidth: '90%', margin: '40px auto'}}>
                <h1 id="centered-text">We'll help you file a claim based on your condition.</h1>
                
                {!submitted ? (
                    <>
                        <textarea
                            value={input}
                            onChange={handleInputChange}
                            placeholder="Enter details of your injury here..."
                            style={{ 
                                width: '100%', 
                                padding: '10px', 
                                borderRadius: '10px', 
                                border: 'none', 
                                marginBottom: '20px' 
                            }}
                        />
                        <br />
                        <button 
                            onClick={sendInput} 
                            disabled={isLoading} 
                            style={{ 
                                padding: '10px 20px', 
                                borderRadius: '10px', 
                                backgroundColor: '#1c1c1c', 
                                color: 'white', 
                                border: 'none', 
                                cursor: 'pointer' 
                            }}
                        >
                            {isLoading ? 'Loading...' : 'Submit'}
                        </button>
                    </>
                ) : (
                    <div style={{ marginBottom: '20px' }}>
                        <button 
                            onClick={clearState}
                            style={{ 
                                padding: '10px 20px', 
                                borderRadius: '10px', 
                                backgroundColor: '#1c1c1c', 
                                color: 'white', 
                                border: 'none', 
                                cursor: 'pointer',
                                marginRight: '10px'
                            }}
                        >
                            Submit New Claim
                        </button>
                    </div>
                )}

                {response && (
                    <div className="response" style={{ 
                        marginTop: '20px', 
                        whiteSpace: 'pre-wrap',
                        backgroundColor: '#1c1c1c',
                        padding: '20px',
                        borderRadius: '10px',
                        color: 'white'
                    }}>
                        {response.split('\n').map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                )}
                
                {showDownload && <FileDownloadButton />}
            </div>

            {/* Floating button */}
            <button
                onClick={toggleMenu}
                style={{
                    position: 'fixed',
                    bottom: '30px',
                    right: '30px',
                    backgroundColor: '#1c1c1c',
                    borderRadius: '50%',
                    width: '60px',
                    height: '60px',
                    color: 'white',
                    border: 'none',
                    fontSize: '30px',
                    cursor: 'pointer',
                    boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 1000,
                }}
            >
                +
            </button>

            {/* Menu */}
            {menuOpen && (
                <div
                    style={{
                        position: 'fixed',
                        bottom: '100px',
                        right: '30px',
                        backgroundColor: '#fff',
                        borderRadius: '10px',
                        boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)',
                        width: '200px',
                        padding: '10px',
                        zIndex: 1000,
                    }}
                >
                    <Link
                        to="/"
                        style={{
                            display: 'block',
                            padding: '10px',
                            borderBottom: '1px solid #ddd',
                            cursor: 'pointer',
                            textDecoration: 'none',
                            color: '#000',
                        }}
                    >
                        Understanding SHIP
                    </Link>

                    <Link
                        to="/understanding-ship"
                        style={{
                            display: 'block',
                            padding: '10px',
                            cursor: 'pointer',
                            textDecoration: 'none',
                            color: '#000',
                        }}
                    >
                        Insurance Terminologies
                    </Link>

                    <Link
                        to="/claim-generation"
                        style={{
                            display: 'block',
                            padding: '10px',
                            cursor: 'pointer',
                            textDecoration: 'none',
                            color: '#000',
                        }}
                    >
                        Claim Approval Assistant
                    </Link>
                </div>
            )}
        </div>
    );
}

export default HomePage;