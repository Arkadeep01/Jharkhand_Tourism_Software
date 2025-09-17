import React, { useState } from 'react';
import { auth } from '../firebase/config'; // Adjust the import based on your firebase config file
import { signInWithEmailAndPassword } from 'firebase/auth';

const SignIn: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            await signInWithEmailAndPassword(auth, email, password);
            // Handle successful sign-in (e.g., redirect or show a success message)
        } catch (err) {
            setError('Failed to sign in. Please check your credentials.');
        }
    };

    return (
        <div>
            <h2>Sign In</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p>{error}</p>}
                <button type="submit">Sign In</button>
            </form>
        </div>
    );
};

export default SignIn;