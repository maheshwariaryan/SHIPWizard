import React from 'react';
import { useState } from 'react';
import { Link } from 'react-router-dom';

function UnderstandingSHIP() {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const sendInput = async () => {
        setIsLoading(true);
        setResponse('');
        try {
            const res = await fetch('http://localhost:5678/webhook/2e369d11-bd48-403f-9fd4-04b647b2ca57', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    input,
                    fileId: 2
                }),
            });
            const data = await res.text();
            // Format the response by replacing newline characters with actual line breaks
            setResponse(data.replace(/\n/g, '\n') || 'No response received');
        } catch (error) {
            console.error('Error:', error);
            setResponse('Error occurred. Please check the console for details.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-wrapper" style={{ backgroundColor: '#000', minHeight: '100vh', padding: '20px' }}>
            <header className="app-header" style={{ backgroundColor: '#000', color: 'white', padding: '10px 20px' }}>
                <h2 className="app-title">Insurance Terminologies 101</h2>
            </header>
            <div className="container" style={{borderRadius: '20px', padding: '70px', maxWidth: '90%', margin: '40px auto'}}>
                <h1 id="centered-text">A terminology troubling you?</h1>
                <textarea
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Find any definition here..."
                    style={{ width: '100%', padding: '10px', borderRadius: '10px', border: 'none', marginBottom: '20px' }}
                />
                <br />
                <button onClick={sendInput} disabled={isLoading} style={{ padding: '10px 20px', borderRadius: '10px', backgroundColor: '#1c1c1c', color: 'white', border: 'none', cursor: 'pointer' }}>
                    {isLoading ? 'Loading...' : 'Ask'}
                </button>
                <div className="response" style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>
                    {response.split('\n').map((line, index) => (
                        <p key={index}>{line}</p>
                    ))}
                </div>
            </div>

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
                        Insurance Terminology
                    </Link>

                    <Link
                        to="/claim-generation" // Link to the Understanding SHIP page
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

export default UnderstandingSHIP;